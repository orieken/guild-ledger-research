# Evidence log: claude-code-headless (post-cleanup local terminal Claude Code)

Captured 2026-10-21 between 05:34 and 05:37 UTC by the agent running inside the surface being
described, in a new interactive session started **after** the global cleanup recorded in
[15-local-agent-reset.md](../../../docs/research/15-local-agent-reset.md). Every entry is a
redacted observation or a documentation citation. Secret values, credential file contents,
environment values not listed here, hidden system-prompt text, private reasoning, and personal
identifiers were not read into this file. `claude mcp list`/`claude plugin list` output below is
reproduced because server/plugin names, versions, paths and status are configuration metadata, not
secrets; no tokens or credential values are shown.

Status vocabulary used in `report.md`/`capabilities.json`: **observed** (verified here),
**documented** (official docs or local `--help` text), **inferred** (reasoned, unverified),
**unknown**.

## Observations (commands and tool calls)

### E01: CLI binary version and path
- Commands: `which claude`; `claude --version`
- Result: `/opt/homebrew/bin/claude`; `2.1.304 (Claude Code)` — identical to the prior
  (pre-cleanup) report, confirming the cleanup did not change the installed runtime version.

### E02: Process ancestry (surface verification)
- Commands: `ps -p $PPID -o pid,ppid,comm`; a loop walking `ppid` up five levels
- Result:
  ```
  claude (37156) -> zsh (3981, -zsh)
  zsh (3981)      -> login (3790)
  login (3790)    -> Terminal.app (684, .../Terminal.app/Contents/MacOS/Terminal)
  Terminal.app (684) -> launchd (1)
  ```
- Note: same shape as the prior report's E02 (different PID, same ancestry pattern): no cloud
  relay, coordinator, or nested Claude process anywhere in the chain.

