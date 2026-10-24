# Independent T01 acceptance evaluation

The [T01 evaluator](../../evaluators/T01/README.md) supplies the independent full-target observation path that was missing from the offline harness setup. It uses separately authored API assertions and a real Chromium browser; source projection is shared infrastructure, but visible tests and reference code are not its oracle.

The declared acceptance inventory has 23 critical automated criteria plus protected-input/build gates. Complete evaluations use one fixed denominator across prompt levels. Subset diagnostics cannot return full-target acceptance, and evaluator failures produce an unknown outcome rather than a candidate zero. Communicated conformance remains unavailable until a separate criterion-level exposure audit.

The validation corpus includes a complete reference, the earlier visible-only witness, valid component extraction, accessible button labeling and serialization strategies, an unfinished starter, protected-input/build/evaluator-error controls and 28 predeclared defects. The defect catalog is not loaded by the evaluator. Fixtures are fixed; tie/case ordering branches absent from those fixtures and the documented accessibility/source-review limits remain explicit.

The [GitHub workflow](../../.github/workflows/t01-acceptance-evaluator.yml) validates the evaluator without model calls. The existing 15-cell harness mock action continues to measure infrastructure rather than pretending its unchanged mock candidates satisfy product acceptance. A future run collector can consume `guild-ledger.t01-acceptance/v1` reports alongside the runtime/cost records; no paid runtime has been admitted.
