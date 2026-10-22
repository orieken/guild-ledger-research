# Harness² deterministic-demo container

22 October 2026. H4 setup for [Google Research Harness²](https://github.com/google-research/harness2), not Antigravity or Gemini CLI. The upstream framework is pinned to `1cfe254e8d25b15f37048c3730134686abe60335`. The wrapper package is published in [guild-ledger-harness2](https://github.com/orieken/guild-ledger-harness2).

## Build and run

From the research checkout:

```sh
python3 -B containers/harness2/prepare.py \
  --source /absolute/path/to/harness2-upstream-checkout \
  --package ../guild-ledger-harness2/package \
  --digest 98ea2f392df4140dd18cceeecc6b09c442aafa090b50ef62ceba43b5f71f0af0

docker build -t guild-ledger-harness2-demo:local containers/harness2
python3 -B containers/harness2/run.py --output /absolute/path/to/new-output
python3 -B containers/harness2/tests/demo.py
```

Clone `https://github.com/google-research/harness2.git` separately and ensure the pinned revision exists. Preparation exports only tracked source at the pinned commit and verifies its tree/archive hashes; generated `build/` files are ignored. The Docker image uses a digest-pinned Python 3.12 base and the stdlib-only demo path. No pip installation, optional bridge/render dependencies, cloud setup, benchmark download or model executor is required.

The entrypoint runs only upstream `harness2.cli.demo`, `k=2`, both parallel and sequential modes. It cannot dispatch the model-backed benchmark CLI. No Claude, Codex, OpenCode or Google Cloud executable is installed. Containers run non-root with a fresh home/workspace, read-only root, no network, dropped capabilities and CPU/memory/process limits. No host environment variables, credentials, research source or evaluator are mounted.

Outputs include the upstream demo's source tasks, reference/probe/composition outputs, adopted harnesses, libraries and `demo.json`, plus host logs and an attempt manifest. `model_calls=0`; usage and cost stay null. Native `editor_calls` are scripted editor invocations, not LLM requests. Raw upstream demo USD zeros are fixture defaults, not billing records. Repeated experiments start with empty libraries; the native demo deliberately transfers a library entry from its first synthetic task to its second within each mode.

The verified demo processed two tasks in both modes with 28 Python executions and 32 scripted editor calls, and corrected synthetic signed-ledger totals. This establishes mechanics only: it is not Guild Ledger coding performance, a model improvement result or proof of real executor compatibility. The [verification receipt](verification.json) records the image/profile/source identities and offline checks.

[Comparison protocol and remaining admission work](../../docs/research/19-harness2-adaptive-comparison.md). Upstream source and notices are preserved under `/opt/harness2`, including Apache-2.0 licensing and third-party notices.

On Linux, the supervisor uses the non-root host UID/GID for bind-mounted attempt files, preserving private file modes while allowing host evidence collection. Docker Desktop uses UID/GID 10001. Root hosts still use the non-root fallback. Each attempt records its effective worker IDs; this does not mount host configuration or grant extra container capabilities.
