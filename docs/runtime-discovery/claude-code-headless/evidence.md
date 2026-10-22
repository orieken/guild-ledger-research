# Evidence log: claude-code-headless (local terminal Claude Code)

Captured 2026-10-21 between 02:38 and 02:50 UTC by the agent running inside the surface being
described. Every entry is a redacted observation or a documentation citation. Secret values,
credential file contents, environment values not listed here, hidden system-prompt text, private
reasoning, and personal identifiers were not read into this file. `claude mcp list` output below
is reproduced because server names/URLs/connection status are configuration metadata, not
secrets; no tokens or credential values are shown.

Status vocabulary used in `report.md`/`capabilities.json`: **observed** (verified here),
**documented** (official docs linked below), **inferred** (reasoned, unverified), **unknown**.

## Observations (commands and tool calls)

### E01: CLI binary version and path
- Commands: `which claude`; `claude --version` (exit 0)
- Result: `/opt/homebrew/bin/claude`; `2.1.304 (Claude Code)`.

### E02: Process ancestry (surface verification)
- Commands: `ps -p $PPID`, `ps -ef | awk ...`, a loop walking `ppid` up five levels via `ps -o ppid=`
- Result:
  ```
  claude   (54564) -> zsh    (3981, -zsh)
  zsh      (3981)  -> login  (3790)
  login    (3790)  -> Terminal.app (684, /System/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal)
  Terminal.app (684) -> launchd (1)
  ```
- Note: no cloud relay, coordinator, or nested Claude process appears anywhere in this chain.

