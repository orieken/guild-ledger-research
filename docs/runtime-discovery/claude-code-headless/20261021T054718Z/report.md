# Runtime discovery: Claude desktop app Code session launched from Claude Projects (post-cleanup)

Captured 2026-10-21T05:47Z by the agent inside the session it describes. Evidence IDs (E.., D..)
refer to [evidence.md](evidence.md); the machine-readable record is
[capabilities.json](capabilities.json). This is a discovery record, not a benchmark, and it does
not show benchmark performance, harness effects or isolation.

**Read this first.** The folder is filed under `claude-code-headless/` as requested, but this
session is **not headless**. It is an interactive, attended Claude Code session embedded in the
Claude desktop app (`CLAUDE_CODE_ENTRYPOINT=claude-desktop`), started by Claude Projects through
Remote Control and steered through the Projects messaging tools (E01, E03, E16). Nothing here
was executed with `claude -p` or the Agent SDK. The headless sections below are documented or
inferred, never exercised.

Two earlier reports in the parent folder remain unmodified and are the right comparison points:
the pre-cleanup terminal report ([`../report.md`](../report.md), reviewed in
[`../review-codex.md`](../review-codex.md)) and the post-cleanup terminal report
[`../20261021T053558Z/report.md`](../20261021T053558Z/report.md), written ~10 minutes earlier.

## 0. Surface verification

| Question | Finding | Status |
|---|---|---|
| Local Claude Code or Codex? | Claude Code. Codex is not involved. | observed (E01–E03) |
| Which Claude Code? | The desktop app's **own downloaded runtime** at `~/Library/Application Support/Claude/claude-code/2.1.304/…/claude`, parent `Claude.app` 3.1623.0. Not the Homebrew `/opt/homebrew/bin/claude` the terminal reports used. | observed (E01, E02) |
| Where does execution happen? | On Oscar's Mac, in `~/Projects/Rieken/guild-ledger`, under the desktop app's process tree. Model inference goes to `https://api.anthropic.com`. | observed (E01, E03) |
| Who started it? | Claude Projects (cloud coordinator) via a Remote Control proposal that Oscar approved; the desktop app spawned the session through the Agent SDK (`querySource: sdk`, SDK 0.3.304). | observed (E03, E04, E16) |
| Headless? | No. `CLAUDE_CODE_SESSION_ATTENDED=1`, interactive SDK host, permission mode `auto`. | observed (E03, E04) |

Same version number as the terminal binary (2.1.304) does not make them the same surface: the app
keeps its own copies (2.1.299 and 2.1.304 are both on disk) and can update them independently of
Homebrew (E02).

## 1. Identity, model and effort

- **Runtime version:** 2.1.304 bundled; desktop app 3.1623.0; Agent SDK 0.3.304. Observed (E02).
- **Model label:** requested `claude-opus-5-5[1m]`; outbound requests record
  `params.model=claude-opus-5-5`; every response reports `message.model=claude-opus-5-5`
  (22/22). Observed (E04). This is a request-side label and a server-echoed alias. **No dated
  snapshot or verified backend revision is exposed**: unknown.
- **Reasoning/effort:** `CLAUDE_EFFORT=medium`, transcript `effort`/`perTurnEffort=medium`, request
  `output_config.effort=medium`, `thinking={"type":"adaptive","display":"summarized"}`,
  `max_tokens=128000`. Observed (E03, E04). This differs from the terminal session's
  `claude-sonnet-5`/`high`, so the two local surfaces were not running a matched configuration.
- **Pinning:** the desktop app has no settings-level model (`settings_default_model: not set`); the
  Code tab picker remembers its own choice (E11). `--model`/`--effort` exist on the CLI (E12).
  Both select an alias, not a dated revision. Documented/inferred; no pin to a backend revision
  is available as far as observed.
- **Account mode:** Pro subscription, observed directly through the app's plan readout (E10),
  stronger than the terminal reports' inference. No API key in the environment (E03). Extra
  usage disabled.
- **`CLAUDE_CODE_CHILD_SESSION=1`:** present here too. In this surface it is consistent with the
  desktop app being the parent; the terminal reports saw it without such a parent, so its meaning
  remains unknown.

