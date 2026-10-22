# Runtime discovery: claude-code-headless (local terminal Claude Code)

Captured 2026-10-21T02:50Z by the agent running inside this surface, at the user's explicit
request to document **this exact session** — a local terminal Claude Code CLI session, not a
Claude Projects cloud thread and not a nested CLI started inside a cloud session. This is a
discovery record, not a benchmark. It does not show benchmark performance, harness effects, or
complete isolation. Evidence IDs (E.., D..) refer to [evidence.md](evidence.md); the
machine-readable form is [capabilities.json](capabilities.json).

Status labels: **observed**, **documented**, **inferred**, **unknown**. Per the task instructions,
this interactive session inspects local configuration and the *documented* headless (`-p`)
interface; it does not execute `-p`, `--bare`, or any second model call, so it does not itself
prove headless execution or metering. That requires a separately authorized probe (see
[Proposed probes](#proposed-probes-not-executed-each-needs-oscars-approval)).

## Surface verification (requested first, per the task)

Before anything else: process ancestry was walked from the running `claude` process up to PID 1
(E02). It resolves `claude (54564)` → `zsh (3981)` → `login (3790)` → `Terminal.app (684)` →
`launchd (1)`. There is no cloud relay, no coordinator, and no nested parent Claude process in
this chain. `CLAUDE_CODE_ENTRYPOINT=cli` and `TERM_PROGRAM=Apple_Terminal` corroborate it (E04).
The local transcript's 40 `assistant` entries all carry `entrypoint: "cli"` (E11), matching the
prior cloud report's contrasting `entrypoint: "remote_projects"` (claude-code/evidence.md E05).
**Conclusion: this is genuinely local terminal Claude Code.** One anomaly is noted and left
unresolved below (`identity.entrypoint_anomaly`).

## 1. Identity

- **Surface (observed, E01–E04, E11):** Claude Code CLI running interactively in a local
  macOS Terminal.app session (not `-p`, not `--bg`, not `--cloud`). Homebrew install at
  `/opt/homebrew/bin/claude` → Cask `/opt/homebrew/Caskroom/claude-code/2.1.304/claude`.
- **Runtime version (observed, E01, E10, E11):** `2.1.304`, commit `17ab70404e5b`, agreeing across
  the binary (`--version`), `claude doctor`, and every transcript entry's `version` field.
- **Environment (observed, E05):** macOS (Darwin 25.6.0, arm64), user `oscarrieken`, Node v22.22.3,
  working directory `/Users/oscarrieken/Projects/Rieken/guild-ledger` (not itself a git repo; the
  `guild-ledger-research` subfolder is its own git repo, cloned from GitHub but with no commits
  yet locally — E15).
- **Model (observed, E04, E11; cross-validated against this turn's own system reminder):** label
  `claude-sonnet-5`, effort `high` (`CLAUDE_EFFORT=high`), matching 40/40 assistant transcript
  entries. **Verified backend identity: unknown** — no dated snapshot ID is exposed anywhere
  observed; `claude --model` accepts an alias or a full model ID per-session but that is a
  *selection*, not a pin to a specific backend revision (documented, D01/D03 `--help` text).
- **Account/billing mode (observed, E10):** `claude doctor` reports *"Managed settings (remote):
  not fetched — requires an Enterprise or Team subscription"* and *"Organization policy: not
  applicable to Pro and Max accounts."* No `ANTHROPIC_API_KEY` is set (E04). Combined with an
  OAuth credentials file (`~/.credentials.json`, not opened) this indicates an individual
  **Pro/Max subscription** account, not Console/API billing and not an Enterprise/Team managed
  account. This matches the earlier cloud-thread report's finding for the same account
  (claude-code/report.md §6), which is useful corroboration across surfaces but not independent
  proof — both reports read the same underlying account.
- **`identity.entrypoint_anomaly` (observed, unresolved):** `CLAUDE_CODE_CHILD_SESSION=1` is set
  in this process's environment even though the process-ancestry walk above shows a plain,
  directly-launched terminal session with no parent Claude or cloud process. Its meaning here is
  **unknown** — it may be a generic flag unrelated to true session parentage, or may reflect
  something about this specific installed build. Flagged as an open question rather than resolved,
  the same way the cloud report flagged its own unexplained `CLAUDE_CODE_VERSION=2.1.42` conflict.

## 2. Automation

| Need | What exists (local CLI) | Status |
|---|---|---|
| Start a fresh task | `claude -p "<prompt>"` with `--session-id`, `--continue`/`--resume`, or `--fork-session`; `claude --bg` starts a background agent and prints an id that `claude attach/logs/stop/rm/respawn` and `claude agents` operate on | documented (E09); none executed |
| Supply prompt and workspace | Prompt via CLI argument or piped stdin (capped 10 MB). Workspace is the literal filesystem `cwd`, extendable with `--add-dir`. Context is explicit via `--append-system-prompt(-file)`, `--system-prompt(-file)`, `--settings`, `--mcp-config`, `--agents`, `--plugin-dir`/`--plugin-url` | documented (D01, E09) |
| Observe progress | `--output-format stream-json --verbose --include-partial-messages` streams token deltas; the `system/init` event reports model, tools, MCP servers, loaded plugins, and a `capabilities` array; `claude agents` / `claude logs <id>` for background sessions | documented (D01, D02); not exercised |
| Stop | **SIGTERM**: exit code 143, the in-flight turn is left unfinished with **no result recorded**, `SessionEnd` hooks still run, any live Bash process tree is killed. **SIGINT** (or the Agent SDK's `interrupt()`) ends the turn cleanly instead. `claude stop\|kill <id>` for background sessions | documented (D01); not exercised |
| Retrieve changed files | Direct local filesystem access — this *is* the local checkout. No push, PR, or teleport was needed or attempted | observed (E15) |

Unlike the cloud thread (whose host created the job, picked the image/version, and owned the
hooks), on this surface **the researcher's own machine** is the thing that would create, observe,
and stop a headless run. Nothing here is a GitHub Action or a third-party platform.

## 3. Instructions and state

Everything below was directly observed as the actual content/behavior of **this session**, not a
generic description of the product:

1. The built-in Claude Code system prompt (not exported; content unknown).
2. **User-level rules** (observed+documented, E06, D06): `~/.claude/rules/` is a symlink to
   `ai-assistant-dot-files/shared/rules/` (17 `.md` files). Per the official memory docs, files
   under `~/.claude/rules/` are *"personal rules [that] apply to every project on this machine"*
   and load without the per-project trust dialog. This is exactly what appeared in this turn's
   system prompt as "the user's private global instructions for all projects."
3. **Project instructions via `AGENTS.md`, not `CLAUDE.md`** (observed+documented, E18, D06): the
   content injected and labeled "project instructions, checked into the codebase" is
   `/Users/oscarrieken/AGENTS.md` — a file at the researcher's **home directory**, two levels above
   the working directory. The official docs confirm the exact rule that produced this: Claude
   reads `AGENTS.md` from the working directory *and every directory above it* whenever no
   `CLAUDE.md`/`CLAUDE.local.md` exists in that chain. `~/.claude/CLAUDE.md` is a **broken symlink**
   here (target `ai-assistant-dot-files/.claude.md` does not exist, E06/E18) and in any case
   doesn't count toward that check. So `AGENTS.md` loaded, by the documented default rule, not by
   any special-casing of this project.
4. **Hooks: none active** (observed, E06, E07). The only active settings file is the global
   `~/.claude/settings.json`, and its entire content is `{"tui": "fullscreen", "theme":
   "dark-ansi", "switchModelsOnFlag": false}` — no `hooks` key. `guild-ledger` has no
   `.claude/settings.json` or `.claude/settings.local.json` of its own, and no managed-settings
   file exists on this machine (E17). This is a concrete, observed contrast with the cloud thread,
   whose `launcher-settings.json` injected `PostToolUse`/`Stop`/`UserPromptSubmit` hooks the
   researcher could not remove.
5. **Skills and plugins** (observed, E06): `~/.claude/skills/` symlinks to
   `ai-assistant-dot-files/shared/skills/` (71 entries) plus Claude Code's own built-in skills.
   `claude mcp list` (E08) shows account-level and plugin-marketplace MCP servers in a mix of
   connected / needs-authentication / failed states — these are account-wide, not specific to this
   project (`guild-ledger` has no `.mcp.json`).
6. The user's message, this conversation's turns, and the auto-memory scratch directory the
   system prompt names (`.../memory/`), which is empty at the start of this task.

**Resettable / excludable for a future isolated experiment (documented, not applied, D01, D03):**

| Flag | Effect |
|---|---|
| `--bare` | Skips hooks, LSP, plugin sync, attribution, auto-memory, background prefetches, keychain reads, and `CLAUDE.md`/`AGENTS.md` auto-discovery outright. Needs `ANTHROPIC_API_KEY` (OAuth/keychain are never read). Context must then be supplied explicitly via the flags in row 2 of §2 |
| `--safe-mode` | Disables `CLAUDE.md`, skills, installed plugins, hooks, MCP servers, custom commands/agents, output styles, workflows, themes, and keybindings, while keeping auth, model selection, built-in tools, and permissions working normally |
| `--restricted` | Removes Bash/code-execution tools and `WebFetch` unless explicitly named, ignores user/project/local settings files (managed settings and `--settings` still apply), and confines file tools to named working directories |
| `--setting-sources user\|project\|local` | Selects exactly which of the three non-managed settings files load, comma-separated |
| `--strict-mcp-config` | Only the MCP servers passed via `--mcp-config` connect; every other MCP source is ignored |

**Mandatory / not observably excludable:** the built-in system prompt (layer 1); the researcher's
own personal `~/.claude/rules/` and `~/.claude/skills/` are mandatory *for this account* but are
themselves removable with `--bare`/`--safe-mode`/`--setting-sources`, which is the key structural
difference from the cloud thread, where the equivalent layers were asserted as unexportable host
behavior.

## 4. Tools and permissions

- **Available now (observed, this session):** `Bash`, `Read`, `Write`, `Edit`, `WebFetch`, `Agent`,
  `Artifact`, `AskUserQuestion`, `ScheduleWakeup`, `SendFeedback`, `ReportFindings`, `ToolSearch`,
  plus deferred tools (`WebSearch`, `Monitor`, `SendMessage`, `EnterPlanMode`, Cron\*, several MCP
  connector tools) loadable via `ToolSearch`. Tests were available via `Bash` but none were run,
  per the task's constraints.
- **Permission mode (observed, E12):** every `permission-mode` transcript entry this session reads
  `auto` (a classifier reviews most actions); `CLAUDE_CODE_SESSION_ATTENDED=1` (E04).
- **MCP (observed, E08):** `claude mcp list` enumerates account-level connectors
  (`claude.ai Claude Docs`, `Indeed`, `ZipRecruiter`, `Google Drive`, `Gmail`, `Google Calendar`,
  `Notion`) and marketplace plugin servers (`slack`, `linear`, `asana`, `atlassian`, `notion`,
  `github`, `pagerduty`, `datadog`, `bigquery`, `hex`, `amplitude`×2, `definite`) in a mix of
  Connected / Needs authentication / Failed-to-connect states, several with repeated
  `SEP-2352: stored OAuth credential has no 'issuer' stamp` warnings. None of this is
  project-scoped; `guild-ledger` defines no `.mcp.json`.
- **Subagents (documented, D05; local override absent, E19):** the Agent tool is available. By
  default, local CLI subagents can nest **3** layers deep (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`,
  unset here, so the documented default of 3 applies — a materially different default from the
  cloud thread, which had it explicitly pinned to 1) and up to **20** can run concurrently
  (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`). No subagents were spawned this session (task
  constraint), so no `subagents/` transcript subfolder exists yet (E19).
- **Loom binary (observed, E14):** `/opt/homebrew/bin/loom`, version `0.1.1`, is installed on this
  machine. Its only subcommands are `completion`, `health`, `install`, `tools`, `uninstall`,
  `update`, `version` — **there is no `run` or pipeline-execution subcommand in this installed
  version.** It installs agents/skills/rules into AI platforms; it does not itself drive a
  multi-agent pipeline. This matters directly for §8, H3.
- **Filesystem scope:** ordinary user-level access to the researcher's own filesystem under their
  own UID — no container, no sandbox boundary was observed (contrast the cloud thread's
  root-in-container isolation).
- **Human intervention:** the terminal itself; any tool call outside the user's permission
  settings prompts for approval.

## 5. Metrics

- **Per-response usage (observed, E11, E13):** the local transcript
  `~/.claude/projects/-Users-oscarrieken-Projects-Rieken-guild-ledger/<session-uuid>.jsonl` records,
  per `assistant` entry: `message.id`, `requestId`, `timestamp`, `message.model`, `effort`,
  `isSidechain`, `entrypoint`, `version`, and a `message.usage` object with
  `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`,
  `cache_creation.{ephemeral_5m,ephemeral_1h}_input_tokens`, `output_tokens_details.thinking_tokens`,
  `server_tool_use.{web_search,web_fetch}_requests`, `service_tier`, `speed`, `inference_geo`,
  `fallback_credit`, and an `iterations[]` array. This is the **same schema** the earlier cloud
  report found, with the same duplication caveat: at the time of inspection, 40 `assistant` entries
  collapsed to only **17** distinct `message.id`/`requestId` values, so usage must be deduplicated
  by `message.id` before any total is computed (E11).
- **No cost field in this transcript (observed, E13):** a search for `total_cost_usd`/`costUSD`
  anywhere in this session's transcript found no runtime-emitted occurrence — the only string
  matches were this session's own conversational content quoting the prior cloud report's prose
  and this session's own shell commands, which is a false positive, not a cost field. This is
  consistent with the documentation: `total_cost_usd` is a field on the `-p`/SDK **result**
  message, not something the interactive session transcript carries (D02).
- **`usage` vs. `modelUsage`/`total_cost_usd` (documented, D02):** the SDK/CLI docs are explicit
  that these three result-level fields differ once subagents are involved:

  | Field | Subagent activity |
  |---|---|
  | `usage` | main loop only — subagent tokens are **excluded** |
  | `total_cost_usd` | subagent requests **included** alongside the main loop |
  | `modelUsage` | subagent requests **included**, broken down per model |

  **Do not add every result together**, per the task's instruction: independent `query()`/`-p`
  calls must be summed by the caller, but a call that **resumes a session** already reports the
  session's cumulative total (since CLI/SDK v2.1.277; earlier versions started each resumed call at
  zero) — so summing resumed-call totals double-counts. Per-step `output_tokens` on assistant
  messages is a documented **placeholder** captured at `message_start`, before the true count is
  known; the true output count is only correct on the result message. On a crash, the final
  `error_during_execution` result may carry **all three fields zeroed**; recovery requires using
  the previous turn's result where one exists, or (for input/cache tokens only, not output or
  cost) summing per-step `usage` on the assistant messages that arrived before the crash.
- **Subagent/child lineage (documented, D01, D05):** `parent_tool_use_id` on each stream-json
  message distinguishes subagent output from the main loop; it is `null` for the main conversation
  and otherwise carries the originating `Agent`/`Skill` tool-call ID (or a `forked-command-` prefix
  for a prompt-invoked skill). Each subagent additionally gets its **own transcript file** at a
  documented path (`.../subagents/agent-{agentId}.jsonl`). None of this was exercised in this
  session (no subagents were spawned).
- **Errors/retries (documented, D01):** a `system/api_retry` stream-json event reports `attempt`,
  `max_retries`, `retry_delay_ms`, `error_status`, and an `error` category enum
  (`authentication_failed`, `rate_limit`, `overloaded`, `billing_error`, …). None occurred in this
  session.
- **Aggregate/local reporting (documented, D04):** `/usage` (not run, to avoid an extra
  model-adjacent request) shows a session-local `Session` block (tokens, estimated cost, duration)
  plus, on Pro/Max/Team/Enterprise plans, a plan-usage breakdown attributing recent usage to
  skills/subagents/plugins/MCP servers, computed **only from local session history on this
  machine** — it explicitly excludes usage from other devices or from claude.ai.

## 6. Cost

- **Accounting mode (observed+documented, E04, E10, D04):** individual subscription (Pro/Max),
  inferred from the absence of `ANTHROPIC_API_KEY`, the OAuth credentials file, and `claude
  doctor`'s organization-policy/managed-settings messages (§1). Per the cost docs, a Pro/Max
  subscriber's `/usage` session-cost figure is **explicitly described as "not relevant for billing
  purposes"** — billing for this account type is seat/plan-window consumption, not a per-task
  dollar charge, unless the user has separately opted into usage credits with a spend limit.
- **Per-attempt USD (inferred, not obtainable in this session):** no cost field exists anywhere in
  this session's transcript (§5). The CLI *does* produce `total_cost_usd` and a per-model cost
  breakdown, but only as a field on a `-p`/`--output-format json` or SDK **result** message — i.e.,
  only in a headless call this interactive session did not make. That figure would still be a
  **client-side list-price estimate** per the documentation's explicit warning, not authoritative
  billing; authoritative billing for a subscription account is the plan's own usage/analytics
  surfaces, which this session did not query.

## 7. Artifacts and interruptions

- **On SIGTERM (documented, D01):** exit code 143; the in-progress turn is left unfinished with
  **no result recorded**; `SessionEnd` hooks still run; any running Bash process tree is killed;
  no new tool call or model request starts during shutdown. A waiting permission prompt is left
  unanswered (bare process kill) or cleanly cancelled (Agent SDK closing stdin).
- **On SIGINT or `interrupt()` (documented, D01):** the turn ends cleanly instead of being left
  unfinished.
- **On resume (documented, D01):** the interrupted turn is left as-is unless
  `CLAUDE_CODE_RESUME_INTERRUPTED_TURN=1` is set, in which case Claude Code continues it.
- **If the working directory is deleted mid-session (documented, D01):** the session keeps
  running; a `stream-json` warning is emitted; shell commands fail until the directory exists
  again.
- **Persistence (observed, E11, E15):** this session's own transcript is an ordinary file on local
  disk (`~/.claude/projects/.../<uuid>.jsonl`), not container-ephemeral. The research repository
  (`guild-ledger-research`) is a local git working tree with `origin` set to GitHub but **no
  commits made locally yet** and the remote branch reported `[gone]` (E15) — this session wrote
  only to the untracked working tree, as instructed, and made no commit or push.
- **Stable IDs (observed, E04, E11):** `CLAUDE_CODE_SESSION_ID` (36-char UUID) matches the
  transcript filename; each transcript entry carries a `uuid`/`parentUuid`; each API response
  carries `message.id` (`msg_…`) and `requestId` (`req_…`).
- **Scratch-edit demonstration (observed, E16):** a file was created, read back, and removed inside
  the new report folder to confirm local write access, following the same pattern as the prior
  cloud report's E10. This demonstrates **local write/read only** — it says nothing about export,
  cross-session durability beyond what git/filesystem already guarantee, or retention policy,
  per review-codex.md finding F05.

## 8. Harness compatibility

| Harness | Assessment | Status | Notes |
|---|---|---|---|
| **H0**, no added rules | **Partial, but more controllable than the cloud surface.** This session itself loaded the full personal stack (17 user-level rule files, home-directory `AGENTS.md`, 71 skills, several MCP connectors) — none of that is a clean baseline as observed. But unlike the cloud thread, `--bare`, `--safe-mode`, `--restricted`, and `--setting-sources` are real, documented, *local* knobs that can strip hooks/skills/plugins/CLAUDE.md/AGENTS.md discovery/keychain reads for a future run, down to an explicit, flag-supplied context. No hooks were found active in this session's settings layer at all (§3), which is itself a real difference from the cloud baseline. | inferred | `--bare` needs `ANTHROPIC_API_KEY` (not OAuth), a separate auth path from this session |
| **H1**, one guidelines file | **Feasible**, and more directly than on the cloud surface: a single `CLAUDE.md` (or `.claude/settings.json`) committed at the root of each per-condition repo (`guild-ledger-baseline`, `-guidelines`, `-harness`, `-loom`) is read by the documented discovery rule, with `--setting-sources`/`--add-dir` available to scope it further. | documented | Depends on which condition-repo is checked out as `cwd` |
| **H2**, bounded planning/review workflow | **Instruction-level, with real enforcement knobs this surface actually has and the cloud thread didn't document having**: `--max-budget-usd` (dollar cap on a `-p` call), `--permission-mode`/`--permission-prompts none` (unattended runs), subagent depth (3 default, settable down to 1) and concurrency (20 default) caps, and per-subagent `maxTurns`. None of these were exercised this session. | inferred | No experiment-level orchestration logic exists yet; these are primitives, not a built workflow |
| **H3**, pinned Loom profile | **Blocked by the installed binary, observed directly.** `/opt/homebrew/bin/loom` v0.1.1 has no `run`/pipeline subcommand — it is an installer for agents/skills/rules (`install`, `health`, `tools`, `update`, …), not the pipeline-execution tool the shared rules describe (`loom run`, `loom memory agents`, `loom ki scan`, `loom index`). Whether a different Loom release provides that is **unknown** from this session. Reading Loom-authored context files (the `shared/rules/*.md` already loaded here) is a context-only profile, not native pipeline support, matching the cloud report's same caveat. | observed (binary absence of `run`); unknown (whether another release has it) |

## Observed vs unverified

- **Observed:** local terminal surface and process ancestry to Terminal.app, CLI 2.1.304 (binary,
  doctor, transcript all agree), macOS/arm64 environment, model label `claude-sonnet-5` and effort
  `high` across every transcript entry, permission mode `auto`, no hooks active, `AGENTS.md` loaded
  from the home directory with a broken `CLAUDE.md` symlink alongside it, 17 user-level rule files
  and 71 skills via symlink, MCP server connect/auth states, absence of a Loom `run` subcommand,
  absence of any cost field in this transcript, 40 assistant entries collapsing to 17 distinct
  message/request ids, subscription-mode billing indicators, scratch-file write/read/remove.
- **Documented only (not exercised this session):** every `-p`/headless flag and behavior in §2,
  §5, §7 (output formats, SIGTERM/SIGINT semantics, `usage`/`modelUsage`/`total_cost_usd`
  distinction, subagent lineage, resume accumulation, `/usage` plan breakdown).
- **Unverified or unknown:** verified backend model revision; the meaning of
  `CLAUDE_CODE_CHILD_SESSION=1` in a plain local session; whether another installed Loom version
  supports pipeline execution; whether `--bare`'s `ANTHROPIC_API_KEY` requirement is compatible with
  this account's current auth setup (not tested, since testing it means running `-p`).

## Three largest measurement and control gaps

1. **No executed headless call exists yet on this surface.** Every `-p`/SDK behavior in this
   report — output formats, the `usage`/`modelUsage`/`total_cost_usd` split, SIGTERM semantics,
   subagent lineage, resume accumulation — is read from official documentation and `--help` text,
   not exercised. The task explicitly forbids starting another model session from here, so none of
   it is independently confirmed against this account's actual behavior yet.
2. **Per-attempt USD remains unobtainable from an interactive session**, and even once a headless
   call is run, the resulting `total_cost_usd`/`modelUsage` figures are documented as client-side
   list-price estimates, not authoritative billing — true for a Pro/Max subscription account in
   particular, where the subscription's own billing model doesn't price individual tasks at all.
3. **The locally installed Loom binary cannot run a pipeline**, so H3 compatibility cannot be
   assessed beyond "the context files load as instructions" (already true of H1) until either a
   different Loom release is obtained or a decision is made about what "Loom native execution"
   means for this experiment.

## Proposed probes (not executed; each needs Oscar's approval)

| Probe | Purpose | Inputs | Expected evidence | Max calls | Time/spend cap | Enforcement | Known overshoot risk | Approval |
|---|---|---|---|---|---|---|---|---|
| P1: single `-p --output-format json` call, trivial prompt | Confirm `total_cost_usd`/`modelUsage`/`session_id` actually appear in this account's headless output, and whether this account's auth even works under `--bare` | `claude -p "echo ok" --output-format json`, no `--bare` (keeps OAuth), `--max-turns 1` | Exit code, `session_id`, `result`, `usage`, `total_cost_usd`, `modelUsage` (or the specific auth/other error) | 1 model call | ≤ $0.10 list-price-equivalent per the printed `total_cost_usd`; ≤ 2 minutes wall time | `--max-budget-usd 0.10` flag plus a wrapper that kills the process past the time cap | A single call could still include unexpected tool use the classifier auto-approves under default permission mode; mitigate with `--permission-mode dontAsk` or `--allowedTools ""` | Oscar (it is an extra model session, explicitly out of scope for this task) |
| P2: SIGTERM-interrupt behavior | Verify the documented "no result recorded, exit 143" behavior actually holds on this machine/version | One `-p` call on a multi-step prompt, SIGTERM sent ~3s in | Exit code, presence/absence of a result in stdout, session resumability afterward | 1 model call, interrupted | ≤ $0.10, ≤ 1 minute | `--max-budget-usd`, a `timeout`-wrapped `kill -TERM` | Partial tool execution (e.g., a half-run Bash command) before the signal lands | Oscar |
| P3: `--bare` auth check | Determine whether `--bare` mode (needed for a clean H0) can authenticate at all without `ANTHROPIC_API_KEY` set, since this account currently uses OAuth only | `claude --bare -p "echo ok"` with no key set | The specific auth error, or confirmation it works some other way | 1 attempt, expected to fail fast (no billed tokens if auth fails before any API call) | ≤ 1 minute | none needed if it fails before billing; abort if it appears to proceed | If it *does* authenticate via OAuth despite the docs implying it shouldn't, a billed call could follow unexpectedly — would need `--max-budget-usd` added before approval | Oscar |

## Reproduction

```
which claude && claude --version
ps -p $PPID -o pid,ppid,comm   # walk up to confirm terminal ancestry
env | cut -d= -f1 | grep -i claude   # names only
claude doctor
claude mcp list
cat ~/.claude/settings.json
ls -la /Users/oscarrieken/Projects/Rieken/guild-ledger/.claude 2>&1   # confirms absence
which loom && loom --help
```

Tally transcript schema without printing content:
```
python3 - <<'PY'
import json, collections
# point at ~/.claude/projects/<cwd-encoded>/<session-uuid>.jsonl
PY
```

## Delivery note

These files are written directly into the local checkout at
`guild-ledger/guild-ledger-research/docs/runtime-discovery/claude-code-headless/`, since this
session *is* that local checkout — there is no cloud-to-local handoff step this time. Per the
task, all changes are left **uncommitted**.
