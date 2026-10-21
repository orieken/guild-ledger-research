"""Collect report data only; never check out or execute the source PR."""
import base64
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


def api(endpoint):
    result = subprocess.run(
        ["gh", "api", "--hostname", "github.com", endpoint],
        check=True, capture_output=True, text=True, timeout=30,
    )
    return json.loads(result.stdout)


def collect(repository, pr_number, timestamp, output, fetch=api):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("Invalid repository")
    if not re.fullmatch(r"[1-9][0-9]*", pr_number):
        raise ValueError("PR number must be a positive integer")
    if not re.fullmatch(r"[0-9]{8}T[0-9]{6}Z", timestamp):
        raise ValueError("Invalid report timestamp")
    datetime.datetime.strptime(timestamp, "%Y%m%dT%H%M%SZ")
    pr = fetch(f"repos/{repository}/pulls/{pr_number}")
    if pr["base"]["repo"]["full_name"].lower() != repository.lower():
        raise ValueError("Unexpected PR base repository")
    # Same-repository branches only; default GITHUB_TOKEN cannot read arbitrary forks.
    head_repo = pr["head"]["repo"]["full_name"]
    if head_repo.lower() != repository.lower():
        raise ValueError("Fork PR collection is not supported")
    sha = pr["head"]["sha"]
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("Invalid source commit")
    prefix = f"docs/runtime-discovery/github-copilot-coding-agent/{timestamp}"
    files = {}
    for name in ("report.md", "capabilities.json", "evidence.md"):
        record = fetch(f"repos/{repository}/contents/{prefix}/{name}?ref={sha}")
        if record.get("type") != "file" or record.get("encoding") != "base64":
            raise ValueError(f"Expected a base64 file: {name}")
        if record.get("size", 1000001) > 1000000:
            raise ValueError(f"Report exceeds 1 MB limit: {name}")
        data = base64.b64decode("".join(record["content"].split()), validate=True)
        if not data or len(data) > 1000000:
            raise ValueError(f"Empty or oversized report: {name}")
        data.decode("utf-8")
        files[name] = data
    capabilities = json.loads(files["capabilities.json"])
    if not isinstance(capabilities, dict) or capabilities.get("schema_version") != "guild-ledger.runtime-discovery/v1-draft":
        raise ValueError("Unexpected capability schema version")
    manifest = {
        "schema_version": "guild-ledger.report-collection/v1",
        "repository": repository, "pr_number": int(pr_number),
        "source_commit": sha, "source_directory": prefix,
        "collected_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "collector_run_id": os.environ.get("GITHUB_RUN_ID"),
        "collector_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "collector_commit": os.environ.get("GITHUB_SHA"),
        "verification": "Collected agent-authored claims; runtime identity and metrics not independently verified",
        "files": {name: {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)} for name, data in files.items()},
    }
    output.mkdir(parents=True, exist_ok=False)
    for name, data in files.items():
        (output / name).write_bytes(data)
    (output / "collection-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    result = collect(os.environ["SOURCE_REPOSITORY"], os.environ["PR_NUMBER"],
                     os.environ["REPORT_TIMESTAMP"], Path("collected-copilot-report"))
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
            summary.write(f"Collected three report files from PR #{result['pr_number']}, commit `{result['source_commit']}`.\n\nClaims are not independently verified; no Copilot task was launched.\n")
