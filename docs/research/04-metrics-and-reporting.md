# Metrics and reporting contract

Visual companions: [run lifecycle](07-system-diagrams.md#5-run-lifecycle-and-unsuccessful-outcomes) and [metrics provenance and ingestion](07-system-diagrams.md#7-metrics-provenance-and-research-ingestion).

## Measurements and provenance

The agent generates code. The trusted supervisor records generation behavior. The independent evaluator measures the final artifact. GitHub Actions packages these records. The research collector validates and archives them, then analysis derives tables and posts.

Do not ask an agent to estimate how many tokens it used. A commit timestamp, code size, or CI duration cannot reconstruct generation usage. If historical provider usage is absent, cost remains unknown.

## Required dimensions

| Dimension | Fields | Source |
|---|---|---|
| Identity | campaign, slot, attempt, parent/retry, task, prompt level, harness/profile, model config | Trusted campaign and supervisor |
| Reproducibility | exact revisions/hashes, input order, environment, workflow definition | Resolved manifest |
| Generation status | completed, needs-human, budget/time limit, agent error, infrastructure error, cancelled | Supervisor, not agent's final claim |
| Correctness | requirement results, communicated/full-target critical acceptance, regressions | Independent evaluator |
| Resources | input/output/cache/reasoning usage, invocation and tool counts | Runtime/provider plus trusted tool gateway |
| Money | reported charge, estimate, pricing snapshot, completeness, compute/tool costs | Provider billing/usage and infrastructure records |
| Time | generation elapsed, agent-active, gate wait, queue, evaluation, human active time | Monotonic supervisor timing and recorded interventions |
| Review | readability, cohesion, complexity, ease of change, reviewer agreement | Blinded anchored review |
| Evidence | final patch/archive, test reports, usage/events, artifact hashes | Supervisor/evaluator/publisher |

Line count, lint count, and coverage percentage are diagnostic measures, not substitutes for correctness or maintainability. Record dependency additions and patch size to help explain changes.

## Primary and secondary outcomes

Updated comparison definitions: [C1–C4 protocol](10-comparison-protocol.md). The primary operational endpoint is **autonomous full-target functional success**: completed generation within limits, all canonical critical requirements passing, and valid evidence. Communicated conformance remains a separate implementation diagnostic. Report artifact-only results and requirement counts alongside autonomous outcomes so missing information, non-completion, and coding defects are not conflated.

Use two binary fields plus requirement counts:

* `communicated`: all critical criteria available in that condition pass.
* `full_target`: all canonical critical criteria pass.

The evaluator may measure a stopped attempt's partial artifact, but primary success additionally requires autonomous completion. A known needs-human/timeout/budget stop establishes autonomous non-completion even if artifact evaluation is unavailable. Show artifact-only acceptance separately: an evaluator outage leaves unmeasured artifact acceptance `null`, not `false`. When generation completed but evaluation is unavailable, autonomous success is also unknown. Infrastructure errors follow the separately frozen classification/replacement policy. The draft summary schema still needs revision to encode this distinction; its current evaluator-error null rule is not the final operational contract.

Report the following separately: full-target requirement pass fraction, UI behaviors, regression preservation, security/robustness, maintainability rubric scores, agent-written test effectiveness, completion rate, intervention rate, and cost/time. Avoid one weighted leaderboard score.

## Status is not a verdict

Separate fields are essential:

* `generation.status` describes why construction stopped.
* `evaluation.status` is `completed`, `error`, or `not_run`.
* `acceptance` describes independently observed behavior, or is null.
* `integrity` says whether evidence/input hashes/boundaries passed validation.

An agent saying “done” means generation completed; its code may still fail. A failed acceptance suite is an ordinary result and should produce a valid report. A missing evaluator or corrupted artifact is a research pipeline problem and must not masquerade as a coding failure.

## Cost accounting

Persist one usage record per model invocation, including child/reviewer calls, with provider-native fields and a normalized mapping. Preserve raw evidence securely. Input-token conventions differ: mark whether cached input is included in total input, and whether reasoning is included in output. Never add a subset twice.

Per-invocation USD estimate uses the frozen provider-specific pricing function. Sum across **all** invocations, including failed calls with charged usage. Separate reported charge and estimated charge. Set comparison cost to reported if complete and trustworthy, otherwise a complete estimate, otherwise null. Record its basis. Partial subtotals remain labeled partial; a missing charge is never treated as zero.

Meter compute, tools, independent evaluation, and storage separately. Setup/adaptation/maintenance and active human intervention are labor measures with declared hourly-rate scenarios. Gate wait is elapsed time, not active labor.

Derived per-cell metrics:

```text
autonomous_success_rate = successful_attempts / eligible_scheduled_slots
observed_generation_cost_per_success = total_generation_cost / successful_attempts
```

The cost-per-success ratio is defined only when all included generation costs are known and at least one attempt succeeds. Otherwise show unknown or no-success, plus completeness counts. Do not sum only successful attempts or omit expensive failures. Infrastructure replacements follow the preregistered rule and retain their operational cost in a separate all-execution total.

The success-rate formula is a point estimate only after every eligible slot has a valid observed endpoint. If some evaluations are missing or errored, show observed successes, known failures, and unknown slots separately; report the possible success-rate range from `successes / eligible slots` to `(successes + unknown slots) / eligible slots`. Do not silently count unknown evaluations as coding failures or drop them to improve a rate. This missingness range is distinct from a statistical confidence interval.

End-to-end scenario cost = generation + evaluation + infrastructure/tools + active human labor + setup/maintenance allocated over a stated reuse count. Report several reuse counts, rather than implying a harness's setup cost is free. No-success cells have no finite observed cost per success.

## Time and budgets

Use non-overlapping duration definitions:

* `generation_elapsed_seconds`: supervisor start to construction stop, including approval waits.
* `gate_wait_seconds`: portion spent waiting for human approval/input.
* `agent_active_seconds`: generation elapsed minus gate wait; may include tools and provider latency.
* `human_active_seconds`: measured intervention effort; can overlap elapsed time and must not be added to derive wall time.
* `queue_seconds`: GitHub scheduling delay, outside generation.
* `evaluation_seconds`: independent assessment elapsed, outside generation.

Parallel model latencies can sum to more than wall time. Retain per-invocation timings without interpreting their sum as elapsed duration. Record CPU/memory limits, runner image, and hardware class. Use deterministic fixtures and fixed clock injection where needed.

Total budget enforcement must include every model call. Enforce spend through a supervisor/provider gateway where possible; log cap overshoot caused by in-flight requests. A GitHub job timeout alone is not a reliable model-spend cap.

## Review rubric

Reviewers score each dimension 1–5, with 1 meaning substantial defects, 3 understandable with localized issues, and 5 clear and easy to modify. Record evidence comments for the assigned score. Review readability, responsibility boundaries, unnecessary complexity, and ease of implementing a specified follow-up change. Use at least two reviewers on a balanced subset; report agreement and adjudication rather than silently averaging disagreement away.

Hide harness labels and randomize review order where possible. Repository structure/style may reveal conditions; acknowledge imperfect blinding. If an LLM judge is added, freeze its prompt/model, count its cost separately, and validate against human judgments. Do not let a harness grade its own output.

## Machine-readable artifact

Every attempt publishes one bundle:

```text
run-record.json              # contracts/run-record.schema.json
resolved-manifest.json       # exact limits, inputs, schedule, versions
generation-events.jsonl      # supervisor stage/stop/intervention events
invocations.jsonl            # provider-native usage + normalized mapping
requirements.json           # criterion results and exposure mapping
evaluation-summary.json      # independent verdicts, evaluator identity
junit.xml                    # optional convenience for standard tools
subject.tar                  # final source snapshot, no credentials
subject.patch                # changes relative to pinned starter
evidence-manifest.json       # SHA-256, byte size, media type for every file
```

Usage logs may contain private metadata; public exports are reviewed/redacted versions with a redaction manifest. CI logs and public summaries contain bounded synthetic identifiers and measured properties, not credentials or full prompt/completion payloads. Raw transcripts, where collected, stay in a controlled archive with a stated retention policy.

`run-record.schema.json` is a draft summary contract. Rich per-invocation/event/manifest schemas are implementation work; do not claim a complete telemetry API from this one schema. Synthetic examples use conspicuous IDs and `synthetic: true`; collectors must exclude them from research datasets.

## Research ingestion

The collector discovers completed reporting artifacts only from registered repository IDs and workflow IDs. It verifies origin, workflow revision, run attempt, artifact ID/digest, bundle manifest, schema, exact campaign slot, subject/evaluator hashes, and required evidence. Validate JSON and file sizes before ingestion. Treat archived application files as data, never commands to execute in the collector.

Primary key: campaign + slot + attempt ID. Repeated collection of the same digest is a no-op. The same identity with different content is quarantined. Schema versions route to explicit migrations; unknown versions are not guessed. A scheduled slot with no artifact is recorded as missing, not dropped from the denominator.

Persist an immutable raw archive, normalized run table, invocation table, requirement table, and review table. Export JSONL and CSV for research notebooks, with Parquet optional later. Separate operational pipeline failures from accepted experimental observations. Store rerun lineage and analytical inclusion reason.

Actions artifacts are transport storage with configurable retention, not the permanent dataset. Archive evidence before expiration and verify backups. See [GitHub artifact retention and transfer](https://docs.github.com/en/actions/tutorials/store-and-share-data).

## Analysis outputs

Produce: cell counts and missingness; communicated/full-target success with intervals; per-task requirement failures; cost/time distributions including failures; cost-versus-quality plots; intervention/gate burden; infrastructure/retry totals; and profile/model stratification. Weight tasks according to the frozen analysis plan. Treat repetitions as nested in task and do not count correlated assertions as independent samples.

The pilot tests the machinery. A main study must predeclare contrasts, task aggregation, exclusion/rerun rules, multiplicity handling, effect-size target, sample size, and stopping rule. Publish null results and all condition denominators.
