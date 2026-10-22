# H4: Google Research Harness²

Added 22 October 2026. [Official source](https://github.com/google-research/harness2), pinned revision `1cfe254e8d25b15f37048c3730134686abe60335`. [Offline container](../../containers/harness2/README.md), [profile registry](../../harness-packages.json). The wrapper repository is [orieken/guild-ledger-harness2](https://github.com/orieken/guild-ledger-harness2); its published package commit is pinned in the registry.

## Discovery and placement

Harness² optimizes the surrounding agent system rather than model weights. Its task loop proposes candidate changes, probes them, and composes a selected harness. A second loop retains lessons for subsequent tasks. The inspected release provides OpenCode and Codex substrates; Claude support is not established. [Upstream README](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md).

Register it as **H4**, with separate profile IDs. Do not substitute it for H3 Loom, equate it with Antigravity, or switch our first campaign to a Gemini model. Runtime/substrate and optimizer are distinct axes. This addition does not expand the authorized run count: no paid calls or benchmark runs are approved.

## Two future comparisons

| Profile | What changes | Appropriate comparison |
|---|---|---|
| H4 native adaptive | Task-local optimization plus ordered persistent learning | A separate native adaptive campaign, measuring complete task streams and total resources |
| H4 frozen optimized | Optimize on disjoint development tasks, export a fixed package, then stop optimization | Candidate fixed-harness comparison on a supported matched runtime after admission |

The frozen profile is our proposed ablation, not a feature already validated by this setup. A task-local reset profile would also be a deliberately reduced variant. Do not silently disable native learning and call the result the full framework.

For native learning, the experimental unit is an ordered stream replicate. Freeze task order/seed, initial library digest, recursion mode and `k`; give each replicate its own library. Record state before/after every task. Never let one repetition, prompt level or harness condition seed another. Report aggregate stream outcomes and uncertainty at the stream level; within-stream tasks are not independent replicates.

For frozen optimization, development tasks and feedback must be separated from held-out evaluation. Freeze selected assets, optimizer revision, tuning inputs and total tuning spend before evaluating. Report tuning cost separately and any amortization over a stated number of evaluation attempts. Do not pick a winning harness using private evaluation results.

## Information and execution boundaries

Only the assigned prompt completeness level, canonical starter and visible check evidence may enter optimization. Candidate/probe executions must not receive the full specification behind P1/P2, hidden acceptance tests or private evaluator feedback. Final evaluation occurs outside the optimizer and cannot trigger repairs. Changes to prompts, memory, tools, skills and scripts are confined to the declared treatment surface in a disposable worker; supervisor, budget ledger, credential controls and evaluator stay outside its write boundary.

The inspected upstream model-backed defaults allow unrestricted network access and disable Codex's internal sandbox. Our external worker boundary and egress policy must remain enforced before any real integration; the offline demo does not validate those defaults for Guild Ledger. [Upstream experiment guide](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md), [Codex substrate](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py).

## Accounting contract

One attempt/stream allowance must cover proposer, reference solver runs, candidate probes, composition, selection, reflection, child calls, retries and failures. Native `k` is a recursion parameter, not a total call or money cap. Persist call lineage, usage completeness, stop reasons and adopted-asset hashes outside the mutable harness. Keep solver and optimizer model identities/effort explicit. Changing the optimizer model is a complete-system difference even if solver weights stay fixed.

Additional record fields: optimizer/substrate revisions; execution and optimizer model configurations; `k`; parallel/sequential mode; task index/order/seed; library input/output digest; proposed/probed/composed/adopted asset digests; per-role call/usage/time totals; setup and tuning resources; final source and independent score. Missing charges remain unknown, never zero.

## Verified now

A source/profile-pinned, network-disabled Python 3.12 image runs the actual upstream deterministic demo. It uses scripted editors/selectors and Python execution, not an OpenCode/Codex model session. Two synthetic ledger tasks run through both modes. Empty libraries are recreated between experiments; within each mode the second task receives an entry learned from the first. Reference/probe/composition outputs and native library files are retained.

Offline checks cover repeatable fresh experiments, final synthetic compositions, library state transfer, rejected image/profile identity, external credentials, inherited workspace files and timeout evidence. These are infrastructure tests, not code-quality or monetary measurements.

## Admission work remaining

Implement a Guild Ledger task adapter, choose and match a supported solver runtime, define the optimizer model policy, protect hidden evaluation and task disclosure, constrain the mutable surface and network, verify aggregate metering/termination, and decide which profile/stream design to preregister. A bounded separately authorized calibration comes afterward. H0/H1/H2 and Loom configuration remain unchanged.
