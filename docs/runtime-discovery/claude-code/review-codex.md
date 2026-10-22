# Review of Claude's runtime discovery

Review concerns the report files currently delivered in this folder. Reviewer: Codex. No cloud reproduction, additional model calls, authentication changes, or proposed probes were executed. Original report files are preserved.

## Assessment

Accept as a useful **discovery report for a Claude Projects cloud thread**. Do not treat it as a validated local Claude CLI profile, certified metering implementation, or evidence of benchmark quality. The report is appropriately explicit about many unknowns; some categorical conclusions and implementation suggestions still exceed its evidence.

Local checks: `capabilities.json` parses; 30 capability records contain the requested fields/status values; all referenced evidence IDs resolve with no duplicates; E01–E14 have evidence-log entries. These checks establish internal traceability, not authenticity or reproducibility of remote observations. The source files contain narrative observations and selected redacted snippets, not the complete raw records or a tested usage extractor.

## Findings in priority order

### F01 · High · Register the actual surface separately

[Report identity](report.md#1-identity) and E02/E04 describe `remote_projects` and a child cloud session. The tool ID/folder is `claude-code`, which can be mistaken for the local CLI profile in our runtime shortlist.

**Consequence:** A cloud observation must not certify local/headless behavior, nor can cloud H0 be substituted for local H0 in one controlled campaign. This report does not invalidate the local CLI candidate; it simply did not inspect that candidate.

**Action:** Preserve these source files, but register the normalized profile as `claude-projects-cloud` with its discovery folder reference. Keep a separate `claude-code-headless` discovery/profile with its own version, account mode, effective settings, tools, and evidence.

### F02 · High · Token schema discovery is not complete usage capture

[Metrics](report.md#5-metrics), E05, and `metrics.per_call_usage` identify repeated message IDs and uncertainty about output counts. Coordinator usage is separate and child lineage is unresolved. A single sample is explicitly not a total.

**Consequence:** Deduplicating input rows is necessary, but insufficient to compute reliable whole-attempt tokens or USD. A list-price estimate is not complete when required token categories/children are missing. Do not mark estimated cost complete simply because a formula can be applied to the visible fields.

**Action:** Obtain an allowlisted usage-only export and reproducible extraction procedure. Retain message/request/session IDs, timestamps, finality, parent lineage, model labels, cache TTL categories, and capture cutoff. Determine whether repeated rows are identical or updates; define how final usage is selected. Compare against an independent aggregate where available. Otherwise mark output, child, coordinator and cost completeness partial/unknown.

The [SDK cost documentation](https://code.claude.com/docs/en/agent-sdk/cost-tracking) corroborates deduplication and placeholder-output cautions for the SDK, but that does not prove the cloud transcript has identical semantics. Keep this cross-surface inference explicitly unresolved.

### F03 · High · Unknown platform control should not become universal impossibility

[Compatibility](report.md#8-harness-compatibility) says the surface is not comparable to a bare headless baseline and later says a clean H0 is not achievable. Mandatory runtime behavior is real baseline behavior, but H0 was defined as no **added experimental** harness, not no built-in system behavior.

**Consequence:** It is premature to permanently exclude all within-cloud H0/H1 comparisons. What is currently missing is evidence that host inputs, model fallback, memory, coordination, and settings are stable enough for the intended contrast. The reported state is not sufficient for admission today.

**Action:** Record `controlled_admission: not_yet_demonstrated`; treat it as a native-system candidate. If the same cloud baseline can be held stable across treatments, some within-surface comparisons may be valid with stated limitations. Never describe them as equivalent to local CLI results or evidence of no platform harness.

### F04 · Medium · Split mixed claims into atomic evidence statuses

Some capability rows labeled `observed` bundle observations with documentation or inference. For example `automation.observe_progress` includes a CLI follow-up method not exercised; `instructions.context_management` combines observed flags with documented commands. `tools.edit_shell_tests` is true even though the tool was available but no test execution was demonstrated. Names of telemetry environment variables indicate configuration hints, not proof of accessible, emitted, complete telemetry. Host-reported CPU/memory should also distinguish visible capacity from verified enforced limits.

**Action:** Split available/configured/exercised into separate claims. Link a concrete redacted observation or reproducible command to each observed assertion. Keep full hidden prompt text and credentials out of evidence. Do not infer a fixed instruction hierarchy merely from the order categories were listed unless precedence was independently established.

### F05 · Medium · File writability does not establish durable export

[Artifact claims](report.md#7-artifacts-and-interruptions) and E10 show a scratch edit succeeded in the shared project folder. They do not demonstrate cross-thread durability, export completeness, interrupted-write recovery, or retention after environment reclamation. `artifacts.interruption_survival` partly blends documentation and an untested persistence conclusion.

**Action:** Separate local write/read, cross-session visibility, external delivery, and expiry survival. We can now observe that the three delivered docs exist in the research checkout; that verifies this handoff only, not automatic synchronization or usage-log survival. Treat durable generation telemetry as unverified until exercised.

### F06 · Medium · Repository attachment preflight is not a failed push

E08 records `add_repo(..., access=push)` with a refused `push_check`. The report also explicitly says no push was attempted. Calling it a refused push is easy to misread as evidence of a failed `git push`. Attaching a repository is also a control-plane state change, so future read-only probes should distinguish attachment from listing metadata.

**Action:** Use “repository attachment push-access preflight denied.” Separate that environment configuration issue from runtime suitability. Do not install apps, reconnect accounts, or push changes as part of this review.

### F07 · Medium · Proposed probes do not have enforceable accounting bounds

[Probe table](report.md#proposed-probes-not-executed-each-needs-oscars-approval) proposes a percentage of a subscription window, a time-only routine test, and one headless turn with a dollar target. Percentage-of-quota is not a reliable per-attempt cost ceiling; a proposed cap is not an enforcement mechanism. One turn does not establish exactly one request or cover all tool/auxiliary behavior.

**Action:** Define each probe's actual request/tool/agent controls, time cutoff, permitted spend basis, in-flight overshoot, cleanup, and durable evidence before authorization. Do not treat these probes as approved. Skip the nested-cloud-CLI probe for now: local headless discovery is the more direct test of the initial runtime candidate. Test nested CLI only if we deliberately want a nested native-cloud deployment.

## Important local-headless accounting follow-up

For a future CLI/SDK adapter, the current [cost guide](https://code.claude.com/docs/en/agent-sdk/cost-tracking) distinguishes main-loop `usage` from whole-tree `modelUsage`, describes cumulative totals across resumed sessions, and warns that error results may omit or zero usage. Dollar fields remain estimates. These are requirements to validate on the chosen installed version, not evidence that cloud metering is solved.

Use fake fixtures for duplicate messages, cumulative updates/resume, missing final output, child calls, and interrupted/error results. Do not blindly sum every result or count absent data as zero.

## What this changes for our plan

| Item | Review disposition |
|---|---|
| Claude Projects cloud report | Retain; useful discovery with unresolved controls |
| Local Claude Code headless profile | Still pending its own discovery; no admission inferred from this report |
| H0/H1 within Projects | Possible research question, control stability not yet demonstrated |
| H2 enforcement on Projects | Unknown beyond instruction-level feasibility |
| Loom context-only profile | Distinct from native executor; not validated |
| Loom nested native execution | Unverified; not required for the first local campaign |
| Complete per-attempt USD from this cloud report | Not established |
| Proposed extra calls/probes | Not authorized or run |

## Recommended next handoff

Run the discovery prompt in a **local terminal Claude Code session** attached to the research checkout, not through Projects and not by starting a nested CLI inside this cloud session. Label the output surface explicitly and use a new folder, for example `docs/runtime-discovery/claude-code-headless/`. Read-only inventory can establish invocation/configuration surfaces; live headless metering still requires a separately bounded calibration.

Request atomic evidence labels and a usage-only export example that distinguishes actual captured records from schema-only illustrations. Do not change personal/global configuration to simulate a baseline during discovery. Then normalize this cloud report and the local report side by side before choosing the initial runtime campaign.
