# Antigravity Runtime Discovery Evidence Archive

Captured: 2026-10-21T05:31:26Z (Session Start) / 2026-10-21T06:36:50Z (Probe Timestamp)  
Tool Surface: Antigravity IDE 2.5.5 (attended desktop IDE)  
Host: macOS Darwin 25.6.0 arm64  
Repository: `orieken/guild-ledger-research` (local checkout at `/Users/oscarrieken/Projects/Rieken/guild-ledger/guild-ledger-research`)

---

## 1. Observed Evidence Items (E01 – E16)

### E01: Process Ancestry and Execution Surface
- **Command:** `ps -p $$ -o pid,ppid,args; ps -p $PPID -o pid,ppid,args; ps -p 64171 -o pid,ppid,args; ps -p 64781 -o pid,ppid,args`
- **Exit Status:** 0
- **Redacted Output:**
  ```text
    PID  PPID ARGS
  90903 64781 zsh -c ...
    PID  PPID ARGS
  64781 64171 /Applications/Antigravity IDE.app/Contents/Resources/app/extensions/antigravity/bin/language_server_macos_arm ...
    PID  PPID ARGS
  64171     1 /Applications/Antigravity IDE.app/Contents/MacOS/Electron .
  ```
- **Finding:** The agent runs inside `Antigravity IDE.app`. Process tree originates at `launchd` (PID 1) -> `Electron` (PID 64171) -> `language_server_macos_arm` (PID 64781) -> `zsh` subshell. This confirms an attended desktop IDE surface, not a cloud VM, container, or standalone headless CLI session.

### E02: Application and Binary Metadata
- **Commands:**
  1. `cat "/Applications/Antigravity IDE.app/Contents/Info.plist" | grep -A 1 -E "CFBundleShortVersionString|CFBundleVersion|CFBundleIdentifier"`
     - Exit Status: 0
     - CFBundleIdentifier: `com.google.antigravity-ide`
     - CFBundleShortVersionString: `2.5.5`
     - CFBundleVersion: `2.5.5`
  2. `python3 -c 'import json; print(json.load(open("/Applications/Antigravity IDE.app/Contents/Resources/app/package.json"))["version"])'`
     - Exit Status: 0
     - Result: `1.107.0` (Core editor version based on VS Code)
  3. `python3 -c 'import json; print(json.load(open("/Applications/Antigravity IDE.app/Contents/Resources/app/extensions/antigravity/package.json"))["version"])'`
     - Exit Status: 0
     - Result: `0.2.0` (Antigravity extension)
  4. `md5 "/Applications/Antigravity IDE.app/Contents/Resources/app/extensions/antigravity/bin/language_server_macos_arm"`
     - Exit Status: 0
     - Result: `MD5 = 4cce31914fcf08f689da569e00e3b303`

### E03: Environment Variables Inspection
- **Command:** `python3` inspecting `os.environ` keys matching `ANTIGRAVITY_*` and `VSCODE_*`
- **Exit Status:** 0
- **Redacted Output:**
  ```text
  ANTIGRAVITY_AGENT=1
  ANTIGRAVITY_AGENTAPI_EXE=/Applications/Antigravity IDE.app/Contents/Resources/app/extensions/antigravity/bin/language_server_macos_arm
  ANTIGRAVITY_CONVERSATION_ID=299c055d-0914-4b64-b8e6-3601f0308fac
  ANTIGRAVITY_CSRF_TOKEN=[REDACTED: len=36]
  ANTIGRAVITY_EDITOR_APP_ROOT=/Applications/Antigravity IDE.app/Contents/Resources/app
  ANTIGRAVITY_LS_ADDRESS=localhost:62669
  ANTIGRAVITY_LS_VERSION=ide-2.4.5
  ANTIGRAVITY_SAFECLIS_SOURCE=/Users/oscarrieken/.gemini/antigravity-ide/bin/safeclis/src
  ANTIGRAVITY_SOURCE_METADATA={"tool":{"conversationId":"299c055d-0914-4b64-b8e6-3601f0308fac","stepIndex":127,"toolCall":{"id":"call_1139402","name":"run_command", ... "thinkingSignature":"..."}}}
  ANTIGRAVITY_TRAJECTORY_ID=a56e9152-5ffe-4570-b5b7-6ce6cde07275
  VSCODE_CWD=/Users/oscarrieken/Projects/Rieken/guild-ledger
  VSCODE_PID=64171
  ```
