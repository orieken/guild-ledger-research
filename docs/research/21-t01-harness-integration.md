# T01 harness/container integration

The [T01 integration guide](../../containers/t01/README.md) defines the canonical task transport, the common offline test command, native mock adapters, source protection, post-run testing and retained evidence.

This closes the earlier gap where T01 bundles were accepted by H0–H2 but their application tests could not run in workers. All five mock harnesses now have preinstalled visible-test tooling. Loom's optional assigned-prompt transport preserves the pinned profile and native gates. Harness² has a dedicated no-op T01 adapter using the pinned native recursion and selection engine; it remains separate from the upstream ledger/library demo.

The offline Actions workflow now runs packaging/projection checks, original harness regressions and all 15 prompt/harness combinations. An unchanged mock candidate must have green startup/build checks and exactly the expected red feature checks, inside the worker and again after export. A separate positive witness must pass the visible suite. `verification_passed` describes infrastructure only.

Remaining admission work: independent full-target evaluator; criterion-level disclosure freeze; live tool/runtime/model configuration and accounting; model usage calibration; budget and authorization. No paid execution is enabled by this integration.

The mechanical T01 envelope now names the shared test command for all prompt levels. The starter application archive is unchanged. The explicit overlay profile binds mock adapter/tool bytes and is recorded separately from the original H3/H4 package manifests. Local results and source hashes are recorded in `containers/t01/verification.json`; the updated GitHub workflow needs a subsequent push before hosted verification.
