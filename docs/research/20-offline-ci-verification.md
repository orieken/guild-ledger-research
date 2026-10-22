# Offline harness CI verification

Added 22 October 2026. Workflow: [Offline harness setup](../../.github/workflows/offline-harness-tests.yml). Local driver: [offline_harness_ci.py](../../scripts/offline_harness_ci.py).

## Triggers and scope

The workflow supports manual dispatch and runs on main pushes or pull requests affecting containers, T01 task inputs/packaging, the harness registry, its drivers or workflow. It uses an Ubuntu 24.04 hosted runner, a read-only repository token and commit-pinned checkout/artifact actions. Checkout credentials are not persisted. No model/provider secrets are requested or passed.

It checks out the research repo under `guild-ledger-research/`, then creates sibling checkouts for H1–H4 at the exact commits in the registry. It verifies package/asset hashes and identical H1/H2 guideline bytes. Loom uses the checked-in tested source snapshot; Harness² is exported from its immutable public source pin. Public checkouts do not need cross-repository write tokens.

Builds have network access for image/release/module downloads. Every agent worker still uses `--network none`, fresh state and the existing non-root isolation policy. The shared T01 tool starts temporary services on worker localhost. Independent post-run service probes use fresh internal-only networks with no host ports. The real Claude image is exercised for version/help only; all other execution is fake, mock or deterministic. This workflow cannot authorize paid calls. GitHub Actions build/test compute is separate from model charges.

## Checks

| Check | Coverage |
|---|---|
| Claude startup | Fresh offline attempts, contamination rejection, timeout/failure source capture, real binary version/help |
| H1/H2 packages | Pinned assets, identical guidelines, H0 byte preservation and explicit treatment exposure |
| H2 controller | 24 implementation/review/repair and failure/limit cases |
| Loom source snapshot | Exact hash, tamper rejection, traversal and external-link rejection |
| Loom native mock | 10 gate, completion, interruption/resume and integrity cases |
| Harness² demo | 7 deterministic recursion/library, isolation and timeout cases |
| T01 packaging | Deterministic archives, prompt separation and clean-input audit |
| T01 supervisor boundaries | 8 fixed-input, missing-lock, symlink, editable-source and wrong-image cases |
| T01 harness integration | All 15 P1–P3 × H0–H4 mock combinations, in-worker and post-export checks, green controls and rejection controls |

The base build driver attempts all four original images. The T01 integration additionally builds fixed application/probe images and three worker overlays with preinstalled visible-test tools. The test driver runs all eight regression/unit suites and the full T01 integration even if another fails; the workflow also continues unaffected build/test/report steps after preparation failures. The job remains failed when any required source, build or suite is missing or unsuccessful. No `continue-on-error` hides a failing check.

## Evidence

An always-run finalizer writes a Markdown job summary and `ci-offline-results/report.json`. The 30-day artifact also contains per-build/per-suite logs and statuses, package identities and actual image IDs/platform/layer information. Original regression scripts create disposable attempt directories. T01 integration additionally retains the task manifests, full per-cell native runtime evidence, in-worker test events, exported application projections and post-run service/test logs under `ci-offline-results/t01/`. Existing committed verification receipts remain historical local evidence and are not overwritten with CI results.

A green result means all required preparation, builds and suites passed. It is not code-quality evaluation, runtime admission or a spend-metering result. A missing checkout or killed runner can prevent finalization; `always()` is not durable external checkpointing. Action artifacts should be archived separately if used in a publication.

## Loom availability issue resolved by approved snapshot

Fresh retrieval established that Loom pin `3f2817818c68f42520229aab9342ce91533cef2f` was absent from the public remote; its published main was substantially older. The user authorized publishing the exact previously tested source archive in this research repository rather than publishing unrelated pending upstream commits.

The [snapshot and provenance](../../vendor/loom/README.md) retain the existing source/archive hashes and licenses. CI verifies the snapshot against the unchanged H3 package, checks archive paths/links, and builds from those bytes. It does not fetch the missing upstream commit or silently replace it with a different revision. Hash/path failures remain blocking failures. Untracked working-tree files are excluded.

The pinned Harness² source is fetched separately, and its archive hash was reproduced using Linux Git. Package checkouts remain pinned to their published wrapper commits.

## Local commands

```sh
python3 -B scripts/offline_harness_ci.py prepare
python3 -B scripts/offline_harness_ci.py build
python3 -B scripts/offline_harness_ci.py test
python3 -B scripts/offline_harness_ci.py report
```

Preparation uses public remotes and refuses mismatched or dirty checkouts. Results go to ignored `ci-offline-results/`. The workflow verifies the committed source snapshot before building; an existing local image is not enough to pass preparation. Full setup verification and suite success are reported separately.

## Linux ownership verification

The first hosted run exposed private output files owned by container UID 10001 that the CI user could not read. Supervisors now use the non-root host UID/GID on Linux, retaining private modes and the existing container restrictions. Effective IDs are recorded in attempt manifests; Docker Desktop retains the original fallback. This addresses evidence collection without root workers or broad permission changes.
