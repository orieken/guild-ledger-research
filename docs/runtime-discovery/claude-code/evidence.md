# Evidence log: claude-code (Claude Projects cloud thread)

Captured 2026-10-21 between 01:16 and 01:25 UTC by the agent running inside the surface being described. Every entry is a redacted observation or a documentation citation. Secret values, credential files, environment values not listed here, hidden prompt text, private reasoning and personal identifiers were not read into this file. Session and request identifiers are truncated.

Status vocabulary used in `report.md` and `capabilities.json`: **observed** (verified here), **documented** (official docs linked below), **inferred** (reasoned, unverified), **unknown**.

## Observations (commands and tool calls)

### E01: CLI binary version
- Command: `claude --version` (exit 0); `which claude`
- Result: `2.1.305 (Claude Code)`; binary at `/opt/node22/bin/claude`.
- Note: this is the binary installed in the container. The running agent's transcript also records `version: 2.1.305` (E05), so the binary and the running agent agree.

### E02: Selected runtime flags (non-secret values only)
- Command: printed 19 hand-picked variable names with values; all other variables were not printed. Credentials, tokens, URLs, account and organization identifiers, and the user email were deliberately skipped.
- Values observed:
  - `CLAUDE_CODE_ENTRYPOINT=remote_projects`
  - `CLAUDE_CODE_CCR_SURFACE=tag`
  - `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`
  - `CLAUDE_CODE_PROJECTS_SESSION=1`, `CLAUDE_CODE_CHILD_SESSION=1`
  - `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST=1`
  - `CLAUDE_CODE_REMOTE_HERMETIC_MODE=0`
  - `CLAUDE_CODE_ENVIRONMENT_RUNNER_VERSION=release-66c6e19d9d-ext`
  - `CLAUDE_CODE_VERSION=2.1.42`: **conflicts** with E01/E05 (2.1.305). Its meaning is unknown; do not use it as the runtime version.
  - `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=80`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW=500000`
  - `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`
  - `CLAUDE_EFFORT=medium`
  - `CLAUDE_CODE_SESSION_ATTENDED=1`, `CLAUDE_CODE_RETRY_WATCHDOG=1`
  - `CLAUDE_CODE_INCLUDE_PARTIAL_MESSAGES=true`, `CLAUDE_CODE_TEE_SDK_STDOUT=true`, `CCR_ENABLE_TRACING=true`
  - `IS_SANDBOX=1`
- The set of variable names also includes OTLP-metrics, tracing, proxy, egress-gateway and hook-related names. They show that host-side telemetry exists, but none of it can be read from inside the session.

### E03: Operating environment
- Commands: `uname -srm`, `/etc/os-release`, `id -un`, `nproc`, `free -h` (all exit 0)
- Result: Linux 6.18.44-fc-v139 x86_64, Ubuntu 24.04.5 LTS, user `root`, cwd `/home/claude`, 4 vCPU, 15 GiB RAM.
- Toolchain (`--version`): git 2.43.0, gh 2.89.0, node v22.22.0, npm 10.9.4, Python 3.13.16, Docker 29.9.1 client. Docker was not run.

### E04: Session record from the host control plane
- Tool: `mcp__claude-code-remote__get_session` (no session id, so it describes this session)
- Redacted result:
  ```json
  {
    "id": "session_012E…",
    "session_status": "SESSION_STATUS_RUNNING",
    "environment_kind": "anthropic_cloud",
    "origin": "claude-in-hearth",
    "configured_model": "claude-opus-5-5[1m]",
    "session_context": {"model": "claude-opus-5-5[1m]", "effort_level": "medium", "permission_mode": "auto", "autofix_on_pr_create": true},
    "external_metadata": {
      "last_served_model": "claude-opus-5-5",
      "context_usage": {"max_tokens": 500000, "used_tokens": 0},
      "rate_limit_info": {"rateLimitType": "five_hour", "status": "allowed", "isUsingOverage": false, "resetsAt": "<epoch>"}
    },
    "parent_session_id": "session_0176…",
    "lineage": {"depth": 1, "limit": 8},
    "tags": ["hearth-thread", "config:hearth-projects-session", "…"]
  }
  ```
- Note: `context_usage.used_tokens: 0` was reported while the session had already made several model calls, so this field is not a reliable usage counter.
- The session's own configuration, visible to the agent, also lists a model fallback order: `claude-opus-5[1m]`, then `claude-opus-4-8[1m]`. It states that the serving model can change mid-session.

### E05: Local transcript schema (keys and types only, plus counts)
- Path pattern: `~/.claude/projects/-home-claude/<session-uuid>.jsonl` (inside the container)
- Method: an isolated Python script tallied keys, types and counts. Message content was not printed.
- At capture time there were 78 lines. Entry types: `assistant` 19 (21 later), `user` 14, `attachment` 25, `queue-operation` 6, `ai-title` 5, `atis-latch` 5, `last-prompt` 4.
- `assistant` entry keys: `uuid, parentUuid, sessionId, timestamp, requestId, requestedModel, effort, perTurnEffort, thinkingDurationMs, isSidechain, entrypoint, version, cwd, gitBranch, message, …`
- `message` keys: `id, model, role, type, content, stop_reason, stop_sequence, stop_details, usage, container, context_management, diagnostics, input_transformations`
- `message.usage` fields: `input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens, cache_creation.ephemeral_5m_input_tokens, cache_creation.ephemeral_1h_input_tokens, output_tokens_details.thinking_tokens, server_tool_use.web_search_requests, server_tool_use.web_fetch_requests, service_tier, speed, inference_geo, fallback_credit, iterations[]`
- Values: `message.model = "claude-opus-5-5"` (21/21), `requestedModel = "claude-opus-5-5[1m]"`, `version = "2.1.305"`, `entrypoint = "remote_projects"`, `service_tier/speed/inference_geo = standard/standard/global`, `isSidechain = false` everywhere.
- **Duplication:** 21 assistant entries share only 7 distinct `message.id` values and 7 distinct `requestId` values (prefixes `msg_`, `req_`). Usage must be deduplicated by message id.
- Redacted sample `usage.iterations[0]` for one API response (observed, single response, not a total): `{"input_tokens": 2, "output_tokens": 736, "cache_read_input_tokens": 97390, "cache_creation_input_tokens": 2011, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 2011}, "type": "message"}`
- No cost or USD field exists anywhere in the transcript entries.

### E06: Effective local Claude Code settings
- Files: `~/.claude/settings.json` does not exist, and neither does `/etc/claude-code/`. `~/.claude/launcher-settings.json` was read for its key structure and hook commands only.
- Hooks: `PostToolUse` runs a status-nudge script. `Stop` runs a git check and a reply gate. `UserPromptSubmit` runs a reply reminder. `permissions.allow = ["Skill"]`.
- The `~/.claude` directory also holds `plugins/synced/<org>_<id>`, `skills/synced/<org>_<id>`, `skills/session-start-hook`, `sessions/`, `projects/`, `shell-snapshots/` and `backups/`. A credentials file is present but was **not opened**.

### E07: Tools exposed to the agent in this session
- Source: the agent's own tool list (names only).
- Built in: `Bash, Read, Write, Edit, Glob, Grep, Agent (subagents), WebFetch, WebSearch, Skill, Artifact, NotebookEdit, Task*, Monitor, Cron*, EnterWorktree`.
- MCP servers: `github` (repo tools, Copilot tools, merge), `claude-code-remote` (list/get/interrupt/archive sessions, triggers, `add_repo`, `subscribe_pr_activity`, `read_documentation`), `hearthbot` (thread messaging, checklist, decisions, remote control, device folders), `remote-devices` (user-device folder and computer-use tools), `Claude_Docs`, plus account-level connectors unrelated to this work (names omitted).
- 12 plugin-provided MCP servers failed to connect: the proxy refused the tunnel with a 403, and one server needs authentication. Skills from account-synced plugins are listed.
- Context windows mentioned in the configuration: `[1m]` model suffix, a 500k auto-compact window, and compaction at 80%.

### E08: Repository discovery and attachment
- `list_repos(query="guild-ledger")`: 5 repositories (`guild-ledger-research`, `-baseline`, `-guidelines`, `-harness`, `-loom`), all public, listing `can_push: true`.
- `add_repo(orieken/guild-ledger-research, access=push)`: attached, but `push_check: "refused"` with the message that Claude does not have GitHub access to the repository for the user's organization. The stated remedy is to install the Claude GitHub App on it or reconnect GitHub.

### E09: Repository state
- `git clone --depth 1 …/guild-ledger-research`: warned "You appear to have cloned an empty repository." `git ls-remote origin` exited 0 with no refs.
- Consequence: the planning files in the local checkout have never been pushed, so this hosted surface cannot see them on GitHub. They are visible only through the project's uploaded folder copy at `/mnt/project-files/guild-ledger/guild-ledger-research/`.

### E10: Edit demonstration (scratch file)
- In `/mnt/project-files/guild-ledger/guild-ledger-research/docs/runtime-discovery/claude-code/`, the agent created `.scratch-edit-probe.txt`, read it back, and removed it (`rm` exit 0). The folder listing afterwards was empty. Timestamp 2026-10-21T01:17:32Z.

### E11: User-device reachability
- `list_devices`: `{"devices": [], "folders": []}`. The session record (E04) names a bound device, but this session has no reachable device folders. The user's local checkout was not touched.

### E12: Visible instruction sources (categories only)
- The agent receives these layers, listed from highest to lowest precedence as the agent was told:
  1. Built-in Claude Code system prompt.
  2. Hosted cloud-environment and Projects-thread role instructions, including PR attribution, assignee and reviewer requirements, and git push rules.
  3. Hook-injected reminders (E06).
  4. Session-context block. It lists project name, files, and requester identity. **No project instructions text was present.**
  5. The coordinator's relay note, written by another Claude session.
  6. The user's task message.
  7. Project memory directory (`MEMORY.md` index reported empty).
  8. Skill listings from synced and plugin skills.
- No repository `CLAUDE.md` existed because the repo is empty.
- The full text of layers 1 to 3 is not reproduced here.

### E13: Documentation-help tool
- `read_documentation(topic=session.resources | github.access)` returned short platform guidance. github.access confirms the remedy for refused pushes: connect GitHub at claude.ai/connect-github and install the Claude GitHub App.

### E14: Prior local observation (different surface, not re-verified)
- `docs/research/12-runtime-options.md` records Claude Code `2.1.292` installed on the researcher's machine. That is the **local CLI** surface, not this one.

## Official documentation (retrieved 2026-10-21)

| ID | Page | Used for |
|---|---|---|
| D01 | https://code.claude.com/docs/en/claude-code-on-the-web | Cloud sessions: `claude --cloud`, `claude -p "<msg>" --cloud <session-id>` (`--output-format json` returns `{ok, session_id, url}`), `--teleport`, archive/delete, environment expiry (conversation restored; running background work not), `/compact` works, `/clear` does not, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` set by host and overriding user value, usage counts against plan limits with no separate VM charge |
| D02 | https://code.claude.com/docs/en/headless | Local headless CLI: `-p`, `--bare`, `--output-format json/stream-json`, `total_cost_usd` is a client-side estimate, SIGTERM leaves turn unfinished (exit 143), `system/api_retry` events, `parent_tool_use_id` for subagent lineage |
| D03 | https://code.claude.com/docs/en/agent-sdk/cost-tracking | Deduplicate per-step usage by message id; per-step `output_tokens` is a placeholder; `modelUsage` includes subagents; `total_cost_usd`/`costUSD` are estimates, not billing; crash results may be zeroed |
| D04 | https://code.claude.com/docs/en/claude-projects | Projects: public beta on Pro/Max; coordinator + threads; thread model/effort in Project settings; threads in auto mode; project instructions ≤16,000 chars; project memory `MEMORY.md`; repo `CLAUDE.md` loaded from clones; Usage page shows token use by thread and model; usage counts against plan limits; 200 new threads/day; Pause and Delete; Claude GitHub App required on project repos |
| D05 | https://code.claude.com/docs/en/routines | Scheduled tasks (research preview): API trigger `POST https://api.anthropic.com/v1/claude_code/routines/<trig_id>/fire` with `Authorization: Bearer`, `anthropic-beta: experimental-cc-routine-2026-04-01`; returns `claude_code_session_id` and URL; fire `text` wrapped as untrusted; runs draw subscription usage; 30 fires/hour per task, 100/hour per account |
| D06 | Platform guidance via `read_documentation` (E13) | GitHub access remedy |

## Not tested (deliberately)

- Starting any new session, thread, routine or trigger. Calling `interrupt_session`, `archive_session`, `fire_trigger` or `create_trigger`.
- Running `claude -p` or any nested model call inside the container. Running Loom.
- Spawning subagents (the Agent tool is available but was not used).
- Pushing, opening a PR, merging, or changing settings, environments or CI.
- Reading credentials, the full environment, hook script bodies, or full transcript content.
- Measuring cancellation behavior, or exporting the transcript off the container.
- Verifying the backend model identity beyond the response-reported `message.model` field.
