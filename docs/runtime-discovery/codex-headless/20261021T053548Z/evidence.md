# Evidence ledger

Captured: 2026-10-21T05:35:48Z. Status labels describe claims, not confidence scores. Configured means a stored setting; available means advertised by help/session tools; exercised means actually used in this discovery. No headless model invocation was exercised.

## E01 — project references, observed reads

Read `../../discovery-prompt.md`, `../../../research/13-harness-alignment.md`, and `../../../research/15-local-agent-reset.md`; combined read exit 0. Historical reset claims were not substituted for current checks. No backup archive or memory/conversation content was read.

## E02 — installed CLI, observed help/version

`command -v codex`: `/opt/homebrew/bin/codex`, exit 0. `codex --version`: `codex-cli 0.163.0`, exit 0. `codex --help`, `codex exec --help`, `codex exec resume --help`: exit 0. These are help checks, not task launches. They warned that PATH aliases could not be created due to permissions. No settings workaround was attempted. `command -v claude` found a separate executable; it was not invoked. `command -v loom` returned 1.

## E03 — safe local inventory

Selective parsed inspection of `~/.codex/config.toml` using Python 3.13: exit 0; no full config, env values, commands, authentication or credential files exported. Model `gpt-6.1-sol`; effort `low`; user approval/sandbox keys absent. Features `js_repl=false`, `memories=false`; memory use/generation false. Thirteen plugin entries, every enabled flag false. MCP: node_repl enabled key absent; computer-use false; cua_repl false. Notification present; hook state includes persisted trust records for disabled browser/chrome/computer-use plugin hooks. Commands and trust hashes omitted from this report.

Ancestor inventory checked AGENTS.md and AGENTS.override.md on both paths through root. Only project-mirror AGENTS.md found; read-only-source rule retained. Global Codex AGENTS/override absent; rules directory empty; user skills contains `.system`; home `.agents/skills` absent; research `.codex`/`.agents` absent. Two explicit Loom executable paths absent. These checks do not inventory every possible managed configuration source.

Initial Python attempt exited 1 before inspection because Python 3.10 lacks tomllib; repeated safe parse with installed Python 3.13 succeeded. Another combined inventory exited 1 only at process ancestry collection: `ps` was denied by sandbox. Earlier filesystem and OS observations completed. No escalation to inspect processes was attempted.

## E04 — authentication status

`codex login status`: exit 0; `Logged in using ChatGPT`. No auth file, token, email, account identifier or plan details read.

## E05 — current session and execution

Observed shell `pwd` is the project mirror; local research files readable; platform probe reports Darwin 25.6.0 arm64. Desktop chat surface has shell/web tools and exposed connector/MCP/skill catalogs; this is not a headless transcript. Tool exposure persists beyond the local cleanup settings. Effective model/effort/backend/usage for this chat are not independently exported. Prior chat content remains inherited. No hidden prompt inspection, unrelated conversation lookup, private reasoning export or subagent use.

## E06 — official documentation, documented only

Retrieved 2026-10-21: [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode), originally requested through developers.openai.com/codex/noninteractive and redirected to the official Learn page. Relevant lifecycle and usage example read. Markdown-suffix requests for that page and config reference failed with unsupported content-type; they provide no additional evidence.

Schema-only representation, with nulls replacing all example totals and identifiers; **not a captured event**:

```json
{"type":"thread.started","thread_id":null}
{"type":"turn.completed","usage":{"input_tokens":null,"cached_input_tokens":null,"output_tokens":null,"reasoning_output_tokens":null}}
```

No request ID, charge, child coverage, deduplication or cumulative-resume guarantee follows from this example.

## E07 — repository status

`git status --short`: exit 0; preexisting untracked README.md, docs/, repositories.json. `git rev-parse HEAD`: exit 128, no valid HEAD commit. Initial codex-headless destination absent. No index change, commit or push. Existing reports preserved.

## E08 — validation

Three new files only. JSON parsed; required top-level fields and all capability fields checked; statuses restricted to observed/documented/inferred/unknown; evidence references resolve; non-unknown entries have evidence; local Markdown links resolve. No runtime metrics invented. SHA-256 hashes of the three required source documents recorded below to identify exactly what was read.

## Not tested

No fresh or resumed model run; cancellation; code artifact generation by headless CLI; reasoning content; actual usage export; provider request IDs; retries; child/reviewer usage; charge reconciliation; native Loom; Claude cleanup revalidation; tool installation; settings modification; app restart; benchmark; CI; remote write. No benchmark conclusions.

- `docs/runtime-discovery/discovery-prompt.md`: SHA-256 `aab77364a6b2fda37ff1e911b5eefd62ea417d29e835c41d3eb348c05f424abd`

- `docs/research/13-harness-alignment.md`: SHA-256 `caf46bb09e770368fd4afa95e0e22cca533328354915f0297a66d236a0131fd1`

- `docs/research/15-local-agent-reset.md`: SHA-256 `90a2a20fce451406bf68e8daae2499eec6d86ef744f5c6dcebc9c66cf26c1696`
