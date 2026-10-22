# Runtime comparison and selection

Updated 21 October 2026 after all returned discovery reports and merged Copilot PR #1. This is a design recommendation, not measured runtime performance or admission to paid experiments. No calibration or benchmark calls were made for this update.

## Decision

Use **Claude Code headless CLI as the first controlled-study candidate**, **Codex CLI as a second, separate controlled campaign**, and **GitHub-hosted Copilot plus Antigravity IDE for a later native-workflow campaign**. Keep Claude desktop/Projects out of the initial controlled study. Defer OpenCode, Aider, and a custom API coding loop until the measurement path works.

Claude-first is an integration choice: the inspected Loom executor already invokes Claude CLI. It is not evidence that Claude produces better or cheaper code. No runtime is admitted yet. A failed admission gate means defer that profile, not weaken the comparison silently.

## Evidence across all reports

Reported observations are agent-authored evidence unless independently verified below. Historical versions are capture-time values, not claims about today's installed binaries. Each report folder also contains capabilities and evidence files.

| Report / exact surface | Observed or reported evidence | Remaining gap | Decision |
|---|---|---|---|
| [Claude Projects cloud](../runtime-discovery/claude-code/report.md), pre-reset | Hosted coordinator/tool context; report labels runtime 2.1.305 | Complete call lineage, stable context and accounting unproved | Historical discovery; separate native surface |
| [Claude terminal, pre-reset](../runtime-discovery/claude-code-headless/report.md) | CLI 2.1.304; personal rules/skills/MCP; old Loom binary lacked pipeline commands | Contaminated personal state; no headless execution | Historical comparison for cleanup |
| [Claude terminal, post-reset](../runtime-discovery/claude-code-headless/20261021T053558Z/report.md) | CLI 2.1.304, model label sonnet-5/high; configured plugins disabled, MCP list empty; transcript usage IDs | Interactive session, not a headless test; tool exposure and full accounting still unverified | Best evidence for first CLI candidate |
| [Claude desktop via Projects](../runtime-discovery/claude-code-headless/20261021T054718Z/report.md) | Bundled CLI 2.1.304; opus-5-5/medium label; account plugins/connectors loaded despite local settings | Different model/effort and host context; no attributable session USD | Exclude from controlled pilot; optional native extension |
| [Codex desktop discovery](../runtime-discovery/codex-headless/20261021T053548Z/report.md) | Installed CLI 0.163.0; help supports noninteractive execution; config model/effort differs from proof of effective model | Desktop report does not exercise CLI; node_repl enablement ambiguous; child/retry/error accounting unverified | Second CLI campaign candidate |
| [Copilot local VS Code](../runtime-discovery/github-copilot-coding-agent/20261021T065724Z/report.md) | Local SDK/editor surface; version/model/accounting mostly unknown | Not GitHub-hosted Copilot | Retain as distinct evidence; no hosted capability attribution |
| [Copilot GitHub-hosted](../runtime-discovery/github-copilot-coding-agent/20261021T143620Z/report.md) | Linux x86_64 hosted runner; runtime build a3b15b7…; GitHub MCP and platform tools | Model/effort unknown, detailed usage export and billed cost absent, effective gates unverified | Native-workflow candidate; controlled H0 remains unadmitted |
| [Antigravity IDE](../runtime-discovery/antigravity/20261021T053126Z/report.md) and [self-audit](../runtime-discovery/antigravity/20261021T053126Z/audit.md) | Attended IDE 2.5.5; reported model label; agentapi launcher; global plugins/skills; no token metrics found in inspected records | Automated completion/cancellation, full telemetry, cost and backend pinning not established | Native-workflow candidate; cost unknown |

The older Claude [cloud review](../runtime-discovery/claude-code/review-codex.md) and [terminal review](../runtime-discovery/claude-code-headless/review-codex.md) remain relevant. Reports under folders named `headless` are not automatically headless evidence.

## What we independently verified

Copilot PR #1 contained only the three requested report files. Its H0 assessment was corrected to a candidate awaiting validation, and the missing E08 evidence entry was added before merge. [PR #1](https://github.com/orieken/guild-ledger-research/pull/1) merged as `5bfcc7c4c81e35a79295a3236d63bc01661c3098`.

