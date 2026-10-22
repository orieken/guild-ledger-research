# Guild Ledger Research

Research comparing prompt completeness and coding-agent harnesses using Guild Ledger, a fantasy adventurers’ guild application.

## Start here

- [Comparison definitions: prompts, harnesses, interaction and native workflows](docs/research/10-comparison-protocol.md)
- [Article review: metrics capture and reporting](docs/research/11-article-metrics-review.md)
- [Runtime comparison, all reports and recommended campaigns](docs/research/12-runtime-options.md)
- [Claude runner containers and offline smoke tests](containers/claude/README.md)
- [Discovery prompt for Claude, Copilot and Antigravity](docs/runtime-discovery/discovery-prompt.md)
- [Harness treatment definitions and implementation order](docs/research/13-harness-alignment.md)
- [Review of Claude’s Projects cloud discovery](docs/runtime-discovery/claude-code/review-codex.md)
- [Review of local Claude CLI/headless discovery](docs/runtime-discovery/claude-code-headless/review-codex.md)
- [Global Loom removal and experiment implications](docs/research/14-global-loom-removal.md)
- [Local Claude/Codex reset and verification](docs/research/15-local-agent-reset.md)

- [Research plan and document index](docs/research/README.md)
- [Critical review and 26 unresolved gaps](docs/research/08-critical-review-and-gaps.md)
- [Experiment diagrams](docs/research/07-system-diagrams.md)
- [Local workspace and separate repositories](docs/research/09-workspace-layout.md)
- [Repository registry](repositories.json)

## Repositories

| Condition | Repository |
|---|---|
| Research, shared tasks, independent evaluation and collection | [guild-ledger-research](https://github.com/orieken/guild-ledger-research) |
| H0: baseline | [guild-ledger-baseline](https://github.com/orieken/guild-ledger-baseline) |
| H1: guidelines | [guild-ledger-guidelines](https://github.com/orieken/guild-ledger-guidelines) |
| H2: custom harness | [guild-ledger-harness](https://github.com/orieken/guild-ledger-harness) |
| H3: Loom | [guild-ledger-loom](https://github.com/orieken/guild-ledger-loom) |

Each repository is a sibling checkout beneath the local `guild-ledger/` workspace parent. Each experiment uses a clean, isolated task workspace rather than access to all siblings.

Status: runtime discovery reports reviewed; the Copilot report collector is implemented and has successfully collected the hosted report merged in PR #1. Claude CLI is the first controlled-study candidate, Codex CLI the second; Copilot and Antigravity are native-workflow candidates. An offline Claude container runner is built and smoke-tested; live generation and the independent evaluator are not implemented, and no paid benchmark/calibration runs are authorized. Planning documentation is draft and profile admission remains open.

Draft schemas and synthetic examples are illustrative contracts, not evidence of measured results. The next step is resolving the protocol decisions and T02 contract gaps before implementing the local measurement path.
