# Evidence and bounded inspection record

Captured 2026-10-21 (UTC). Evidence IDs are used consistently in `report.md` and `capabilities.json`. Tracked-file and configuration inspection was read-only; one `git fetch` populated local `FETCH_HEAD` only to verify the branch base, without changing tracked files or settings. No credentials, raw session/run IDs, private reasoning, or unrelated account logs were collected.

## Local inspection

### E01 — Hosted surface markers [Observed]

Bounded command:

```bash
for n in GITHUB_ACTIONS GITHUB_WORKFLOW GITHUB_RUN_ID GITHUB_RUN_ATTEMPT GITHUB_JOB COPILOT_AGENT_SESSION_ID COPILOT_CLI_VERSION VSCODE_PID TERM_PROGRAM CODESPACES CI; do
  if printenv "$n" >/dev/null 2>&1; then
    case "$n" in
      GITHUB_RUN_ID|GITHUB_RUN_ATTEMPT|COPILOT_AGENT_SESSION_ID) printf '%s=<present; value withheld>\n' "$n" ;;
      *) printf '%s=%s\n' "$n" "$(printenv "$n")" ;;
    esac
  else
    printf '%s=<unset>\n' "$n"
  fi
done
```

Relevant redacted output:

```text
GITHUB_ACTIONS=true
GITHUB_WORKFLOW=dynamic/copilot-swe-agent/copilot
GITHUB_RUN_ID=<present; value withheld>
GITHUB_RUN_ATTEMPT=<present; value withheld>
GITHUB_JOB=copilot
COPILOT_AGENT_SESSION_ID=<present; value withheld>
COPILOT_CLI_VERSION=<unset>
VSCODE_PID=<unset>
TERM_PROGRAM=<unset>
CODESPACES=<unset>
CI=true
```

The combination identifies a GitHub-hosted Copilot cloud-agent task, not a local editor/CLI task. IDs were present but not copied into the report.

### E02 — Runner, runtime, checkout [Observed]

Bounded commands:

```bash
pwd
uname -srm
git status --short --branch
git rev-parse --show-toplevel
git branch --show-current
git fetch --no-tags origin main
git log -1 --format='%H %P %s' HEAD
git log -1 --format='%H %P %s' FETCH_HEAD
git merge-base HEAD FETCH_HEAD
git rev-list --left-right --count HEAD...FETCH_HEAD
```

Relevant output:

```text
/home/runner/work/guild-ledger-research/guild-ledger-research
Linux 6.17.0-1022-azure x86_64
## copilot/create-runtime-discovery-report...origin/copilot/create-runtime-discovery-report
/home/runner/work/guild-ledger-research/guild-ledger-research
copilot/create-runtime-discovery-report
HEAD and fetched main were both b1b0c9d93e9b40f58251829751051c827b0dcd55
merge-base was b1b0c9d93e9b40f58251829751051c827b0dcd55
HEAD...main relation: 0 0
```

Selected non-secret metadata:

```bash
for n in COPILOT_AGENT_RUNTIME_VERSION COPILOT_AGENT_SOURCE_ENVIRONMENT COPILOT_PREINSTALLED_RUNTIME COPILOT_MCP_ENABLED COPILOT_PERMISSION_MODE COPILOT_PERMISSION_GATE_REASON RUNNER_ENVIRONMENT RUNNER_OS RUNNER_ARCH; do
  if printenv "$n" >/dev/null 2>&1; then
    printf '%s=%s\n' "$n" "$(printenv "$n")"
  else
    printf '%s=<unset>\n' "$n"
  fi
done
```

Output:

```text
COPILOT_AGENT_RUNTIME_VERSION=runtime-cca-vendored-a3b15b740302d352cffb1bec7e01de2f5a4bffce
COPILOT_AGENT_SOURCE_ENVIRONMENT=gc-cus-02
COPILOT_PREINSTALLED_RUNTIME=true
COPILOT_MCP_ENABLED=true
COPILOT_PERMISSION_MODE=default
COPILOT_PERMISSION_GATE_REASON=enabled
RUNNER_ENVIRONMENT=github-hosted
RUNNER_OS=Linux
RUNNER_ARCH=X64
```

Runtime version is the value supplied by the task environment, not a public product release number. Permission metadata does not reveal exact user approval gates.

