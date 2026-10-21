# Runtime discovery report

Captured: 2026-10-21 14:36:20 UTC  
Tool: `github-copilot-coding-agent`  
Folder: `docs/runtime-discovery/github-copilot-coding-agent/20261021T143620Z/`

## Executive summary

**Exact runtime surface observed:** GitHub-hosted Copilot coding agent running in a GitHub Actions-hosted Linux x86_64 runner, in the `dynamic/copilot-swe-agent/copilot` workflow and `copilot` job. This is not a local VS Code or CLI session. [Observed; E01]

The runtime reports `runtime-cca-vendored-a3b15b740302d352cffb1bec7e01de2f5a4bffce`; the host reports Linux `6.17.0-1022-azure` x86_64. [Observed; E01, E02] Product release/version, model label, selected reasoning effort, and whether this task had a user-selectable model pin are **unknown**. [Unknown; E03, E04]

This task is a hosted-platform baseline, not a controlled experiment. No benchmark, auxiliary agent/model session, dependency installation, settings/workflow change, or Loom execution was performed. Available platform capabilities are not evidence that each was exercised. [Observed; E05]

## Runtime, configuration, and access

- **Surface and isolation:** The hosted runner and cloud-agent workflow markers establish this as a GitHub-hosted Copilot coding-agent task, not a local editor/CLI run. The checkout is an ephemeral task workspace; official documentation says cloud-agent environments are destroyed when a session ends while the session log remains available. [Observed; E01, E02; Documented; E06]
- **Version/model:** Runtime build identifier is observed above. Product version and model identity are unknown: no safe model label was exposed in the inspected metadata. Reasoning setting is unknown. [Observed; E02; Unknown; E03, E04]
- **Model pinning:** GitHub documents model selection and configurable reasoning for supported entry points; when a picker is absent, Auto is used. The entry point's selected model/reasoning and whether its picker was used are unknown here. Thus available controls are documented, not exercised or verified for this task. [Documented; E04]
- **Checkout/setup:** The task repository is checked out at `/home/runner/work/guild-ledger-research/guild-ledger-research` on `copilot/create-runtime-discovery-report`. No `AGENTS.md` or `copilot-setup-steps.yml` was found in the inspected parent/repository paths. No setup/install command was run. [Observed; E02, E05]
- **Effective task guidance:** The task prompt supplied constraints; the repository's inspected collection guide documents the expected three-file report and collector workflow. There were no repository `AGENTS.md` files in the inspected tree. Hidden platform instructions are not reproduced. [Observed; E05; Documented; E10]
- **Available tools/skills:** The session interface exposed repository/file/search/shell tools, GitHub operations, browser/web retrieval, progress reporting, validation/security checks, and memory/session-store tools. The available named skills were `customize-cloud-agent` and `merge-branch`. This is an interface inventory; it does not imply each tool or skill was invoked. [Observed; E07]
- **MCP:** `COPILOT_MCP_ENABLED=true` was observed, and a GitHub MCP tool set was exposed in the session interface. Whether other servers or tools were enabled by policy, and which MCP calls were exercised, is not established by this inventory. [Observed; E02, E07]
- **Hooks and memory:** No repository hook configuration was identified in the inspected files. Hooks' runtime execution is unknown. Memory-related tools were exposed, but no repository memory content was inspected or used for this report. [Observed; E05, E07; Unknown; E08]
- **Network and approvals:** The actual firewall/allow-list and outbound network policy were not read or tested. The documentation describes configurable firewall and runner/setup options. `COPILOT_PERMISSION_MODE=default` and `COPILOT_PERMISSION_GATE_REASON=enabled` were observed; exact approval rules, prompts, and gates for this task are unknown. [Observed; E02; Documented; E09; Unknown; E08]

## Task lifecycle, progress, and artifacts

- **Submission:** Copilot cloud agent tasks can be started from documented GitHub.com agent entry points, but this task's original submission route is unknown. [Documented; E06; Unknown; E08]
- **Monitoring and steering:** GitHub's session interface documents real-time progress/session logs and steering. The session logs can show tool use, token usage, and session length. This discovery records no private reasoning. [Documented; E06, E10]
- **Cancellation and partial work:** The documented Stop session control ends the Actions run and preserves commits already pushed. This task has a progress/commit mechanism, but no interrupted task or partial-result scenario was tested. [Documented; E06; Unknown; E08]
- **Report artifact retrieval:** The repository's existing manually dispatched **Collect Copilot discovery report** Action takes a PR number and timestamp, retrieves the three files at the PR head SHA, and uploads them as `copilot-discovery-<PR>-<timestamp>` with a 90-day retention period. The workflow transports report files; it does not export private session telemetry. [Documented; E10]

## Usage evidence and billing provenance