### E03: Env var names only (claude/anthropic-related), no values
- Command: `env | cut -d= -f1 | sort | grep -i -E "claude|anthropic|sandbox|cursor|codex|copilot"`
- Result: `CLAUDE_CODE_CHILD_SESSION`, `CLAUDE_CODE_ENTRYPOINT`, `CLAUDE_CODE_EXECPATH`,
  `CLAUDE_CODE_MESSAGING_SOCKET`, `CLAUDE_CODE_MESSAGING_TOKEN`, `CLAUDE_CODE_SESSION_ATTENDED`,
  `CLAUDE_CODE_SESSION_ID`, `CLAUDE_EFFORT`, `CLAUDE_PID`, `CLAUDECODE`. Identical name set to the
  prior report. No `ANTHROPIC_API_KEY`, `CLAUDE_CODE_VERSION`,
  `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, or `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` present.

### E04: Values of the non-secret vars named in E03, plus terminal vars
- Commands: `printenv` on each named variable (not bash `${!v}` indirection, which failed under
  this zsh shell — noted as a tooling correction, not a finding); `wc -c` on the session-id length
  only
- Result: `CLAUDE_CODE_ENTRYPOINT=cli`; `CLAUDE_CODE_CHILD_SESSION=1`; `CLAUDECODE=1`;
  `CLAUDE_EFFORT=high`; `CLAUDE_CODE_SESSION_ATTENDED=1`; session-id length = 37 characters
  (36-char UUID + trailing newline from `printenv`, consistent with the prior report's 36);
  `TERM_PROGRAM=Apple_Terminal`; `SHELL=/bin/zsh`;
  `PWD=/Users/oscarrieken/Projects/Rieken/guild-ledger`; `CLAUDE_CODE_VERSION` /
  `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` / `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` all empty
  (unset). `CLAUDE_CODE_CHILD_SESSION=1` is present again despite a plain, directly-launched
  terminal ancestry (E02) — the same anomaly the prior report flagged, now observed a second time
  in an independently started session, which weakens (but does not resolve) the hypothesis that it
  reflects true session parentage.

### E05: Operating environment
- Commands: `whoami`, `hostname`, `uname -srm`, `node --version`, `date -u`
- Result: user `oscarrieken`, host `Mac`, `Darwin 25.6.0 arm64`, Node `v22.22.3` — identical to the
  prior report.

### E06: `~/.claude` directory structure and settings content (post-cleanup)
- Commands: `ls -la ~/.claude/`; `cat ~/.claude/settings.json`; `ls -la ~/.claude/CLAUDE.md`;
  `ls -la ~/.claude/rules` + `ls ~/.claude/rules/ | wc -l`; `ls -la ~/.claude/skills` +
  `find ~/.claude/skills/synced -maxdepth 2 -mindepth 1 | wc -l`; `cat
  ~/.claude/framework-install.json`; `ls -la ~/.claude/plugins/`; `file ~/.claude/rules`;
  `file ~/.claude/skills`
- Result (all deltas relative to the pre-cleanup report's E06):
  - `~/.claude/settings.json` now reads
    `{"tui":"fullscreen","theme":"dark-ansi","switchModelsOnFlag":false,"autoMemoryEnabled":false,"disableClaudeAiConnectors":true,"enabledPlugins":{"engineering@synced":false,"data@synced":false,"searchfit-seo@synced":false}}`
    — directly confirms the three settings-level changes claimed in `15-local-agent-reset.md`
    (auto-memory disabled, connector fetching disabled, all three synced plugins disabled). Still
    no `hooks` key.
  - `~/.claude/CLAUDE.md` **no longer exists** (previously a broken symlink to
    `ai-assistant-dot-files/.claude.md`; `ls` now returns "No such file or directory").
  - `~/.claude/rules` is now a **real, empty directory** (`file` reports "directory", not a
    symlink; 0 entries) — previously a symlink to `ai-assistant-dot-files/shared/rules/` holding
    17 files.
  - `~/.claude/skills` is now a **real directory** (not a symlink) containing only a `synced/`
    subfolder — previously a symlink to `ai-assistant-dot-files/shared/skills/` holding 71 entries.
    `synced/` holds one empty `.bucket-<id>` marker file and one `<id>` directory with 13
    subdirectories (`built-in-browser`, `chrome-browser`, `computer-use`, `deep-research`, `docs`,
    `docx`, `google-workspace`, `import-memory`, `morning`, `pdf`, `pptx`, `skill-creator`, `xlsx`)
    plus a `manifest.json` — these names match this session's own `anthropic-skills:*`
    system-reminder skill listing, i.e. this is the account-level built-in/synced skill catalog,
    not the removed personal skill set.
  - `~/.claude/framework-install.json` **no longer exists** (previously present, documenting the
    `ai-assistant-dot-files` symlink source).
  - `~/.claude/plugins/` still has `blocklist.json`, `known_marketplaces.json`, a
    `plugin-directory-cache-v2.json` cache, and `synced/` — a stale on-disk plugin cache, which
    `claude plugin list` (E08 below) confirms is inert (all three entries disabled).
  - `~/.claude/` also now shows additional housekeeping paths not inventoried in the prior report:
    `.last-cleanup` (a one-line UTC timestamp marker, `2026-10-21T02:58:03.725Z`), `backups/`,
    `cache/`, `chrome/`, `file-history/`, `ide/`, `mcp-needs-auth-cache.json`, `paste-cache/`,
    `session-env/` (per-session scratch subfolders keyed by UUID, names only inspected),
    `shell-snapshots/`, `telemetry/`. None of these were opened beyond directory/file listing;
    they are ordinary app-state paths, not inspected for content.

### E07: Absence of project-level `.claude/` directories
- Commands: `ls -la .../guild-ledger/.claude`; `ls -la .../guild-ledger/guild-ledger-research/.claude`
- Result: both fail with "No such file or directory" — unchanged from the prior report. Neither
  the parent folder nor the research checkout defines project-level settings, hooks, or
  `.mcp.json`.

### E08: Configured MCP servers and plugin status (post-cleanup)
- Commands: `claude mcp list`; `claude plugin list`
- Result: `claude mcp list` → **"No MCP servers configured. Use `claude mcp add` to add a server."**
  — a complete change from the prior report's ~12 account-level and marketplace-plugin servers in
  mixed connected/needs-auth/failed states. `claude plugin list` shows all three synced plugins
  (`engineering@synced` v1.2.0, `data@synced` v1.1.0, `searchfit-seo@synced` v1.0.0) with
  `Status: ✘ disabled`, matching `enabledPlugins` in E06 and `claude_plugins_still_enabled: []` in
  the cleanup receipt (E20).
- `~/.claude/mcp-needs-auth-cache.json` still lists nine server names with stale timestamps (a
  leftover auth-check cache, not live connections — consistent with "a plugin cache remaining on
  disk is not an enabled plugin" from `15-local-agent-reset.md`).

### E09: `claude --help` (full flag and subcommand text, captured verbatim this session)
- Command: `claude --help`
- Result: version-matched (2.1.304) full help text captured directly into this session (see
  `report.md` §2/§8 for the specific flags cited). Confirms, in the tool's own wording, the
  distinction the prior Codex review (F01) asked to resolve: `--allowedTools`/`--disallowedTools`
  are auto-approval lists ("tool names to allow/deny"), while `--tools <tools...>` is the actual
  built-in-tool catalog control ("Use `\"\"` to disable all tools, `\"default\"` to use the default
  set, or specify tool names"); `--restricted` separately removes code-running tools and
  `WebFetch` "unless `--tools` names them." `--max-turns` is **still absent** from this version's
  `--help` output, the same discrepancy the prior review (F05) flagged against the official CLI
  reference — not re-resolved this session (would require either a newer version or reading
  parser source, neither done here). New flags visible in this verbatim capture not called out
  by name in the prior (summarized) E09 include `--cloud`, `--desktop`, `--remote-control`,
  `--file`, `--chrome`/`--no-chrome`, `-w/--worktree` with `--tmux`,
  `--allow-dangerously-skip-permissions` (distinct from `--dangerously-skip-permissions`),
  `--autocompact`, `--exclude-dynamic-system-prompt-sections`, `--prompt-suggestions`,
  `--from-pr`, `-n/--name`, `--betas`, `--brief`, `--ax-screen-reader`; subcommands `gateway`,
  `purge`, `ultrareview` also appear. Whether these are genuinely new to this install or were
  simply omitted from the prior report's selective summary is **unknown** — the prior evidence.md
  stated it recorded only "headless/automation-relevant flags," not a verbatim diff baseline.

