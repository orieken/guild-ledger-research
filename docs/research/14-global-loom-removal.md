# Global Loom removal

User explicitly requested removal after local runtime discovery. Completed at 2026-10-21T03:48Z (20 October 2026, America/Chicago). This is a developer-environment change, not an experimental outcome.

## Completed

- Uninstalled Homebrew formula `loom` v0.1.1; no Loom executable remains on the current PATH.
- Archived and unlinked 55 identified Loom-owned global files/symlinks across Claude, Cursor, Gemini/Antigravity, Copilot, Windsurf, JetBrains/Junie, and home-level framework entrypoints, including home-level `AGENTS.md`.
- Verified removal of the global framework marker and all planned active paths. A bounded scan of the audited global configuration locations found no active symlinks into the Loom source checkout.
- Preserved the framework source checkout, local modifications, all five research/harness repositories, credentials, personal Claude settings, sessions, and unrelated configuration. Legacy inert backup files were neither restored nor deleted.

The installed CLI could not uninstall the legacy global setup because its expected manifest was absent. The source shell uninstaller could restore prior framework symlinks and remove directories broadly, so it was not used. Instead, individual links were identified by source resolution and generated files by installed-revision matches or framework-specific attribution/structure; originals were archived before unlinking. Symlink targets were not deleted.

## Recovery record

Private archive outside the Git repositories:

`/Users/oscarrieken/Projects/Rieken/guild-ledger/.local-backups/loom-global-20261021T034807Z/`

It contains original files/symlinks, an ownership manifest, removed-path log, Homebrew output and verification receipt. Do not publish the backup as research data. Restoration must check for newly created destination files rather than blindly overwrite them. Restoring context files and reinstalling an executable are separate actions.

## Implication for the experiment

Earlier discovery reports remain unchanged as historical observations of the pre-removal environment. Newly launched sessions should no longer automatically inherit the removed global framework entrypoints; already running sessions may retain previously loaded instructions.

This does not certify a clean H0. Other account plugins, built-in runtime behavior, authentication, permissions, ancestor/project instructions, and future invocation settings still require explicit control. Validate the effective input catalog in a fresh isolated attempt.

H3 can later use a pinned, project-scoped framework package or separate research-local source build. Do not restore global context merely to enable one harness condition. No model calls, cloud workflows, commits or pushes were performed during removal.
