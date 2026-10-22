# Antigravity Runtime Discovery Report

**Captured:** 2026-10-21T05:31:26Z (Session Start) / 2026-10-21T06:36:50Z (Verification Probe)  
**Tool Surface:** `antigravity` (Antigravity IDE 2.5.5, attended desktop IDE)  
**Destination:** `guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/`  
**Schema Version:** `guild-ledger.runtime-discovery/v1-draft`  
**Status:** Discovery only. No benchmark, no paid run, no unapproved live probe, no subagent spawn, no Loom execution, no setting modification, no commit, and no push.

Evidence references (`E01`–`E16`, `D01`–`D06`) link directly to [evidence.md](evidence.md). Machine-readable capability definitions are in [capabilities.json](capabilities.json).

---

## 1. Scope, Surface, and Model Identity

### Surface Verification and Process Provenance
- **Observed [E01, E02, E04]:** This session executes inside the standalone desktop application **Antigravity IDE** (`CFBundleIdentifier: com.google.antigravity-ide`, version `2.5.5`). The core editor is a customized fork of VS Code `1.107.0`, hosting the `antigravity` extension (`0.2.0`).
- **Process Hierarchy [E01]:** Execution ancestry traces directly from the OS supervisor:
  `launchd (PID 1)` → `Electron (PID 64171, /Applications/Antigravity IDE.app)` → `language_server_macos_arm (PID 64781)` → `zsh (tool execution subshell)`.
  This is a local, attended IDE desktop surface. It is **not** a cloud container, **not** a remote VM, and **not** a standalone headless CLI run.
- **Local vs. Hosted Execution [E01, E04]:** Tool invocations (file system edits, terminal commands, directory scans) execute locally on macOS Darwin 25.6.0 arm64 under the user account (`oscarrieken`). Model inference is hosted: the language server daemon connects via outbound TLS to Google Cloud endpoints (`34.54.84.110:443`, `172.217.115.4:443`, `172.217.114.4:443`) and the Cloud Code endpoint `https://cloudcode-pa.googleapis.com`.

### Model Identity, Reasoning Effort, and Pinning Controls
- **Observed [E03, E07]:**
  - **User Configured Label:** `Gemini 3.8 Flash (High)` (selected via IDE model picker).
  - **Human-Readable Name:** Gemini 3.8 Flash with high reasoning effort.
  - **Internal Model Identifier:** Direct inspection of the session's SQLite database (`gen_metadata` row 0) reveals the internal variant string `gemini-3.8-flash-n` and `model_enum: MODEL_PLACEHOLDER_M318`.
  - **Reasoning Effort:** High reasoning effort. Internal thinking signatures are carried in `ANTIGRAVITY_SOURCE_METADATA` (`thinkingSignature`).
- **Documented, Available Tiers [E05, D06]:** The CLI wrapper `agentapi` accepts `--model=<flash_lite|flash|pro>`. The IDE settings menu allows toggling between Flash, Pro, and Flash-Lite variants.
- **Unknown / Absent [E04, E07]:** **No dated snapshot identifier** (e.g. `gemini-3.8-flash-001`) or immutable backend commit hash is exposed. The researcher cannot pin a specific dated backend snapshot through the IDE UI or `agentapi`. Backend model revision pinning is **unknown and unverified**.

---

## 2. Automation Interfaces

