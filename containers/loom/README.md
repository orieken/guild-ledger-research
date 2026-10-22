# Loom native/mock container

22 October 2026. Builds the real Loom CLI from a frozen tracked-source export, then runs its native `deliver-feature` pipeline with `--provider mock`. This is H3-native infrastructure validation, not reduced H3-context or a controlled harness-effect result.

## Prepare and build

First build the shared `guild-ledger-claude-smoke:local` runner per [Claude container instructions](../claude/README.md). It supplies the common development tools and has no Claude binary. Then run from the research repository root:

```sh
python3 -B containers/loom/prepare.py \
  --source /absolute/path/to/ai-assistant-dot-files \
  --package ../guild-ledger-loom/package \
  --manifest-digest a85d54356d04fbdcfd3caf90a12ff6de48571e7188d8e49093ab0697561212af

docker build -t guild-ledger-loom-mock:local containers/loom
python3 -B containers/loom/tests/pipeline.py
```

The source must contain pinned upstream commit `3f2817818c68f42520229aab9342ce91533cef2f`; current working-tree state is irrelevant. `prepare.py` uses `git archive` at that revision, checks its tree and compressed-archive digest, and writes only the ignored `build/` directory. It does not use untracked files, reset the checkout, install globally, or execute upstream setup scripts. Clone/export that exact upstream revision when preparing another machine; do not silently select its latest HEAD.

The compiler is Go 1.26.5 in a digest-pinned image. Build dependencies are resolved with the upstream go.sum and `-mod=readonly`; the binary is built with `CGO_ENABLED=0`, `GOTOOLCHAIN=local`, `-trimpath`, and VCS auto-discovery off. The source archive, compiler image and resulting binary/image identities are recorded in the [verification receipt](verification.json). Compiler base is pinned; the local shared runtime base tag is mutable, so the receipt records its actual image ID. Freeze/archive the resulting images for campaign use rather than assuming a later rebuild is identical.

The final image contains Loom, its embedded framework content, upstream code/content licenses and source lock. It contains no Claude executable. Embedding framework assets does not exercise them as model context: the mock provider returns canned artifacts and does not construct real Claude calls.

## Run the gate-preserving default

Use a small standalone synthetic task directory; do not pass a repository parent or personal checkout.

```sh
python3 -B containers/loom/run.py \
  --task /absolute/path/to/synthetic-task \
  --package ../guild-ledger-loom/package \
  --manifest-digest a85d54356d04fbdcfd3caf90a12ff6de48571e7188d8e49093ab0697561212af \
  --output /absolute/path/to/new-output
```

Expected outcome is `needs-human` at `confirm-design`, with native exit code 3 and no approvals. The CLI wrapper exits nonzero for this outcome; it is a recorded gate, not a broken collector.

Add `--fixture-approvals` only for a synthetic integration run. It explicitly approves the three known gates through native `--resume --approve` invocations and records every approval as synthetic, not human authorization. The mock route settles all 16 native stages: nine completed, seven skipped. The ship gate remains even though its devops stage is routed out. Fixture completion is not autonomous benchmark success, production approval or acceptance evidence.

`--hang` pauses the context-engineer mock stage, then the watchdog sends SIGINT so Loom can checkpoint before container termination. `--hang --resume-after-interrupt` also performs one explicitly requested mock resume, which reaches the design gate again. Every invocation names `--provider mock`; non-mock provider state is refused. No implicit error retries or arbitrary upstream flags are exposed.

## Isolation and artifacts

Each invocation has a fresh container and tmpfs home, non-root UID 10001, read-only root, dropped capabilities, resource limits and no network. Only an isolated copy of task files and explicit profile/request inputs are mounted. It creates a **disposable synthetic Git baseline inside the container** so Loom's native posture/diff checks operate; no host repo, Git identity, hooks, global settings or credentials are copied. No user repository commits are created.

The source lock binds the requested profile manifest to the binary's source. The host validates profile and spec hashes before launch; container preflight verifies them again. Inputs can select only mock execution and explicit test controls. The runner does not load global skills or invoke the Loom installer.

Output contains `attempt.json`, profile bytes, per-invocation request/stdout/stderr/native checkpoint copies, and the complete generated workspace. Native artifacts include state documents, timeline events, local traces, mirror documents, a local synthetic episode database and fixture code. Artifact SHA-256 values are checked by the test suite. Generated `.claude/` and memory files are native run output, not inherited personal context.

A shared execution deadline limits launches; timeout requests a native SIGINT checkpoint and gives Docker a 3-second stop grace. Docker operations have separate control timeouts and export adds overhead. Hard host/process failure can still prevent export; this is not durable external telemetry. Unknown model usage/cost stays null, not zero. There are zero model calls, but build/CI compute is a separate resource.

The mock produced posture and post-review-edit warnings for its synthetic writes. Those warnings and native metadata are preserved and tested. We did not patch upstream to silence them or infer real code quality from a green fixture run.

## Remaining gates

No live Claude provider, paid usage calibration, real benchmark task, context-only Loom treatment, independent evaluator or native model routing has been admitted. The underlying binary also implements other CLI commands, but this container entrypoint exposes only the fixed mock pipeline boundary. Future real execution needs a separately reviewed profile, explicit auth/tools/context controls, aggregate model/child usage and cost accounting, and genuine human gates.

Attribution: [Loom by Oscar Rieken](https://github.com/orieken/loom), code MIT; embedded instructional content CC BY 4.0. Upstream LICENSE and LICENSE-CONTENT.md are retained in `/opt/loom/`.