The [corrected collection run](https://github.com/orieken/guild-ledger-research/actions/runs/39621746415) succeeded. Its downloaded manifest identified source PR commit `6db2a1bc89fa3d92a6c59fdd553ed0aabf86e8f9`; all three file hashes and sizes matched. This verifies transport and revision, not the runtime claims. The artifact has 90-day retention and is not permanent storage.

Read-only source inspection reconfirmed Loom checkout HEAD `3a41006238a43bbd0920f3ef108091641b1be00e`: `cmd/loom/cmd/run_providers.go` selects `claude` or `mock`; `internal/provider/claude/claude.go` invokes `claude -p --output-format json`. The working tree is not frozen; a HEAD hash alone does not identify dirty bytes. The global Loom binary was deliberately removed; source remains available. No global reinstall is needed for a future project-local build.

## Why these runtimes

Claude provides a documented noninteractive CLI, and its SDK documents usage and aggregate results. Those features make it a practical first adapter, but their behavior on our account still needs calibration. Reported USD fields are client-side estimates. [Headless interface](https://code.claude.com/docs/en/headless), [usage and estimates](https://code.claude.com/docs/en/agent-sdk/cost-tracking), checked 21 October 2026.

Codex documents noninteractive JSONL events and token usage. This supports a second adapter; it does not establish complete interrupted/child/retry accounting for our installation. [Official noninteractive documentation](https://learn.chatgpt.com/docs/non-interactive-mode), checked 21 October 2026.

GitHub documents Copilot session progress, token usage and session length in its UI. Our file collector does not export those measurements. Treat the hosted report as a useful native-system starting point, not a metered benchmark result. [Managing sessions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents), checked 21 October 2026.

Antigravity's negative telemetry findings are limited to inspected records. Its proposed `$0` probe bound is not established; use unknown. Killing a background command does not prove inference cancellation, and local file persistence does not establish indefinite retention. Its SDK/CLI claims require separate official-source verification before implementation; do not infer IDE capabilities from another interface.

## Campaigns and permissible claims

| Campaign | Initial cells | Claim supported after validation |
|---|---|---|
| A: Claude CLI controlled | P1/P2/P3 × H0/H1/H2; add H3-context only if admitted | Prompt and added-harness effects within a fixed Claude runtime/model/account configuration |
| B: Codex CLI replication | Same prompts and treatments on a separate frozen Codex profile | Whether within-runtime patterns replicate; cross-runtime differences remain complete-system differences |
| C: Native workflows | Start at P3: GitHub-hosted Copilot, Antigravity IDE, Loom native on Claude | Operational quality, elapsed time, human effort, and available costs for complete systems |

H3-context is a reduced Loom-derived treatment, not full Loom. H3-native is a separate native system. If reduced Loom cannot be defined faithfully, A starts with H0–H2 and the four-condition factorial stays blocked. The earlier 108-attempt proposal requires four admitted conditions; three conditions would be 81 attempts for the same 3 tasks × 3 prompts × 3 repetitions. Neither count is authorized or a power calculation. Do not run both H3 profiles under one condition ID.

## Controls and admission

Select the auth mode before live calibration and hold it constant across harnesses. Prefer a separately approved metered API-backed mode for cost attribution. Current subscription discovery does not establish attributable charges. A subscription campaign can report quality/time and measured token equivalents, with billed USD null. No auth change or paid call is authorized by this document.

Record requested and response-reported model labels separately. Pin runtime binary/version/hash and effort where possible; a model alias is not an immutable backend snapshot. If snapshots are unavailable, declare that limit, block/randomize conditions in time, and record dates and observed response labels. This supports bounded reproducibility, not identical backend weights.

Admission requires: a frozen task and input exposure manifest; fresh isolated workspace/state; verified tool/network policy; common task mechanics; correct source snapshot capture; structured usage and completeness flags; timeout/needs-human/error handling; evaluator separation; and zero-model lifecycle fixtures. Separately authorized calibration must then confirm the actual emitted events and accounting. Missing usage is unknown, never zero. Do not omit failed attempts from denominators or infer invoice cost from subscription percentages.

Next implementation and harness decisions are in [harness alignment](13-harness-alignment.md).

## Native Loom mock integration — 22 October 2026

A separate [H3-native-mock profile](18-loom-native-mock-integration.md) is now built and verified from upstream commit `3f2817818c68f42520229aab9342ce91533cef2f` using Go 1.26.5. It preserves native gates and explicitly distinguishes synthetic fixture approvals from autonomous execution. This validates mock mechanics only; the controlled H3-context slot and live Loom admission remain unresolved.

## H4 Harness² addition — 22 October 2026

[Google Research Harness²](19-harness2-adaptive-comparison.md) is registered as an optimizer/treatment family, not a new model or Antigravity runtime. The inspected release has OpenCode/Codex substrates; our implementation currently permits only its deterministic offline demo. Native adaptive streams and a proposed frozen-optimized profile need separate study designs. No additional controlled cells or paid runs are admitted.