| Interface | Status | Mechanism & Findings | Evidence |
|---|---|---|---|
| **Create Fresh Task** | Documented / Observed | `agentapi new-conversation [--model=<flash_lite|flash|pro>] [--title=<title>] [--profile=<profile>] <prompt>`. Present at `/Users/oscarrieken/.gemini/antigravity-ide/bin/agentapi`. Wraps `language_server_macos_arm`. | E05 |
| **Supply Workspace / Prompt** | Observed | Workspace is bound at conversation start (`file:///Users/oscarrieken/Projects/Rieken/guild-ledger`). `agentapi` inherits caller CWD or active workspace. | E03, E06 |
| **Observe Progress** | Observed | IDE canvas displays streaming output. Structured steps are written synchronously to `~/.gemini/antigravity-ide/brain/<conv-id>/.system_generated/logs/transcript.jsonl` and persisted in SQLite DB. | E07, E08 |
| **Stop / Cancel** | Observed | IDE Stop button halts generation. Background commands are terminated via `manage_task(Action='kill')` (verified via Go context cancellation on `task-98`). SIGINT/SIGTERM cleanly terminates tool child processes. | E16 |
| **Retrieve Changes** | Observed | Changes are applied directly to the local filesystem working tree. Artifacts are written to `~/.gemini/antigravity-ide/brain/<conv-id>/`. | E08, E13 |
| **Standalone CLI (`agy`)** | Documented, Not Installed | `which agy` returned 127 (`command not found`). The standalone terminal CLI described in official documentation is not on PATH. | E05, D02 |
| **Python SDK** | Documented, Not Installed | `google-antigravity` is published on GitHub/PyPI, providing `Agent(config)` and async streaming. `python3 -c "import google.antigravity"` failed with `ModuleNotFoundError`. | E14, D05 |

**Headless Automation Summary:** While an `agentapi` wrapper exists on this machine, it is a lightweight conversation launcher and metadata inspector. It lacks headless streaming flags (e.g. `--output-format stream-json`), explicit turn caps (`--max-turns`), budget bounds (`--max-budget-usd`), or non-interactive batch runners comparable to headless CLI environments.

---

## 3. Effective Instructions, Customizations, and Inherited State

```
+--------------------------------------------------------------------------------+
|                         Effective Instruction Hierarchy                        |
+--------------------------------------------------------------------------------+
|  [Mandatory Host] Language Server Hardcoded System Prompt & Safety Boundaries  |
|         ↓                                                                      |
|  [User Rules]     ~/.gemini/GEMINI.md (0 bytes - EMPTY)                        |
|                   ~/.gemini/antigravity-ide/rules -> ~/.claude/rules (EMPTY)   |
|         ↓                                                                      |
|  [Project Rules]  None. (No GEMINI.md, AGENTS.md, or .agents/ in workspace)    |
|         ↓                                                                      |
|  [Plugins/Skills] 5 global plugins in ~/.gemini/config/plugins/                |
|                   Exposes 41 on-demand skills (progressive disclosure)         |
|         ↓                                                                      |
|  [Memory / KI]    Knowledge Items: ~/.gemini/antigravity-ide/knowledge (EMPTY) |
|         ↓                                                                      |
|  [MCP Servers]    ~/.gemini/config/mcp_config.json (0 bytes - EMPTY)           |
+--------------------------------------------------------------------------------+
```

- **User and Project Rules [E09]:** Both `~/.gemini/GEMINI.md` and the rules symlink directory are completely empty, verifying that the previous agent reset preserved clean rule state. No project-level `GEMINI.md`, `AGENTS.md`, or `.agents/` folder exists in `guild-ledger` or `guild-ledger-research`.
- **Global Plugins and Skills [E10]:** Five plugins are installed in `~/.gemini/config/plugins/`: `chrome-devtools-plugin`, `firebase`, `google-antigravity-sdk`, `modern-web-guidance-plugin`, and `science`. Together with built-ins, they expose 41 skills. Skills operate under **progressive disclosure**: only descriptions are injected into the base prompt; the full body (`SKILL.md`) is loaded only if explicitly read.
- **Memory and MCP [E09]:** No active Knowledge Items (KIs) exist on disk (`knowledge.lock` is 0 bytes). `mcp_config.json` is empty (0 bytes); no MCP server tools are registered.
- **Permissions and Approvals [E05, E09, E11]:**
  - `~/.gemini/config/config.json` specifies `globalPermissionGrants` allowing 29 command/read patterns (e.g. `git diff`, `ls`, `grep`, `npm run`, `just test`).
  - Browser access is strictly constrained by `browserAllowlist.txt` (78 allowed domains).
  - Hardcoded safety boundary rules enforce read blocks on sensitive system executables (e.g., `read_file` on binary `agentapi` was denied by a hardcoded boundary rule).

