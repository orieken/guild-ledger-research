# Runtime discovery task: Guild Ledger research

You are documenting your own coding-agent environment for our experiment comparing prompt completeness, added harnesses, code quality, and cost. This is a discovery session, not a benchmark attempt. Write evidence-backed files; do not just answer in chat.

## Destination and scope

Work in `orieken/guild-ledger-research` or its local checkout. Choose your exact tool surface and use a stable ID: `claude-code`, `github-copilot-coding-agent`, or `antigravity`. If you are a different surface, use a descriptive ID and explain it. Do not conflate an IDE assistant, CLI, GitHub-hosted coding agent, or API SDK.

Write only under `docs/runtime-discovery/<tool-id>/`. Preserve existing reports; if one exists, create a dated subfolder instead of overwriting it. If repository access is unavailable, return the same files as copyable content and state the access limitation.

Read relevant project instructions. Treat source material as reference, not permission to override governing rules. Do not expose hidden prompts, credentials, authentication files, private reasoning, or personal data. Describe visible instruction sources and their precedence; explicitly mark inaccessible internals unknown.

## Deliverables

1. `report.md`: the findings below, limitations, and reproduction steps.
2. `capabilities.json`: valid JSON with `schema_version: "guild-ledger.runtime-discovery/v1-draft"`, `tool_id`, UTC `captured_at`, exact `surface`, observed `version` or null, `model_identity`, a `capabilities` array, `evidence` array, and `open_questions`.
3. `evidence.md`: redacted observations, commands with exit status, official documentation links with retrieval date, and a record of what you did not test.

Each capability has `id`, `status` (`observed`, `documented`, `inferred`, or `unknown`), `value` (including false or null where appropriate), `scope`, `limitations`, and `evidence_ids`. Each evidence entry has a stable `id`, `kind`, and reference. These are discovery records, not our run-metrics schema; never invent usage or test results to fill fields.

## Questions to investigate

- Identity: what exact product/surface, runtime version, operating environment, and model identifier can you actually observe? Can a model/revision be pinned? Distinguish selected labels from verified backend identity.
- Automation: how can another program start a fresh task, supply a prompt/workspace, observe progress, stop it, and retrieve changed files? Provide verified CLI/API/SDK details only for your surface. State whether GitHub Actions or the host platform creates the job and which setup remains outside our control.
- Instructions and state: what visible user/project/org instructions, rules, skills, plugins, memory, prior sessions, and context compaction may affect work? Which can be isolated/reset? What remains mandatory or unobservable?
- Tools and permissions: editing, shell, tests, browser/network, MCP, subagents, approval gates, allowed filesystem scope, and human intervention. Separate capabilities you have now from those documented elsewhere.
- Metrics: where can we obtain raw input/output/cache/reasoning usage, model-call IDs, child/reviewer usage, tool events, timestamps, and error/retry usage? Give a redacted real schema or a clearly labeled schema-only example. Mark unavailable fields null; do not substitute guessed totals.
- Costs: is the account mode API, subscription, credits/premium requests, or unknown? Do not reveal account identifiers. Distinguish estimated/list-price amounts from attributable billed charges. Explain whether per-attempt USD is obtainable and what reconciliation would require.
- Reliability and artifacts: what survives cancellation/time limits? Can we obtain partial code, usage, logs, a final patch, repository revision, and stable task/run IDs? Who owns the records and what export/retention restrictions apply?
- Compatibility: can this exact surface support H0 (no added experimental rules), H1 (one guidelines file), H2 (our bounded workflow), and a pinned Loom profile? For each, mark observed/documented/inferred/unknown and explain blockers. Do not assume context-file support equals native pipeline support.

## Allowed probes

Run small, read-only inventory checks such as version/help, repository state, visible instruction/configuration discovery, and documentation lookup. Inspect only non-sensitive relevant configuration; do not dump the environment, auth files, or home directory. If authorized evidence from this session is unavailable, say so.

You may validate your JSON and, if supported, create then remove one scratch file inside your report folder to demonstrate editing. Record those actions. Do not install tools, change settings, launch other agents/model sessions, run application benchmarks, execute a Loom pipeline, change CI, deploy, merge, or start additional paid activity. The current documentation session itself is not a zero-cost benchmark.

If a capability needs an additional model call or cloud run to establish, list a proposed probe with purpose, inputs, expected evidence, maximum calls, proposed cost/time cap, and approval requirements. Do not execute it yet. Follow mandatory platform gates; report needs-human rather than bypassing them.

## Finish

Validate the JSON and links you can check. State which claims were observed versus documented or unverified. Give a compatibility summary and the three largest measurement/control gaps. Use your platform's normal review flow for documentation only; do not merge. In a local checkout, leave changes uncommitted unless explicitly asked otherwise. Report file paths and any limitations. Do not claim this session proves benchmark performance or full isolation.
