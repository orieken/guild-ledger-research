# Runtime discovery: claude-code-headless, post-cleanup (local terminal Claude Code)

Captured 2026-10-21T05:37Z by the agent running inside this surface, documenting **this exact
session** — a local terminal Claude Code CLI session, not a Claude Projects cloud thread and not a
nested CLI started inside a cloud session — **after** the global cleanup recorded in
[15-local-agent-reset.md](../../../docs/research/15-local-agent-reset.md) and the Loom removal in
[14-global-loom-removal.md](../../../docs/research/14-global-loom-removal.md). This is a discovery
record, not a benchmark. It does not show benchmark performance, harness effects, or complete
isolation. Evidence IDs (E.., D..) refer to [evidence.md](evidence.md); the machine-readable form
is [capabilities.json](capabilities.json). The prior report at
[`../report.md`](../report.md)/[`../capabilities.json`](../capabilities.json) (captured
2026-10-21T02:50Z, pre-cleanup) is preserved unmodified; this report is written as a **diff-aware
update**, not a restart from zero, and calls out every point where this session's observations
differ from it.

## Surface verification (requested first, per the task)

Process ancestry was walked from the running `claude` process up to PID 1 (E02): `claude (37156)`
→ `zsh (3981)` → `login (3790)` → `Terminal.app (684)` → `launchd (1)`. No cloud relay, no
coordinator, no nested parent Claude process. `CLAUDE_CODE_ENTRYPOINT=cli`, binary/doctor/transcript
all agree on version `2.1.304` (E01, E04, E10, E11). **Conclusion: this is genuinely local terminal
Claude Code**, the same surface the prior report documented, now a fresh independent session on
the same machine/account after the cleanup. The `CLAUDE_CODE_CHILD_SESSION=1` anomaly the prior
report flagged recurs here too, in an independently started session with the same plain-terminal
ancestry (E04) — see "Identity" below.

A sibling report at
[`../../codex-headless/20261021T053548Z/report.md`](../../codex-headless/20261021T053548Z/report.md)
(E21), captured about two minutes before this one, documents a separate Codex session given the
same discovery task. It is cited here only for cross-reference, not as evidence about this Claude
Code session.

## 1. Identity

- **Surface (observed, E01–E04, E11):** Claude Code CLI running interactively in a local macOS
  Terminal.app session. Homebrew install at `/opt/homebrew/bin/claude` → Cask
  `/opt/homebrew/Caskroom/claude-code/2.1.304/claude` — **unchanged** from the prior report.
- **Runtime version (observed, E01, E10, E11):** `2.1.304`, commit `17ab70404e5b` — **unchanged**.
  The cleanup touched configuration/state, not the installed binary.
- **Environment (observed, E05):** macOS Darwin 25.6.0 arm64, user `oscarrieken`, Node v22.22.3,
  working directory `/Users/oscarrieken/Projects/Rieken/guild-ledger` (not itself a git repo; the
  `guild-ledger-research` subfolder is its own git repo, cloned from GitHub with no local commits
  yet — E15). Unchanged.
