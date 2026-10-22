# Codex runtime discovery after global cleanup

Captured: 2026-10-21T05:35:48Z. Discovery only; no benchmark, new model session, subagent, Loom execution, installation, settings change, commit or push.

## Scope and identity

**Observed [E01,E02,E05]:** This discovery runs in an interactive desktop chat with a local shell operating on Darwin 25.6.0 arm64. The starting workspace is a ChatGPT project mirror, not the research checkout. The requested three documents were located and read in the local research checkout. A separate installed executable resolves to `/opt/homebrew/bin/codex` and reports `codex-cli 0.163.0`. Claude is also installed; that does not make this a Claude session. Local filesystem observations support local tool execution; process ancestry inspection was denied. **Unknown:** desktop harness build, executor process provenance beyond those observations, and location of model inference. Folder name `codex-headless` identifies the target profile, not evidence that this chat is headless.

**Observed [E03,E04]:** User configuration selects `gpt-6.1-sol` and effort `low`; CLI login status says ChatGPT. **Unknown:** actual backend model/revision, effective effort in this chat, account plan, billing allocation and desktop authentication route. **Observed, available only [E02]:** CLI model and configuration overrides exist. **Inferred:** record exact executable hash/version and frozen invocation for reproducibility. **Unknown:** immutable backend revision pinning and server-side enforcement of requested settings.

## Cleanup and remaining inherited state

**Observed [E03]:** All thirteen configured optional plugin entries are false. Memory feature, use and generation flags are false. The personal rules directory is empty; global Codex AGENTS and override files are absent; only `.system` remains in the user skills directory; no home `.agents/skills` directory. No AGENTS/override was found along checkout ancestors. The mirror has its read-only-source instruction file. The research checkout has no `.codex` or `.agents` directory. Global Loom executable checks at Homebrew/local-bin locations and PATH resolution found none; this is a bounded inventory, not proof of removal from every path.

**Observed [E03]; discrepancy with historical receipt [E01]:** `computer-use` and `cua_repl` explicitly have `enabled: false`; `node_repl` is configured but has no `enabled` field. `features.js_repl` is false. These are different controls. **Unknown:** whether that MCP server initializes in a fresh CLI. Do not claim both MCP servers are verified disabled now. No repair was made.

**Observed [E03]:** Notification configuration and plugin hook trust metadata remain. **Unknown:** effective hook invocation in a fresh CLI. Trust metadata does not prove enabled hooks.

**Observed [E05]:** This existing chat retains previous conversation material and currently exposes plugin/connector and MCP namespaces despite local disabled plugin settings. Available skill catalog includes system imagegen, OpenAI Docs, skill creation/installation, plugin management, Sites and Work Pets skills. OpenAI Docs was read/applied; other skills were not exercised. Shell, web lookup and report writing were exercised. Node REPL, GitHub, Sites, pets, document/artifact tools and collaboration capabilities were available in the session catalog but not exercised. Their exposure does not prove fresh-CLI availability or authenticated service access. **Unknown:** complete organization/cloud instruction, rules and memory state. Governing platform policy remains mandatory; no hidden instruction bodies were inspected or exported. Fresh chat and per-attempt input isolation are still required for H0.

## Headless automation and artifacts

**Observed, available only [E02]:** Installed help supports `codex exec`, prompt argument/stdin, `-C`, model/config overrides, sandbox choice, JSONL, final-message output, final-response schema, explicit resume/fork, ephemeral mode, ignoring user configuration and ignoring execpolicy rules. Top-level approval policy has `never` and `on-request`. Help/version checks produced a PATH-alias permission warning but returned zero. No inference command was started.

**Documented [E06]:** Official noninteractive guidance defines structured lifecycle events and usage fields; see the evidence schema below. **Unknown:** actual events emitted by this installation under success, failure, retry, resume or cancellation. An interactive chat is not a headless test.

**Inferred [E02,E07]:** A caller should create a clean standalone workspace, supply only approved task inputs, capture stdout/stderr separately with host timestamps, save exit status and immutable input hashes, and snapshot all changed and untracked files. The final response file is not a code artifact bundle. Preserve binary files and partial writes separately from a patch. A supervisor must handle timeout/process groups; no hard money, token or turn cap was established from help. Killing the local process cannot promise cancellation or nonbilling of in-flight inference.

**Observed [E07]:** This checkout reports README, docs and repositories.json as untracked and has no HEAD commit. Preserve this preexisting state. Do not use `git diff HEAD` as a complete collector here. **Unknown:** platform retention/export guarantees, ownership terms, interrupted final-message persistence, or complete remote records. Reports are local files; export/retention policy needs a separate agreement.

