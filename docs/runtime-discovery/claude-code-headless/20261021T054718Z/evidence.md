# Evidence: Claude desktop app Code session over Remote Control (20261021T054718Z)

Captured 2026-10-21 by the agent inside this session. All commands ran read-only on the user's Mac
except the scratch-edit demo (E14) and writing these three files. Values that are credentials,
account/org UUIDs, email addresses, messaging tokens or socket paths were **not printed**; only
variable *names* were listed for those. Exit status is 0 unless stated.

## Observations

### E01 · process ancestry
`ps` walk from the shell's parent to PID 1:

```text
80682 80681 ~/Library/Application Support/Claude/claude-code/2.1.304/6bbba6adc37f/claude.app/Contents/MacOS/claude
80681 69323 /Applications/Claude.app/Contents/Helpers/disclaimer
69323     1 /Applications/Claude.app/Contents/MacOS/Claude
    1     0 /sbin/launchd
```

No Terminal.app, no `zsh` login shell, no Homebrew `claude` in the chain. The runtime is the copy
the desktop app downloaded into its own Application Support folder.

### E02 · runtime and app versions
- `which claude` → `/opt/homebrew/bin/claude`; `claude --version` → `2.1.304 (Claude Code)` (the
  Homebrew copy, **not** the one running this session).
- `"$CLAUDE_CODE_EXECPATH" --version` → `2.1.304 (Claude Code)` (the bundled copy actually running).
- `ls ~/Library/Application Support/Claude/claude-code/` → `2.1.299`, `2.1.304` (two bundled
  versions retained by the app).
- `CLAUDE_AGENT_SDK_VERSION=0.3.304`, `CLAUDE_CODE_DESKTOP_APP_VERSION=3.1623.0`;
  `Claude.app` Info.plist `CFBundleShortVersionString` → `3.1623.0`.

### E03 · selected environment variables (values shown only where non-sensitive)

```text
CLAUDE_CODE_ENTRYPOINT=claude-desktop
CLAUDE_CODE_CHILD_SESSION=1
CLAUDE_CODE_SESSION_ATTENDED=1
CLAUDE_EFFORT=medium
CLAUDE_CODE_SESSION_ID=07197307-1d89-4916-8c29-631390b30bbf
CLAUDE_CODE_SIMPLE=0
CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING=true
CLAUDE_CODE_EAGER_FLUSH=1
CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH=1
CLAUDE_CODE_TERMINAL_MCP_TOOLS=mcp__ccd_turn__wrap_up
ANTHROPIC_BASE_URL host = https://api.anthropic.com
ANTHROPIC_API_KEY = unset
ANTHROPIC_MODEL, CLAUDE_CODE_SUBAGENT_MODEL, CLAUDE_CODE_REMOTE = unset
```

Names present but values withheld: `CLAUDE_CODE_ACCOUNT_UUID`, `CLAUDE_CODE_ORGANIZATION_UUID`,
`CLAUDE_CODE_USER_EMAIL`, `CLAUDE_CODE_OAUTH_SCOPES`, `CLAUDE_CODE_MESSAGING_SOCKET`,
`CLAUDE_CODE_MESSAGING_TOKEN`, `CLAUDE_CODE_HOST_SESSION_ID`.

### E04 · this session's transcript, schema only
File `~/.claude/projects/-Users-oscarrieken-Projects-Rieken-guild-ledger/07197307-….jsonl`
(mode 0600, ~1.09 MB at capture). Tallied with a `python3 -I` script that printed counts and key
names only:

