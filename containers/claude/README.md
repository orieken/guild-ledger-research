# Isolated Claude runner containers

Initial no-model implementation, 21 October 2026. Build two targets: `smoke` contains a synthetic CLI fixture; `claude` contains the real pinned Claude Code 2.1.304 binary. Both include Node 24.10.0, Go 1.26.0, Debian Python 3.11, make, Git, compilers and a PostgreSQL client. This is the agent development environment, not the application/database/evaluator stack. No optional agent skills, plugins, MCP servers or personal rules are installed.

## Build and test

Run from the research repository root, with Docker running:

```sh
docker build --target smoke -t guild-ledger-claude-smoke:local containers/claude
docker build --target claude -t guild-ledger-claude:2.1.304 containers/claude
python3 -B containers/claude/tests/smoke.py
python3 -B containers/claude/tests/treatments.py
python3 -B containers/claude/tests/h2.py
```

Builds download OS dependencies and a Claude release, but make no model calls. The Claude build verifies the release manifest's GPG signature against the documented signing fingerprint, then verifies the platform binary's SHA-256 checksum. The base Node/Go image references are pinned by digest. OS packages come from live Debian repositories: the resulting image ID is the repeatable execution reference; rebuilding later is not guaranteed byte-identical. Freeze OS package sources and archive images before campaign admission.

## Run an offline synthetic attempt

Create a small standalone task directory and prompt file outside the research checkout. Do not use the sibling-repository parent as a task directory.

```sh
python3 -B containers/claude/run.py \
  --image guild-ledger-claude-smoke:local \
  --task /absolute/path/to/task \
  --prompt /absolute/path/to/prompt.txt \
  --output /absolute/path/to/new-attempt-output
```

The output directory must not already exist or sit inside the task. It contains stdout events, stderr, a source snapshot and a host-generated manifest with input/output hashes, image ID, timestamps, timeout and exit state. Synthetic token counts are fixture data, not measurements. `--mode preflight` checks startup only. Use the real image with `--mode cli-info --timeout 90` to inspect its binary hash, version and help without credentials or inference.

The launcher resolves the image tag to its local image ID before creating the container. It copies task inputs into a disposable staging directory, mounts only that copy writable, and mounts only the prompt inputs read-only. Evidence output is never mounted in the container. Agent-created symlinks are preserved as untrusted output and their targets are recorded; the collector does not follow them to read host files.

## Isolation policy

- Fresh tmpfs home and temporary directory per container; no host home, credentials, configuration cache, sibling checkout, Docker socket, or evaluator mount.
- non-root UID/GID, read-only root filesystem, all Linux capabilities dropped, no privilege escalation, bounded memory/CPU/process count, and Docker init for child reaping.
- Network disabled for every currently supported mode. No environment variables from the host are forwarded into the container.
- Startup checks reject known instruction filenames, agent configuration directories, MCP configuration, dependency caches, symlinks and special files in inputs. The host performs the same input check before copying. Task inputs remain strict. H1/H2 packages now use a separate explicit, hash-verified read-only input; they do not bypass task auditing. Loom and starter exceptions remain unsupported.
- Input audits are a bounded filesystem/environment check, not proof of effective model context. Native runtime tools and instructions still exist. Arbitrarily named instruction prose cannot be detected by filename checks; campaign input hashes and exposure review remain necessary.
- A host watchdog kills the container on timeout and snapshots partial edits. Local termination does not prove cancellation of a remote provider request. These initial modes never submit one.

## Deliberate boundary before paid calibration

The entrypoint accepts only `preflight`, `fake`, and `cli-info`. Live Claude execution, credentials, provider egress, live H2 stage orchestration, H3 injection and application service networking are not enabled. H1/H2 prompt assembly and the H2 fake-stage controller are supported offline. The user has authorized container construction, not paid calls. No personal sign-ins or global installation are changed.

Before enabling live mode, implement and validate a fixed launch contract (candidate: bare mode with explicit task/treatment input and tool catalog), approved authentication, restricted provider egress, actual init-event tool/context verification, per-request/child usage accounting, aggregate limits and failure completeness. Bare mode and auth compatibility require calibration; do not copy the entire personal Claude directory. Permission approvals and tool availability are separate controls. Do not enable unrestricted permission bypass as a substitute for those decisions.

These containers share Docker's kernel boundary and are an initial development isolation layer, not a claim of adversarial sandbox certification. Future benchmark workers must keep evaluator and durable telemetry outside agent access.

## Sources

Checked 21 October 2026: [Claude development containers](https://code.claude.com/docs/en/devcontainer), [installation and release signature verification](https://code.claude.com/docs/en/setup#binary-integrity-and-code-signing), [CLI controls](https://code.claude.com/docs/en/cli-reference). Documentation describes available behavior; real runtime context and metering remain unvalidated.

## H1/H2 package loading

See [treatment definitions](../../docs/research/16-h1-h2-treatment-definitions.md) for package hashes and commands. Pass `--harness-id`, `--harness` (the package directory only), and `--harness-digest` together. H0 is the default. Both host and container validate the exact payload; no directory discovery is enabled. The original `run.py` command confirms single-stage assembly. The separate [H2 controller](../../docs/research/17-h2-fake-stage-controller.md) now exercises the complete graph with synthetic fixtures; real-agent compliance remains untested.

On Linux, the supervisor uses the non-root host UID/GID for bind-mounted attempt files, preserving private file modes while allowing host evidence collection. Docker Desktop uses UID/GID 10001. Root hosts still use the non-root fallback. Each attempt records its effective worker IDs; this does not mount host configuration or grant extra container capabilities.
