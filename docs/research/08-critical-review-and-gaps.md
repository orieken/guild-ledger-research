# Critical review and missing parts

Review date: 20 October 2026. Scope: the current local research pack, worked prompts, metrics schema, and synthetic example. This is a design audit, not experimental evidence about any harness. No paid calls or cloud changes were made.

## Follow-up

[Comparison definitions C1–C4](10-comparison-protocol.md) now specify the questions, endpoint priority, treatment boundaries, and contrast hierarchy. G01 is addressed at working-definition level. G02–G06 have concrete proposed controls but still require prompt edits and runtime/profile validation. The audit findings below remain the review baseline; they are not all closed.

## Verdict

The pack has a useful structure, but it is not yet an executable or preregistered research protocol. Its strongest pieces are immutable shared inputs, separate development/evaluation boundaries, preservation of failures, and explicit cost provenance. The largest remaining risks are weak treatment separation, an unclear headline claim, a narrow author-built task corpus, and unimplemented contracts beneath the workflow diagrams.

“Missing” below distinguishes a decision not yet made, a specification conflict, a planned implementation not yet built, and a later extension. Existing docs already acknowledge many implementation gaps; this review does not present them as newly discovered defects.

Priority: **P0** blocks interpretable paid comparisons; **P1** must be resolved before a larger campaign or credible publication; **P2** is a useful extension. Owners below are roles to assign, not additional agents or people already engaged.

## A. Research design and claims

### G01 · P0 · The principal claim and estimand are not fixed

**Evidence:** [prompt protocol](03-prompt-protocol.md) asks about prompt completeness and harness interaction; [metrics](04-metrics-and-reporting.md) makes communicated conformance the primary endpoint; [repository plan](02-repositories-and-isolation.md) also permits native system comparisons.

**Why it matters:** These answer different questions. A P1 pass rate against five communicated criteria and a P3 rate against seventeen criteria are not directly comparable quality measures. Native model routing adds another treatment dimension.

**Close it:** Preregister three named questions: (A) harness effect within a fixed prompt/model; (B) effect of disclosed requirements on a fixed full-target outcome; (C) end-to-end system cost/quality in native workflows. Define population, unit, outcome, contrast, and claim limits for each. Use communicated conformance as the implementation diagnostic and full-target fit for cross-prompt comparisons. Owner: research design.

### G02 · P0 · H0 and H1 overlap before the treatment starts

**Evidence:** The [common envelope](prompts/T02/00-shared-envelope.md) already requires preserving behavior, recording assumptions, reporting changed files, checks, results, and limitations. H1 repeats several of these. P2 also explicitly asks for tests and verification.

**Why it matters:** A null H1 effect could mean the guidelines were already supplied to H0. The baseline is a configured coding agent, not a raw model, and its default behavior may already include planning/review.

**Close it:** Define baseline as “no added harness,” inventory base runtime behavior, and publish the full assembled inputs. Make the common envelope mechanical; obtain reporting evidence through instrumentation where possible. Put task-independent process instructions only in the assigned treatment. Keep remaining prompt-specific process wording deliberate and label it. Owner: protocol/harness implementation.

### G03 · P0 · Prompt levels bundle information, structure, examples, and workflow instructions

**Evidence:** P3 adds exact semantics, examples, error mappings, test guidance, and formatting at once. P1 lacks all of those.

**Why it matters:** The experiment can measure a completeness package, but cannot establish that prose length, writing quality, examples, or specification format caused the result. One wording per level can also make a result specific to that wording.

**Close it:** Name the first treatment “requirement completeness,” remove incidental workflow differences where feasible, and freeze the disclosure inventory. Later add information-equivalent prose/spec and with/without-example ablations, or a small predeclared set of prompt paraphrases. Do not expand the pilot into every ablation. Owner: prompt authoring/research design.

### G04 · P0 · Full information exposure is not audited

**Evidence:** The disclosure table concerns prompt text. The envelope already provides an idempotency header, atomic reservation API, and replay/conflict behavior in the Go dependency. Existing DTOs, tests, source, helper names, and seeded examples may reveal more.

**Why it matters:** A supposedly unspecified behavior may be discoverable, weakening the intended separation. A harness retrieval corpus may contain task-specific solutions.

**Close it:** Make a machine-readable requirement-to-input map covering prompts, starter code, tests, contracts, and retrieval assets. Have an independent reviewer classify exposure before freeze. Prohibit the full research repo and prior outputs in generation. Record runtime instructions that cannot be fully inspected as a limitation. Owner: task/evaluation design.