### E10: `claude doctor` (read-only health check)
- Command: `claude doctor`
- Result:
  ```
  Running: package-manager (2.1.304)
  Commit: 17ab70404e5b
  Platform: darwin-arm64
  Package manager: homebrew
  Path: /opt/homebrew/Caskroom/claude-code/2.1.304/claude
  Config install method: unknown
  Search: OK (bundled)
  Auto-updates: Managed by package manager
  Auto-update channel: latest
  Last update attempt: none recorded
  Managed settings (remote): not fetched — requires an Enterprise or Team subscription
  Organization policy: not applicable to Pro and Max accounts

  Remote Control
  Control this session from claude.ai/code or the Claude mobile app

  No installation issues found.
  ```
  Same version/commit as the prior report; this capture additionally shows a "Remote Control"
  section ("Control this session from claude.ai/code or the Claude mobile app") not quoted in the
  prior evidence.md. Not exercised — unknown whether this changes effective control/isolation of
  this local session, or was simply not quoted before.

### E11: Local session transcript schema (this session; keys/types/counts only, no content printed)
- Path: `~/.claude/projects/-Users-oscarrieken-Projects-Rieken-guild-ledger/0ce38a75-14d9-451d-ae7f-c49bce7d1eda.jsonl`
  (session UUID matches the scratchpad path given in this session's own environment block,
  already visible to the user in their own terminal).