- **Model (observed, E04, E11; cross-validated against this turn's own system reminder):** label
  `claude-sonnet-5`, effort `high`, matching 39/39 assistant transcript entries this session.
  **Verified backend identity: still unknown** — no dated snapshot ID is exposed anywhere observed;
  `--model`/`--effort` are per-session *selections*, not pins to a dated backend revision.
- **Account/billing mode (observed, E10):** `claude doctor` again reports *"Managed settings
  (remote): not fetched — requires an Enterprise or Team subscription"* and *"Organization policy:
  not applicable to Pro and Max accounts."* No `ANTHROPIC_API_KEY` set (E04). Same
  individual-subscription inference as the prior report, now with an additional **Remote Control**
  line in `doctor`'s output ("Control this session from claude.ai/code or the Claude mobile app")
  not quoted in the prior evidence.md — observed text only; not exercised, and unknown whether
  this is new behavior or simply wasn't quoted before.
- **`identity.entrypoint_anomaly` (observed, unresolved, now recurring):** `CLAUDE_CODE_CHILD_SESSION=1`
  is set again in this independently-launched session despite the same plain terminal ancestry.
  Observing it twice, across two separately started sessions with identical process-ancestry
  shapes, makes "this session is literally a child of some other Claude process" less plausible and
  "this is a generic default value set by this installed build regardless of ancestry" more
  plausible — but the meaning is still **unknown**, and this report does not upgrade it past that.

## 2. Instructions and state — the headline change this session

This is where the cleanup is directly observable, not merely documented secondhand:

| Layer | Pre-cleanup (prior report) | Post-cleanup (this session) | Status |
|---|---|---|---|
| `~/.claude/CLAUDE.md` | broken symlink to `ai-assistant-dot-files/.claude.md` | **does not exist** | observed, E06 |
| `~/.claude/rules/` | symlink → `ai-assistant-dot-files/shared/rules/` (17 files), loaded as "the user's private global instructions for all projects" | **real, empty directory** (0 files) | observed, E06 |
| `~/.claude/skills/` | symlink → `ai-assistant-dot-files/shared/skills/` (71 entries) + built-ins | **real directory**, only `synced/` (13 built-in/account skill dirs + manifest, matching this session's own `anthropic-skills:*` system-reminder listing) | observed, E06 |
| `~/.claude/framework-install.json` | present (`ai-assistant-dot-files` v3.3.14, symlink mode) | **does not exist** | observed, E06 |
| `/Users/oscarrieken/AGENTS.md` (home dir) | 76,630 bytes; loaded as "project instructions, checked into the codebase" even though two directories above `cwd` | **does not exist** | observed, E18 |
| `claude mcp list` | ~12 account/marketplace servers, mixed connected/needs-auth/failed | **"No MCP servers configured."** | observed, E08 |
| `claude plugin list` / `enabledPlugins` | not separately queried; plugins were loadable | all three (`engineering@synced`, `data@synced`, `searchfit-seo@synced`) explicitly `disabled` | observed, E06, E08 |
| `autoMemoryEnabled` / `disableClaudeAiConnectors` | absent from `settings.json` | **explicit `false` / `true`** in `settings.json` | observed, E06 |
| Hooks | none active (no `hooks` key anywhere) | none active — **unchanged** | observed, E06, E07 |
| Project-level `.claude/` (either `guild-ledger` or `guild-ledger-research`) | absent | absent — **unchanged** | observed, E07 |
| Managed settings file | absent | absent — **unchanged** | observed, E17 |

**Net effect, observed directly rather than inferred from file listings alone (E18):** this
session's own system prompt carried **no** personal-rules section and **no** project-instructions
section corresponding to any of the removed files. For this specific project directory, the
instruction-discovery chain that the prior report found non-trivial (17 rule files + a
home-directory `AGENTS.md` two levels above `cwd` + 71 skills + ~12 MCP servers) is now, as far as
this session's own observable inputs go, **empty**. This is a materially cleaner candidate H0
starting point than the prior report could claim — see §8.

**What this does *not* establish:** this is still a per-machine, per-account configuration state,
not a sandboxed experiment boundary (the prior Codex review's F07 point stands unchanged — ordinary
user-level filesystem access, sibling repositories, and the researcher's own account/billing
context are all still present). `--bare`/`--safe-mode`/`--restricted`/`--setting-sources` remain
documented-only knobs for an even more explicit, flag-pinned future invocation (D01, D03); none
were applied this session, because none were needed to reach an empty discovery chain this time —
the global cleanup did that at the account/filesystem level instead.

## 3. Automation

Unchanged from the prior report; re-verified against this version's own `claude --help` text
captured directly in this session (E09) rather than carried over by assertion:

| Need | What exists (local CLI) | Status |
|---|---|---|
| Start a fresh task | `claude -p "<prompt>"` with `--session-id`, `-c/--continue`, `-r/--resume`, `--fork-session`; `claude --bg` for a named background agent managed by `claude agents`/`attach`/`logs`/`stop`/`rm`/`respawn` | documented (E09); none executed |
| Supply prompt and workspace | Prompt via CLI argument or piped stdin. Workspace is the literal `cwd`, extendable with `--add-dir`. Context explicit via `--append-system-prompt(-file)`, `--system-prompt(-file)`, `--settings`, `--mcp-config`, `--agents`, `--plugin-dir`/`--plugin-url` | documented (E09) |
| Observe progress | `--output-format stream-json --verbose --include-partial-messages`; `claude agents`/`claude logs <id>` for background sessions | documented (E09); not exercised |
| Stop | SIGTERM/SIGINT semantics (see §7); `claude stop\|kill <id>` for background sessions | documented (E09 subcommand list; behavior from D01); not exercised |
| Retrieve changed files | Direct local filesystem access | observed (E15) |

**Tool-removal clarification this session resolves (prior Codex review F01):** `claude --help`'s
own text (E09) now distinguishes, in its own wording, `--allowedTools`/`--disallowedTools` as
auto-**approval** lists ("tool names to allow/deny") from `--tools <tools...>` as the actual
built-in **catalog** control (`""` disables all tools, `"default"` restores the default set, or a
named subset). `--restricted` separately strips code-running tools and `WebFetch` "unless `--tools`
names them." A future no-tools metering probe should use `--tools ""`, not an empty
`--allowedTools` or an unattended permission mode, which only change approval, not availability.

**Still-open discrepancy (prior Codex review F05, not resolved this session):** `--max-turns` is
documented in the official CLI reference but is still **absent** from this exact version's
`--help` output (E09), the same gap the prior review flagged. Whether it works despite being
unlisted, or is version-gated, remains unknown without executing it.

## 4. Tools and permissions

- **Available now (observed, this session):** `Bash`, `Read`, `Write`, `Edit`, `Agent`, `Artifact`,
  `AskUserQuestion`, `ScheduleWakeup`, `SendFeedback`, `ReportFindings`, `ToolSearch`, plus deferred
  tools (`WebFetch`, `WebSearch`, `Monitor`, `SendMessage`, Cron\*, several MCP connector tool
  names, Chrome-extension tool names) loadable via `ToolSearch`. No `Bash`/file-write action beyond
  this task's own scratch-edit demo and the new report files was taken.
- **MCP (observed, E08):** **zero** configured servers — a complete change from the prior report's
  mixed-state account/plugin list, directly confirming the `disableClaudeAiConnectors: true`
  setting (E06) is effective, not merely declared.
- **Plugins (observed, E06, E08):** all three previously-synced plugins (`engineering`, `data`,
  `searchfit-seo`) show `disabled` via both `settings.json` and `claude plugin list`'s own status
  field — consistent with the cleanup receipt's `claude_plugins_still_enabled: []` (E20), while the
  underlying plugin-directory cache file remains on disk (inert, per `15-local-agent-reset.md`'s
  own caveat that a cache is not an enabled plugin).
- **Subagents (documented, D05; local override absent, E19):** unchanged — default spawn depth 3,
  default concurrency 20, neither overridden in this session's environment. Not exercised.
- **Loom binary (observed, E14):** **`loom not found`** — a complete change from the prior report's
  installed-but-pipeline-less `/opt/homebrew/bin/loom` v0.1.1. The 55-path global removal recorded
  in `.local-backups/loom-global-20261021T034807Z/` (E20) accounts for this. This session did not
  check whether the separate `ai-assistant-dot-files` source checkout the prior Codex review (F03)
  pointed to still contains a buildable executor — that checkout is an unrelated sibling project
  and was out of scope here.
- **Filesystem scope:** unchanged — ordinary user-level access, no container/sandbox boundary
  observed.
- **Human intervention:** unchanged — the terminal itself; permission-gated tool calls prompt for
  approval.

## 5. Metrics

- **Per-call usage schema (observed, E11):** byte-for-byte identical key set to the prior report's
  E11 (`input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`,
  `cache_creation.{ephemeral_5m,ephemeral_1h}_input_tokens`, `output_tokens_details.thinking_tokens`,
  `server_tool_use`, `service_tier`, `speed`, `inference_geo`, `fallback_credit`, `iterations[]`,
  plus `message.id`/`requestId`/`timestamp`). The cleanup changed configuration and instruction
  state; it did not change the transcript's recorded usage schema.
- **Duplication ratio is session-dependent, not fixed (observed, E11 — new finding this session):**
  this session's 39 `assistant` entries collapse to **9** distinct `message.id`/`requestId` values
  (~4.3x), versus the prior report's 40→17 (~2.35x) on a different session. Any usage-estimation
  approach must dedupe by `message.id` **per session**, not assume a stable multiplier derived from
  one prior observation.
- **No cost field in this transcript either (observed, E12):** the same documented
  `total_cost_usd`/`modelUsage` placement (on a `-p`/SDK **result** message only, per D02) holds;
  the only substring matches in this session's own transcript were this very system prompt's prose
  about "the cost of pausing to confirm," a false positive, not a runtime field — matching the
  prior report's finding on an independent session.
- **`usage` vs `modelUsage`/`total_cost_usd`, resume accumulation, crash zeroing, subagent lineage,
  aggregate `/usage` breakdown (documented, D01/D02/D04/D05):** unchanged from the prior report;
  not re-verified this session (no `-p` call, no subagent, no crash, no `/usage` invocation).

## 6. Cost

- **Accounting mode (observed+documented, E04, E06, E10, D04):** unchanged — individual Pro/Max
  subscription, inferred from absent `ANTHROPIC_API_KEY`, OAuth credential file presence (not
  opened), and `doctor`'s organization-policy/managed-settings messages. Per D04, this account
  type's `/usage` cost figure is explicitly "not relevant for billing purposes."
- **Per-attempt USD (inferred, still not obtainable in an interactive session):** no cost field
  exists anywhere in this session's transcript (§5, E12). A `-p`/SDK result message would carry
  `total_cost_usd`/a per-model breakdown, but only as a documented client-side list-price estimate
  (D02), and no such call was made this session.
- **No cost-relevant change from the cleanup itself:** the cleanup disabled connectors/plugins/
  memory and removed stale instruction files; nothing in the receipts (E20) or this session's
  observations touches billing mode, spend limits, or usage-credit configuration.

## 7. Artifacts and interruptions

Unchanged from the prior report — documented only, not exercised this session (D01):

- **SIGTERM:** exit code 143; in-flight turn left unfinished with no result recorded; `SessionEnd`
  hooks still run; any live Bash process tree is killed.
- **SIGINT / `interrupt()`:** the turn ends cleanly instead.
- **Resume:** the interrupted turn is left as-is unless `CLAUDE_CODE_RESUME_INTERRUPTED_TURN=1`.
- **Working-directory deletion mid-session:** session keeps running; shell commands fail until
  restored.
- **Persistence (observed, E11, E15):** this session's transcript is an ordinary local file, not
  container-ephemeral; `guild-ledger-research` remains a local git working tree with `origin` set
  but zero local commits (unchanged — E15).
- **Stable IDs (observed, E04, E11):** `CLAUDE_CODE_SESSION_ID` (36-char UUID, matches the
  transcript filename `0ce38a75-14d9-451d-ae7f-c49bce7d1eda.jsonl`); per-response `message.id`
  (`msg_…`) / `requestId` (`req_…`); per-entry `uuid`/`parentUuid`.
- **Scratch-edit demonstration (observed, E16):** a file was created, read back, and removed inside
  this new report folder, following the same pattern as both prior reports' equivalent probes.

## 8. Harness compatibility

| Harness | Assessment | Status | Notes |
|---|---|---|---|
| **H0**, no added rules | **Materially closer to a clean baseline than the prior report found**, and directly observed rather than inferred from file listings: this session's own instruction-discovery chain (user rules, project `AGENTS.md`/`CLAUDE.md`, personal skills, account MCP servers, synced plugins) is now empty for this project directory (§2). Hooks remain absent. This is still account/filesystem-level cleanliness, not a sandboxed per-attempt isolation boundary (prior Codex review F07 stands) — a fresh clone into a disposable workspace, not reuse of this exact home-directory account state, is still the stronger guarantee for an actual admitted H0 profile. | observed (for this session's own inputs); not yet admitted as an experiment boundary | `--bare`/`--safe-mode`/`--restricted` remain available as additional, unused belt-and-suspenders knobs (D01/D03) |
| **H1**, one guidelines file | **Feasible, and now starting from a cleaner floor**: a single `CLAUDE.md`/`.claude/settings.json` committed at a per-condition repo root would be the *only* instruction-discovery input, since no competing personal rule file or home-directory `AGENTS.md` exists anymore to interact with it. | documented | Not exercised; depends on which condition repo is checked out as `cwd` |
| **H2**, bounded planning/review workflow | **Unchanged**: real local enforcement primitives (`--max-budget-usd`, `--permission-mode`/`--permission-prompts none`, subagent depth/concurrency, `--tools ""` for genuine tool removal per §3) exist as primitives; no built workflow exists yet. | inferred | None exercised this session |
| **H3**, pinned Loom profile | **Differently blocked, not resolved**: the prior report found an installed Loom binary with no `run` subcommand; this session finds **no Loom binary on `PATH` at all** (loom removal, E14/E20). Whether a pipeline-capable release exists anywhere, and whether the `ai-assistant-dot-files` source checkout (prior Codex review F03) still holds a buildable executor after the broader cleanup, is **unknown** from this session — out of scope to inspect a sibling, unrelated checkout. | observed (absence from PATH); unknown (whether a pipeline-capable build exists anywhere) | A future H3 decision needs either a separately obtained/rebuilt Loom release or an explicit decision that "Loom native execution" means something to (re)install deliberately, not something to assume from account history |

## Observed vs unverified

- **Observed:** local terminal surface and process ancestry to Terminal.app (new session, same
  pattern), CLI 2.1.304/commit `17ab70404e5b` unchanged, macOS/arm64 environment unchanged, model
  label `claude-sonnet-5`/effort `high` across 39/39 entries, zero MCP servers, all three synced
  plugins disabled, `autoMemoryEnabled`/`disableClaudeAiConnectors` explicit in `settings.json`,
  `~/.claude/rules` emptied, `~/.claude/skills` reduced to the synced/built-in catalog,
  `~/.claude/CLAUDE.md` and `~/.claude/framework-install.json` removed, home-directory `AGENTS.md`
  removed (and absent from this session's own system prompt), no project-level `.claude/`, no
  managed-settings file, Loom absent from `PATH`, no cost field in this transcript, 39 assistant
  entries collapsing to 9 distinct message/request ids (a different ratio from the prior session's
  40→17), `CLAUDE_CODE_CHILD_SESSION=1` recurring in a second independently-launched session.
- **Documented only (not exercised this session):** every `-p`/headless flag and behavior in §3,
  §5, §7; official documentation D01–D06 were **reused from the prior report, not re-fetched**
  this session (a stated limitation, not a verified-fresh citation).
- **Unverified or unknown:** verified backend model revision; the meaning of
  `CLAUDE_CODE_CHILD_SESSION=1`, now seen twice; whether a pipeline-capable Loom build exists
  anywhere on this machine or in the sibling source checkout; whether the "Remote Control" line
  newly quoted in `doctor`'s output is itself new or was simply not quoted before; whether
  `--max-turns` is truly absent from this version or just missing from `--help`.

## Three largest measurement and control gaps

1. **No executed headless call exists yet on this surface, still.** Every `-p`/SDK behavior in
   this report is read from official documentation and `--help` text, not exercised, in both this
   session and the prior one. The cleanup changed what instructions/tools are *available*; it did
   not and could not demonstrate what a headless call's output actually contains on this account.
2. **Per-attempt USD remains unobtainable from an interactive session**, unchanged by the cleanup —
   this is a property of the account's billing mode (Pro/Max subscription) and the headless
   result-message cost field's documented placement, not of instruction/plugin/connector state.
3. **The cleanup raises a new, narrower gap: Loom's absence from `PATH` is now observed, but
   whether any pipeline-capable Loom build still exists anywhere (rebuildable from source, or a
   different release) is unknown.** H3 compatibility moved from "installed binary lacks `run`" to
   "no binary found at all," which is not the same as "native execution is impossible" — it is an
   open question about what, if anything, should be deliberately (re)installed for a future H3
   profile, now that the account-level cleanup has removed the ambient installation entirely.

## Proposed probes (not executed; each needs Oscar's approval)

Carried forward from the prior report, adjusted for the now-cleaner baseline and the F01/F05
corrections resolved in §3 above. None were executed this session.

| Probe | Purpose | Inputs | Expected evidence | Max calls | Time/spend cap | Enforcement | Known overshoot risk | Approval |
|---|---|---|---|---|---|---|---|---|
| P1: single `-p --output-format json --tools ""` call, trivial text-only prompt, no `--bare` | Confirm `total_cost_usd`/`modelUsage`/`session_id` actually appear in this account's headless output on the now-cleaned instruction/plugin/MCP state, with tool availability genuinely removed (not just auto-approval) | `claude -p "reply with the single word ok" --output-format json --tools "" --max-turns 1 --max-budget-usd 0.10` | Exit code, `session_id`, `result`, `usage`, `total_cost_usd`, `modelUsage` | 1 model call | ≤ $0.10 list-price-equivalent; ≤ 2 minutes wall time | `--max-budget-usd 0.10` plus a wrapper that kills the process past the time cap | A supervisor dollar cap is an estimated-spend check that may overshoot per the CLI reference; account for that, don't assume exactness | Oscar (extra model session, out of scope for this task) |
| P2: SIGTERM-interrupt behavior | Verify the documented "no result recorded, exit 143" behavior holds on this exact installed version post-cleanup | One `-p` call on a multi-step prompt, SIGTERM sent ~3s in | Exit code, presence/absence of a result, session resumability afterward | 1 model call, interrupted | ≤ $0.10, ≤ 1 minute | `--max-budget-usd`, a `timeout`-wrapped `kill -TERM` | Partial tool execution before the signal lands | Oscar |
| P3: `--bare` auth check, now with no Loom/rules/AGENTS ambient state to confound it | Determine whether `--bare` authenticates at all under this account's OAuth-only setup, now that the instruction/plugin chain is already empty without it | `claude --bare -p "reply with the single word ok" --max-turns 1` with no key set | The specific auth error, or confirmation it works some other way | 1 attempt, expected to fail fast | ≤ 1 minute | none needed if it fails before billing; abort if it appears to proceed | If it *does* authenticate unexpectedly, a billed call could follow — would need `--max-budget-usd` added before approval | Oscar |

## Reproduction

```
which claude && claude --version
ps -p $PPID -o pid,ppid,comm   # walk up to confirm terminal ancestry
printenv CLAUDE_CODE_ENTRYPOINT CLAUDE_CODE_CHILD_SESSION CLAUDE_EFFORT CLAUDE_CODE_SESSION_ATTENDED
claude doctor
claude mcp list
claude plugin list
cat ~/.claude/settings.json
ls -la ~/.claude/rules ~/.claude/skills ~/.claude/CLAUDE.md 2>&1
find /Users/oscarrieken/Projects/Rieken/guild-ledger -maxdepth 2 -iname "CLAUDE.md" -o -iname "AGENTS.md"
ls -la /Users/oscarrieken/AGENTS.md 2>&1
which loom 2>&1
```

Tally transcript schema without printing content:
```
python3 -I - <<'PY'
import json, collections
# point at ~/.claude/projects/<cwd-encoded>/<session-uuid>.jsonl
PY
```

## Delivery note

These files are written directly into the local checkout at
`guild-ledger/guild-ledger-research/docs/runtime-discovery/claude-code-headless/20261021T053558Z/`,
a new dated subfolder alongside the preserved, unmodified prior report at the parent
`claude-code-headless/` level (`report.md`, `capabilities.json`, `evidence.md`,
`review-codex.md`). Per the task, all changes are left **uncommitted**.
