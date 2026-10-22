# Source review: metrics capture

20 October 2026. Research note; no metering implementation or paid calls.

## Source finding

The [article](https://martinfowler.com/articles/are-harnesses-worth-the-cost.html) names Specmatic for behavioral checks, but does not document the exact token collector, parsing script, or reproducible cost-calculation pipeline. Do not infer an undocumented telemetry tool from its results.

## Related reporting documentation

[Specmatic reports](https://docs.specmatic.io/references/configuration/reports) documents HTML and CTRF output and API coverage. It labels CTRF as commercial. [CTRF](https://ctrf.io/docs/specification/overview) is a JSON test-execution interchange format; it is not a replacement for provider usage metering. Product documentation describes available capabilities, not proof of the exact experiment configuration.

## Proposed capture architecture for our experiment

Keep three independently attributable evidence streams:

1. Generation: provider/runtime invocation usage, cached categories, charged errors/retries, model identity and child/reviewer calls. Preserve provider-native evidence and normalize through a declared adapter.
2. Execution: trusted supervisor timings, stop reasons, resource limits, interventions and subject hashes. Do not ask the coding agent to estimate these.
3. Quality: independent requirement/test results, regressions and separate review dimensions. Export JUnit initially if suitable; consider CTRF as an optional interoperability layer after version/license review.

The report assembler joins streams by attempt identity and exact subject hash. Actions publishes the resulting artifact and human summary. The collector validates, deduplicates and archives it. Test-report compatibility alone does not validate generation costs.

## Questions our capture specification must answer

- Which trusted event/file/API is the source for each metric, and which fields are unavailable?
- Are cached/reasoning categories subsets or additive, and how is that verified?
- Which model calls are included: initial work, review, compaction, retries and child agents?
- What price snapshot and formula produce estimates, and how do estimates differ from attributable billed charges?
- Where do generation and evaluation clocks start/stop? Are setup, queueing and human waits separated?
- Can known failures and interrupted runs still produce durable, valid records?
- Can an independent reviewer recompute totals from archived evidence?

## Next action

Select a runtime and inspect an actual usage record before choosing a metering library. First build a local fake-provider fixture that exercises complete, missing, partial and interrupted usage. A later separately authorized real-provider calibration must reconcile reported usage with the adapter. Do not add Specmatic or any telemetry library solely because a source experiment used it.

This note adds implementation questions to the existing gap review. It does not change comparisons C1–C4 or select a tool.