---

## 4. Usage Evidence and Telemetry

- **Session and Trajectory Identifiers [E03, E06, E07]:**
  - **Conversation ID:** `299c055d-0914-4b64-b8e6-3601f0308fac` (UUID)
  - **Trajectory ID:** `a56e9152-5ffe-4570-b5b7-6ce6cde07275` (UUID)
  - **Internal Session ID:** `-3750763034362895579` (numeric)
  - **Initialization State ID:** `7abc2de6-f148-4d88-aa39-9d0f1b11a653`
  - **Tool Call IDs:** Unique step-level strings (e.g. `call_1139402`).
- **Transcript Schema [E08]:**
  - Logs are written to `~/.gemini/antigravity-ide/brain/<conv-id>/.system_generated/logs/transcript.jsonl`.
  - Keys per line: `step_index`, `source`, `type`, `status`, `created_at`, `content`, `thinking`, `tool_calls`, `exit_code`.
- **Token and Usage Tracking [E07, E08]:**
  - **CRITICAL FINDING: ZERO TOKEN TELEMETRY.** An exhaustive search across `transcript.jsonl`, `transcript_full.jsonl`, and all SQLite database tables (`gen_metadata`, `steps`, `trajectory_meta`) revealed **no prompt tokens, candidates tokens, cached tokens, reasoning tokens, or financial cost fields**.
  - All occurrences of the words "token" or "usage" in the SQLite DB were conversational text or prompt excerpts, not system-emitted metrics.
- **Documented SDK Telemetry [D05]:** In the Python SDK, `agent.conversation.total_usage` is documented to provide `prompt_token_count`, `cached_content_token_count`, `candidates_token_count`, `thoughts_token_count`, and `total_token_count`. That telemetry is not exposed on this IDE surface.

---

## 5. Billing, Accounting, and Costs

- **Authentication and Account Mode [E03, E04]:** The IDE authenticates via Google account Single Sign-On against `https://cloudcode-pa.googleapis.com` using local CSRF/OAuth credentials. It does not use a metered `GEMINI_API_KEY`.
- **Attributable Billed Charges [E07, E08]:** **Zero monetary metrics are exposed.** No per-turn cost, accumulated cost, subscription quota deduction, or invoice allocation is accessible.
- **Quota Conversion:** No formula or conversion method exists to turn internal Cloud Code requests into USD amounts. Substituting speculative API list-price calculations is explicitly rejected as ungrounded.
- **Study Implication:** For the Guild Ledger experiment, per-attempt USD cost for Antigravity IDE runs cannot be computed from local telemetry. Cost must be marked `null` or `unknown` unless Google Cloud project audit billing is separately configured and reconciled.

---

## 6. Harness Compatibility Assessment

| Harness Level | Claim Status | Assessment | Blockers & Requirements |
|---|---|---|---|
| **H0 (No added rules)** | Inferred [E09, E10] | **Candidate / Partial** | User and project rules are empty, but 5 global plugins (41 skills) are loaded in `~/.gemini/config/plugins/`. Achieving pure H0 requires isolating or temporarily unlinking the global plugins directory. |
| **H1 (Fixed guidelines)** | Inferred [E09] | **Feasible** | Can be supplied via a single committed `GEMINI.md` or `AGENTS.md` at repository root. Discovered automatically during hierarchical path walk. |
| **H2 (Bounded workflow)** | Inferred [E05, D05] | **Feasible (External)** | Step-by-step planning and artifact review are native to the IDE. However, hard turn bounds and budget caps require external watchdog supervision since `agentapi` lacks `--max-turns` and `--max-budget-usd`. |
| **H3 (Loom Context-Only)** | Inferred [E09] | **Feasible** | Loom guidelines and reference bundles can be committed as project rule files or context documents. |
| **H3 (Loom Native Pipeline)** | Observed [E12] | **Blocked** | Loom executable is uninstalled (`which loom` returned 127). Even if reinstalled, Loom v0.1.1 lacked pipeline run commands and has no native Antigravity IDE execution adapter. |

