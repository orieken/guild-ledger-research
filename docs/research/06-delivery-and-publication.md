# Delivery, decisions, and publication

## Milestones

| Stage | Deliverable | Completion evidence |
|---|---|---|
| M0: design review | This pack, chosen task scope, agreed repository layout | Decisions recorded; open assumptions assigned |
| M1: benchmark foundation | Canonical starter, T01–T03 task snapshots, reference implementations, visible/private tests | References pass; deliberately flawed variants fail intended criteria |
| M2: contracts and fake runner | Campaign/adapter/event/invocation schemas, local supervisor, fixture provider | Complete/fail/timeout/budget/needs-human records validate without model calls |
| M3: four harness packages | H0/H1/H2 and supported H3 profile | Frozen instructions, no information leakage, fresh state, full usage coverage |
| M4: Actions and collection | Shared pinned orchestration, publisher, pull collector, durable archive | Fake campaign ingests once; retries/missing artifacts/corruption handled |
| M5: pilot freeze | Preregistered manifests, pricing, limits, analysis, schedule | Exact 108-slot schedule; budget authorized separately |
| M6: pilot | Complete evidence and operational report | Every slot accounted for; no premature efficacy ranking |
| M7: main study | Revised frozen protocol and held-out tasks | Sample size and stop rule justified; contemporaneous baselines |
| M8: extensibility | New framework adapter and replication guide | New campaign, same common evaluator, provenance complete |

M1–M4 can be implemented and verified without paid model generation. The user subsequently supplied five GitHub repositories, which have been cloned locally. Credential setup and cloud jobs remain future work; no paid runs have occurred.

## Prompt preparation work

The T02 worked prompts are ready for review but not frozen. After the actual starter exists:

1. Verify all paths, API/client DTOs, and commands in the common envelope.
2. Check the starter and visible tests for requirements disclosed outside prompts.
3. Independently review the requirement exposure matrix and private criteria.
4. Author equivalent P1/P2/P3 sets for T01 and T03.
5. Hash the complete assembled inputs, with injection order and runtime instructions.

Do not improve prompts after seeing a held-out harness fail without versioning the task/protocol and invalidating that comparison. Record improvements from pilot failures as methodology revisions, not hidden cleanup.

## Pilot schedule and spending

Initial proposal remains three tasks, three prompt levels, four harnesses, three repetitions, one model: 108 slots. A compatible controlled H3 profile is required for that exact count. If only Loom native pipeline is available, keep it in a separate profile/campaign rather than mislabeling it controlled.

Before approving spend, use a small separately authorized metering calibration to estimate attempt distributions, then choose per-attempt and campaign ceilings with explicit failure reserves. No calibration model calls are currently authorized. The local dry run uses synthetic usage and must never be included as real results.

Record total cap, slot caps, concurrency, shutdown behavior, price basis, and maximum allowed in-flight overshoot. CI runtime/storage costs are budgeted separately from model costs. No branch push or ordinary PR should trigger paid runs automatically.

## Decision log

| ID | Date | Decision or proposal | Status / effect |
|---|---|---|---|
| D01 | 2026-10-20 | Guild Ledger fantasy guild domain | User accepted |
| D02 | 2026-10-20 | Vue/TypeScript, Python, Go, PostgreSQL; REST first | Proposed stack; exact versions unresolved |
| D03 | 2026-10-20 | Four thin harness repos and central research repo | Proposed here; no repositories created |
| D04 | 2026-10-20 | Independent evaluator and immutable shared task bundles | Research validity requirement |
| D05 | 2026-10-20 | Runtime usage capture; Actions publication; research pull ingestion | Proposed implementation architecture |
| D06 | 2026-10-20 | Design-only, no paid runs | User instruction in force |
| D07 | 2026-10-20 | Task ladder rather than rebuilding full app every attempt | Proposed cost/attribution control |
| D08 | 2026-10-20 | Separate communicated conformance from full product fit | Proposed scoring protocol |
| D09 | 2026-10-20 | Cancellation and ambiguous failure recovery follow T02 | Proposed explicit scope boundary |
| D10 | 2026-10-20 | User supplied five GitHub repositories; cloned as sibling checkouts | Local setup completed; docs copied into research repo; no commits or pushes |
| D11 | 2026-10-20 | Define C1 prompt, C2 harness, C3 interaction, C4 native workflow comparisons | Working definitions drafted in 10-comparison-protocol.md; campaign remains unfrozen |

Future entries include reason, author, timestamp, artifact hashes before/after, affected campaigns, and whether results remain comparable. Protocol corrections never overwrite prior raw records.

## Open decisions

| Choice | Recommended starting point |
|---|---|
| GitHub owner and visibility | User-selected owner; private research and treatment repos initially |
| Runtime/model | One common pinned configuration for controlled comparisons; verify Loom compatibility first |
| Loom scope | Context profile controlled if supported; full native pipeline separately |
| Task versions | Pilot T01/T02/T03; cancellations/reconciliation in later tasks |
| Human clarification | No live answers in primary track; recorded needs-human outcomes |
| H2 verification | Same tools as other controlled cells; mandatory bounded workflow, max two review rounds |
| Review effort | Balanced blinded subset with two reviewers; account for labor |
| Storage | Durable research archive plus Actions transport artifacts; retention chosen before cloud runs |
| Publication | Methods first; pilot operational findings; main results only after protocol freeze |

## Research post series

1. **What does a harness buy?** Hypotheses, fair comparisons, prompt-information confounding, disclosure of our Loom authorship.
2. **Building Guild Ledger as a benchmark.** Product invariants, canonical tasks, independent evaluation, flawed-variant sensitivity checks.
3. **Measuring the whole attempt.** Usage instrumentation, failures, setup/human effort, CI publication and ingestion.
4. **What the pilot broke.** Missing telemetry, leakage, flaky checks, ceiling effects, and protocol changes. No broad rankings from a feasibility sample.
5. **Prompt detail versus harness behavior.** Main-study results by task/model/profile with intervals and all denominators.
6. **Why results differ.** Ablations for guidelines, retrieval, feedback cadence, review loops, and native orchestration.
7. **Adding another framework.** GitHub adapter, replication, version drift, maintenance cost, contemporaneous baseline.

Each post has a claim ledger: claim text → analysis version and dataset hash → campaign/attempt IDs → raw evidence references. Label observations, interpretations, and hypotheses separately. Keep failure examples and null results. Publish reviewed synthetic inputs, prompts, frozen configuration, rubric, analysis, and reproducibility instructions; withhold credentials and active private test answers until their evaluation role ends.

## Local documentation verification

Before delivery: parse all JSON, check the JSON Schema, validate the synthetic example, verify relative links, inspect requirement IDs and scope consistency, and confirm that no document suggests models or cloud workflows already ran. Future executable adapters need meaningful tests; these documents do not establish their behavior.