## 2. Instructions and state after the cleanup

| Layer | Terminal CLI (05:35 report + E05/E06) | This desktop session | Status |
|---|---|---|---|
| `~/.claude/CLAUDE.md`, `~/AGENTS.md`, `~/.claude/rules/*` | absent / empty | absent / empty; no corresponding instruction section in context | observed (E05) |
| Project `.claude/`, `CLAUDE.md`, `AGENTS.md` | absent | absent | observed (E13) |
| Hooks in user settings | none | none in `settings.json` | observed (E05); effective hooks from plugins/app not enumerated: unknown |
| Auto-memory | `autoMemoryEnabled=false`; memory dirs removed | no memory dir for this project; no memory section loaded | observed (E05, E15) |
| Synced plugins | all three `disabled` in `enabledPlugins` and `claude plugin list` | **loaded anyway**: `engineering:*`, `data:*`, `searchfit-seo:*` skills and 17 `plugin:*` MCP servers are present; `ListPlugins` shows all three enabled on the claude.ai account | observed (E06, E07, E08) |
| claude.ai connectors | `disableClaudeAiConnectors=true`; `claude mcp list` empty | **4 connectors connected** (Claude Docs, Indeed, visualize, ZipRecruiter) | observed (E05, E07) |
| Host-injected tools | n/a | Projects messaging (`hearthbot`), Remote Control, scheduled tasks, desktop session/window/settings/PR tools, browser pane, iOS simulator, Chrome tool names | observed (E07) |
| Host instructions | none | a large app/Projects system prompt plus per-turn reminders (~26k tokens of system prompt, ~38k of MCP tool schemas, ~9.5k of skills at capture) | observed sizes (E09); text not reproduced |

**Cleanup verification:** the file-level cleanup recorded in `15-local-agent-reset.md` holds
(E05, E06, E15). But the two user-settings switches that were meant to remove optional context,
`enabledPlugins:false` and `disableClaudeAiConnectors:true`, **do not govern this desktop
session**. D02 documents that local desktop sessions load skills enabled on the claude.ai
account; the observation shows the same for plugin MCP servers and account connectors. The
cleanup document's own caveat ("user configuration does not automatically override every
… cloud-host-delivered feature") is confirmed concretely here.

**Remaining inherited context in this session:** account plugins (3), account connectors (4),
the desktop app and Projects host prompts and tools, and Projects thread history fetched on
demand. None of these can be removed from inside the session without changing account or app
settings, which this task forbids. Whether they can be disabled at all is answerable only by
Oscar in the app or on claude.ai: unknown from here.

## 3. Headless automation (documented, not exercised)

From D01 and the bundled `--help` (E12):

| Need | Mechanism | Status |
|---|---|---|
| Start fresh task | `claude -p "<prompt>"`, optional `--session-id <uuid>`, `--no-session-persistence` | documented |
| Explicit workspace/context | `cwd`, `--add-dir`; `--bare` with `--append-system-prompt[-file]`, `--settings`, `--mcp-config --strict-mcp-config`, `--agents`, `--plugin-dir`; `--setting-sources`, `--safe-mode`, `--disable-slash-commands` | documented |
| Tool catalog | `--tools ""` removes built-ins; `--allowedTools` only auto-approves | documented (E12, D01) |
| Structured events | `--output-format stream-json --verbose [--include-partial-messages]`; `system/init` (model, tools, MCP, plugins, `plugin_errors`), `system/api_retry`, `permission_denied`, final `result` | documented |
| Stop | SIGTERM → exit 143, no result for in-flight turn; SIGINT/`interrupt()` ends the turn | documented |
| Limits | `--max-budget-usd` (estimated spend, `-p` only), `--permission-mode`, `--permission-prompts none`; `--max-turns` in docs but absent from `--help` | documented; discrepancy observed (E12) |
| Retrieve artifacts | local filesystem; session `.jsonl` transcript; `--resume <id or path>` | observed for filesystem/transcript (E04, E14) |

**Desktop app as an automation target:** D02 describes no headless or scripting interface for
starting desktop sessions. Projects/Remote Control can start a desktop session (this session is
the proof), but that path is interactive, attended, host-prompted and loads account plugins and
connectors. It is unsuitable as a controlled benchmark launcher. Inferred.