- Method: a Python script, run with `python3 -I` (isolated mode, no site/user-dir code injection)
  directly against this agent's own trusted session file, tallied `type` values, key sets,
  model/entrypoint/version/isSidechain counts, distinct `message.id`/`requestId` counts, and
  printed exactly one redacted `usage` sample. No prompt or completion text was printed.
- Result at time of inspection: **168** total lines. Type counts: `mode` 9, `permission-mode` 9,
  `atis-latch` 9, `file-history-snapshot` 1, `user` 27, `attachment` 23, `last-prompt` 8,
  `ai-title` 8, `assistant` **39**, `api-request-shape` 1, `api-request-blob` 25, `api-request` 9.
- `assistant` keys, `message` keys, and `usage` keys are byte-for-byte identical to the prior
  (pre-cleanup) report's E11 — the transcript schema did not change across the cleanup.
- Values: `model = "claude-sonnet-5"` (39/39); `isSidechain = false` (39/39); `version = "2.1.304"`
  (39/39); `entrypoint = "cli"` (39/39). **Distinct `message.id` values: 9. Distinct `requestId`
  values: 9.** 39 assistant entries collapse to 9 unique API responses — a **~4.3x** duplication
  ratio, versus the prior report's **~2.35x** (40/17) on a different session. This confirms the
  duplication factor is **not a fixed constant**: any usage-estimation approach must dedupe by
  `message.id` per session rather than assume a stable multiplier.
- Redacted single-response sample (not a total):
  ```json
  {"input_tokens": 2, "cache_creation_input_tokens": 12205, "cache_read_input_tokens": 34728,
   "output_tokens": 364, "output_tokens_details": {"thinking_tokens": 83},
   "server_tool_use": {"web_search_requests": 0, "web_fetch_requests": 0},
   "service_tier": "standard",
   "cache_creation": {"ephemeral_1h_input_tokens": 12205, "ephemeral_5m_input_tokens": 0},
   "inference_geo": "global", "speed": "standard", "fallback_credit": null,
   "iterations": [{"...": "one-entry array, same shape as the single usage object"}]}
  ```

### E12: Search for a cost field in this session's own transcript
- Commands: `grep -o -i '"[a-z_]*cost[a-z_]*"' <file>` (0 real JSON-key matches);
  `grep -c "costUSD|total_cost_usd|totalCostUsd" <file>` (4 raw substring matches);
  `grep -o '.\{10\}cost[A-Za-z_]*.\{10\}' <file>` to inspect match context
- Result: all 4 substring matches are this session's **own system-prompt/conversational text** —
  specifically the phrase "the cost of pausing to confirm is low, while the cost of an unwanted
  action... could be very high" from this very system prompt's "Executing actions with care"
  section, and "times the cost" / "lity, and cost" fragments from the same passage — not a
  runtime-emitted cost field. **No genuine cost field exists in this interactive transcript**,
  matching the prior report's E13 finding on a different session.