```text
entry types: queue-operation 3, user 15, attachment 31, last-prompt 9, atis-latch 9,
             api-request-shape 1, api-request-blob 20, api-request 12, assistant 22
assistant: 22 entries → 12 distinct message.id, 12 distinct requestId
assistant message.model: claude-opus-5-5 (22/22)
entrypoint: claude-desktop (72/72) · version 2.1.304 (86/86) · querySource: sdk
requestedModel: claude-opus-5-5[1m] · advisorModel: claude-opus-5-5 · effort/perTurnEffort: medium
permissionMode: auto (1 entry)
api-request.params keys: betas, context_management, max_tokens, model, output_config, thinking
  params.model=claude-opus-5-5 · max_tokens=128000 · thinking={"type":"adaptive","display":"summarized"}
  output_config={"effort":"medium"}
usage keys: input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens,
  cache_creation.{ephemeral_5m,ephemeral_1h}_input_tokens, output_tokens_details.thinking_tokens,
  server_tool_use.{web_search_requests,web_fetch_requests}, service_tier, speed, inference_geo,
  fallback_credit, iterations
```

No `costUSD`/`total_cost_usd` field: the single substring hit was this session's own Bash command
text, a false positive. `api-request*` entry types did not appear in the prior terminal report's
schema tally (E11 there); this is the first observation of client-recorded outbound request
parameters on this machine.

### E05 · user settings (`~/.claude/settings.json`, keys and relevant values only)
`tui`, `theme`, `switchModelsOnFlag` (type only); `autoMemoryEnabled=false`,
`disableClaudeAiConnectors=true`,
`enabledPlugins={"engineering@synced":false,"data@synced":false,"searchfit-seo@synced":false}`.
No `hooks`, `permissions`, `model`, `env` keys. No `~/.claude/settings.local.json`,
`~/.claude/CLAUDE.md` or `~/AGENTS.md`. `~/.claude/rules/` is an empty real directory.
`~/.claude/skills/` contains only `synced/<account-id-dir>`.

### E06 · CLI inventory (Homebrew `claude`, same version)
- `claude mcp list` → `No MCP servers configured.`
- `claude plugin list` → `engineering@synced` 1.2.0, `data@synced` 1.1.0, `searchfit-seo@synced`
  1.0.0, each `Status: ✘ disabled`.

### E07 · effective MCP servers in **this** session (`session_connectors_status`, read-only app tool)
- 17 plugin-provided servers: `plugin:engineering:{slack,linear,asana,atlassian,notion,github,pagerduty,datadog}`
  and `plugin:data:{bigquery,hex,amplitude,amplitude-eu,definite}` → `needs_auth`;
  `plugin:engineering:{google calendar,gmail}`, `plugin:data:{snowflake,databricks}` → `failed`
  ("No URL configured").
- 4 claude.ai connectors **connected**: Claude Docs (8 tools), Indeed (4), visualize (2),
  ZipRecruiter (1).
- Host servers connected: `hearthbot` (21 tools, Projects messaging), `claude-code-remote` (1),
  `scheduled-tasks` (6). The tool list also exposes desktop-app tool families (`ccd_session`,
  `ccd_session_mgmt`, `ccd_settings`, `ccd_pr`, `ccd_host`, `ccd_window`, …), the built-in
  browser pane, the iOS simulator tool, and Claude in Chrome tool names.

### E08 · effective skills in this session
The session's skill listing (names only) includes `engineering:*` (10), `data:*` (10),
`searchfit-seo:*` (17, plus 3 `searchfit-seo` agent types), `anthropic-skills:*` (17) and
built-in skills (artifact, code-review, schedule, etc.). `ListPlugins` (claude.ai
account plugins) returns `searchfit-seo`, `engineering`, `data`, all `"enabled": true`.

### E09 · context-window composition (`get_usage`, self)
140,134 / 1,000,000 tokens at capture; auto-compact at 97 %. Categories: Messages 38,143;
MCP tools 37,634; System tools 27,860; System prompt 25,984; Skills 9,534; MCP server
instructions 638.

### E10 · plan limits (`get_usage`)
`plan: "Pro"`; 5-hour window 19 % used; weekly all-models 29 % used; extra usage `enabled:false`,
`spent:"0.00" USD`. Percentages only; no token or dollar figures per session.

