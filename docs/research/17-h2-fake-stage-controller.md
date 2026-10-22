# H2 fake-runtime stage controller

Implemented 22 October 2026. This controller executes the H2 stage graph with synthetic runtime fixtures in isolated Docker containers. It does not submit model calls, implement an independent evaluator, or admit H2 to paid experiments. The H1/H2 package bytes and pinned source commits remain unchanged.

## Run

From the research repository root, after building the smoke image:

```sh
python3 -B containers/claude/h2.py \
  --task /absolute/path/to/synthetic-task \
  --prompt /absolute/path/to/assigned-prompt.txt \
  --output /absolute/path/to/new-attempt \
  --harness ../guild-ledger-harness/package \
  --harness-digest f5b160533d307fcd627080d4dc5555b71d2fdc53453ea56de2b3de644d18c5a6 \
  --fixture repair \
  --wall-seconds 60 \
  --max-synthetic-tokens 54
```

`pass` executes implementation and review only. `repair` executes implementation, review and one repair. `--editable-prefix` may be repeated to constrain review finding paths; without it the standalone fixture task is wholly editable. A real benchmark needs its machine-readable edit-scope contract configured explicitly.

The controller inspects the image and refuses images without the synthetic runtime marker. Its only execution path calls the existing runner in `fake` mode, with network disabled and no credentials. The smoke image contains no Claude binary. Image identity is frozen to its local content ID for all stages of an attempt.

## Stage isolation and transitions

Every stage gets a new container, session ID, tmpfs home, copied source directory, read-only task/treatment/evidence inputs and a shared absolute monotonic deadline. Original assigned prompt bytes are preserved in every stage; only the explicit stage instruction and handoff differ. Public handoff/visible-check claims are synthetic agent data, not trusted test results.

Implementation supplies its public plan, handoff and visible-check evidence in the fake result. Review receives that concise result, the candidate source snapshot, its source hashes and a diff against the original starter, rather than implementation conversation history. Repair receives the same evidence plus the validated review. All input files and assembled prompts are archived with hashes.

The controller permits exactly one review, followed by zero or one repair. It validates review structure, verdict/findings consistency, relative file paths, existing candidate files and configured editable prefixes before repair. Review runs in its own copy; changed output hashes stop with `reviewer-mutated`. Review output never replaces the candidate. Source from an implementation or repair is retained even when the stage exits unsuccessfully.

No-findings review yields a completed workflow without repair. Completion means orchestration finished, not that code passed acceptance. Independent evaluation remains a separate future operation. Neither repair nor review can trigger an additional review cycle.

## Limits and incomplete evidence

One wall-clock deadline covers setup and stage execution; remaining time is checked before each launch and passed to the runner. A stage cannot acquire a new full deadline. Deadline expiry kills the stage container and stops subsequent stages. Docker cleanup/control operations have individual 10-second timeouts; evidence export also takes time outside the stage execution budget. This is not a guarantee that the complete host process exits at exactly the configured second, nor proof of remote inference cancellation.

Synthetic fixtures declare 18 tokens per successful stage. The controller requires enough remaining synthetic allowance before a stage starts and aggregates reported fixture counts across stages. The default 54 allows at most the three planned fixture stages. A limit of 36 can allow implementation and review but block repair. These are test units, not model-token predictions or paid spend enforcement. `cost_usd` remains null.

Missing stage usage is not zero: the record contains a known subtotal and `usage_complete=false`, and no later stage starts. Failed/interrupted/malformed stages retain raw outputs and available source but may lack usable usage; those attempts are explicitly incomplete. The controller does not silently rerun a stage or repair malformed review JSON.

Stop reasons include `completed`, `limit`, `timeout`, `needs-human`, `runtime-error`, `invalid-result`, `invalid-review`, `reviewer-mutated`, and `missing-usage`. Unsupported candidate symlinks stop rather than being promoted. OS/Docker errors and rejected non-synthetic images are recorded as runtime errors. Forced termination of the host or a broken Docker daemon can still interrupt export; durable out-of-worker checkpoints remain a production requirement.

## Output contract

- `attempt.json`: updated atomically at stage boundaries and completion; image/package identities, shared limits, stage lineage, session IDs, known synthetic usage, completeness, timestamps, stop reason and final candidate hashes.
- `implementation/`, `review/`, optional `repair/`: per-stage runner manifest, exact inputs, public stdout events, stderr and that stage's disposable source snapshot.
- `review/validated-review.json`: written only after successful review validation.
- `candidate/`: last implementation/repair source, or the original starter if no stage produced a usable candidate. Reviewer edits are excluded.

No host output directory, personal configuration or evaluator is mounted in a stage container. The controller's stage records and raw fake events are operational test evidence, not measured coding quality or provider accounting.

## Verified flows

```sh
python3 -B containers/claude/tests/smoke.py
python3 -B containers/claude/tests/treatments.py
python3 -B containers/claude/tests/h2.py
```

The H2 suite covers 24 cases: pass/repair branches; malformed review, traversal and missing-file findings; reviewer mutation; missing usage; failure, needs-human and malformed output at every stage; aggregate limits before implementation/review/repair; timeouts at every stage with partial candidates; edit-scope rejection; and refusal of the real Claude image. It also checks fresh session IDs/home state, original prompt preservation, explicit handoffs, no input-source mutation, final candidate selection and durable stop records.

Before live calibration: add an approved real-runtime adapter, actual usage lineage and aggregate cost controls, effective tool/context verification, stricter runtime-result schemas, enforced child-agent restrictions, full task edit-scope checks, service networking and independent evaluation. No paid invocation is enabled by this implementation.