### E13: Subagent lineage absence and sibling-session structure (names only)
- Commands: `find ~/.claude/projects/-Users-oscarrieken-Projects-Rieken-guild-ledger -maxdepth 2`
- Result: this project's transcript directory contains this session's own `.jsonl`, plus one
  **other, earlier session** (`11bb697c-fcb7-45a2-96dc-fab08ed3b4e1`, both a `.jsonl` file and a
  `tool-results` subfolder — not this session, not opened/read, noted structurally only as
  "unrelated conversation," per the task's restriction). No `subagents/` subfolder exists under
  this session's own id — confirming no subagents were spawned this session (task constraint).

### E14: Loom binary (post-removal)
- Commands: `which loom`; `loom --version`; `loom --help`
- Result: **`loom not found`** — the prior report's `/opt/homebrew/bin/loom` v0.1.1 installation is
  gone from `PATH` on this machine, consistent with the 55-path removal recorded in
  `.local-backups/loom-global-20261021T034807Z/receipt.json` (`loom_on_path: null`,
  `homebrew_exit_code: 0`). This session did not inspect whether the separate
  `ai-assistant-dot-files` source checkout (referenced by the prior Codex review, F03) still
  contains a buildable pipeline executor elsewhere on disk — that checkout is a sibling project
  outside this task's scope and was not opened.

### E15: `guild-ledger-research` git state
- Commands: `git status --short --branch`; `git remote -v`; `git log --oneline -5` (run inside that
  checkout)
- Result: `## No commits yet on main...origin/main [gone]`; untracked: `README.md`, `docs/`,
  `repositories.json`; `origin` set to `https://github.com/orieken/guild-ledger-research.git`
  (fetch+push); `git log` fails ("your current branch 'main' does not have any commits yet") —
  unchanged from the prior report. This session's new files are added to that same untracked
  `docs/` tree and remain uncommitted, per the task.

### E16: Scratch-edit demonstration
- Commands: create → `cat` (read back) → `rm` a file named `.scratch-edit-probe.txt` inside this
  new report folder, with a UTC timestamp written into it
- Result: recorded in `report.md` §"Finish"; demonstrates local write/read/remove access only,
  following the same pattern as both prior reports' equivalent probes.

### E17: Managed-settings file absence
- Commands: `ls -la "/Library/Application Support/ClaudeCode/managed-settings.json"`;
  `ls -la "/etc/claude-code/managed-settings.json"`
- Result: both "No such file or directory" — unchanged from the prior report.

### E18: `AGENTS.md` / `CLAUDE.md` discovery inputs (post-cleanup)
- Commands: `find .../guild-ledger -maxdepth 2 -iname "CLAUDE.md" -o -iname "AGENTS.md"`;
  `ls -la /Users/oscarrieken/AGENTS.md`; `ls -la /Users/oscarrieken/CLAUDE.md`
- Result: **nothing found anywhere** — no `CLAUDE.md`/`AGENTS.md` under the project tree, and the
  previously-present `/Users/oscarrieken/AGENTS.md` (76,630 bytes, the file the prior session's own
  system prompt had labeled "project instructions, checked into the codebase") **no longer exists**.
  This matches the last entry of `removed-paths.json` (`"AGENTS.md"`) in the loom-global-removal
  backup. **This session's own system prompt carried no project-instructions section corresponding
  to any of these files** — a directly observable behavioral confirmation that the removal is
  effective for this session, not just a file-listing inference.

### E19: Subagent spawn-depth/concurrency override absence
- Command: `printenv CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS
  CLAUDE_CODE_SUBAGENT_MODEL`
- Result: all empty/unset — unchanged from the prior report; documented defaults (depth 3,
  concurrency 20) would apply if the Agent tool were used, which it was not this session (task
  constraint).

### E20: Cleanup receipts (read as operation records, not personal content)
- Files read: `.local-backups/agent-clean-state-20261021T035433Z/manifest.json` and `receipt.json`;
  `.local-backups/loom-global-20261021T034807Z/receipt.json` and `removed-paths.json`
- Result: these are the researcher's own prior-session operation logs (file paths, actions taken,
  SHA-256 hashes of removed files, and summary counts) describing exactly the changes corroborated
  by E06–E09/E14/E18 above. No personal file *content* was read — the manifest lists paths and
  hashes, not the archived files' bodies. Key figures: 12 extra files/links archived+removed, 12
  project-memory directories / 17 memory files archived+removed (none of them for this `guild-ledger`
  project — all were for `ai-assistant-dot-files`, `Training`, `phd-research`, `jobforge`, and
  `rieken-budget`), 3 plugins disabled, connector fetching disabled, auto-memory disabled; separately,
  55 global Loom-related paths removed with Homebrew exit code 0 and `loom_on_path: null`.

### E21: Sibling Codex discovery report (same prompt, same approximate timestamp)
- Command: `find .../docs/runtime-discovery/codex-headless/20261021T053548Z`; read that folder's
  `report.md`