### E11 · Code tab settings (`get_settings`, read-only)
`default_permission_mode: default` (no settings tier sets it), auto mode and bypass mode allowed by
policy, `settings_default_model: not set`, `settings_fast_mode: not set`,
`connect_new_sessions_to_remote_control: not set`, `browser_tools: On`,
`prompt_suggestions: On` ("each suggestion is one more model request").

### E12 · bundled CLI help (`"$CLAUDE_CODE_EXECPATH" --help`, grep)
Lists `-p/--print`, `--output-format`, `--input-format`, `--tools`, `--allowedTools`, `--bare`,
`--safe-mode`, `--restricted`, `--setting-sources`, `--strict-mcp-config`, `--mcp-config`,
`--model`, `--effort`, `--session-id`, `--permission-mode`, `--no-session-persistence`,
`--max-budget-usd` ("only works with --print"), `--append-system-prompt`,
`--disable-slash-commands`. `--max-turns` did **not** match, same as the prior reports.

### E13 · repository state
`guild-ledger-research`: branch `main`, no commits, `origin` →
`https://github.com/orieken/guild-ledger-research.git`; untracked `README.md`, `docs/`,
`repositories.json`. Parent `guild-ledger/` is not a git repo. No project-level `.claude/`,
`CLAUDE.md` or `AGENTS.md` within depth 2 (prior report E07, re-checked by listing).

### E14 · scratch-edit demonstration
Created `20261021T054718Z/scratch.tmp`, read it back (`scratch 20261021T054718Z`), removed it;
folder then held 0 entries before these reports were written.

### E15 · memory directory
`~/.claude/projects/-Users-oscarrieken-Projects-Rieken-guild-ledger/memory` does not exist. The
project transcript directory holds 3 `.jsonl` files (contents not read beyond this session's own).

### E16 · Projects context
The project chat shows Oscar's request, the coordinator's Remote Control proposal for folder
`~/Projects/Rieken/guild-ledger`, and an `active` Remote Control record before this thread's
session started. This session was launched by Claude Projects through the desktop app, not by
the user typing in a terminal.

### E17 · prior reports read (not modified)
`claude-code/` (cloud thread), `claude-code-headless/` (pre-cleanup terminal, with
`review-codex.md`), `claude-code-headless/20261021T053558Z/` (post-cleanup terminal),
`codex-headless/20261021T053548Z/`.

## Official documentation (retrieved 2026-10-21)

- **D01** [Run Claude Code programmatically](https://code.claude.com/docs/en/headless): `-p`,
  `--output-format json|stream-json`, `--bare` skips hooks/skills/plugins/MCP/auto memory/CLAUDE.md
  and never reads OAuth credentials (needs `ANTHROPIC_API_KEY` or `apiKeyHelper`); JSON result has
  `total_cost_usd` and per-model breakdown, described as client-side estimates; resumed runs report
  cumulative totals; SIGTERM → exit 143 with no result for the in-flight turn; `system/init` lists
  model, tools, MCP servers, plugins; `system/api_retry` events; subagent messages carry
  `parent_tool_use_id`; `-p` defaults to Manual permission mode from v2.1.302.
- **D02** [Claude desktop app](https://code.claude.com/docs/en/desktop): reads the same settings
  files as the CLI for `permissions.defaultMode` and `env`; local sessions load skills enabled for
  the claude.ai account (skipped only if an org sets `disableSideloadFlags`); Remote Control
  switch, `connect new sessions` setting, `disableRemoteControl`; page describes **no** headless
  or scripting interface for starting desktop sessions. Only the first ~100k characters of the
  page were read.
- **D03** [CLI reference](https://code.claude.com/docs/en/cli-reference) and
  **D04** [Agent SDK cost tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking):
  cited via D01's links; not re-fetched in this session.

## Not tested

No `claude -p`, `--bare`, SDK call, background agent, subagent, signal/interrupt, `/usage`,
transcript export, routine run or Loom command. No settings changed (all `ccd_settings`/
`ccd_connectors` calls were read-only). No credential, auth file, other transcript, desktop-app
database or hidden prompt text was opened.