### G05 · P0 · Harness configurations and runtime compatibility remain hypothetical

**Evidence:** H2 is a proposed workflow; H3 has not been exercised; the common runtime/model is TBD. The 108-slot count assumes a compatible controlled Loom profile.

**Why it matters:** A framework running a different model mix, tool catalog, memory corpus, or human-gated pipeline is not the same controlled treatment. A nominal “controlled Loom” may omit the mechanisms that make Loom useful.

**Close it:** Build a capability matrix: runtime/model support, context tools, reviewers, budgets, usage capture, memory, and gates. Freeze exact profiles. Do not force unsupported controlled profiles; keep native workflows in their own campaign. Explain what is included/excluded from each framework's treatment. Owner: harness integration.

### G06 · P1 · Equal resources and practical economics need separate views

**Evidence:** The plan proposes shared spend, token/tool, and time ceilings, but none are chosen. H2 has extra review steps and native workflows may use multiple models.

**Why it matters:** A tight time ceiling can exclude a high-quality but slower system; a large budget can conceal inefficiency. Simultaneously restrictive ceilings change which mechanism stops each harness.

**Close it:** Declare a primary operating constraint, with other ceilings as guardrails. Report the binding stop reason. Add quality-versus-cost/time curves at selected budgets later, without privately extending failed runs. Use the same total accounting boundary for child calls. Owner: protocol/operations.

### G07 · P0 · The corpus does not yet support broad language or harness claims

**Evidence:** Three pilot tasks share one authored product. T02 keeps Go correct and fixed; T03 tests a Go defect. T01/T03 prompt sets are not written.

**Why it matters:** Language, task type, and difficulty are entangled. Results cannot establish Python-versus-Go differences or general harness superiority. Three repetitions per cell are suitable for mechanics, not a reliable ranking.

**Close it:** Limit pilot claims explicitly. Implement independent task snapshots and difficulty checks. For main-study breadth, add tasks from more than one domain, multiple tasks per relevant category/language, and held-out tasks selected before tuning. Separate paired language implementations would be needed for language-effect claims. Owner: benchmark/research design.

### G08 · P1 · Author advantage and independent review are not operationalized

**Evidence:** We author the benchmark and H2, and the user authors Loom. Disclosure is planned, but no independent adjudication process or harness-tuning budget is set.

**Why it matters:** Tasks, severity labels, allowed dependencies, and exclusions can unintentionally favor familiar frameworks. Disclosure alone does not prevent that.

**Close it:** Assign independent review of task expectations, prompt exposure, scorer sensitivity, and representative outputs. Give new harnesses the same documented setup/tuning opportunity on development tasks. Freeze evaluation before optimizing H2/H3; retain all tuning history. Owner: research governance.

## B. Application and evaluator contracts

### G09 · P0 · T02 restart scope contradicts itself

**Evidence:** The [application spec](01-application-spec.md) says “process restarts belong to T05,” then requires persisted successful idempotency across application restarts. P3 also explicitly requires successful replay after restart.

**Why it matters:** A scorer could demand either ordinary persistence or full interrupted-operation recovery without agreement.

**Close it:** State that T02 covers orderly restart after a completed success; T05 covers crashes/restarts during an operation and uncertain remote outcomes. Update canonical requirements, prompts, and tests together. Owner: product/evaluation design.

### G10 · P0 · Expedition lifecycle and failure cleanup are underspecified

**Evidence:** States pending/accepted/cancelling are referenced, but no authoritative state-transition contract exists. Stock failure forbids an accepted expedition yet does not explicitly resolve a pending record. T02 excludes ambiguous failures but successful Go reservation followed by a Python database failure is still possible.

**Why it matters:** A party may remain permanently busy, reservations may be orphaned, or a hidden evaluator may demand an unannounced recovery architecture.

**Close it:** Specify allowed states/transitions, which errors create rows, and cleanup/retry invariants. For T02, either explicitly constrain fault injection to definitive pre-write failures and classify untested windows, or include a recovery requirement and the necessary APIs. Do not imply distributed consistency is covered merely because the happy path passes. Owner: product/service design.

### G11 · P0 · Idempotency is defined only for the easy terminal case