**Bare mode and Pro:** D01 says `--bare` never reads OAuth credentials and needs
`ANTHROPIC_API_KEY` or `apiKeyHelper`. With a Pro login and no API key (E03, E10), bare mode should
fail to authenticate. Inferred; not run.

## 4. Usage capture

- **Interactive transcript (observed, E04):** per-response `usage` with input, output, cache write
  (5m/1h split), cache read, `thinking_tokens`, server web search/fetch counts, `service_tier`,
  `speed`, `inference_geo`, `fallback_credit`, `iterations`; IDs `message.id`, `requestId`,
  `sessionId`, `uuid`/`parentUuid`; timestamps. New in this build's desktop transcript:
  `api-request` entries recording outbound `model`, `max_tokens`, `thinking`, `effort`, `betas`,
  `context_management` per request.
- **Duplicates:** 22 assistant entries → 12 distinct `message.id`/`requestId` (≈1.8×). The
  terminal sessions saw 2.35× and 4.3×. Dedupe by `message.id` per session; there is no fixed
  ratio. Observed.
- **Child calls:** none made. Documented: headless subagent messages carry `parent_tool_use_id`
  (D01). Interactive transcript lineage for subagents: unknown here.
- **Resumed totals:** documented as cumulative in the JSON result (D01); not exercised.
- **Interrupted results:** documented as absent for SIGTERM (D01); not exercised.
- **Classifier/advisor calls:** auto mode is active (E04, E11) and the transcript records an
  `advisorModel` field. Whether auto-mode classifier or advisor calls appear as usage records is
  **unknown**; they could be unmetered in this transcript. Prompt suggestions (on, E11) are
  described by the app as extra model requests; their accounting is also unknown.

## 5. Cost provenance

- Account mode: **Pro subscription** (observed, E10). Usage counts against 5-hour and weekly
  percentage windows; extra usage disabled, `$0.00` spent.
- Actual charges: the subscription fee. Per-session or per-attempt billed USD is not exposed;
  the app reports percentages only. Unknown/not attributable.
- Client estimates: `total_cost_usd` exists only on `-p`/SDK result messages and is documented as
  a client-side estimate (D01). This transcript has no cost field (E04).
- Subscription allocation: no documented formula converts window percentages into tokens or USD.
  Any per-attempt USD would be a list-price estimate from deduplicated token counts, not a charge.

## 6. Harness compatibility

| Profile | This desktop/Projects surface | Local headless CLI (for contrast) |
|---|---|---|
| H0 baseline | **Blocked**: account plugins, connectors and host prompts load regardless of user settings (observed). | Candidate via `--bare`, but needs API-key auth (documented); or plain `-p` from the cleaned terminal, which then loads account skills if signed in (D02, inferred). |
| H1 fixed guidelines | Possible in a repo `CLAUDE.md`, but contaminated by the same host context. Inferred. | `--append-system-prompt-file` or repo `CLAUDE.md` under the chosen H0 mode. Documented. |
| H2 bounded workflow | Instruction-level only; the app adds its own workflow rules and subagent/session tools. Inferred. | Budget, tool, permission and subagent primitives exist; nothing built. Documented. |
| Loom context-only | Could be read as context; not a native pipeline. Inferred. | Same. |
| Loom native pipeline | No `loom` on PATH (prior report E14); not re-checked. Unknown. | Needs a deliberately built, pinned executable. |

## Observed vs unverified

**Observed:** desktop-app ancestry and bundled runtime 2.1.304 / app 3.1623.0 / SDK 0.3.304;
entrypoint `claude-desktop`; attended; permission mode `auto`; model alias `claude-opus-5-5` in
request and response; effort `medium` with adaptive thinking; Pro plan with percentage windows;
file-level cleanup intact; plugins and connectors still loaded despite user settings; context
composition sizes; transcript usage schema and new `api-request` entries; no cost field;
`--max-turns` absent from `--help`; scratch edit.

**Documented only:** all `-p`, `--bare`, stream-json, SIGTERM, budget and resume behavior;
desktop loading of account skills; no desktop scripting interface.

