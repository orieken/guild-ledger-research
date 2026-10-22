# Prompt detail × coding harness experiment

Design draft v0.1 · 20 October 2026 · Owner: Oscar Rieken

Status: design only. No paid runs authorized or performed. No results yet.

Update: the [Guild Ledger research pack](research/README.md) develops this proposal into an application specification, repository architecture, worked prompt set, metrics contract, and GitHub Actions/collection plan. Use that newer pack for Guild Ledger-specific scope decisions.

## Research question

How do prompt completeness and agent harness design affect functional correctness, maintainability, reliability, time, and total cost of producing code? Does a harness help most when the prompt leaves decisions unresolved, and does its benefit justify its overhead?

This is an extensible benchmark, with a versioned task corpus, interchangeable harness adapters, an independent evaluator, and an evidence archive that supports a series of posts.

## Starting point and limits of the source experiment

Naresh Jain's [Are Harnesses Worth the Cost?](https://martinfowler.com/articles/are-harnesses-worth-the-cost.html), published on Martin Fowler's site on 13 October 2026, separates development feedback from external evaluation. Its stated limitations include one greenfield service, an unusually detailed brief, ten paired runs per model, bundled guides and sensors, and excluded setup and repair labor. Our design extends those dimensions; it should not be described as a reproduction until the original artifacts and execution configuration are independently inspected.

## Experimental factors

| Factor | Initial levels |
|---|---|
| Prompt | P1 brief; P2 detailed; P3 specification with boundaries and examples |
| Harness | H0 minimal agent; H1 fixed guidelines; H2 our complete harness; H3 Loom |
| Model | One pinned model/configuration in pilot; at least two capability/cost tiers in the main study |
| Task | Multiple greenfield and existing-code tasks |
| Repetition | Independent attempts, with fresh state |

The initial matrix has 12 prompt/harness cells per task and model. The important outcome is the interaction: does the benefit of a harness change with prompt detail? Do not average that interaction away in a single leaderboard.

### Prompt definitions

All variants describe the same underlying task and use one language/stack and the same mechanical launch interface. Length is recorded, but is not the definition of completeness.

* P1: goal and minimum interface, little product detail.
* P2: goal, main behavior, constraints, and important failure cases in prose.
* P3: numbered requirements, explicit exclusions, boundary behavior, acceptance examples, and completion criteria.

Create each variant from a canonical requirement inventory. Map each requirement to explicitly supplied, reasonably inferable, or unspecified for each variant. Freeze this map before runs.

Score two different things: (a) conformance to requirements actually communicated in that condition; (b) satisfaction of the complete intended product. A low P1 product score can reflect missing information rather than poor implementation. Report those separately. Hidden tests must not silently turn an unspecified product choice into a coding defect.

Task examples must be disjoint from hidden evaluation fixtures. A specification can reveal required behavior without revealing the test answers or fixture values.

### Harness definitions

| ID | Definition to freeze before execution |
|---|---|
| H0 | Same base agent runtime, editing/shell tools, dependencies, and visible starter tests; no added project rules, memory, skills, or orchestration |
| H1 | H0 plus one short, fixed guidelines file; no extra task requirements or added tool feedback |
| H2 | Our versioned guidance, planning, visible verification, bounded repair, and completion-evidence workflow |
| H3 | A pinned Loom configuration: exact installed bundles, tools, pipeline, routing, model choices, memory policy, and gate handling |

“No harness” is shorthand for no added behavioral harness. An agent still has runtime instructions, tools, and stopping behavior. Record those rather than claiming a completely unharnessed model.

H1 candidate text: inspect the repository; make a short plan; implement the requested scope; add appropriate tests; run available checks; review the diff; report verification and unresolved assumptions. Freeze exact wording before the pilot.

H2 must be frozen before measuring it. Start with: requirement/assumption inventory → plan → implementation and visible checks → bounded review/repair → evidence summary. Record every model invocation and tool call. It may use the selected prompt and ordinary repository information; it may not read the canonical private specification or hidden suite. Freeze loop bounds and stop criteria in its manifest.

## Two comparison tracks

### A. Controlled comparison

Hold model, reasoning configuration, base runtime where compatible, task information, external access, starter commit, resources, and total spending limits constant. Harnesses may organize work and invoke declared development checks. Those changes are part of the treatment and must be logged.

Do not hand P3's missing requirements to P1 through a harness contract or retrieval corpus. If a harness requires extra task-specific inputs, either derive them only from the supplied prompt, include their generation in cost, or put that configuration in Track B. A framework unsupported on the selected runtime is incompatible, not an excuse for a silent substitution.

### B. Native workflow comparison

Run each framework as intended, including model routing, multiple agents, retrieval, task preparation, and human gates. Measure the entire workflow. Conclusions concern the configured system, not the isolated effect of its harness.

Human-authored specifications, contracts, and examples are inputs with creation cost. Report them explicitly. Do not compare a single-model baseline against a multi-model pipeline and attribute the whole difference to context engineering.

