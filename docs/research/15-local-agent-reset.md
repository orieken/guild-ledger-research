# Local Claude and Codex clean-state reset

Completed at the user's explicit request after global Loom removal, including the user's follow-up choice to disable optional plugins/connectors. This changes the developer environment, not any benchmark outcome. Existing runtime discovery reports remain historical snapshots.

## Archived outside the repositories

Private recovery directory:

`/Users/oscarrieken/Projects/Rieken/guild-ledger/.local-backups/agent-clean-state-20261021T035433Z/`

The directory is owner-only and contains originals, configuration snapshots, an operation manifest and a verification receipt. Do not publish these contents; settings backups and project memories may contain personal data.

- Twelve stale/custom files and links were archived and removed: leftover home-level framework instruction links/backups, an old Claude state backup, three stale Claude framework backup links, the empty Codex-wide AGENTS file, and the saved command-rule file.
- The Codex rule file contained 152 remembered command-prefix allow rules. Removing it resets remembered approvals; it does not weaken sandbox or approval policy.
- Twelve Claude project-memory directories containing seventeen files were archived and removed. Conversation transcripts/history were retained.

## Disabled through configuration

| Surface | Result |
|---|---|
| Claude synced plugins | `engineering`, `data`, `searchfit-seo` disabled through user plugin preferences |
| Claude account connector fetching | Disabled in user settings |
| Claude auto-memory | Disabled in user settings |
| Codex optional plugins | All thirteen currently configured plugin entries disabled |
| Codex MCP | `node_repl` and `computer-use` disabled without deleting configuration or credentials |
| Codex memories | Feature, use and generation disabled |

The Claude bulk CLI disable command returned nonzero for this setup; explicit user-scoped plugin preferences were then written, and the fresh CLI plugin inventory verified every installed plugin disabled. Do not record the bulk command as successful.

Codex configuration was edited with a TOML-preserving parser, and unrelated parsed keys were checked unchanged. Claude display preferences were retained. App-managed notification/hook trust metadata was preserved; disabling plugin entries controls their optional components. Built-in/system skills remain installed as runtime-provided capabilities, not personal custom skills.

## Verification

- Fresh `claude mcp list`: no MCP servers configured.
- Fresh Claude plugin inventory: zero enabled plugins.
- Codex MCP inventory: both configured servers report `enabled: false`.
- Codex configuration: zero enabled plugin entries; memory flags false.
- No remaining personal command-rule files in the inspected Codex rules directory.
- No remaining Claude project-memory files in the inspected memory directories.
- Authentication files and both chat-history files remain present. Live SQLite databases, synced ChatGPT project sources, sessions, app state, research repositories and framework source were not deleted or reset.

## Restart and experimental limits

Fully quit and reopen the agent applications before starting fresh discovery or benchmark sessions. Existing chats retain prior context and may retain tools loaded earlier. User configuration does not automatically override every organization/workspace-managed or cloud-host-delivered feature. This reset verifies local terminal/configuration state, not a universal cloud/account reset.

Per-attempt isolation is still required: control instruction inputs, effective tools, runtime/model, account mode, local/project overrides and memory behavior explicitly. Do not claim H0 is admitted solely because personal global configuration has been cleaned. A plugin cache remaining on disk is not an enabled plugin; deleting active app databases or system skill bundles is not needed to remove these customizations.

## Recovery

Restore selected archived files/symlinks only after checking destinations for newer changes. Restore configuration selectively to avoid reverting unrelated future edits. No account connectors were disconnected, sign-ins revoked, app uninstalled, extra model sessions launched, commits created, or remote changes pushed.

Reference behavior: [Codex configuration](https://learn.chatgpt.com/docs/config-file/config-reference), [Claude MCP controls](https://code.claude.com/docs/en/mcp), and [Claude memory controls](https://code.claude.com/docs/en/memory). These document local controls; observed verification above concerns this machine.
