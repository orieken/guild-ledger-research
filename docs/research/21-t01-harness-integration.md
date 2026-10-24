# T01 harness/container integration

The [T01 integration guide](../../containers/t01/README.md) defines the canonical task transport, the common offline test command, native mock adapters, source protection, post-run testing and retained evidence.

This closes the earlier gap where T01 bundles were accepted by H0–H2 but their application tests could not run in workers. All five mock harnesses now have preinstalled visible-test tooling. Loom's optional assigned-prompt transport preserves the pinned profile and native gates. Harness² has a dedicated no-op T01 adapter using the pinned native recursion and selection engine; it remains separate from the upstream ledger/library demo.

The offline Actions workflow now runs packaging/projection checks, original harness regressions and all 15 prompt/harness combinations. An unchanged mock candidate must have green startup/build checks and exactly the expected red feature checks, inside the worker and again after export. A separate positive witness must pass the visible suite. `verification_passed` describes infrastructure only.

Remaining admission work: independent full-target evaluator; criterion-level disclosure freeze; live tool/runtime/model configuration and accounting; model usage calibration; budget and authorization. No paid execution is enabled by this integration.

The mechanical T01 envelope now names the shared test command for all prompt levels. The starter application archive is unchanged. The explicit overlay profile binds mock adapter/tool bytes and is recorded separately from the original H3/H4 package manifests. Local results and source hashes are recorded in `containers/t01/verification.json`; that receipt describes the pre-publication local run.

## Hosted verification — 22 October 2026

The [offline harness action](https://github.com/orieken/guild-ledger-research/actions/runs/39847929663) passed for research commit `5c20e475809e0297a860ff9485dff030e335b10b` on Ubuntu 24.04. The downloaded artifact confirmed all 15 P1–P3 × H0–H4 cells, 21 in-worker visible-test invocations, all green/rejection controls, and unchanged application source in every mock candidate. Native evidence confirmed H2 implementation/review/repair, three explicitly synthetic Loom gate approvals, and Harness² parallel/sequential selection. Both aggregate CI flags (`verification_passed` and `all_suites_passed`) were true.

The separate [canonical starter action](https://github.com/orieken/guild-ledger-research/actions/runs/39847929709) also passed all 16 verification checks for the same commit. Model calls remained disabled; these results establish offline infrastructure and expected-result assertions, not product quality or live runtime admission. Quest feature tests remain intentionally red for the unchanged mock candidates.

GitHub retains the run artifacts for 30 days. A local copy of the full hosted harness artifact is archived under ignored `ci-offline-results/hosted-39847929663/`. The committed local verification receipt remains historical evidence and has not been rewritten as a hosted run.

The subsequent [independent evaluator work](22-t01-independent-evaluator.md) implements the missing full-target automated checks. Its acceptance score remains distinct from the infrastructure-only results recorded above.