## Loom integration notes

Read-only inspection source: `/Users/oscarrieken/Projects/Rieken/ai-assistant-dot-files`.

Observed HEAD: `3a41006238a43bbd0920f3ef108091641b1be00e`. The checkout was dirty on inspection; this commit alone does not identify its complete current state. Before a run, select a clean commit or archive the intended diff and untracked inputs with hashes.

The root README describes shared agents/rules/skills and platform installs. `cmd/loom/README.md` documents pipeline routing, review loops, human approval gates, run events, and provider-reported usage. `shared/evaluation/README.md` also distinguishes specifications from implemented automation. These are documentation observations, not verified runtime capabilities.

Define H3 precisely before implementation:

* Context-only profile, if supported: selected bundles on the same agent as H0–H2.
* Native pipeline profile: the actual delivery workflow, with its routing and model choices recorded in Track B.
* Cold memory for primary trials. Any bundled knowledge corpus must be frozen and audited for task solutions. Warm/cross-run learning belongs in a separate experiment.
* Preserve gate behavior. An autonomous run stopping for human approval is `needs_human`; do not silently bypass gates. An assisted extension records active human minutes, waiting time, decisions, and edits.
* Missing provider usage is unknown, never zero. Reconcile reported spend and independent usage records where available.

Do not export the user's global configuration, private knowledge, or live service credentials into benchmark workspaces. Use a scoped synthetic configuration. The source repository remains unchanged.

## Task corpus

Use three tasks in the feasibility pilot, all in one stack:

1. Small greenfield API: validation, persistence, pagination, and error behavior.
2. Existing-code bug fix: reproduce a defect and preserve unrelated behavior.
3. Existing-code feature: implement a bounded change across an integration boundary.

Expand to at least six independently scored tasks before making broad claims, including a refactor preserving behavior and a dependency-failure scenario. Add UI/accessibility tasks as a separate stratum with appropriate evaluation.

Every task needs a pinned starter repository, canonical requirement inventory, three prompts, visible smoke tests, private acceptance/regression tests, fixed fixtures, and a reference implementation. Verify that the reference passes and deliberately flawed implementations fail relevant checks. The evaluator must test behavior, not reference-code similarity.

Use synthetic repositories initially to reduce unknown exposure to published solutions. Keep a development task set for harness tuning and a held-out evaluation set. Once a held-out task is used to tune a harness, retire it from confirmatory evaluation.

## Repeatable execution

1. Freeze protocol, prompts, tasks, harnesses, model settings, pricing snapshot, resource limits, and analysis plan into a campaign manifest.
2. Generate the full schedule before execution. Randomize cell order inside task/model/repetition blocks to spread time/provider effects. Store the randomization seed; this does not guarantee deterministic model outputs.
3. Start each attempt in a fresh container/workspace and fresh agent home. Strip inherited project/global instructions, memories, sessions, and plugins. Use a declared dependency-cache policy and record model cache usage separately.
4. Mount only the task, selected prompt, and declared harness assets. Isolate the evaluator and private fixtures outside agent-readable files and tools. Use fixed dependencies and synthetic local services; declare network policy.
5. Apply the same total cost, token/tool, and wall-clock ceilings to controlled cells. Count every spawned agent. A timeout, budget limit, or request for help is an observed outcome.
6. Stop on completion or the predefined limit. Archive the final patch and run independent evaluation once, without returning private failures to the coding agent.
7. Save all outcomes, including failures. Repair after external scoring is a separate, predefined experiment and receives its own cost record.

Infrastructure failures need a predeclared classification and rerun rule. Retain the original attempt; never relabel an agent-caused dependency or configuration failure as infrastructure merely because it is inconvenient. Record evaluator flakes separately and investigate before freezing a corpus.

## Quality measures

Primary outcome: fraction of attempts satisfying every predefined critical acceptance criterion, conditional on the communicated requirement set. Also report full intended-product acceptance separately.

Secondary measures:

* Requirement-level behavior coverage, grouped by feature so many near-duplicate assertions do not dominate.
* Regressions in existing-code tasks.
* Robustness and security checks appropriate to the task, defined in advance.
* Maintainability: blinded review of readability, cohesion, unnecessary complexity, and ease of change using an anchored rubric.
* Agent-written test quality: independent behavior checks or mutation testing where suitable; self-reported pass counts are not quality evidence.
* Completion and intervention rates, stage/repair counts, and time distributions.

Keep these dimensions separate. Avoid an arbitrary single quality number. Use at least two reviewers on a balanced subset, randomize artifact order, hide condition labels where feasible, and report agreement and disagreements. Generated artifacts may reveal a framework's style, so blinding is imperfect. LLM judgments can supplement human review only with a fixed judge configuration and documented bias checks.

## Economics

Save per invocation: model ID, input/output/cache usage, reported charge if available, estimated charge if needed, price source/date, latency, and parent run/stage. Preserve provider-specific usage categories; prevent double counting cached tokens. Track missing data explicitly.

