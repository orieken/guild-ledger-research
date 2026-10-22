"""No inference entrypoint: validate inputs, demonstrate synthetic edits, inspect CLI."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from treatment import load_package, assemble, sha

RULE_NAMES = {"agents.md", "claude.md", "gemini.md", "copilot-instructions.md"}
STATE_DIRS = {".claude", ".codex", ".agents", ".gemini", ".git", "node_modules", ".venv"}


def audit_tree(root):
    for p in root.rglob("*"):
        if p.is_symlink():
            raise ValueError(f"Symlink disallowed: {p.relative_to(root)}")
        if not p.is_file() and not p.is_dir():
            raise ValueError(f'Special file disallowed: {p.relative_to(root)}')
        if p.name.lower() in RULE_NAMES or p.name in STATE_DIRS:
            raise ValueError(f"Undeclared instructions/state: {p.relative_to(root)}")
        if p.is_file() and (p.name.endswith((".instructions.md", ".agent.md", ".prompt.md")) or p.name == ".mcp.json"):
            raise ValueError(f"Undeclared agent asset: {p.relative_to(root)}")


def preflight():
    if os.getuid() == 0:
        raise ValueError("Runner must be non-root")
    if Path('/var/run/docker.sock').exists():
        raise ValueError("Host Docker socket must not be mounted")
    for root in (Path('/home/runner'), Path('/workspace'), Path('/inputs')):
        audit_tree(root)
    for p in (Path('/etc/claude-code'), Path('/CLAUDE.md'), Path('/AGENTS.md'), Path('/home/CLAUDE.md')):
        if p.exists():
            raise ValueError(f"Unexpected ancestor or managed configuration: {p}")
    unexpected = [k for k in os.environ if k.startswith(('ANTHROPIC_', 'AWS_', 'GOOGLE_', 'GH_', 'GITHUB_', 'CLAUDE_')) and k not in {
        'CLAUDE_CONFIG_DIR', 'CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC'}]
    if unexpected:
        raise ValueError("Unexpected environment keys: " + ', '.join(sorted(unexpected)))
    inputs = Path('/inputs')
    if (inputs / 'exposure.json').exists():
        exposure = json.loads((inputs / 'exposure.json').read_text())
        expected = exposure['files']
        actual = {str(p.relative_to(inputs)): sha(p.read_bytes()) for p in inputs.rglob('*')
                  if p.is_file() and p.name != 'exposure.json'}
        if expected != actual:
            raise ValueError('Input exposure digest/file-set mismatch')
        package = None
        if exposure['harness_id'] != 'H0':
            package = load_package(inputs / 'treatment', exposure['manifest_sha256'], exposure['harness_id'])
        assembled = assemble((inputs / 'prompt.txt').read_bytes(), inputs / 'treatment', package)
        if assembled != (inputs / 'assembled-prompt.txt').read_bytes():
            raise ValueError('Assembled prompt mismatch')
        print(json.dumps({'type': 'runner_treatment', 'harness_id': exposure['harness_id'],
                          'manifest_sha256': exposure['manifest_sha256'], 'assembled_prompt_sha256': sha(assembled),
                          'scope': 'offline initial-stage assembly only; no multi-stage execution'}), flush=True)
    print(json.dumps({"type": "runner_preflight", "status": "passed", "uid": os.getuid(),
                      "kind": os.environ['RUNNER_KIND'], "scope": "filesystem and environment checks; not proof of effective model context"}), flush=True)


def main():
    mode = sys.argv[1] if len(sys.argv) == 2 else ''
    if mode not in {'preflight', 'fake', 'cli-info'}:
        raise ValueError('Only preflight, fake and cli-info are supported; live inference is disabled')
    preflight()
    if mode == 'fake':
        if os.environ['RUNNER_KIND'] != 'synthetic':
            raise ValueError('Fake mode requires the smoke image')
        return subprocess.call(['python3', '/opt/runner/fake-claude.py'])
    if mode == 'cli-info':
        if os.environ['RUNNER_KIND'] != 'claude':
            raise ValueError('CLI info requires the Claude image')
        binary=Path('/usr/local/bin/claude')
        print(json.dumps({'type':'binary_identity','sha256':hashlib.sha256(binary.read_bytes()).hexdigest()}),flush=True)
        for args in (['--version'], ['--help']):
            subprocess.run([str(binary), *args], check=True, timeout=30)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print(f'runner rejected: {exc}', file=sys.stderr)
        sys.exit(2)