### E03 — Safe model metadata check [Observed/Unknown]

The inference-identity metadata variable was present. A bounded local parser checked only simple fields named `model`, `model_id`, `model_name`, `label`, `provider`, `reasoning`, `reasoning_effort`, or `version`; it did not print the raw value.

Relevant output:

```text
inference_identity_model_fields=not exposed in simple metadata fields
```

Therefore model/provider label, product version, selected reasoning level, and pinning state remain unknown. No raw inference identity, auth material, credentials, or secrets were read into evidence.

### E05 — Repository/task scope [Observed]

Bounded inspection:

```bash
find .. -name AGENTS.md -print
```

Output was empty. Repository path inspection found the collection guide, collector script, and collector workflow; no `.github/workflows/copilot-setup-steps.yml` or repository hook configuration was identified among inspected files. The task itself prohibited benchmarks, extra agent/model sessions, installs, configuration/workflow edits, and Loom execution; none were performed.

Relevant files read:

- `docs/runtime-discovery/github-copilot-coding-agent/collection-workflow.md`
- `.github/workflows/collect-copilot-report.yml`
- `scripts/collect_copilot_report.py`

No report collector or other workflow was run during discovery.

### E07 — Available tool/skill inventory [Observed]

The task interface made repository inspection/editing, shell, GitHub, web/browser, progress reporting, validation/security, memory, and session-store tools available. The available named skills were `customize-cloud-agent` and `merge-branch`. This is a declaration of exposed options, not an invocation log; no additional agent/model session was launched.

## Official documentation

All URLs below are GitHub documentation pages retrieved 2026-10-21. Documentation supports product-level capability statements; it does not prove that a feature was active or exercised in this task.

### E04 — Model selection and reasoning [Documented]

URL: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/changing-the-ai-model  
Retrieved: 2026-10-21

The page says cloud-agent model selection is supported only at specified entry points; supported models may offer configurable reasoning. Where a model picker is unavailable, Auto is used. It does not disclose this task's selected model or setting.

### E06 — Session lifecycle and session data [Documented]

URLs:

- https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents
- https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/session-data

Retrieved: 2026-10-21

The pages document progress/session logs, steering and stopping; session logs can show token usage and session length. Stopping a session ends the Actions run and preserves commits already pushed. Cloud-agent environments are ephemeral while session logs remain available; cloud-agent sessions are shared by default with repository collaborators. These pages do not provide this task's detailed usage export or account retention configuration.

### E09 — Environment customization [Documented]

URL: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment  
Retrieved: 2026-10-21

The page documents GitHub Actions-backed ephemeral development environments, repository `copilot-setup-steps.yml`, supported runner customization, and setup behavior. It also links to firewall customization and secrets/variables. This report did not inspect account firewall configuration or test outbound access.

### E10 — General GitHub.com product surface [Documented]

URL: https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github  
Retrieved: 2026-10-21

The page describes cloud-agent delegation, session context/logs, and available customization categories including custom instructions, agents/skills, MCP, and hooks. These are documented features, not proof of current-task use.

### E11 — Copilot usage and billing [Documented]

URLs:

- https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals
- https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing
- https://docs.github.com/en/copilot/concepts/billing-and-usage

Retrieved: 2026-10-21

Current individual billing documentation describes AI credits, token/model-dependent pricing, included plan allowances, and possible extra usage. No account plan, usage page, invoice, budget, or charge record was accessed. The legacy premium-request page was not used to infer this task's actual billing.

### E12 — Proposed probe only [Inferred]

A bounded, one-task calibration probe is proposed in `report.md`; it has not been run. This report does not claim that documentation or a proposal demonstrates Loom, model pinning, telemetry export, or billing attribution.

## Repository collector behavior [Documented from repository]

`docs/runtime-discovery/github-copilot-coding-agent/collection-workflow.md`, `.github/workflows/collect-copilot-report.yml`, and `scripts/collect_copilot_report.py` document a manual Action accepting PR number and `YYYYMMDDTHHMMSSZ`, reading the three report files at the immutable PR head SHA, creating a hash/provenance manifest, and uploading `copilot-discovery-<PR>-<timestamp>` with a 90-day retention period. It does not execute report content, launch Copilot, merge a PR, or retrieve private session telemetry.
