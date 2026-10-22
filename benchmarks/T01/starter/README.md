# Guild Ledger — T01 canonical starter

Implement the supplied quest-browser assignment. This starter intentionally returns 501 from the two quest routes and contains a placeholder UI. Feature tests start red; that is not an infrastructure failure.

Prerequisites: Docker with Compose, Python 3.10+, Make. Ports: UI 15173, Guild 18000, Armory 18001, bound to localhost. Run only one copy on these ports at a time.

- `make up`: build and wait for all three health checks.
- `make test-startup`: green infrastructure checks, no quest implementation required.
- `make test-visible`: API checks then UI component tests (stops at first failed suite).
- `make test-web`: run the UI component checks alone.
- `docker compose run --rm --no-deps web npm run build`: TypeScript and production build.
- `make reset`: remove Compose resources/volumes and recreate the original fixture-backed state; this does not revert source edits.
- `make down`: stop and remove this workspace's containers.

The fixed input is `fixtures/quests.json`. No database or write operation is needed in this read-only task. PostgreSQL and reservation operations belong to subsequent task snapshots. The Go service currently exposes health only.

Change `web/src/` and `services/guild/app.py`; tests, fixtures, lockfiles and infrastructure are fixed experiment inputs. The API uses `/api/quests` and `/api/quests/{quest_id}`. The list response is `{ "quests": [quest, ...] }`; detail is a quest object. Use same-origin `/api` requests from the UI; Vite forwards them to Guild. Quest fields and enum values appear in the fixture. Common error format is `{ "error": { "code": "...", "message": "..." } }`.

Visible tests are available to every prompt/harness condition. They are examples, not a complete acceptance evaluator. A view-details control has accessible button name `View <quest title>`. List failures expose a nonempty `role="alert"`. These are common interface contracts.