### E03: Env var names only (claude/anthropic-related), no values
- Command: `env | cut -d= -f1 | sort | grep -i -E "claude|anthropic|sandbox|cursor|codex|copilot"`
- Result: `CLAUDE_CODE_CHILD_SESSION`, `CLAUDE_CODE_ENTRYPOINT`, `CLAUDE_CODE_EXECPATH`,
  `CLAUDE_CODE_MESSAGING_SOCKET`, `CLAUDE_CODE_MESSAGING_TOKEN`, `CLAUDE_CODE_SESSION_ATTENDED`,
  `CLAUDE_CODE_SESSION_ID`, `CLAUDE_EFFORT`, `CLAUDE_PID`, `CLAUDECODE`. No `ANTHROPIC_API_KEY`
  name present. No `CLAUDE_CODE_VERSION`, `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, or
  `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` names present either (absence noted, not just unset).

### E04: Values of the non-secret vars named in E03, plus terminal vars
- Commands: individual `echo "$VAR"` calls; `wc -c` on the session-id length only (not its value)
- Result: `CLAUDE_CODE_ENTRYPOINT=cli`; `CLAUDE_CODE_CHILD_SESSION=1`; `CLAUDECODE=1`;
  `CLAUDE_EFFORT=high`; `CLAUDE_CODE_SESSION_ATTENDED=1`; session-id length = 36 characters (a
  UUID shape, value itself not printed); `TERM_PROGRAM=Apple_Terminal`; `TERM=xterm-256color`;
  `SHELL=/bin/zsh`; `PWD=/Users/oscarrieken/Projects/Rieken/guild-ledger`.

### E05: Operating environment
- Commands: `whoami`, `hostname`, `uname -srm`, `node --version`, `date -u`
- Result: user `oscarrieken`, host `Mac`, `Darwin 25.6.0 arm64`, Node `v22.22.3`.

### E06: `~/.claude` directory structure and settings content
- Commands: `ls -la ~/.claude/`; `cat ~/.claude/settings.json`; `cat
  ~/.claude/framework-install.json`; `find ~/.claude -maxdepth 3 -iname "settings*.json"`
- Result: `~/.claude/settings.json` = `{"tui": "fullscreen", "theme": "dark-ansi",
  "switchModelsOnFlag": false}` — no `hooks` key. `~/.claude/CLAUDE.md` is a symlink to
  `ai-assistant-dot-files/.claude.md`, which **does not exist** (broken link — confirmed by a
  failed `wc -l` on the target). `~/.claude/rules` symlinks to
  `ai-assistant-dot-files/shared/rules/` (17 files, listed by name/size/mtime only). `~/.claude/skills`
  symlinks to `ai-assistant-dot-files/shared/skills/` (71 entries, count only). `~/.claude/plugins/`
  holds `blocklist.json`, `known_marketplaces.json`, a plugin-directory cache, and a `synced/`
  folder (names/sizes only; contents not read). `~/.claude/framework-install.json`:
  `source_repo=.../ai-assistant-dot-files`, `git_tag=v3.3.14`,
  `commit_sha=dd78f1df496edeb65baa7acf3b4a37e09bbac1b7`, `mode=symlink`, `framework_level=base`,
  `platforms=[claude-code, cursor, windsurf, github-copilot, gemini, jetbrains, openai-codex]`,
  `stack=go,typescript`. Only `~/.claude/settings.json` exists among the four non-managed settings
  files for this project.
- Credential files present but **not opened**: `~/.claude/.credentials.json`,
  `~/.claude/.credentials.lock`.

### E07: Absence of a project-level `.claude/` directory
- Commands: `ls -la /Users/oscarrieken/Projects/Rieken/guild-ledger/.claude`; `cat
  .../guild-ledger/.claude/settings.json`; `cat .../guild-ledger/.claude/settings.local.json`
- Result: all three fail with "No such file or directory." `guild-ledger` itself defines no
  project-level settings, hooks, or `.mcp.json`.

### E08: Configured MCP servers
- Command: `claude mcp list`
- Result (names, URLs, and connection status only — reproduced verbatim as configuration
  metadata, no tokens):
  ```
  claude.ai Claude Docs: https://api.anthropic.com/v1/pages/mcp - Connected
  claude.ai Indeed: https://mcp.indeed.com/claude/mcp - Connected
  claude.ai ZipRecruiter: https://api.ziprecruiter.com/mcp - Connected
  claude.ai Notion: https://mcp.notion.com/mcp - Needs authentication
  claude.ai Google Drive / Gmail / Google Calendar - Connected
  plugin:engineering:slack / linear / atlassian / notion / datadog - Needs authentication
  plugin:engineering:asana / github / pagerduty - Failed to connect (incompatible auth server)
  plugin:data:bigquery - Failed to connect; plugin:data:hex / amplitude / amplitude-eu - Needs auth
  plugin:data:definite - Failed to connect (endpoint not found)
  plugin:engineering:google calendar / gmail, plugin:data:snowflake / databricks - Not configured
  ```
  Several entries preceded by repeated `[mcp-sdk] SEP-2352: stored OAuth credential has no
  'issuer' stamp` warnings (one per affected server health check).

### E09: `claude --help` (full flag and subcommand enumeration)
- Command: `claude --help` (exit 0), read in three sequential chunks
- Result (headless/automation-relevant flags only, names and documented effect; full text is
  long and omitted here): `-p/--print`, `--bare`, `--safe-mode`, `--restricted`,
  `--output-format text|json|stream-json`, `--input-format text|stream-json`,
  `--permission-mode acceptEdits|auto|bypassPermissions|manual|dontAsk|plan`,
  `--permission-prompts host|none`, `--max-budget-usd`, `--allowedTools`/`--disallowedTools`,
  `--setting-sources`, `--strict-mcp-config`, `--mcp-config`, `--add-dir`, `--session-id`,
  `--no-session-persistence`, `--fork-session`, `-c/--continue`, `-r/--resume`,
  `--fallback-model`, `--agent`/`--agents`, `--model`, `--effort`, `--json-schema`,
  `--include-partial-messages`, `--include-hook-events`, `--forward-subagent-text`,
  `--replay-user-messages`, `--system-prompt`/`--system-prompt-snapshot`,
  `--append-system-prompt(-file)`, `--plugin-dir`/`--plugin-url`, `-w/--worktree`, `--tmux`,
  `--teleport`, `--cloud`, `--environment`, `--bg/--background`, `--dangerously-skip-permissions`.
  Subcommands: `agents`, `attach`, `auth`, `auto-mode`, `doctor`, `gateway`, `import`, `install`,
  `logs`, `mcp`, `plugin`/`plugins`, `purge`, `respawn`, `rm`, `setup-token`, `stop`/`kill`,
  `ultrareview`, `update`/`upgrade`.

### E10: `claude doctor` (read-only health check)
- Command: `claude doctor`
- Result:
  ```
  Running: package-manager (2.1.304)
  Commit: 17ab70404e5b
  Platform: darwin-arm64
  Package manager: homebrew
  Path: /opt/homebrew/Caskroom/claude-code/2.1.304/claude
  Auto-updates: Managed by package manager
  Managed settings (remote): not fetched — requires an Enterprise or Team subscription
  Organization policy: not applicable to Pro and Max accounts
  No installation issues found.
  ```

### E11: Local session transcript schema (keys/types/counts only; no message content printed)
- Path: `~/.claude/projects/-Users-oscarrieken-Projects-Rieken-guild-ledger/<session-uuid>.jsonl`
  (session UUID matches `CLAUDE_CODE_SESSION_ID`/the scratchpad path given in this session's own
  environment block; not reproduced here as it is this session's own identifier, already visible
  to the user in their own terminal).
- Method: a Python script (run directly with `python3`, this being this agent's own trusted
  session file, not untrusted downloaded content) tallied `type` values, key sets per type, model
  names, `isSidechain`/`version`/`entrypoint` value counts, distinct `message.id`/`requestId`
  counts, and printed exactly one redacted `usage` sample. No prompt or completion text was
  printed.
- Result at time of inspection: **222** total lines. Type counts: `mode` 11, `permission-mode` 11,
  `atis-latch` 11, `file-history-snapshot` 2, `user` 25, `attachment` 33, `last-prompt` 10,
  `ai-title` 10, `api-request-shape` 1, `api-request-blob` 50, `api-request` 17, `assistant` **40**,
  `system` 1.
- `assistant` entry keys: `apiBlockIndex, cwd, effort, entrypoint, gitBranch, isSidechain, message,
  parentUuid, perTurnEffort, requestId, requestRef, requestedModel, serverClassifierRequest,
  sessionId, session_id, thinkingDisplay, thinkingDurationMs, timestamp, type, userType, uuid,
  version, wireToolInputs`.
- `message` keys: `container, content, context_management, diagnostics, id, input_transformations,
  model, role, stop_details, stop_reason, stop_sequence, type, usage`.
- `usage` keys: `cache_creation, cache_creation_input_tokens, cache_read_input_tokens,
  fallback_credit, inference_geo, input_tokens, iterations, output_tokens,
  output_tokens_details, server_tool_use, service_tier, speed`.
- Values: `model = "claude-sonnet-5"` (40/40); `isSidechain = false` (40/40); `version = "2.1.304"`
  (40/40); `entrypoint = "cli"` (40/40). **Distinct `message.id` values: 17. Distinct `requestId`
  values: 17.** (40 assistant entries collapse to 17 unique API responses — the same
  per-content-block duplication the cloud report found, here confirmed on the local surface.)
- Redacted single-response sample (not a total; one `usage` object):
  ```json
  {"input_tokens": 2, "cache_creation_input_tokens": 69321, "cache_read_input_tokens": 34728,
   "output_tokens": 177, "output_tokens_details": {"thinking_tokens": 38},
   "server_tool_use": {"web_search_requests": 0, "web_fetch_requests": 0},
   "service_tier": "standard",
   "cache_creation": {"ephemeral_1h_input_tokens": 69321, "ephemeral_5m_input_tokens": 0},
   "inference_geo": "global", "speed": "standard", "fallback_credit": null}
  ```

### E12: Other local transcript entry types (keys/values only)
- Method: same script, extended to tally keys for `api-request-shape`, `api-request`,
  `api-request-blob`, `system`, `mode`, `permission-mode`, `atis-latch`, `file-history-snapshot`,
  `last-prompt`, `ai-title`, plus one structural (not content) sample of `system` and
  `api-request-shape`.
- Result: `api-request-shape` keys `sessionId, shape, shapeHash, timestamp, type, version`, where
  `shape` is itself a structural digest (tool names, `input_schema` field types — not real tool
  inputs). `api-request` keys include `base, cacheControl, id, keep, params, querySource,
  requestDigest, sessionId, shapeHash, tail, timestamp, type, version` — consistent with a
  prompt-cache bookkeeping record, not a copy of the request body. `api-request-blob` keys
  `hash, message, sessionId, type` (a hash plus an opaque blob reference; not decoded here).
  `system` entry keys: `cwd, durationMs, entrypoint, gitBranch, isMeta, isSidechain, messageCount,
  parentUuid, sessionId, subtype, timestamp, type, userType, uuid, version`; the one `system` entry
  observed has `subtype = "turn_duration"`. `mode` values: `{"normal": 13}`. `permission-mode`
  values: `{"auto": 13}`.

### E13: Search for a cost field in this session's own transcript
- Commands: `grep -o -i '"[a-z_]*cost[a-z_]*"' <file>`; `grep -c "costUSD\|total_cost_usd\|totalCostUsd" <file>`;
  a follow-up `grep -o '.\{15\}costUSD\|...' | cut -c1-15` to inspect match context
- Result: the field-name grep matched **zero** real JSON keys. The raw substring grep matched 3
  times, but every match's surrounding text was this session's **own prior conversational
  content** (this agent quoting phrases like "headless CLI's `total_cost_usd`" from the cloud
  report it had read, and this agent's own shell command text containing the string
  `total_cost_usd`) — i.e., a false positive from the transcript recording this very
  investigation, not a runtime-emitted cost field. **No genuine cost field exists in this
  interactive transcript.**

### E14: Loom binary
- Commands: `which loom`; `loom --version`; `loom --help`
- Result: `/opt/homebrew/bin/loom`; version `0.1.1`. Subcommands: `completion, health, install,
  tools, uninstall, update, version`. Description: "Loom installs agents, skills, and rules for
  Claude Code, Cursor, Windsurf, and other AI platforms." No `run` or pipeline-execution
  subcommand is present.

### E15: `guild-ledger-research` git state
- Commands: `git status --short --branch`; `git remote -v` (run inside that subfolder)
- Result: `## No commits yet on main...origin/main [gone]`; three untracked entries
  (`README.md`, `docs/`, `repositories.json`); `origin` set to
  `https://github.com/orieken/guild-ledger-research.git` (fetch+push). No commit exists locally
  to compare against the remote.