- **Finding:** Language server daemon version is `ide-2.4.5`. The tool execution context receives full JSON source metadata per tool invocation including conversation ID, step index, tool call ID, and encrypted thinking signature.

### E04: Language Server Daemon and Network Sockets
- **Command:** `ps -ww -p 64781; lsof -Pan -p 64781 -i; lsof -Pan -p 64171 -i`
- **Exit Status:** 0
- **Redacted Command Line:**
  ```text
  /Applications/Antigravity IDE.app/Contents/Resources/app/extensions/antigravity/bin/language_server_macos_arm \
    --csrf_token [REDACTED: 36 chars] \
    --extension_server_port 62662 \
    --extension_server_csrf_token [REDACTED: 36 chars] \
    --app_data_dir antigravity-ide \
    --subclient_type ide \
    --cloud_code_endpoint https://cloudcode-pa.googleapis.com
  ```
- **Redacted Sockets:**
  - PID 64781 (language server) listens on TCP 127.0.0.1:62668 and 127.0.0.1:62669 (`ANTIGRAVITY_LS_ADDRESS`).
  - PID 64781 connects to Electron IPC on 127.0.0.1:62662.
  - Outbound HTTPS connections to Google Cloud endpoints: `34.54.84.110:443`, `172.217.115.4:443`, `172.217.114.4:443`.
- **Finding:** Language server routes inference and control through `https://cloudcode-pa.googleapis.com` and Google Cloud services. Local IPC is bridged to Electron.

### E05: CLI and Executable Inventory
- **Commands:**
  1. `which agy`
     - Exit Status: 127 (`agy not found`)
  2. `ls -la /Users/oscarrieken/.gemini/antigravity-ide/bin/agentapi`
     - Exit Status: 0 (`POSIX shell script text executable`, 141 bytes)
  3. `cat /Users/oscarrieken/.gemini/antigravity-ide/bin/agentapi`
     - Exit Status: 0
     - Contents: `exec "/Applications/Antigravity IDE.app/Contents/Resources/app/extensions/antigravity/bin/language_server_macos_arm" agentapi "$@"`
  4. `agentapi --help`
     - Exit Status: 0
     - Commands: `get-conversation-metadata <conversation_id>`, `new-conversation [--model=<flash_lite|flash|pro>] [--title=<title>] [--profile=<profile>] <prompt>`, `send-message [--title=<title>] <recipient_id> <content>`
- **Finding:** The standalone `agy` CLI is not installed on PATH. However, an `agentapi` CLI wrapper is available in `~/.gemini/antigravity-ide/bin/agentapi`. It directly interfaces with `language_server_macos_arm`.

### E06: Programmatic Conversation Metadata
- **Command:** `agentapi get-conversation-metadata 299c055d-0914-4b64-b8e6-3601f0308fac`
- **Exit Status:** 0
- **Redacted Output:**
  ```json
  {
    "response": {
      "conversationMetadata": {
        "metadata": {
          "workspaces": [
            {
              "workspaceFolderAbsoluteUri": "file:///Users/oscarrieken/Projects/Rieken/guild-ledger",
              "gitRootAbsoluteUri": "",
              "branchName": ""
            }
          ],
          "createdAt": "2026-10-21T05:31:26.719337Z",
          "initializationStateId": "7abc2de6-f148-4d88-aa39-9d0f1b11a653",
          "parentConversationId": "",
          "rootConversationId": "299c055d-0914-4b64-b8e6-3601f0308fac",
          "workspaceUris": [
            "file:///Users/oscarrieken/Projects/Rieken/guild-ledger"
          ],
          "nestingDepth": 0,
          "mendelExperimentIds": [
            101551624, 101868197, 103012592, "...", 106865006
          ]
        }
      }
    }
  }
  ```
- **Finding:** Metadata provides conversation IDs, timestamps, workspace URIs, and 94 Google internal Mendel A/B experiment flag IDs.

