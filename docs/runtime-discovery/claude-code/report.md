# Runtime discovery: claude-code (Claude Projects cloud thread)

Captured 2026-10-21 (UTC) by the agent running inside this surface. This is a discovery record, not a benchmark. It does not show benchmark performance, harness effects, or complete isolation. Evidence IDs (E.., D..) refer to [evidence.md](evidence.md), and the machine-readable form is [capabilities.json](capabilities.json).

Status labels: **observed**, **documented**, **inferred**, **unknown**.

## 1. Identity

- **Surface (observed, E02/E04):** Claude Code running as a **thread of a Claude Projects project** on claude.ai. Each thread is a child cloud session started by the project coordinator, itself another Claude session. It runs in an Anthropic-hosted container (`entrypoint=remote_projects`, `environment_kind=anthropic_cloud`, `cloud_default`, `IS_SANDBOX=1`). This is not the local CLI, an IDE extension, the Desktop app, the Agent SDK, or the GitHub Action, so findings must not be transferred to those surfaces.
- **Runtime version (observed, E01/E05):** `2.1.305`, from the container binary, and the running transcript records the same version. An environment variable `CLAUDE_CODE_VERSION=2.1.42` conflicts with it and its meaning is unknown. The researcher's local CLI was 2.1.292 (E14), which is a different surface. The host picks the version, and pinning it from the researcher's side is not possible as far as we can tell (inferred).
- **Environment (observed, E03):** Ubuntu 24.04.5, Linux 6.18 x86_64, 4 vCPU, 15 GiB, running as root. The container is ephemeral and is reclaimed after inactivity (documented, D01).
- **Model (observed, E04/E05):** the configured label is `claude-opus-5-5[1m]`. The host reports `last_served_model=claude-opus-5-5`, and every API response carries `message.model="claude-opus-5-5"`. Effort is `medium`. The session configuration also lists a **fallback chain** (`claude-opus-5[1m]`, then `claude-opus-4-8[1m]`) and says the serving model can change mid-session.
  - **Verified backend identity: unknown.** We only have response-reported names. No dated snapshot ID is exposed.
  - **Pinning:** thread model and effort are project settings (documented, D04). Pinning a revision and disabling fallback are unknown.

## 2. Automation

| Need | What exists | Status |
|---|---|---|
| Start a fresh task | Project threads are created by the coordinator (or the UI). There is **no documented public API to create a project thread**. External alternatives that are **not project threads**: `claude --cloud "<task>"` from a CLI signed in to claude.ai, or a scheduled task (routine) API trigger `POST https://api.anthropic.com/v1/claude_code/routines/<trig_id>/fire` with `Authorization: Bearer <token>`, `anthropic-beta: experimental-cc-routine-2026-04-01`, `anthropic-version: 2023-06-01`. The routine call returns `claude_code_session_id` and a URL. | documented (D01, D04, D05); none executed |
| Supply prompt and workspace | The prompt is a CLI argument, a routine's saved prompt plus `text` (wrapped as untrusted), or a coordinator relay. The workspace is a GitHub clone (Claude GitHub App required for project repos), a bundle upload via `claude --cloud`, or files mounted at `/mnt/project-files`. In this thread, the coordinator relayed and annotated the user's task (E12). | documented / observed |
| Observe progress | `get_session` returns status, models, and rate-limit and context metadata (E04). The claude.ai UI shows the live transcript. `claude -p "<msg>" --cloud <session-id> [--output-format json]` queues follow-ups. | observed / documented |
| Stop | Project **Pause** interrupts all threads. Sessions can be archived or deleted. An `interrupt_session` tool exists. | documented; not exercised |
| Retrieve changed files | Push a `claude/` branch and open a PR, use `claude --teleport <id>` locally, or write into `/mnt/project-files` (observed writable, E10). **Push to `orieken/guild-ledger-research` was refused** because Claude GitHub App access is missing (E08), and the GitHub repo is **empty** (E09). | observed blocker |

GitHub Actions does not create these jobs. The host platform creates them, and environment image, version, hooks and model fallback stay outside the researcher's control.

## 3. Instructions and state

Visible layers, from highest to lowest precedence as given to the agent (E12; categories only, text not exported):

1. The built-in Claude Code system prompt.
2. Hosted cloud and Projects-thread role instructions: reply etiquette, PR attribution, assignee and reviewer rules, git rules.
3. Hook-injected reminders: `PostToolUse` status nudge, `Stop` git check and reply gate, `UserPromptSubmit` reminder (E06).
4. The session-context block with project name, file list and requester. **No project instructions were set.**
5. The coordinator's relay note.
6. The user's message.
7. Project memory (`MEMORY.md` index empty at capture). Threads and the coordinator can write it, and later threads read it (D04).
8. Synced account skills, plugins, connectors and MCP servers (E06/E07).
9. Repository `CLAUDE.md` files. None here, because the repo is empty.