### E16: Scratch-edit demonstration
- Commands: create → `cat` (read back) → `rm` a file named `.scratch-edit-probe.txt` inside the
  new `docs/runtime-discovery/claude-code-headless/` folder, with a UTC timestamp written into it
- Timestamp: `2026-10-21T02:43:12Z`. Folder listing immediately after showed it empty again.

### E17: Managed-settings file absence
- Commands: `ls -la "/Library/Application Support/ClaudeCode/managed-settings.json"`; `ls -la
  "/etc/claude-code/managed-settings.json"`
- Result: both "No such file or directory."

### E18: `AGENTS.md` / `CLAUDE.md` discovery inputs
- Commands: `find /Users/oscarrieken/Projects/Rieken/guild-ledger -maxdepth 2 -iname "CLAUDE.md"
  -o -iname "AGENTS.md"`; `ls -la /Users/oscarrieken/AGENTS.md`
- Result: nothing found under the project tree; `/Users/oscarrieken/AGENTS.md` exists, 76,630
  bytes, owned by `oscarrieken`. This is the file whose content this turn's own system prompt
  labeled "project instructions, checked into the codebase," even though it is not inside the
  `guild-ledger` project tree — it is two directories above the working directory, at the home
  directory. Cross-referenced against D06 (§ below).

