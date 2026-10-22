# T01 harness input alignment

Use one exported workspace hash across conditions, and the same envelope + selected product prompt bytes. Keep the task manifest outside the worker. Harness instructions remain separate registered inputs, never files in the canonical starter.

| Condition | Current adapter | T01 readiness |
|---|---|---|
| H0 | Claude fake supervisor accepts task directory + prompt | Clean-input audit verified; no implementation execution admitted |
| H1 | Same supervisor + pinned guidelines package | Uses identical T01 input contract; mock assembly only |
| H2 | Fake implementation/review/repair controller | Uses identical T01 input contract; fake artifacts are not quest code |
| H3 Loom | Native mock pipeline takes a workspace and fixed mock spec | Workspace can be staged; assigned T01 prompt transport still needs an adapter; mock spec is not a benchmark attempt |
| H4 Harness² | Deterministic upstream demo | Does not yet consume arbitrary Guild Ledger workspaces/prompts; task adapter and stream protocol required |

## Next admission work

1. Prebuild application and test images from this starter; record immutable image IDs, dependency locks, platform and startup/reset evidence. Build downloads are setup cost. Worker executions must not download dependencies.
2. Give all controlled harnesses the same isolated application/test interface without Docker daemon access, host home mounts, credentials or unrestricted network. Current workers deliberately have network disabled, so `make up` inside them is not supported. A trusted outer supervisor must own the application lifecycle.
3. Mount only exported workspace and assigned prompt, then attach the pinned treatment. Adapt Loom's task prompt and Harness²'s task execution explicitly; preserve their different comparison tracks and gate/stream policies.
4. Develop and independently verify the full-target evaluator. Visible tests are public scaffolding checks, not the main score. Freeze detailed requirement-to-input exposure before any attempt.
5. Freeze runtime/model/configuration, budgets, schedule and artifacts, then request paid-run authorization.

No model calls are needed for steps 1–4. Do not substitute a successful deterministic demo or a green visible witness for task acceptance or runtime admission.
