# Shared T01 offline tools and mock integration

Run from the research repository after preparing the pinned packages/source exports:

```sh
python3 -B scripts/offline_harness_ci.py prepare
python3 -B scripts/t01_harness_smoke.py --build --output /tmp/t01-all-harnesses
```

The default is all 15 combinations: P1/P2/P3 × H0/H1/H2/H3/H4. `--levels P1` provides a shorter wiring check. Outputs must be new directories. Builds download public dependencies; execution makes no model calls. This command does not commit or publish anything.

Three dedicated worker images share the same installed public test tool and locked application dependencies. No model CLI is installed. H0/H1/H2 use the Claude fake runtime; H3 copies the pinned native Loom binary; H4 copies the pinned Harness² Python source. Original standalone smoke images and package bytes remain separate. The image IDs used in each run are recorded and tags are resolved once. `profile.json` explicitly identifies these mock overlays, binds their adapter/tool hashes and cites the unchanged source profiles; the worker image labels must match its hash. The T01 Harness² adapter is an additional boundary, not a relabeling of the original ledger-demo entrypoint.

The common task envelope names the same command for every harness. Every worker can run:

```sh
python3 /opt/t01/visible_checks.py
```

The tool starts Python, Go and Vue servers inside that worker's isolated localhost namespace, runs the supplied startup/API/UI checks and TypeScript/production build, and stops its servers. Dependencies are already installed; no Docker socket, registry access, host ports or model credentials are supplied. Its scratch volume is executable for Node's native build dependencies, with a read-only root filesystem and no external network. The tool emits a JSON event with real command exits and logs. The normal command exits nonzero when visible features fail. Mock fixtures use `--expect-starter-red`, which succeeds only for the known unfinished starter's exact assertion failures and green startup/build checks. That flag is a mock assertion, not a future live-agent stopping rule.

## Actual harness paths

| Harness | Mock execution exercised |
|---|---|
| H0 | Unchanged assigned prompt, fake runtime, in-worker visible checks |
| H1 | Same task + pinned guideline package, fake runtime, in-worker checks |
| H2 | Fresh implementation → review → repair workers; in-worker checks in each stage; original prompt and native controller evidence preserved |
| H3 | Assigned prompt appended to the fixed mock spec with hash attestation; pinned native 16-stage pipeline; first invocation runs in-worker checks; three **synthetic fixture approvals** resume gates |
| H4 | Dedicated T01 adapter calls pinned native `run_task(k=2)` in parallel and sequential modes, scripted proposer/selector and no-op solver; in-worker checks before adaptation; selected exports are asserted unchanged |

The H4 mock deliberately produces `NO_ENTRY` rather than inventing optimization evidence: this single-task no-op run does not test experience-library transfer. Original upstream ledger demo tests still cover persistent library mechanics. H3's fixed mock provider ignores task requirements; prompt transport is not proof of real solver behavior. All mocks preserve the unfinished application. Independent acceptance observations are now collected for those synthetic candidates; they are not measurements of model or harness quality.

## Independent post-run checks

The trusted host supervisor exports only application files. It rejects changed fixed tests, fixtures, locks and infrastructure, missing protected inputs, symlinks and special source files. Native state such as Loom's `.git`/`.claude` output and fake marker files remains runtime evidence and is excluded from the runnable application projection.

Each exported candidate is tested again with trusted, fixed test/service images on a fresh Docker **internal-only** network, without host ports. Only editable source is mounted read-only; candidate Compose files, Dockerfiles, test code and dependencies never execute. The UI component/build containers need no network. A separate visible-test witness must pass all checks both inside the worker tool and through the external supervisor, and deliberate protected-test edits and source symlinks must be rejected. Every cell reports infrastructure success separately from its expected red feature tests. After worker exit, the trusted supervisor runs the complete independent API/Chromium evaluator against the same projected application bytes. Each cell retains the full acceptance record, its candidate/evaluator identities, all criterion observations and a digest-linked `acceptance/report.json`. A completed full-target rejection is expected for every unchanged mock; an evaluator error, missing criterion, changed candidate identity or failed cleanup fails the integration check. No acceptance feedback is passed to a worker or repair stage. Summary JSON and detailed per-stage/test/evaluator logs are retained.

```mermaid
flowchart TD
  B[Canonical T01 bundle + assigned prompt] --> W[Fresh offline harness worker]
  T[Same preinstalled public test tool] --> W
  W --> L[Ephemeral localhost Python / Go / Vue]
  L --> I[In-worker visible test event]
  W --> C[Exported candidate + native evidence]
  C --> P[Trusted source projection and input checks]
  P --> N[Fresh internal-only application test network]
  N --> R[Startup / API / UI / build evidence]
  I --> S[Per-cell summary]
  R --> S
  P --> E[Separate independent API / Chromium evaluator]
  E --> A[Full-target acceptance + criterion evidence]
  A --> S
  S --> J[Aggregate report + digest-linked artifacts]
  PC[Separate positive witness] --> N
```

## Limits

These are offline integration checks with real full-target observations of synthetic unchanged candidates, not model-quality measurements or runtime admission. A paid run still requires evaluator/exposure freeze, an admitted live provider configuration, usage/cost calibration, budget and authorization. The current mocks do not request tests after generated edits; a future live runtime's tool use must be recorded separately. Infrastructure and model costs remain distinct; unknown provider usage/cost stays null in native records.

## Report contract

The matrix summary is `guild-ledger.t01-harness-smoke/v2`; the independent evaluator retains `guild-ledger.t01-acceptance/v1`. Per-cell `passed` means the mock integration assertions held, while `acceptance.full_target_acceptance` describes the exported product. `mock_acceptance_expectation_passed` asserts the completed unfinished-starter rejection (including A01/U01 failures) and is specific to these fixtures. It must not become a live candidate success rule.

The aggregate `independent_acceptance` includes completed/accepted/rejected/unknown counts and one compact result per prompt/harness cell. Artifact paths are relative to the matrix summary directory. Each cell also stores `acceptance_artifact.path` relative to its own directory. Both paths refer to the same SHA-256-linked report. Missing/error evaluations remain unknown, never an invented zero score. `communicated_conformance` remains null pending the exposure audit.

Offline CI builds the digest-labeled judge image, runs score-integrity tests, captures its image identity, uploads all acceptance artifacts and exposes the compact matrix under `t01_independent_acceptance` in `guild-ledger.offline-ci/v1`. Its `t01_report` path is relative to the CI artifact root. Historical v1 matrix artifacts have no acceptance section; consumers must not infer missing results as rejection.