**Unknown:** backend model revision; whether account plugins/connectors can be excluded from
desktop sessions without uninstalling them on claude.ai; effective hooks contributed by plugins or
the app; accounting for auto-mode classifier, advisor and prompt-suggestion calls; whether
`--bare` works at all on this Pro login; whether the terminal `-p` path also loads account skills
after cleanup.

## Three largest control/metering gaps

1. **The cleanup does not reach account-delivered context.** On this surface, three plugins
   (with 17 MCP servers and 37 skills) and four connectors load even though user settings
   disable them, and the Projects/desktop host adds its own large prompt and tool set. H0 cannot
   be certified on any surface that signs in with this account until account-level exclusion is
   demonstrated.
2. **No headless call has run on this machine.** Every `-p`/SDK field, cost estimate, stop behavior
   and bare-mode auth outcome is still documentation. The two local Claude surfaces also ran
   different model/effort settings, so even interactive observations are unmatched.
3. **Pro billing yields no attributable per-attempt USD, and hidden calls may be unmetered.**
   The plan exposes only window percentages; `total_cost_usd` is a client estimate; auto-mode
   classifier, advisor and prompt-suggestion requests have unknown accounting.

## Recommended next probe (not executed; needs Oscar's approval)

**P1′ — one isolated headless metering call from a plain terminal, not from this app.**

| Item | Value |
|---|---|
| Purpose | Establish what a headless call on this machine actually loads and reports: `system/init` plugins/MCP/model, `result.usage`, `modelUsage`, `total_cost_usd`, `session_id`, exit code. |
| Command | From an empty temp directory: `claude -p "Reply with the single word ok." --output-format stream-json --verbose --tools "" --strict-mcp-config --mcp-config '{"mcpServers":{}}' --model claude-sonnet-5 --effort low --max-budget-usd 0.05 --no-session-persistence`, wrapped in `timeout 120`. No `--bare` (Pro login has no API key). |
| Expected evidence | Whether account skills/plugins appear in `system/init` despite `enabledPlugins:false`; whether any tools remain; one deduplicated usage record; the estimated cost field. |
| Limits | 1 invocation, expected 1 model request; 120 s wall clock; `--max-budget-usd 0.05` estimated spend. |
| Spend basis | Pro subscription window (a small fraction of one 5-hour window); USD figure is a list-price estimate, not a charge. |
| Enforcement | `timeout` kills the process; budget flag is a client check; empty tool catalog prevents edits/shell. |
| Overshoot risks | Budget is checked after spend and may overshoot by one request; auxiliary requests (title generation, classifier) could occur and might not be reported; a retry on error adds a request. |
| Approval | Oscar, explicitly. It is an extra model session, outside this task. |

Earlier P1–P3 (transcript export, routine start/stop, nested `claude -p`) remain unapproved and
unexecuted. P1′ supersedes the terminal report's P1 by adding `--strict-mcp-config` and an
explicit model/effort, and by checking the account-plugin question this report raises.

## Reproduction

```sh
p=$PPID; while [ "$p" != 0 ]; do ps -o pid=,ppid=,comm= -p $p; p=$(ps -o ppid= -p $p | tr -d ' '); done
printenv CLAUDE_CODE_ENTRYPOINT CLAUDE_EFFORT CLAUDE_CODE_SESSION_ATTENDED CLAUDE_AGENT_SDK_VERSION CLAUDE_CODE_DESKTOP_APP_VERSION
"$CLAUDE_CODE_EXECPATH" --version; claude --version
claude mcp list; claude plugin list
python3 -I -c 'import json;d=json.load(open("'$HOME'/.claude/settings.json"));print({k:d.get(k) for k in ("enabledPlugins","autoMemoryEnabled","disableClaudeAiConnectors")})'
```

Within a desktop session, the read-only app tools `session_connectors_status`, `get_settings`,
`get_usage` and `ListPlugins` produced E07–E11. Transcript schema was tallied with a `python3 -I`
script printing key names and counts only.

## Delivery

Files are in `guild-ledger-research/docs/runtime-discovery/claude-code-headless/20261021T054718Z/`.
Earlier reports were not modified. Nothing was committed or pushed.