Context management: auto-compaction triggers at 80% of a 500k window. The host forces this, and it overrides user values (E02, D01). `/compact` works and `/clear` does not (D01).

- **Resettable:** a new thread starts with fresh conversation state. Project instructions and memory can be edited or emptied. Connectors can be toggled, but that changes the account default (D04).
- **Mandatory or inaccessible:** layers 1 to 3 and 5, the host's compaction override, model fallback, and the hook scripts. `--bare` is a headless-CLI flag and has no equivalent here (inferred).

## 4. Tools and permissions

**Available now (observed, E07):**
- File read, write and edit, plus Bash as root in the container. Tests can run via Bash, but none were run.
- Web fetch and search through an egress proxy. code.claude.com was reachable, and several plugin MCP hosts were refused with a 403.
- The GitHub MCP, including merge tools, gated by policy. The claude-code-remote MCP for sessions, triggers and repo attachment. Projects messaging tools. User-device folder and computer-use tools; no device folders were reachable (E11).
- The Agent tool for subagents, with max spawn depth 1 (E02).
- Permission mode is `auto`, where a classifier reviews actions, and `permissions.allow=[Skill]` (E04/E06).
- Filesystem scope covers the container plus `/mnt/project-files`, which is shared by all threads in the project.
- Human intervention is possible at any time: thread messages, decision cards, Pause.

**Documented elsewhere, not observed here:** agent teams (env flag), self-hosted environments, Auto-fix PR watching, and routines with GitHub triggers (D01, D05).

## 5. Metrics

- **Per-API-response usage (observed, E05):** the container-local transcript `~/.claude/projects/<cwd>/<uuid>.jsonl` records, per response:
  - `message.id` (`msg_…`), `requestId` (`req_…`), `timestamp`, `message.model`, `requestedModel`, `effort`, `isSidechain`
  - `usage.{input_tokens, output_tokens, cache_creation_input_tokens, cache_creation.{ephemeral_5m,ephemeral_1h}_input_tokens, cache_read_input_tokens, output_tokens_details.thinking_tokens, server_tool_use.{web_search,web_fetch}_requests, service_tier, speed, inference_geo, iterations[]}`

  Redacted single-response sample (not a total): input 2, output 736, cache read 97,390, cache write (1h) 2,011.
- **Caveats:**
  - 21 transcript entries mapped to only 7 distinct message IDs, so deduplicate by `message.id`.
  - The SDK docs say per-step `output_tokens` is a placeholder (D03). Whether that applies to this transcript is unknown.
  - The file lives only in the ephemeral container.
  - The coordinator's usage is in a separate session.
  - `get_session.context_usage.used_tokens` read 0 after several calls, so it is unreliable.
- **Aggregate:** Project settings has a Usage page showing tokens by thread and by model (documented, D04). It has no documented export.
- **Child and reviewer usage:** `isSidechain` exists, but lineage on this surface is unknown. Headless `parent_tool_use_id` and `modelUsage` are documented for `-p` and the SDK only (D02, D03).
- **Tool events:** tool_use and tool_result blocks are in the transcript (inferred from the schema; content not printed).
- **Errors and retries:** a retry watchdog is enabled (E02). `system/api_retry` events are documented for stream-json (D02); none were observed.
- **Host telemetry:** OTLP and tracing variables exist (E02), but that data is not accessible from the session.
- **Unknown:** reasoning content (beyond thinking-token counts), coordinator token totals, and classifier calls.

## 6. Cost

- **Accounting mode (observed, E04; documented, D01/D04):** claude.ai subscription plan limits. The session reports a `five_hour` rate-limit window and `isUsingOverage=false`. Cloud VMs carry no separate charge, and Projects threads draw on the same plan limits. Usage credits (metered overage) apply only if the user enabled them.
- **Per-attempt USD:** **not obtainable as an attributable billed charge** (inferred). There is no cost field in transcripts and no per-session invoice. A **list-price estimate** can be computed from deduplicated tokens, but it is an estimate under a subscription that is not billed per token. The headless CLI's `total_cost_usd` is itself a client estimate (D02/D03) and is not exposed on this surface. Reconciliation would need API-key billing with the Usage and Cost API, which this surface does not support for cloud sessions (cloud sessions require a claude.ai login, D01).

## 7. Artifacts and interruptions

- **On environment expiry (documented, D01):** the conversation is restored on reopen. Running background work, subagents and shell commands are not.
- **Persistence:** pushed branches and PRs persist on GitHub. `/mnt/project-files` persists across threads (observed writable). The container transcript, uncommitted files and partial usage are probably lost when the VM is reclaimed (inferred; not tested).
- **Stable IDs (observed):** host `session_…`, `parent_session_id` (coordinator), transcript session UUID, per-entry `uuid`, `msg_…` and `req_…`.
- **Retention and ownership:** sessions belong to the claude.ai account and can be archived or deleted. No bulk export of transcripts or usage is documented.