## Usage and cost

**Documented [E06]:** The official example exposes a thread ID and input, cached-input, output and reasoning-output token fields. **Unknown:** provider request IDs, per-request usage, exact cache semantics, retries/errors, compaction overhead, child/reviewer attribution, duplicate delivery and whether resumed totals are incremental or cumulative. Preserve raw event envelopes and arrival order; do not sum repeated lifecycle items or resumed totals until their semantics are verified. Do not inspect or retain private reasoning text for this study; extract allowed metadata/categories only.

**Observed [E05]:** Shell tool elapsed times and execution result IDs are visible; these are not inference request IDs or model-token totals. No actual model usage or charges were exported. **Unknown:** attributable billed USD and subscription allocation. ChatGPT login is not API per-token billing evidence. A future list-price multiplication would be a client estimate with model, rate date and formula, never an actual charge. Reasoning/cache categories may be subsets; avoid double counting. Reconciliation requires authorized provider usage/billing records correlated to attempt/request lineage; if unavailable, keep per-attempt USD null. This documentation session itself must not be described as zero-cost.

## Harness compatibility

| Profile | Claim status | Assessment |
|---|---|---|
| H0 baseline | Inferred [E01,E03,E05] | Candidate; not admitted. Mandatory native runtime remains, node_repl ambiguous, prior chat/context persists. |
| H1 fixed guidelines | Inferred [E01,E02] | Frozen explicit file/input plausible; hash treatment and prove identical H0 mechanics. |
| H2 bounded workflow | Inferred [E01,E02] | Planning/checks plausible; enforce limits externally and meter all calls. Not exercised. |
| Loom context-only | Inferred [E01,E02] | Frozen text/assets plausible; distinct reduced profile. Not loaded. |
| Loom native pipeline | Unknown [E01] | Historical selector inspection found no Codex provider; current source/provider execution not verified. |

## Three largest gaps

1. **Observed/unknown [E03,E05]:** Local cleanup does not prove effective fresh-task isolation; MCP discrepancy and inherited app tools/context remain.
2. **Unknown [E06]:** Complete usage lineage across requests, children, retries, duplicate events, resume and interruption is unverified.
3. **Unknown [E02,E04]:** Actual per-attempt charges, backend revision enforcement and a hard spend cap are unavailable.

## Recommended next probe — proposed, not run

**Inferred proposal [E02,E06]:** After separate authorization and resolving/explicitly accepting the MCP discrepancy, run one fresh CLI invocation in a disposable, standalone directory containing only a tiny synthetic instruction: return one fixed JSON object with no tool calls. This first probe tests startup/context controls and telemetry, not coding performance. Use the recorded CLI version, explicit model/effort, read-only sandbox, approval never, `--ignore-user-config`, `--ignore-rules`, `--json`, output schema and final-message capture. Verify exact effective input/tool isolation first; those flags alone do not prove it. Do not reuse/resume this discovery chat, load Loom, or enable reviewers.

Expected evidence: command manifest and hashes, host start/end, exit status, thread ID if emitted, redacted lifecycle events and all supplied usage categories, final JSON, no workspace changes, and authorized billing reconciliation if available. Limits: one CLI invocation, one requested user turn, no child agents/tools, 30 seconds plus a 5-second termination grace period; no automatic retries by the supervisor. A supervisor process group watchdog enforces local wall time; prompt restrictions on internal calls are not hard enforcement. Actual model requests may exceed one due to runtime retries. Spend basis: current ChatGPT-auth allocation is unknown; do not call it free or assign a USD cap. Require explicit acceptance of unknown subscription usage before proceeding, or establish a separately authorized API billing setup with independently enforced limits first. No auth/config changes are proposed for this discovery.

Overshoot risks: request already in flight, retries before interruption, delayed telemetry, child processes and server-side completion after local kill. No strict dollar bound is established. A single successful probe will not settle resume, interruption, child accounting or native Loom compatibility; propose separate probes afterward only if needed.

## Reproduction and validation

**Observed [E01–E08]:** Read the three referenced project documents; inspect ancestor AGENTS filenames and safe config fields; run only CLI version/help/login-status and repository-status checks; compare findings to the historical cleanup record; retrieve official noninteractive documentation; create these three new files and validate JSON fields, evidence references and local links. Preserve earlier reports and leave all changes uncommitted. See [evidence](evidence.md) and [capabilities](capabilities.json).
