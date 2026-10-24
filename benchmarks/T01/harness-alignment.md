# T01 harness input alignment

Use one exported workspace hash across conditions, and the same envelope + selected product prompt bytes. Keep the task manifest outside the worker. Harness instructions remain separate registered inputs, never files in the canonical starter.

| Condition | Current adapter | T01 readiness |
|---|---|---|
| H0 | Claude fake supervisor + shared T01 tools | Same prompt/workspace; visible checks run inside worker and after export |
| H1 | Same supervisor + pinned guidelines + shared tools | Same T01 input and verification contract |
| H2 | Fake stage controller + shared tools | Implementation/review/repair each run visible checks; exported source retested |
| H3 Loom | Native mock pipeline + optional assigned prompt | Prompt hash attested; in-worker checks and fixture-gated native stages; no real solver behavior |
| H4 Harness² | Dedicated T01 no-op adapter | Native k=2 parallel/sequential recursion and selection; source unchanged; no experience learning claim |

## Next admission work

1. Prebuild application and test images from this starter; record immutable image IDs, dependency locks, platform and startup/reset evidence. Build downloads are setup cost. Worker executions must not download dependencies.
2. The common offline tool now owns ephemeral localhost services inside workers; the trusted outer supervisor owns independent post-run services. `make up` inside a worker remains unsupported because workers have no Docker socket. Freeze the final live-runtime tool contract and collect actual tool-use evidence.
3. Keep Loom native pipeline and Harness² adaptive comparisons separately labeled. Their T01 mock transports are implemented; live provider and library/stream admission still need explicit profiles.
4. The [independent evaluator](../../evaluators/T01/README.md) now provides API/Chromium acceptance checks validated against full references and seeded defects. Visible tests remain public scaffolding checks. Review/freeze the evaluator and detailed requirement-to-input exposure before paid attempts.
5. Freeze runtime/model/configuration, budgets, schedule and artifacts, then request paid-run authorization.

No model calls are needed for steps 1–4. Do not substitute a successful deterministic demo or a green visible witness for task acceptance or runtime admission.

Implementation and invocation: [shared T01 tools](../../containers/t01/README.md).