Report per cell:

* Mean/median attempt cost and time, including unsuccessful attempts.
* Observed cost per accepted result = total measured attempt cost / accepted attempts. If none pass, report undefined/no accepted results. This is not a promise about future retry cost.
* Setup/adaptation/maintenance hours, per-run human minutes, compute/tool spend, and independent evaluation cost, each separately.
* End-to-end cost scenarios at stated labor rates and reuse counts: allocated setup cost + recurring generation + evaluation + intervention/repair costs.
* Active runtime and human waiting time separately.

Subscription usage without attributable billing is an API-equivalent estimate, not actual cash spend. Recompute estimates using a frozen price snapshot and retain original measurements. Plot cost against acceptance/quality with uncertainty; avoid declaring a winner from point estimates alone.

## Pilot and analysis plan

Suggested feasibility pilot: 3 prompts × 4 harnesses × 3 tasks × 3 repetitions × 1 model = **108 attempts**. Its job is to detect leakage, broken adapters, scoring ambiguity, ceiling effects, and missing telemetry. It does not establish reliable rankings. Paid execution remains off until separately authorized.

Use pilot variance and the smallest meaningful effect to size the main study. Ten or twenty repetitions are not automatically enough, especially for rare failures or small interactions. Budget the expanded matrix before execution; two models, six tasks, and ten repetitions would already mean 1,440 attempts for four harnesses.

Predeclare primary contrasts (H1/H2/H3 versus H0 within each prompt level), task aggregation weights, exclusions, and stopping rules. Report run counts, denominators, confidence intervals, and per-task results. Treat attempts on the same task as clustered; the task, not each acceptance assertion, is the basis for cross-task generalization. Analyze prompt × harness interaction and model-specific effects. Adjust for multiple exploratory comparisons or label them exploratory. No optional stopping when a favorite configuration pulls ahead.

## Adding GitHub harnesses

Use an adapter registry. A new harness declares source URL, immutable revision, license, configuration/assets hashes, supported runtimes, model policy, commands, tools/network needs, memory policy, gates, retry behavior, setup work, and telemetry mapping. Inspect capabilities and install behavior before running it.

Adapter lifecycle: prepare isolated workspace → launch → collect raw evidence → normalize usage/outcome → clean up. The evaluator consumes only the final artifact and standard launch contract. Harness adapters cannot alter scoring inputs.

Admission checks: no hidden-evaluator access; no stale sessions or solution corpus; all child invocations accounted for; stop limits enforced; missing usage represented; failed runs preserved. Unsupported features are recorded as such. Test adapters with a fake provider/local fixture before spending on models.

Additions become a new campaign version. Run new harnesses against the frozen corpus and rerun contemporaneous baseline cells to detect model/runtime drift. Do not silently mix dates or changed models into one ranking. Future ablations can separate guidance, context retrieval, feedback cadence, and orchestration.

## Evidence and publication

Proposed repository layout:

```text
protocol/          versioned design, decisions, preregistration
tasks/<id>/        starter reference, requirements, prompts, visible tests
private-eval/      separately stored; inaccessible to coding agents
harnesses/<id>/    manifests, adapters, frozen configuration
campaigns/<id>/    immutable schedule and resolved run manifests
runs/<id>/         events, usage, transcript references, patch, evaluation
analysis/          reproducible tables, plots, analysis configuration
posts/             drafts, evidence references, publication checklist
```

Each run records IDs/hashes for campaign, task, prompt, harness, model configuration, starter, evaluator, environment, and price snapshot. Record status, stop reason, timestamps, all invocation usage, human interventions, test results, and artifact locations. Store transcripts securely; publish only reviewed synthetic material and redact credentials. Published redactions need a record so evidence omissions are visible.

Each claim in a post should link to an analysis output and underlying run IDs. Keep a dated decision log: what changed, why, before/after hashes, and whether the change invalidates comparisons. Publish failures and null results, distinguish hypotheses from measurements, and disclose our authorship of Loom and H2. Freeze evaluation before optimizing either.

Proposed series:

1. The question and preregistered experiment: definitions, fairness, budget, hypotheses.
2. Building a trustworthy benchmark: tasks, isolation, scoring, adapter contract.
3. Pilot findings: operational failures and protocol revisions, without broad rankings.
4. Main results: prompt completeness × harness × model, cost and quality with uncertainty.
5. Explaining effects: ablations of guidelines, retrieval, feedback, and orchestration.
6. Extending the comparison: GitHub harnesses, replication, maintenance, and drift.

## Next design decisions

Choose pilot stack and tasks; select the common agent/model configuration; define H2's exact bounded workflow; choose Loom's controlled profile and native profile; decide how assisted gates will be measured; finish the requirement-level scoring rubric. Then build a local zero-cost adapter/evaluator dry run. No model calls are needed to validate scheduling, isolation, artifact capture, and report generation.
