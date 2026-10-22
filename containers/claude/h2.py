#!/usr/bin/env python3
"""Bounded H2 stage controller. Synthetic Docker runtime only; no live adapter."""
import argparse
import datetime
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time

from run import run, digest_tree
from treatment import load_package, validate_review

FIXTURES = {'pass', 'repair', 'invalid-review', 'invalid-path', 'missing-file', 'review-mutation', 'missing-usage'} | {
    f'{stage}-{suffix}' for stage in ('implementation', 'review', 'repair')
    for suffix in ('failure', 'timeout', 'needs-human', 'malformed')}
STAGE_TOKENS = 18  # Fixture contract only, never an estimate of provider usage.


def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def write_json(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def changed_files(before, after):
    changes = []
    old, new = digest_tree(before), digest_tree(after)
    for name in sorted(old.keys() | new.keys()):
        if old.get(name) == new.get(name):
            continue
        change = {'file': name, 'before_sha256': old.get(name), 'after_sha256': new.get(name)}
        try:
            a = (before/name).read_text() if name in old else ''
            b = (after/name).read_text() if name in new else ''
            change['diff'] = ''.join(difflib.unified_diff(a.splitlines(True), b.splitlines(True), fromfile='before/'+name, tofile='after/'+name))
        except UnicodeError:
            change['diff'] = None
        changes.append(change)
    return changes


def result_event(folder):
    path = folder/'stdout.jsonl'
    if path.stat().st_size > 1024*1024:
        raise ValueError('Oversized stage output')
    events = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    results = [e for e in events if isinstance(e, dict) and e.get('type') == 'result']
    if len(results) != 1 or results[0].get('synthetic') is not True:
        raise ValueError('Exactly one synthetic result required')
    return results[0]


def execute(image, task, prompt, output, harness, harness_digest, fixture='pass',
            wall_seconds=60, max_synthetic_tokens=54, editable_prefixes=None):
    if fixture not in FIXTURES or not 0 < wall_seconds <= 120 or type(max_synthetic_tokens) is not int or max_synthetic_tokens < 0:
        raise ValueError('Invalid fixture or aggregate limits')
    if task.is_symlink() or prompt.is_symlink() or not task.is_dir() or not prompt.is_file():
        raise ValueError('A real task directory and prompt file are required')
    load_package(harness, harness_digest, 'H2')
    if output.exists() or output.resolve().is_relative_to(task.resolve()):
        raise ValueError('Output must be new and outside task inputs')
    editable_prefixes = editable_prefixes if editable_prefixes is not None else ['.']
    if not editable_prefixes or any(Path(p).is_absolute() or '..' in Path(p).parts for p in editable_prefixes):
        raise ValueError('Invalid editable prefixes')
    started = time.monotonic(); deadline = started + wall_seconds
    output.mkdir(parents=True)
    record = {'schema_version':'guild-ledger.h2-attempt/v1', 'synthetic':True,
              'started_at':stamp(), 'harness_id':'H2', 'harness_manifest_sha256':harness_digest,
              'fixture':fixture, 'wall_seconds':wall_seconds, 'max_synthetic_tokens':max_synthetic_tokens,
              'cleanup_operation_timeout_seconds':10, 'editable_prefixes':editable_prefixes,
              'known_synthetic_tokens':0, 'usage_complete':True, 'cost_usd':None,
              'model_calls':0, 'evaluation_performed':False, 'stages':[], 'stop_reason':'running'}
    candidate = task
    implementation = None
    review = None

    def save():
        record['elapsed_seconds'] = time.monotonic()-started
        write_json(output/'attempt.json', record)

    save()
    try:
        info = json.loads(subprocess.check_output(['docker','image','inspect',image], text=True,
                                                 timeout=max(.001, deadline-time.monotonic())))[0]
        if 'RUNNER_KIND=synthetic' not in info['Config'].get('Env', []):
            raise ValueError('H2 controller accepts only a synthetic runtime image')
        image = info['Id']; record['image_id'] = image
        for stage in ('implementation', 'review', 'repair'):
            if stage == 'repair' and review['verdict'] == 'pass':
                break
            if time.monotonic() >= deadline:
                record['stop_reason'] = 'timeout'; break
            if record['known_synthetic_tokens'] + STAGE_TOKENS > max_synthetic_tokens:
                record['stop_reason'] = 'limit'; break
            folder = output/stage
            handoff = {}
            if stage != 'implementation':
                handoff = {'implementation':implementation, 'changes':changed_files(task, candidate),
                           'candidate_sha256':digest_tree(candidate)}
                if stage == 'repair':
                    handoff['review'] = review
            item = {'stage_id':stage, 'started_at':stamp(), 'input_candidate_sha256':digest_tree(candidate),
                    'parent_stage':record['stages'][-1]['stage_id'] if record['stages'] else None,
                    'status':'running', 'known_synthetic_tokens':None,
                    'remaining_wall_seconds_at_start':max(0,deadline-time.monotonic())}
            record['stages'].append(item); save()
            try:
                stage_record = run(image, candidate, prompt, folder, timeout=wall_seconds,
                                   harness=harness, harness_digest=harness_digest, harness_id='H2',
                                   stage_id=stage, handoff=handoff, fixture=fixture, deadline=deadline)
                item['session_id'] = stage_record['session_id']
                item['exit_code'] = stage_record['exit_code']
                item['assembled_prompt_sha256'] = stage_record['assembled_prompt_sha256']
                if stage_record.get('output_symlinks'):
                    raise ValueError('Symlinks in candidate output are not supported')
                if stage != 'review':
                    candidate = folder/'workspace'  # Partial edits survive unsuccessful stages too.
                elif digest_tree(folder/'workspace') != item['input_candidate_sha256']:
                    item['status'] = record['stop_reason'] = 'reviewer-mutated'; break
                if stage_record.get('timed_out') or time.monotonic() >= deadline:
                    item['status'] = record['stop_reason'] = 'timeout'; break
                if stage_record['exit_code'] != 0:
                    item['status'] = record['stop_reason'] = 'runtime-error'; break
                try:
                    event = result_event(folder)
                except (ValueError, OSError):
                    item['status'] = record['stop_reason'] = 'invalid-review' if stage == 'review' else 'invalid-result'
                    break
                usage = event.get('usage')
                valid_usage = (isinstance(usage, dict) and all(type(usage.get(k)) is int and usage[k] >= 0
                               for k in ('input_tokens', 'output_tokens')))
                if valid_usage:
                    item['known_synthetic_tokens'] = usage['input_tokens'] + usage['output_tokens']
                    record['known_synthetic_tokens'] += item['known_synthetic_tokens']
                if event.get('stop_reason') == 'needs-human':
                    item['status'] = record['stop_reason'] = 'needs-human'; break
                if not valid_usage:
                    item['status'] = record['stop_reason'] = 'missing-usage'; break
                if record['known_synthetic_tokens'] > max_synthetic_tokens:
                    item['status'] = record['stop_reason'] = 'limit'; break
                if event.get('stop_reason') != 'completed' or not isinstance(event.get('result'), dict):
                    item['status'] = record['stop_reason'] = 'invalid-review' if stage == 'review' else 'invalid-result'; break
                if stage == 'review':
                    try:
                        review = event['result']; validate_review(review)
                        for finding in review['findings']:
                            path = candidate/finding['file']
                            if not path.is_file() or path.is_symlink() or not any(
                                Path(finding['file']).is_relative_to(Path(prefix)) for prefix in editable_prefixes):
                                raise ValueError('Finding outside existing editable candidate')
                    except (ValueError, TypeError, KeyError):
                        item['status'] = record['stop_reason'] = 'invalid-review'; break
                    write_json(folder/'validated-review.json', review)
                    item['verdict'] = review['verdict']
                elif stage == 'implementation':
                    implementation = event['result']
                item['status'] = 'completed'
            except subprocess.TimeoutExpired:
                item['status'] = record['stop_reason'] = 'timeout'; break
            except (ValueError, OSError, subprocess.CalledProcessError) as exc:
                item['status'] = record['stop_reason'] = 'runtime-error'
                item['error'] = str(exc); break
            finally:
                item['finished_at'] = stamp()
                if item['known_synthetic_tokens'] is None:
                    record['usage_complete'] = False
                save()
        if record['stop_reason'] == 'running':
            record['stop_reason'] = 'completed'
    except subprocess.TimeoutExpired:
        record['stop_reason'] = 'timeout'
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        record['stop_reason'] = 'runtime-error'; record['error'] = str(exc)
    finally:
        shutil.copytree(candidate, output/'candidate', symlinks=True)
        record['candidate_sha256'] = digest_tree(output/'candidate')
        record['finished_at'] = stamp(); save()
    return record


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('task','prompt','output','harness'): p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--harness-digest',required=True)
    p.add_argument('--image',default='guild-ledger-claude-smoke:local')
    p.add_argument('--fixture',choices=sorted(FIXTURES),default='pass')
    p.add_argument('--wall-seconds',type=float,default=60)
    p.add_argument('--max-synthetic-tokens',type=int,default=54)
    p.add_argument('--editable-prefix',action='append',dest='editable_prefixes')
    args=vars(p.parse_args())
    result=execute(**args)
    print(json.dumps({'stop_reason':result['stop_reason'],'stages':[s['stage_id'] for s in result['stages']]}))
    raise SystemExit(0 if result['stop_reason']=='completed' else 1)