**Evidence:** Completed replay and changed-payload conflicts are described; key handling after validation failure, insufficient stock, downstream unavailability, concurrent in-progress requests, and failed persistence is not complete. UI retry key behavior is also unspecified.

**Why it matters:** Retrying can either allocate twice or remain stuck forever. Two correct-looking implementations may disagree about whether failed requests consume keys.

**Close it:** Add a request/key state table: new, in progress, accepted, definitively rejected, retryable failure. Define key scope/lifetime, response for concurrent same-key calls, replay persistence, when a UI reuses/regenerates a key, and payload normalization. Specify a permitted implementation-neutral behavior per task. Owner: API/evaluation design.

### G12 · P0 · Interface details are still prose placeholders

**Evidence:** Client DTOs, OpenAPI, seed contract, migrations, `make` commands, statuses, and launch paths are promised but not implemented. “Explicit finite timeout” has no agreed value/bound. P3's ID-existence precedence may require an item lookup before a replay, but the listed Go API has no independent lookup contract.

**Why it matters:** The evaluator could enforce details that the assigned inputs did not communicate, or agents could lack an interface needed to satisfy the ordering.

**Close it:** Publish validated agent-visible API/schema and environment contracts; distinguish wire shape from optional product semantics. Specify ID/quantity representation, validation/coercion, error precedence, timeout configuration, health readiness, migration/reset behavior, and the actual dependency client surface. Check replay behavior against lookup/availability rules. Owner: service/starter implementation.

### G13 · P0 · No executable independent scorer or sensitivity evidence exists

**Evidence:** Private tests, reference passes, faulty variants, browser checks, bounded database probes, and deterministic concurrency tests are all planned.

**Why it matters:** Test counts do not establish coverage or correctness. A brittle scorer can reward hardcoded fixtures, punish equivalent correct implementations, or double-count one root cause.

**Close it:** Build the criterion registry with inputs, observations, severity, exposure, and task applicability. Validate a reference plus deliberately flawed variants. Add alternate fixture values, boundary cases, and metamorphic/property checks where appropriate. Use external concurrency coordination and record test reliability. Require a scorer version and test-review signoff before paid comparison. Owner: evaluator implementation.

### G14 · P1 · Quality breadth and weighting are unresolved

**Evidence:** Most critical T02 criteria concern backend behavior. R18 exact error mappings can overlap other failures; accessibility is non-critical. Maintainability uses broad 1–5 anchors and hypothetical ease-of-change judgments.

**Why it matters:** The benchmark may reward detailed HTTP compliance while making weak claims about “code quality” or usable web applications. An all-or-nothing endpoint can hide large partial differences.

**Close it:** Separate behavioral correctness, robustness, UI usability/accessibility, security scope, and maintainability. Justify criticality, show requirement-level results, group dependent failures, and avoid counting a root defect repeatedly as independent evidence. Define per-dimension rubric examples and review selection. Add an empirical follow-up change task to measure maintainability when budget permits. Owner: evaluation/review design.

## C. Metrics and analysis

### G15 · P0 · Reporting schemas and semantic validator are incomplete

**Evidence:** Only a summary schema exists; the contract notes explicitly defer semantic checks and invocation/event/campaign/evidence schemas. Direct local probes confirmed that the summary shape schema accepts: needs-human with autonomous acceptance=true; passed=99 with total=17; comparison cost differing from estimate; and invalid integrity with acceptance=true.

**Why it matters:** Shape-valid JSON can still corrupt success rates, costs, and denominators. This is an acknowledged implementation gap, not a claim that the schema promised to enforce arithmetic.

**Close it:** Implement and test the semantic validator and all referenced schemas. Extend the data model for native model mixtures, review/intervention records, stage/child lineage, limits and overshoot, partial evaluation results, and inclusion reasons. Require agreement with supervisor/evaluator evidence, not just field consistency. Owner: telemetry/collector implementation.

### G16 · P0 · Attribution of paid usage is not demonstrated

**Evidence:** Runtime/provider capture is proposed, but no selected runtime, adapter trace, child-call reconciliation, failed-call behavior, or billing completeness check exists.

**Why it matters:** Costs can exclude retries, context compaction, reviewer calls, cache charges, or calls made outside the metered route. A fake-provider dry run validates plumbing, not real provider metering.

**Close it:** Define per-invocation IDs and parent/stage lineage; retain raw usage and category mapping; distinguish reused cached context from repeated input; account for errors and charged retries. After separate spending authorization, run a tiny real metering calibration before any comparative pilot. Report provider/runtime usage as measured or estimated according to evidence. Owner: runtime/telemetry implementation.

