# P3 — specification

Implement quest acceptance in the supplied Guild Ledger application using the shared envelope's routes, wire schemas, stack, and write boundaries. Preserve existing browsing and party selection.

## Required behavior

1. Let the player select a quest, an existing party, and a non-empty equipment list. On success, obtain one atomic reservation from the Go service, persist one accepted expedition with the reservation ID, and show the saved result. It must remain retrievable after page reload and application restart.
2. Only open quests are eligible. Party size must be within inclusive minimum/maximum bounds, and **every member** must meet the minimum level. An average party level is insufficient.
3. A party may have at most one pending or accepted expedition. Reject a second operation for that party even when it uses a different idempotency key. The same successful operation can still be replayed as described below.
4. Unknown party, quest, or item IDs are rejected. Equipment quantities must be positive integers; reject repeated item IDs and an empty item list. Do not silently combine duplicate lines.
5. Reservation is all-or-none. Insufficient equipment must leave no accepted expedition and no active reservation for the failed request. Python must use the Go API rather than its tables.
6. Persist request identity. The same idempotency key and normalized request replay the same expedition/reservation without allocating again, including after an application restart. Sort item lines by item ID for identity; reordering them alone does not change the request. A different party, quest, item set, or quantity with the same key conflicts. Concurrent same-key calls must converge to one operation. Return `201` for the first successful creation and `200` for a completed replay.
7. Bound the Go request with an explicit finite timeout. For this task's definitive pre-write unavailable fixture, return `503`, leave no accepted expedition, and allow the user to retry. Ambiguous timeouts after a committed reservation and crash recovery between services are outside this task.
8. While submitting, disable duplicate submission and expose pending status. On failure, preserve inputs and show an accessible error message. On success, announce acceptance and display the saved expedition. Follow the starter's accessible form conventions.

## HTTP errors

Use the shared envelope's error object. Return:

| Situation | Status | `error.code` |
|---|---|---|
| Missing/empty idempotency key, malformed request, invalid quantity, duplicate item, empty item list | 400 | `INVALID_REQUEST` |
| Unknown party, quest, item, or requested expedition ID | 404 | `NOT_FOUND` |
| Closed quest, size violation, or insufficient member level | 422 | `PARTY_INELIGIBLE` |
| Another pending/accepted expedition for the party | 409 | `PARTY_BUSY` |
| Same key, different normalized body | 409 | `IDEMPOTENCY_CONFLICT` |
| Definitive insufficient equipment | 409 | `INSUFFICIENT_STOCK` |
| Definitive pre-write Go unavailability | 503 | `ARMORY_UNAVAILABLE` |

Error messages should be useful; exact prose is not graded. Evaluate shape/header and ID existence first, then idempotent replay/key conflict, then party-busy, then quest eligibility, then the inventory request. Do not reject a valid replay merely because its party is now busy with that same expedition. Requests containing several independent invalid fields need only follow this precedence; field ordering within the same category is not graded.

## Examples

* A quest accepts 2–4 members of level 3 or higher. Three members at levels 3, 4, and 5 are eligible; two members at levels 2 and 5 are ineligible.
* Stock has one rope and two lanterns. Requesting one rope and two lanterns succeeds; requesting one rope and three lanterns allocates neither item.
* Key `sample-k1` with one rope and two lanterns creates an expedition. Replaying it with the two lines reversed returns that expedition. Replaying it with three lanterns returns `409 IDEMPOTENCY_CONFLICT`.
* If the fixed armory reports definitive unavailability before writing, show an error while retaining the player's selections. Do not display an accepted expedition.

## Boundaries and completion

Do not add cancellation, scheduling, consumables, authentication, rewards distribution, background reconciliation, GraphQL, or changes to the Go implementation. A fixed quest board, existing parties, and reusable equipment are sufficient.

Add tests covering the happy path, inclusive limits, every-member eligibility, atomic stock failure, normalized replay, key conflict, unknown IDs, unavailability, and UI pending/error behavior. Run the supplied checks and report actual observations. Do not claim independent acceptance based only on your own tests.
