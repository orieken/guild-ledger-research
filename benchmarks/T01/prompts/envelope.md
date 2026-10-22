# Common T01 envelope
Use the supplied Guild Ledger workspace and README for stack, commands, editable paths, fixtures, API shapes and visible tests. Change only `web/src/` and `services/guild/app.py`. Dependencies, infrastructure, fixtures and tests are fixed. Do not deploy, publish, commit or access external services. No live clarifications are available. If blocked on required human input, stop and report needs_human. Attempt limits are supplied by the external supervisor.

Inside the offline benchmark worker containers, run `python3 /opt/t01/visible_checks.py` for the common startup, API, UI and build checks. Docker/Compose commands in the workspace README are for standalone host workspaces; the worker tool requires neither Docker access nor dependency downloads.