- Result: a parallel discovery report already exists at
  `docs/runtime-discovery/codex-headless/20261021T053548Z/`, captured `2026-10-21T05:35:48Z` — about
  two minutes before this report's own timestamp. It documents a **separate Codex session**
  (`codex-cli 0.163.0`), explicitly noting its own process ancestry inspection was denied and that
  it started in a "ChatGPT project mirror," not this research checkout. This confirms the same
  discovery prompt was dispatched to (at least) two independent surfaces; it is read here only to
  avoid contradicting or duplicating that session's claims, not treated as evidence about this
  Claude Code session.

### E22: Permission-mode tally for this session's transcript
- Command: a Python script (`python3 -I`) tallying `type == "permission-mode"` entries in this
  session's own transcript (same file as E11), reading only the `mode` field.
- Result: **14** `permission-mode` entries, all value `auto` — consistent with the "Auto Mode
  Active" disclosure in this session's own system reminder. Added after an internal JSON-validation
  pass found this capability (`tools.permissions`) had been asserted as `observed` with no
  supporting evidence id, the same gap the prior Codex review (F04) flagged on the pre-cleanup
  report; this entry corrects it with a real per-session tally rather than carrying the claim
  forward unsupported.

## Official documentation (prior retrieval, 2026-10-21; not re-fetched this session)

| ID | Page | Used for |
|---|---|---|
| D01 | https://code.claude.com/docs/en/headless | `-p`/`--bare` behavior, output formats, `--max-budget-usd`, SIGTERM/SIGINT semantics, `system/init`/`system/api_retry` events, `parent_tool_use_id` lineage, resume/continue totals |
| D02 | https://code.claude.com/docs/en/agent-sdk/cost-tracking | `usage` vs `total_cost_usd`/`modelUsage` scope; per-step `output_tokens` placeholder; dedupe by message id; crash zeroing/recovery; all cost figures are client-side estimates |
| D03 | https://code.claude.com/docs/en/settings | Settings file scopes/precedence; `--bare`/`--safe-mode`/`--restricted`; `--setting-sources` |
| D04 | https://code.claude.com/docs/en/costs | `/usage` local estimate, explicitly "not relevant for billing" on Pro/Max; plan-usage breakdown scope |
| D05 | https://code.claude.com/docs/en/sub-agents | Default spawn depth 3 / concurrency 20; per-subagent transcript path |
| D06 | https://code.claude.com/docs/en/memory | `AGENTS.md` discovery rule; `~/.claude/rules/` as per-machine personal rules |

This session reused these citations rather than re-fetching, since none of the underlying product
documentation is expected to have changed in the ~3 hours since the prior report, and no
WebFetch/WebSearch call was made this session. This is a limitation: the doc content was **not**
independently re-verified this session, only carried forward.

## Not tested (deliberately)

- Running `claude -p`, `--bare`, `--bg`, `--cloud`, or any other command that would start a second
  model session or an API call (explicitly out of scope for this task).
- Spawning any subagent via the Agent tool.
- Running `/usage`, `/status`, `/doctor` (the slash-command forms) or any other in-session REPL
  command (this agent can only run shell commands via `Bash`, not REPL slash-commands on itself).
- Reading `~/.credentials.json`, `~/.claude/.credentials.json`, or any credential/token value.
- Reading the content of the sibling, unrelated session transcript (`11bb697c-...`) or any
  project-memory/backup file content beyond path/hash metadata.
- Installing, updating, or reconfiguring anything.
- Committing or pushing any change in `guild-ledger-research` or any other repository.
- Measuring actual cancellation/interruption behavior (SIGTERM/SIGINT) against a live run.
- Re-fetching official documentation (D01–D06 carried forward from the prior report, not
  independently re-verified this session).
- Verifying the backend model's dated revision beyond the response-reported `message.model` field.
- Inspecting the `ai-assistant-dot-files` sibling checkout to determine whether a Loom
  pipeline-executor source still exists there after the global removal.
