# GitHub Copilot runtime discovery

Captured: 2026-10-21T06:57:24Z. This is a runtime discovery, not a benchmark. No additional model/cloud task, benchmark, install, settings/CI change, commit, push, or merge was performed. This documentation task itself used normal platform processing; its cost is unknown.

## Identity and boundary

**Observed [E01,E02,E03]:** The active surface is identified by the runtime as **Copilot SDK in VS Code**. This is an interactive assistant session with tools, not GitHub.com Copilot cloud agent. It operated on the local checkout `/Users/oscarrieken/Projects/Rieken/guild-ledger/guild-ledger-research`. The shell reported macOS 26.6.2, Darwin 25.6.0, arm64. The session metadata exposed a start timestamp and current working directory.

**Unknown [E01,E04]:** No product/build version, executable identity, selected model label, backend model/revision, inference region, reasoning setting, or immutable model pin was available from the session metadata or read-only checks performed. The environment's identity label does not prove a particular backend or fixed revision. This report does not identify the runtime as GitHub-hosted Copilot cloud agent.

## Starting, running, and collecting a task

**Observed [E01,E02,E05]:** This task arrived as a user prompt in the active conversation. The exposed session metadata included `createdAt`, working directory, a session URI, and a status; the status was `inProgress` when checked. The workspace is an existing local checkout. Reading and writing workspace files, shell checks, and web lookup are available in this session. The specific repository had no valid local `HEAD`; its contents were already untracked.

**Unknown [E04,E05]:** There is no observed public task-submission API, fresh-task/reset API, task queue, external progress endpoint, cancellation control, or general artifact-export endpoint for this exact surface. Progress is visible through the conversation/tool interaction, not a verified task telemetry API. Cancellation and partial-artifact behavior were not tested. Changed files can be read from the local workspace; the host did not provide a tested patch/export bundle. No GitHub Actions job, cloud checkout, repository setup workflow, or task-specific setup step was observed in this run.

**Documented, different surface [D01-D04]:** GitHub's documentation describes Copilot cloud agent as a GitHub.com experience that works in an ephemeral development environment, uses GitHub Actions for environment setup, can show session logs/progress, and can stop sessions while preserving commits already pushed. These statements describe GitHub-hosted cloud agent and must not be transferred to this local Copilot SDK session.

## Instructions, state, tools, and controls

- **Observed [E06]:** A bounded search of the research checkout found no `AGENTS.md`, `.github/copilot-instructions.md`, `*.instructions.md`, `*.agent.md`, or `*.prompt.md` files. The project README and the user-provided discovery prompt were read. This does not inventory files outside the checkout or prove which content was injected into the model context.
- **Unknown [E01,E06]:** Mandatory platform instruction contents, organization-level instructions/policies, model-side context, memory state, context compaction, hooks, and effective instruction precedence are not exportable from this session. No hidden prompt, private reasoning, credential, memory store, or unrelated log was inspected or included.
- **Observed [E01]:** A skill catalog is exposed to the assistant. No skill or subagent was invoked for this discovery. A listed capability is not proof it was executed.
- **Observed [E02,E05]:** Read-only shell, GitHub repository metadata, and official documentation retrieval succeeded. The available environment also exposes file-view/edit operations. No network policy or complete permission manifest was provided. A successful web lookup does not establish arbitrary shell network access.
- **Observed [E05]:** No approval prompt appeared during the bounded read-only checks. This is not evidence that all writes, commands, external actions, or future tasks are ungated. No general human approval policy was observable.

## Usage, timing, cost, and retention

**Observed [E01,E05]:** Session metadata provided the session start time. Tool invocations and their returned results were visible in the live interaction. No provider usage record or downloadable raw event stream was available through the checks used here. This report does not copy an internal session URI.

**Unknown [E04,E05]:** Input/output tokens, cache tokens, reasoning tokens, per-request IDs, child/reviewer model calls, retries, tool-event export, per-call timestamps, error accounting, interruption accounting, account/billing mode, credits or premium requests, and attributable USD were not available. No measured dollar estimate is supplied. Actions compute was not observed or used; its charge is not part of any amount here. Do not treat missing usage or cost as zero.

**Unknown [E04]:** Session retention, deletion, export, and ownership controls for this exact runtime are not established. The current local documentation files are retrievable from the checkout. The broader retention behavior of the chat and provider records remains outside this task's evidence.

## H0-H3 feasibility for this exact surface

These are feasibility judgments, not demonstrated treatment runs. Here “support” means more than being able to place text in a file: a controlled condition also needs stable task inputs, repeatable session setup, and sufficient measurement to verify exposure.

| Condition | Status | Assessment |
|---|---|---|
| **H0 baseline** | Inferred [E01,E04,E06] | A baseline could omit experimental harness additions, but cannot be called instruction-free: mandatory platform instructions and runtime context remain. Clean session/context reset, fixed model identity, and comparable starting state are unverified. |
| **H1 fixed guidelines** | Inferred [E02,E06,D05] | A guideline document can be placed in a repository and this surface can read workspace files. There is no evidence that an H1 file is automatically loaded, or that exposure can be verified and held constant across new tasks. |
| **H2 custom bounded workflow** | Inferred [E01,E05] | A bounded sequence can be requested in a prompt and carried out manually with available tools. No native orchestrator, hard call/time/spend enforcement, or reliable event accounting was observed; enforcement would need an external controller and separate verification. |
| **H3 Loom** | Unknown [E01,E04] | No Loom-native runtime, selector, or invocation was observed or tested. Instructions/context mentioning Loom would not prove native Loom execution. A compatible Loom profile is not established. |

**Conclusion:** This surface is not currently validated as an executable H0-H3 benchmark harness. A future controlled trial would need explicit approval, a fresh isolated checkout/session per attempt, an identified and pinned model/runtime where possible, an exposure manifest, external limits, complete artifact snapshots, and authorized usage/billing export.

## Repository and review-flow limitation

**Observed [E07]:** The intended checkout is linked to `orieken/guild-ledger-research`, but GitHub reported no default branch name; `git ls-remote --symref origin HEAD` returned no refs (exit 0). The local checkout reports no commits on `main` and pre-existing untracked `README.md`, `docs/`, and `repositories.json`. Therefore, a normal PR with a base branch cannot be created now. The three new discovery documents are left uncommitted; no pre-existing files were staged or altered. Create/establish a reviewed default branch first, then submit these three files on a topic branch.

## Reproduction / verification

The read-only checks and their outcomes are recorded in [evidence.md](./evidence.md). Validate the JSON from the repository root with:

```sh
python3 -m json.tool docs/runtime-discovery/github-copilot-coding-agent/20261021T065724Z/capabilities.json
```

No second model run is required for this documentation. If a later study needs empirical H0-H3 feasibility or usage data, use the bounded, approval-gated probes in the open questions in `capabilities.json`; do not infer those results from these documents.

## Three largest gaps

1. **Runtime/model reproducibility:** version, effective model, backend revision, and clean task/session isolation are unknown.
2. **Usage lineage:** per-request token/cache/reasoning detail, request IDs, child calls, retries, failures, and tool-event export are unavailable.
3. **Cost and control:** attributable USD/credits and task cancellation/partial-result/retention guarantees are unknown; no enforced budget or complete human-gate policy was observed.