### E19: Subagent spawn-depth/concurrency override absence
- Command: `env | grep -c "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH\|CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS\|CLAUDE_CODE_SUBAGENT_MODEL"`;
  `find ~/.claude/projects/-Users-oscarrieken-Projects-Rieken-guild-ledger -maxdepth 2`
- Result: `0` matches (none of those three variables are set in this session's environment); the
  project transcript directory contains only the one session `.jsonl` file and an empty `memory/`
  folder — no `subagents/` subfolder, confirming none were spawned this session.

## Official documentation (retrieved 2026-10-21)

| ID | Page | Used for |
|---|---|---|
| D01 | https://code.claude.com/docs/en/headless | `-p`/`--bare` behavior, output formats, `--max-budget-usd`, SIGTERM (exit 143, no result recorded, `SessionEnd` hooks still run) vs SIGINT, working-directory-deleted behavior, `system/init`/`system/api_retry` stream-json events, `parent_tool_use_id` subagent lineage, `--continue`/`--resume` session totals (since v2.1.277), background-task-at-exit waiting and its cap |
| D02 | https://code.claude.com/docs/en/agent-sdk/cost-tracking | `usage` (main loop only) vs `total_cost_usd`/`modelUsage` (whole tree, subagents included) distinction; per-step `output_tokens` placeholder at `message_start`; dedupe by message id; crash → `error_during_execution` with possibly-zeroed `usage`/`total_cost_usd`/`modelUsage`; recovery procedure from the turn before a crash; cache token fields; all cost figures are explicitly client-side estimates, not billing |
| D03 | https://code.claude.com/docs/en/settings | Settings file scopes (user/shared-project/project-local/managed) and precedence order; `--bare`/`--safe-mode`/`--restricted` differences; `--setting-sources`; `/status` "Setting sources" line; cloud sessions read only some of these files |
| D04 | https://code.claude.com/docs/en/costs | `/usage` Session block is a local list-price estimate; explicitly "not relevant for billing purposes" for Pro/Max subscribers; plan-usage breakdown (attribution by skill/subagent/plugin/MCP, computed from local session history only, not cross-device); usage credits and spend limits; Console/Enterprise-Analytics-API paths that don't apply to a subscription account |
| D05 | https://code.claude.com/docs/en/sub-agents | Default subagent spawn depth **3** (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` to change, `1` disables nesting), default concurrency **20** (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`), no dollar/token cap beyond depth/concurrency/`maxTurns`/model routing, model-resolution order, per-subagent transcript file path |
| D06 | https://code.claude.com/docs/en/memory | Exact `AGENTS.md` discovery rule: read from the working directory and every directory above it when no `CLAUDE.md`/`CLAUDE.local.md` exists in that chain; `~/.claude/CLAUDE.md` and `.claude/rules/` files don't count toward that check and load alongside `AGENTS.md` regardless; `~/.claude/rules/` is documented as "personal rules [that] apply to every project on this machine," loaded without the per-project trust dialog |

## Not tested (deliberately)

- Running `claude -p`, `--bare`, `--bg`, `--cloud`, or any other command that would start a second
  model session or an API call (explicitly out of scope for this task).
- Spawning any subagent via the Agent tool.
- Running `/usage`, `/status`, `/doctor` (the slash-command forms), `/model`, or any other
  in-session command that exists only inside an interactive REPL turn rather than as a shell
  command (this agent can only run shell commands via `Bash`, not REPL slash-commands on itself).
- Reading `~/.credentials.json` or any credential/token value.
- Installing, updating, or reconfiguring anything (`claude update`, `loom install`, etc.).
- Committing or pushing any change in `guild-ledger-research` or any other repository.
- Measuring actual cancellation/interruption behavior (SIGTERM/SIGINT) against a live run —
  reported only from documentation (D01).
- Verifying the backend model's dated revision beyond the response-reported `message.model` field.