- **Available evidence:** GitHub documents session-log access to token usage and session length. The current task environment did not expose an exportable per-session record for input/output/cache/reasoning tokens, request/session identifiers, retries, child calls, interrupted calls, or per-call timestamps. These values are unknown, not zero. [Documented; E06; Unknown; E03, E08]
- **Export:** The inspected collection Action exports the report files, source commit, collection timestamp, and file hashes—not model/token telemetry. A supported export for the detailed usage fields listed above was not established. [Observed; E10; Unknown; E08]
- **Actual charges:** No account billing page, invoice, or usage ledger was accessed. Actual charge for this session is unknown. This documentation task may consume normal Copilot allocation; it is not represented as free. [Observed; E05; Documented; E11; Unknown; E08]
- **Estimates and allocation:** Official individual-plan documentation describes AI credits, token/model-dependent prices, included allowances, and possible paid overage. The active plan, model multiplier, estimate, allowance drawdown, credits, premium requests, and actual charge are unknown for this task. Do not substitute an estimate or allocation for an actual charge. [Documented; E11; Unknown; E03, E08]
- **Actions compute:** The later collector run is a separate GitHub Actions workflow execution. Its compute usage/billing is not part of a measured Copilot session charge and is unknown for this task. [Observed; E10; Unknown; E08]

## Feasibility of experimental conditions

| Condition | Assessment |
| --- | --- |
| **H0 — no added experimental harness** | **Observed baseline; feasible.** This run uses the mandatory native Copilot-hosted task environment and platform workflow. It is not a harness-free or platform-free control: native checkout, task instructions, agent runtime, available tools, and progress/commit mechanisms remain part of H0. No extra harness was installed or configured. [Observed; E01, E02, E05, E07] |
| **H1 — fixed guidelines** | **Feasible in principle; not independently controlled.** A fixed task prompt/repository guidance can specify constraints. This task had explicit guidelines, but prompt capture, model pinning, and repeated-run compliance were not measured. [Observed; E05; Documented; E10; Unknown; E03, E04] |
| **H2 — custom bounded workflow** | **Feasible in principle; not exercised.** GitHub documents setup steps, custom agents/skills, MCP, hooks, runner selection, and firewall configuration. No such custom workflow was added or run here; actual controls/enforcement remain unknown. [Documented; E09; Observed; E05, E07; Unknown; E08] |
| **H3 — Loom** | **Not demonstrated; feasibility unknown.** Loom was not run, and no Loom-backed task or execution evidence was inspected. Reading Loom documentation, if done later, would not establish native Loom execution. [Observed; E05; Unknown; E08] |

## Isolation, retention, and reproducibility

- **Isolation:** GitHub documents an ephemeral cloud-agent development environment. The local checkout and runner markers are consistent with that description. Exact container/VM boundary, tenant isolation controls, and data-plane topology were not independently verified. [Documented; E06; Observed; E01, E02; Unknown; E08]
- **Retention and visibility:** Official docs say the environment is destroyed after the session while its session log remains on GitHub; cloud-agent sessions are shared by default with people who have repository access. The collector artifact described by this repository expires after 90 days. Account-specific retention settings were not inspected. [Documented; E06, E10; Unknown; E08]
- **Reproducibility:** Exact prompt/submission metadata, model identity, reasoning setting, detailed usage telemetry, runner image digest, network policy, hidden platform configuration, and account billing records are unavailable here. A repeat cannot be claimed equivalent from the checked-in report alone. [Unknown; E03, E04, E08]

## Three largest measurement gaps

1. **Model and inference configuration:** selected model, reasoning level, pinning state, and per-call/child-call/retry identity are unavailable. [Unknown; E03, E04]
2. **Usage and cost attribution:** no session-level input/output/cache/reasoning token export or actual Copilot charge/credit/overage record; Actions compute is separate. [Unknown; E03, E08; Documented; E11]
3. **Execution controls and replayability:** no complete task-entrypoint/prompt capture, actual firewall/approval/hook configuration, runner image digest, or independently verified isolation boundary. [Unknown; E08]

## Optional future calibration probe (not executed)

A small, single-task probe could use a fixed benign task, a recorded prompt and source commit, and a preselected model/reasoning setting where the entry point supports selection. Its purpose would be to test reportable session metadata, tool-call/steering/cancellation visibility, and the mapping between session usage records and account billing—not to benchmark model quality. Expected evidence would be the task/session log, visible model/reasoning controls, timestamps, tool/child/retry records if exposed, token categories if exposed, and a separately captured billing/Actions usage record. The probe should be bounded by one task, a human-reviewed repository, least-privilege tools, and a fixed maximum spend/stop condition where the platform supports enforcement. Missing per-call telemetry, nondeterministic model behavior, hidden platform configuration, and the inability to equate an estimate or subscription allocation with a charge would remain limitations. Do not run this probe as part of this report. [Inferred; E12]

## Run the existing collector

After this PR is available on the repository's default branch, run **Actions → Collect Copilot discovery report → Run workflow**. Supply this PR's number and `20261021T143620Z` as the report timestamp. The collector saves a 90-day artifact named `copilot-discovery-<PR>-20261021T143620Z`. It does not launch an agent, merge the PR, or retrieve private session telemetry. [Documented; E10]

## Claim status key

Material claims use **Observed**, **Documented**, **Inferred**, or **Unknown**, with evidence IDs. “Available” indicates documented or exposed capability; it does not mean exercised. Unknown values are intentionally not imputed as zero.