## 8. Harness compatibility

| Harness | Assessment | Status | Blockers |
|---|---|---|---|
| H0, no added rules | Partial. We can add nothing, but the mandatory baseline is large and cannot be exported: thread role prompt, coordinator relay, hooks, synced skills, plugins and connectors, project memory, forced compaction, and the model fallback. It must be recorded as runtime baseline and is **not comparable** to headless `claude --bare` H0. | inferred | Mandatory layers, coordinator rewrite |
| H1, one guidelines file | Feasible via repo `CLAUDE.md` (loaded from clones) or project instructions (≤16k chars). | documented | Repo empty on GitHub; Claude GitHub App or push access missing; adherence is model-followed |
| H2, plan, verify, bounded review | Instruction-level only. Subagents exist (depth 1), but there are no enforced loop caps, metered reviewer lineage, or hard gates. | inferred | No enforcement; child usage lineage unknown |
| H3, pinned Loom profile | **Unknown or blocked.** Loom's native provider shells out to headless `claude`. The binary exists here, but running it would start a nested model session with unknown auth and metering, and it was not executed. Reading Loom context files would be a **context-only profile, not native pipeline support**. | unknown | Nested-session auth and metering, no version pinning, gates unverified |

## Observed vs unverified

- **Observed:** surface and entrypoint, CLI 2.1.305, OS and hardware, configured and served model labels and fallback chain, effort, permission mode, hooks, tool inventory, subagent depth 1, compaction settings, transcript usage schema with duplication, subscription rate-limit mode, push refused, repo empty, scratch edit in the report folder.
- **Documented only:** `claude --cloud`, `-p --cloud` follow-ups, teleport, routines `/fire` API, project Pause, Usage page, expiry semantics, cost-estimate caveats.
- **Unverified or unknown:** backend model identity, model and version pinning, interrupt survival, child usage lineage, usage export, Loom native execution, the meaning of `CLAUDE_CODE_VERSION=2.1.42`.

## Three largest measurement and control gaps

1. **Attributable cost and complete usage lineage.** Usage is subscription-pooled with no per-attempt USD. The per-response transcript is container-local and ephemeral and must be deduplicated, and its output counts may be placeholders. Coordinator and child usage are split across sessions, and no Usage export is documented.
2. **Input isolation.** Mandatory host prompts, a coordinator that rewrites tasks, writable project memory, account-synced skills, plugins and connectors, forced compaction, and a model fallback chain all sit outside experimental control. A clean H0 or matched cross-runtime comparison is not achievable on this surface as observed.
3. **Programmatic lifecycle control.** No public API creates a project thread. External starts (`claude --cloud`, routines `/fire`) produce standalone sessions on a research-preview API. Stop and interrupt semantics are untested, and retrieving changes depends on Claude GitHub App push access, which is currently refused.

## Proposed probes (not executed; each needs Oscar's approval)

| Probe | Purpose | Inputs | Expected evidence | Max calls | Cap | Approval |
|---|---|---|---|---|---|---|
| P1: transcript usage export | Check whether deduplicated per-response usage can be exported before the VM is reclaimed, and whether per-step output tokens are placeholders | One new thread on a tiny synthetic task; a script copies a **usage-only** projection of its transcript to `/mnt/project-files` | Usage JSON compared with the Project Usage page | 1 thread | ≤10 min, ≤1 % of a 5-hour plan window | Oscar |
| P2: routine API start and stop | Verify external start, `get_session` polling, `interrupt_session`, and what survives | A routine with an API trigger on a throwaway repo with the Claude GitHub App installed | Fire response IDs, status transitions, surviving branch, files and transcript | 1 fire + 1 interrupt | ≤15 min | Oscar; GitHub App install |
| P3: nested headless CLI (Loom prerequisite) | Find out whether `claude -p --output-format json` can authenticate and report usage inside a cloud container | One trivial prompt, `--max-turns 1` | Exit status, `session_id`, `usage`, `total_cost_usd`, or the auth error | 1 model call | ≤$0.50 list-price equivalent, 2 min | Oscar (it is an extra model session) |

## Reproduction

In a Projects thread, run `claude --version` and check `CLAUDE_CODE_ENTRYPOINT` and the other non-secret flags listed in E02. Call `get_session` with no ID. Tally key names in `~/.claude/projects/<cwd>/*.jsonl` without printing content. Read the structure of `~/.claude/launcher-settings.json`. Run `list_repos` and `add_repo`. Fetch D01 to D05.

## Delivery note

The GitHub repo `orieken/guild-ledger-research` is empty, and pushes from this surface were refused, so no branch or PR was created. These files were written to the project's shared folder at `guild-ledger/guild-ledger-research/docs/runtime-discovery/claude-code/`. Copy them into the local checkout, uncommitted, for review.
