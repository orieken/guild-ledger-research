# T02 shared envelope — supplied verbatim to all three prompt levels

Draft interface contract. Paths, commands, schemas, and dependency behavior must be implemented and validated in the canonical starter before campaign freeze. Do not launch experiments against placeholders.

You are changing the provided Guild Ledger starter. It contains a working quest browser and party selector, a Python service, and a fixed Go armory dependency. Implement the assigned product request using Vue 3 + TypeScript, Python/FastAPI, Go, and PostgreSQL. Do not change the selected stack.

Editable areas: `web/src/`, `web/tests/`, `services/guild/`, and guild-owned migration files. Preserve existing functionality. The Go armory implementation, Compose services, dependency locks, seed fixtures, and evaluation tooling are outside this task's edit scope. You may add dependencies only through the declared task mechanism; the initial task allows no new runtime dependencies.

Proposed starter commands:

* `make up` — start the pinned local application/dependencies.
* `make test-visible` — run the supplied visible smoke tests and your tests.
* `make reset` — restore deterministic synthetic seed data.

Use the supplied development environment. Do not deploy, publish, commit, or contact external services. No live clarification answers will be provided. Record unresolved assumptions and proceed where possible. Stop if mandatory runtime approval is required. The runner enforces the campaign's shared limits and records them outside your writable directory.

## Common API transport contract

Implement `POST /api/expeditions` with an `Idempotency-Key` string header and a JSON body:

```json
{
  "party_id": "party-lantern",
  "quest_id": "quest-watchtower",
  "items": [
    {"item_id": "item-rope", "quantity": 1},
    {"item_id": "item-lantern", "quantity": 2}
  ]
}
```

Success response fields: `id`, `party_id`, `quest_id`, `status`, `reservation_id`. Error response fields: `error.code`, `error.message`. Implement `GET /api/expeditions/{id}` returning the same expedition representation. The task's prompt defines additional product semantics where supplied. Header presence and field shapes do not specify replay behavior or exact domain-error mapping by themselves.

The fixed Go dependency exposes `POST /internal/reservations` with `Idempotency-Key`, `expedition_id`, and an item list. It returns `201` for creation or `200` for replay with a reservation `id`; `409` for insufficient inventory or a key conflict; `404` for an unknown item; and `503` for the task's definitive pre-write unavailable fixture. Its provided client normalizes these response bodies. It supports atomic item batches and stores idempotency outcomes. Use the supplied service URL. Do not query the armory database from Python.

The starter includes API DTO definitions, an armory client, database access helpers, and examples for calling existing quest/party endpoints. Payload schemas constrain wire types. They do not specify every product rule. The supplied request is a wire-format example, not an acceptance answer key.

Finish by recording the files changed, checks run and their observed results, assumptions, and known limitations. The evaluator will independently test the final artifact after the session ends; it will not send private failures back for repair.