### G17 · P1 · Recurring product cost and benchmark construction cost are mixed in scenarios

**Evidence:** Setup, adaptation, evaluation, maintenance, human work, and reuse are named, but allocation boundaries and units of “successful result” are not fixed.

**Why it matters:** Authoring benchmark-only private tests is not the same cost as maintaining product contracts; a passed bounded change is not a whole delivered application. Shared evaluation work should not be attributed to only one harness.

**Close it:** Define the success unit per task. Keep research-only cost, common product setup, harness-specific setup, recurring generation/verification, and human repair separate. Publish cost scenarios and reuse horizons with identical allocation rules. Distinguish actual bill, API-equivalent estimate, and labor assumptions. Owner: economics/analysis design.

### G18 · P0 · Exclusion, replacement, and missingness rules remain deferred

**Evidence:** The docs require a preregistered infrastructure retry rule and expected-slot ledger but do not define either.

**Why it matters:** Agent-caused launch failures can be relabeled infrastructure, repeated attempts can replace bad outcomes, and missing telemetry may correlate with expensive failures. Valid generation failure may prove autonomous failure even if independent evaluation is missing; partial functional results can still be informative.

**Close it:** Specify observable classifications, who adjudicates, maximum replacements, lineage, analytical selection, and all-execution cost reporting. Separate known autonomous non-completion from unknown artifact quality. Define resumptions versus new attempts and handling of partial evaluator results. Freeze these rules before observing comparative outcomes. Owner: protocol/operations.

### G19 · P1 · The statistical analysis is a checklist, not an analysis plan

**Evidence:** Intervals, clustering, interactions, task weighting, multiplicity, and power are mentioned without selected methods, contrasts, effect sizes, or thresholds.

**Why it matters:** Many comparisons create opportunities for selective interpretation, while three similar tasks do not establish generalization. Run repetition does not create independent product domains.

**Close it:** Name primary contrasts and aggregation weights, meaningful effect sizes, uncertainty method and assumptions, missingness sensitivity, and sample-size rationale. Analyze task/model/profile strata. Predefine how cost-versus-quality tradeoffs will be reported without inventing a single winner. The feasibility pilot need only report operational completeness and descriptive results. Owner: research analysis.

## D. Execution, collection, and publication

### G20 · P0 · The isolation boundary has no implemented threat model or acceptance test

**Evidence:** Generation, subject execution, evaluation, and publishing boundaries are diagrammed, but worker technology, filesystem/network restrictions, credential routing, and test-source separation are not implemented.

**Why it matters:** A private repository or Docker job alone does not prove that code cannot read tests, mutate evidence, or reach host credentials. Evidence can be internally consistent yet originate from an untrusted process.

**Close it:** Document which process/identity can read/write each asset and access each network destination. Use external trusted telemetry, isolated subject execution, fresh state, and clean publication. Prove evaluator files and trusted evidence cannot be modified by agents or generated applications. Owner: execution infrastructure.

### G21 · P1 · End-to-end orchestration and recovery contracts are missing

**Evidence:** Workflow names exist as a plan, but the adapter lifecycle is not an API with arguments, exit codes, stop messages, checkpoint format, or cleanup guarantees. Collection has no implemented cursor/backfill or slot lease.

**Why it matters:** Duplicate dispatch, abandoned jobs, artifact expiration, rate limits, late completion, and a collector restart can lose or double-count observations.

**Close it:** Specify a campaign/slot ledger with exclusive claims, idempotent dispatch, leases/timeouts, cancellation propagation, and reconciliation. Define artifact handoff, polling/backoff, retention margin, restore procedure, schema migration, and duplicate/conflict handling. Keep source/control identities separate from data files. Owner: orchestration/collector implementation.

### G22 · P1 · Reproducibility depends on mutable external state

**Evidence:** Hashing is planned, but versions, dependency cache behavior, package availability, provider aliases, hardware, locale/timezone, database settings, browser versions, and clock policy remain unresolved.

**Why it matters:** “Same model name” or “same branch” may not mean the same environment. Provider nondeterminism is not eliminated by a schedule seed.