---

## 7. Export, Retention, and Isolation

- **Filesystem Isolation [E01, E13]:** Non-containerized. Tool commands run with macOS user permissions. Edits are applied in-place to the local workspace.
- **Network Isolation [E04, E11]:** No egress proxy or network sandbox. The language server maintains persistent outbound connections to Google Cloud. Browser subagents are restricted to the 78 domains in `browserAllowlist.txt`; HTTP read tools (`read_url_content`, `search_web`) operate without domain allowlists.
- **Retention [E07, E08]:** Conversations and step trajectories are permanently stored in local SQLite databases (`~/.gemini/antigravity-ide/conversations/`) and JSONL files (`~/.gemini/antigravity-ide/brain/`). Remote data retention on Google servers is governed by Google Terms of Service and Cloud Code policies.
- **Controls Unavailable to Researcher:**
  1. Cannot pin exact dated backend model snapshots.
  2. Cannot inspect raw token usage (prompt/candidate/thinking) from local telemetry.
  3. Cannot disable the mandatory language server base system prompt.
  4. Cannot enforce hard dollar or token spend limits natively via CLI flags.

---

## 8. Three Largest Measurement and Control Gaps

1. **Zero Observable Token and Cost Telemetry in IDE Surface [E07, E08]:**  
   Neither `transcript.jsonl` nor the SQLite database exposes prompt, completion, cached, or reasoning token counts, and no financial cost is tracked.
2. **No Backend Model Snapshot Pinning [E04, E07]:**  
   The platform exposes model family aliases and effort labels (`Gemini 3.8 Flash (High)`), but provides no immutable dated snapshot ID or commit hash to guarantee reproducible model weights over time.
3. **Absence of Headless Batch Execution and Spend Bounding [E05, E14]:**  
   The surface is an interactive, attended IDE. While `agentapi` can start conversations, it lacks headless streaming, output schema enforcement, turn limits, and budget caps necessary for autonomous, controlled benchmark harness execution.

---

## 9. Recommended Next Probe — Proposed, Not Run

- **Purpose:** Test whether `agentapi new-conversation` can be programmatically executed from an external script in an isolated disposable directory, and verify whether a newly initialized conversation records token telemetry in its database.
- **Inputs:** Disposable directory (`/tmp/antigravity-probe-<timestamp>`), synthetic prompt (`{"action": "ping"}`), flag `--model=flash_lite`.
- **Expected Evidence:** Exit status, returned conversation ID, metadata output via `agentapi get-conversation-metadata <id>`, SQLite database schema and row inspection for token fields.
- **Maximum Calls:** Exactly 1 `agentapi new-conversation` invocation and 1 `agentapi get-conversation-metadata` call.
- **Time / Spend Bounds:** 30 seconds maximum execution time; $0 attributable spend (internal quota / subscription).
- **Enforcement Mechanism:** External Python supervisor with `subprocess.run(..., timeout=30)` and SIGKILL watchdog.
- **Overshoot Risks:** Language server background inference continuing after client process termination; quota exhaustion if looped.

---

## 10. Reproduction and Validation Steps

1. Verify process hierarchy: `ps -p $$ -o pid,ppid,args; ps -p $PPID -o pid,ppid,args`.
2. Inspect IDE application metadata: `cat "/Applications/Antigravity IDE.app/Contents/Info.plist"`.
3. Check environment variables: `python3 -c "import os; [print(k, os.environ[k]) for k in os.environ if 'ANTIGRAVITY' in k]"`.
4. Inspect conversation database: `sqlite3 ~/.gemini/antigravity-ide/conversations/<conv-id>.db "SELECT * FROM trajectory_meta;"`.
5. Verify scratch edit probe: created and removed `.scratch-edit-probe.txt` inside destination folder (verified in E13).
6. Validate JSON output: `python3 -m json.tool capabilities.json > /dev/null`.
7. Leave all changes uncommitted.