### E07: Conversation SQLite Database Inspection
- **Command:** `sqlite3 /Users/oscarrieken/.gemini/antigravity-ide/conversations/299c055d-0914-4b64-b8e6-3601f0308fac.db` inspecting schema, `trajectory_meta`, and `gen_metadata` blobs.
- **Exit Status:** 0
- **Schema:**
  - Tables: `trajectory_meta`, `steps`, `gen_metadata`, `executor_metadata`, `parent_references`, `trajectory_metadata_blob`, `battle_mode_infos`.
- **Blob String Extraction (gen_metadata row 0):**
  - Observed strings: `sessionID: -3750763034362895579`, `gemini-3.8-flash-n`, `model_enum: MODEL_PLACEHOLDER_M318`, `trajectory_id: a56e9152-5ffe-4570-b5b7-6ce6cde07275`, label `Gemini 3.8 Flash (High)`.
- **Telemetry Query:** A regex search for token/cost/usage metrics across `steps` and `gen_metadata` yielded 0 metric entries (matches were conversational text and prompt strings only).
- **Finding:** Internal model string is `gemini-3.8-flash-n` with enum `MODEL_PLACEHOLDER_M318`. No token counts or monetary costs are persisted in the conversation SQLite database.

### E08: Transcript Analysis (transcript.jsonl)
- **Command:** Python script reading `/Users/oscarrieken/.gemini/antigravity-ide/brain/299c055d-0914-4b64-b8e6-3601f0308fac/.system_generated/logs/transcript.jsonl`
- **Exit Status:** 0
- **Structure:**
  - Total entries at inspection: 77.
  - Entry types: `USER_INPUT`, `CONVERSATION_HISTORY`, `KNOWLEDGE_ARTIFACTS`, `VIEW_FILE`, `PLANNER_RESPONSE`, `LIST_DIRECTORY`, `CHECKPOINT`, `GREP_SEARCH`, `RUN_COMMAND`, `ERROR_MESSAGE`.
  - Top-level keys: `['content', 'created_at', 'error', 'exit_code', 'source', 'status', 'step_index', 'thinking', 'tool_calls', 'truncated_fields', 'type']`.
  - Token/Usage search: All keys matching `token`, `cost`, `usage`, `billing` yielded `set()` (empty).
- **Finding:** Token usage and costs are completely absent from the local transcript files.

### E09: Rules, Knowledge, and MCP Configuration Checks
- **Commands:**
  1. `ls -la ~/.gemini/GEMINI.md` -> 0 bytes (empty file).
  2. `ls -la ~/.gemini/antigravity-ide/rules/` -> 0 files (points to empty `~/.claude/rules`).
  3. `ls -la ~/.gemini/config/mcp_config.json` -> 0 bytes.
  4. `ls -la ~/.gemini/antigravity-ide/knowledge/` -> only `knowledge.lock` (0 bytes).
  5. `cat ~/.gemini/config/config.json` -> contains `globalPermissionGrants` (29 allowed patterns: `git diff`, `ls`, `grep`, `mkdir`, `npm run`, `just test`, `uv`, etc.) and `themeMode: "THEME_MODE_DARK"`.
- **Finding:** No active user rules, project rules, KIs, or MCP servers are configured.

### E10: Plugins and Skills Catalog
- **Command:** `ls -la ~/.gemini/config/plugins`
- **Exit Status:** 0
- **Plugins Observed:**
  - `chrome-devtools-plugin`
  - `firebase`
  - `google-antigravity-sdk`
  - `modern-web-guidance-plugin`
  - `science`
- **Skills:** Total of 41 skills exposed across plugins, plus 2 built-in skills (`antigravity_guide`, `agy-customizations`).
- **Finding:** Skills follow progressive disclosure (only name/description in prompt; `SKILL.md` loaded on demand via `view_file`).

### E11: Browser Domain Allowlist
- **Command:** `cat /Users/oscarrieken/.gemini/antigravity-ide/browserAllowlist.txt`
- **Exit Status:** 0
- **Finding:** Contains 78 allowed domains (`github.com`, `gitlab.com`, `cloud.google.com`, `localhost`, etc.). Browser interactions outside this list are blocked.

### E12: Loom Status Check
- **Command:** `which loom; ls -la /opt/homebrew/bin/loom; ls -la .local-backups/loom-global-20261021T034807Z`
- **Exit Status:** 127
- **Finding:** Loom executable is absent from PATH. It was uninstalled from Homebrew and backed up to `.local-backups/loom-global-20261021T034807Z` during cleanup at 03:48:07Z.

