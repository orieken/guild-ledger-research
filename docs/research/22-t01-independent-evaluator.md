# Independent T01 acceptance evaluation

The [T01 evaluator](../../evaluators/T01/README.md) supplies the independent full-target observation path that was missing from the offline harness setup. It uses separately authored API assertions and a real Chromium browser; source projection is shared infrastructure, but visible tests and reference code are not its oracle.

The declared acceptance inventory has 23 critical automated criteria plus protected-input/build gates. Complete evaluations use one fixed denominator across prompt levels. Subset diagnostics cannot return full-target acceptance, and evaluator failures produce an unknown outcome rather than a candidate zero. Communicated conformance remains unavailable until a separate criterion-level exposure audit.

The validation corpus includes a complete reference, the earlier visible-only witness, valid component extraction, accessible button labeling and serialization strategies, an unfinished starter, protected-input/build/evaluator-error controls and 28 predeclared defects. The defect catalog is not loaded by the evaluator. Fixtures are fixed; tie/case ordering branches absent from those fixtures and the documented accessibility/source-review limits remain explicit.

The [GitHub workflow](../../.github/workflows/t01-acceptance-evaluator.yml) validates the evaluator without model calls. The existing 15-cell harness mock action continues to measure infrastructure rather than pretending its unchanged mock candidates satisfy product acceptance. A future run collector can consume `guild-ledger.t01-acceptance/v1` reports alongside the runtime/cost records; no paid runtime has been admitted.

## Published verification — 2026-10-24

Commit `b85c970163fa4f54fcbe0f39a385f5eae5234b41` passed the [independent evaluator workflow](https://github.com/orieken/guild-ledger-research/actions/runs/40101175304). Inspection of the saved `t01-acceptance-40101175304-1` artifact confirmed all 39 validation cases passed: both reference repetitions and the component-refactored reference met all 23 criteria, and all 28 seeded defects failed at their predeclared criterion. Subset defect diagnostics retained a null full-target outcome. Every evaluation reported successful cleanup and zero model calls. The evaluator identity matched the earlier local receipt: `a5bebe1324961c2e85b954843c167838ade4a22e6f426d29c7181c446c30f898`.

The [canonical starter workflow](https://github.com/orieken/guild-ledger-research/actions/runs/40101175347) also passed for that revision. Raw hosted evaluator evidence was downloaded locally under the ignored `ci-acceptance-results/hosted-40101175304/` directory; the workflow artifact is retained for 30 days. The checked-in local verification receipt remains a historical record of the pre-publication validation.

The [offline harness setup regression](https://github.com/orieken/guild-ledger-research/actions/runs/40101175370) passed all 16 recorded build/preparation/test results and all 15 prompt/harness mock combinations (P1–P3 × H0–H4), with zero model calls. These mock results verify integration and the expected unfinished-starter failures; they do not establish generated-code quality. Its artifact was downloaded under `ci-offline-results/hosted-40101175370/`.