**Close it:** Resolve immutable versions/digests, cache/network policy, database isolation and seeds, CPU/memory architecture, locale, clocks, and runner image. Record backend/model revision when available and acknowledge opaque updates. Randomize across time, rerun contemporaneous baselines for later harnesses, and test cold/ordinary-cache scenarios only if predeclared. Owner: environment/reproducibility.

### G23 · P1 · Human-gated systems lack an assisted comparison protocol

**Evidence:** The primary track stops on required approval; native workflows can include gates, and assisted operation is only described at a high level.

**Why it matters:** Ranking a deliberately human-gated system by autonomous completion mostly measures gate policy. Turning gates off changes the system. Giving it unrecorded human help changes the comparison.

**Close it:** Retain autonomous needs-human results, but avoid treating them as a general quality verdict. Define a separate assisted protocol: permitted decisions/edits, response script, participant experience, active time, waiting time, disagreement handling, and repair budget. No bypassing a framework's real gates. Owner: research/human workflow design.

### G24 · P1 · Licensing, release, and reproducibility policy are not executable decisions

**Evidence:** External harness licenses, reviewed transcripts, and dataset publication are mentioned, but no artifact-level release inventory or test-retirement policy exists.

**Why it matters:** Publishing prompt corpora, framework assets, generated source, and evaluation answers can require different attribution and can contaminate later held-out trials.

**Close it:** Record provenance/license/attribution for each distributed asset, use synthetic fixtures, choose data/code licenses, set retention/redaction rules, and identify what can be released when. Separate released demonstration tasks from active held-out tasks; retire or rotate tasks after solution publication. State limits of independent replication when model internals or prompts are unavailable. Owner: publication/data governance.

### G25 · P1 · Ownership, sequencing, and an operational exit gate are missing

**Evidence:** Milestones are listed, but no owner assignments, effort estimates, dependency graph, or concrete local acceptance package exist. 108 attempts is the first fully counted campaign.

**Why it matters:** We could build five repositories and multiple workflows before discovering that the evaluator or chosen runtime cannot support the comparison.

**Close it:** Build one local task end-to-end first. Assign roles and deliverable checklists, then add repo automation. Use milestone evidence instead of a calendar promise. Treat a four-condition single-prompt calibration as an integration check, not research results, and keep all real calls subject to separate budget authorization. Owner: project delivery.

### G26 · P2 · Mechanism explanations and long-term usefulness need follow-up studies

**Evidence:** Ablations, warm memory, additional frameworks, long tasks, and maintenance are deferred.

**Why it matters:** A successful whole harness does not establish which component helped, whether it generalizes to evolving repositories, or whether setup amortizes in practice.

**Close it later:** Guidance-only versus feedback, review cadence, context retrieval, warm versus cold memory, equal-information prompt formats, post-evaluation repair, follow-up modifications, and measured setup reuse. Keep these out of the initial feasibility matrix unless they address a blocking ambiguity.

## Suggested order of work

1. **Resolve the experiment:** G01–G05. Write one page naming the claims and exact treatment differences. Decide which Loom comparison is actually supported.
2. **Make T02 internally consistent:** G09–G12. Freeze lifecycle, replay/failure semantics, and mechanical interfaces; then revise all three prompts and exposure mapping together.
3. **Build a trustworthy local measurement path:** G13, G15, G18, G20. One reference and one faulty subject through fake generation, independent scoring, semantic validation, and duplicate-safe collection.
4. **Calibrate task difficulty and real metering:** G07 and G16. Complete zero-model checks first; request a concrete, bounded spending authorization only when real calibration is ready.
5. **Add the remaining harnesses and cloud automation:** G06, G21–G23, G25. Preserve identical task inputs and explicit profiles.
6. **Freeze the comparative study:** G08, G14, G17, G19, G24. Approve analysis, allocation, review, and publication rules before collecting ranking data.

## What not to infer from this review

Four harness repositories are not themselves the main validity problem; benchmark drift is controlled by shared immutable task/evaluator versions. GitHub Actions is a workable orchestration/reporting location; it does not supply metering, isolation, or experimental design automatically. The schema passing its synthetic example established format compatibility, not trustworthy scientific measurement. The current diagrams explain intent, not tested infrastructure.

## Next concrete artifact

Produce a **protocol decision sheet and T02 contract revision** before implementing repository workflows. That sheet should settle the primary claim, H0/H1 separation, supported Loom profile, task failure scope, request/key state table, and autonomous/assisted outcome rules. Keep unresolved work visible rather than silently treating this review's recommendations as approved protocol changes.