### E13: Scratch Edit Probe
- **Command:**
  ```sh
  mkdir -p guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z && \
  echo "antigravity-edit-probe 2026-10-21T06:36:50Z" > guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/.scratch-edit-probe.txt && \
  cat guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/.scratch-edit-probe.txt && \
  rm guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/.scratch-edit-probe.txt
  ```
- **Exit Status:** 0
- **Output:** `antigravity-edit-probe 2026-10-21T06:36:50Z`
- **Finding:** Local editing in the destination folder succeeded; scratch probe file was verified and removed cleanly.

### E14: Python SDK Verification
- **Command:** `python3 -c "import google.antigravity"`
- **Exit Status:** 1
- **Error:** `ModuleNotFoundError: No module named 'google.antigravity'`
- **Finding:** The public Python SDK is not installed in the default system Python environment.

### E15: Git Working Tree State
- **Commands:**
  1. `git status` in `/Users/oscarrieken/Projects/Rieken/guild-ledger` -> Exit 128 (`fatal: not a git repository`).
  2. `git status` in `/Users/oscarrieken/Projects/Rieken/guild-ledger/guild-ledger-research` -> Exit 0 (On branch `main`, untracked `README.md`, `docs/`, `repositories.json`, no commits yet).
- **Finding:** Repository root `guild-ledger-research` contains the research assets and documentation tree.

### E16: Task Interruption and Cancellation
- **Command:** Background language server probe launched as `task-98`, then cancelled via `manage_task(Action='kill', TaskId='299c055d-0914-4b64-b8e6-3601f0308fac/task-98')`.
- **Exit Status:** Context cancelled.
- **Artifact:** Crash log written to `/Users/oscarrieken/.gemini/antigravity-ide/crashes/crash_96459_6e61648b-9cd4-4419-87b0-a7e18b324f0a.log`. Partial log preserved in `.system_generated/tasks/task-98.log`.
- **Finding:** Cancellation via Go context cleanly terminates subprocesses and records exit events.

---

## 2. Documented Evidence Items (D01 – D06)

| ID | Title / Resource | Canonical Reference | Retrieval Date | Summary of Relevant Guidance |
|---|---|---|---|---|
| D01 | Antigravity Main Documentation | `https://antigravity.google/docs` | 2026-10-21 | System overview, architecture, surfaces (IDE, 2.0 Desktop, CLI, SDK). |
| D02 | Antigravity CLI Reference | `https://antigravity.google/docs/cli/reference` | 2026-10-21 | Documents `agy` CLI flags, slash commands, configuration via `~/.gemini/antigravity-cli/settings.json`. |
| D03 | Antigravity Browser Automation | `https://antigravity.google/docs/ide/browser` | 2026-10-21 | Browser subagent, WebP recording artifact generation, domain allowlist rules. |
| D04 | Agent Permissions & Security | `https://antigravity.google/docs/permissions` | 2026-10-21 | Tool execution policies (`always-proceed`, `request-review`, `strict`, `proceed-in-sandbox`), non-workspace file access policies, allowlist/denylist rules. |
| D05 | Google Antigravity Python SDK | `https://github.com/google-antigravity/antigravity-sdk-python` | 2026-10-21 | Public SDK interface: `Agent`, `LocalAgentConfig`, `CapabilitiesConfig`, streaming tokens, thoughts, tool calls, and `UsageMetadata` (`total_usage`). |
| D06 | Gemini Model Documentation | `https://ai.google.dev/gemini-api/docs/models/gemini` | 2026-10-21 | Official Gemini model identifiers, reasoning/thinking capabilities, token limits. |

---

## 3. Explicit Inventory of What Was NOT Tested

In strict compliance with the discovery prompt guidelines:
1. **No benchmark tasks or code evaluation:** No coding tasks or benchmark suites were run.
2. **No configuration changes:** User settings, plugins, rules, and global configuration files were left untouched.
3. **No Loom pipeline execution:** Loom was not reinstalled or executed.
4. **No additional model sessions or agents spawned:** No child subagents were created; no parallel conversations were started.
5. **No git mutations:** No branches created, no files committed, pushed, or merged.
6. **No paid API usage:** No external paid API keys were used or billed.
