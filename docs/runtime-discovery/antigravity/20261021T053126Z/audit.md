# Antigravity Runtime Discovery Audit

**Audit Date:** 2026-10-21T05:31:26Z (Session Start) / 2026-10-21T06:36:50Z (Verification Probe)  
**Auditor / Agent:** Antigravity Coding Agent (executed inside Antigravity IDE)  
**Target Environment:** Antigravity IDE 2.5.5 on macOS Darwin 25.6.0 arm64  
**Workspace:** `/Users/oscarrieken/Projects/Rieken/guild-ledger`  
**Repository:** `orieken/guild-ledger-research` (local checkout at `guild-ledger-research`)  
**Audit Artifacts Folder:** `guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/`  
**Companion Documents:**
- [`report.md`](report.md)
- [`capabilities.json`](capabilities.json)
- [`evidence.md`](evidence.md)

---

## 1. Executive Disposition

**Candidate interactive IDE surface; not currently viable as an autonomous, metered benchmark harness.**

The Antigravity coding-agent environment operates as an attended, in-editor IDE pair programmer. It executes shell and filesystem tools locally with full user permissions while routing model inference and agent orchestration through an internal Google Cloud Code daemon.

While the environment exhibits strong local execution capabilities, zero personal rule contamination, and clean context cancellation mechanics, it currently cannot be admitted as an unassisted experimental harness for the Guild Ledger study due to three structural blockers:
1. **Total Absence of Token Telemetry:** Neither local transcripts (`transcript.jsonl`) nor the conversation SQLite database records prompt tokens, completion tokens, cached tokens, reasoning tokens, or financial cost.
2. **No Backend Model Snapshot Pinning:** Model selection is constrained to broad family labels (`Gemini 3.8 Flash (High)`). No dated immutable snapshot (e.g. `gemini-3.8-flash-001`) or backend deployment hash is observable or pinnable.
3. **Lack of Headless Batch Execution & External Spend Bounding:** The available CLI wrapper (`agentapi`) supports basic conversation launching and metadata inspection, but lacks headless token streaming, output schemas, turn limits, or budget caps.

---

## 2. Comprehensive Audit by Experimental Axis

### Axis 1: Exact Surface, Process Provenance, and Model Identity
- **Surface Classification:** Attended Desktop IDE (`antigravity-ide/desktop-attended`).
- **Process Lineage (Observed [E01]):**
  ```text
  launchd (PID 1)
    └── /Applications/Antigravity IDE.app/Contents/MacOS/Electron (PID 64171)
          └── language_server_macos_arm (PID 64781, ide-2.4.5)
                └── zsh (PID 90903, tool execution subshell)
  ```
- **App and Component Versions (Observed [E02]):**
  - App Bundle: `com.google.antigravity-ide` v2.5.5
  - Core Editor: VS Code fork v1.107.0
  - Extension: `antigravity` v0.2.0
  - Language Server Daemon: `language_server_macos_arm` (MD5: `4cce31914fcf08f689da569e00e3b303`), reporting `ANTIGRAVITY_LS_VERSION=ide-2.4.5`.
- **Model Identity & Effort (Observed [E03, E07]):**
  - Selected Label: `Gemini 3.8 Flash (High)`
  - Internal DB Variant: `gemini-3.8-flash-n` (`model_enum: MODEL_PLACEHOLDER_M318`)
  - Reasoning Effort: High reasoning effort with encrypted thinking signatures (`thinkingSignature`) passed in tool metadata.
- **Pinning Controls (Unknown [E05, E07, D06]):** Broad tier overrides exist (`flash_lite`, `flash`, `pro`). No immutable dated snapshot identifier or commit hash is exposed or pinnable by the researcher.

### Axis 2: Automation Interfaces and Headless Capability
- **CLI Availability (Observed [E05]):**
  - Standalone `agy` CLI is **not installed** on PATH (`which agy` returned exit code 127).
  - Local wrapper `/Users/oscarrieken/.gemini/antigravity-ide/bin/agentapi` is present, wrapping `language_server_macos_arm agentapi "$@"`.
  - Available subcommands: `new-conversation`, `get-conversation-metadata`, `send-message`.
- **Python SDK (Documented, Not Installed [E14, D05]):**
  - Package `google-antigravity` is published on GitHub/PyPI, offering `Agent(config)`, streaming tokens, thoughts, tool calls, and `agent.conversation.total_usage`.
  - Verified that `python3 -c "import google.antigravity"` fails with `ModuleNotFoundError`.
- **Progress Observation (Observed [E07, E08]):**
  - Interactive chat canvas in the IDE.
  - Synchronous JSON Lines step log appended to `~/.gemini/antigravity-ide/brain/<conv-id>/.system_generated/logs/transcript.jsonl`.
  - SQLite database updated at `~/.gemini/antigravity-ide/conversations/<conv-id>.db`.
- **Stopping / Cancellation (Observed [E16]):**
  - Background processes killed via `manage_task(Action='kill')` terminate cleanly via Go context cancellation, recording exit state in crash logs (`crashes/crash_*`).
  - IDE Stop button cancels in-flight turn generation.

### Axis 3: Instructions, Customizations, and Inherited State
- **User Rules (Observed [E09]):**
  - `~/.gemini/GEMINI.md`: 0 bytes (empty).
  - `~/.gemini/antigravity-ide/rules`: Symlink pointing to `/Users/oscarrieken/.claude/rules`, which is completely empty (cleaned up during prior agent reset).
- **Project Rules (Observed [E09]):**
  - No `GEMINI.md`, `AGENTS.md`, or `.agents/` directory exists in `guild-ledger` or `guild-ledger-research`.
- **Global Plugins and Skills (Observed [E10]):**
  - 5 plugins installed in `~/.gemini/config/plugins/`: `chrome-devtools-plugin`, `firebase`, `google-antigravity-sdk`, `modern-web-guidance-plugin`, `science`.
  - 41 skills exposed in prompt context via **progressive disclosure** (only names and descriptions loaded initially; full `SKILL.md` loaded on demand via `view_file`).
- **Memory / Knowledge Items (Observed [E09]):**
  - `~/.gemini/antigravity-ide/knowledge/`: Contains only `knowledge.lock` (0 bytes). Zero active KIs.
- **MCP Servers (Observed [E09]):**
  - `~/.gemini/config/mcp_config.json` and `~/.gemini/antigravity-ide/mcp_config.json` are both 0 bytes. No MCP servers active.
- **Permissions & Approval Gates (Observed [E05, E09, E11]):**
  - `globalPermissionGrants` in `~/.gemini/config/config.json` whitelists 29 command/read patterns.
  - Browser restricted to 78 domains in `browserAllowlist.txt`.
  - Hardcoded safety boundary rules block reading system binaries.

### Axis 4: Usage Evidence, Telemetry, and Identifiers
- **Stable Identifiers (Observed [E03, E06, E07]):**
  - Conversation ID: `299c055d-0914-4b64-b8e6-3601f0308fac` (UUID)
  - Trajectory ID: `a56e9152-5ffe-4570-b5b7-6ce6cde07275` (UUID)
  - Session ID: `-3750763034362895579` (numeric)
  - Initialization State ID: `7abc2de6-f148-4d88-aa39-9d0f1b11a653`
  - Tool Call IDs: e.g. `call_1139402`
- **Telemetry Schema & The Zero-Token Gap (Observed [E07, E08]):**
  - Transcript fields: `step_index`, `source`, `type`, `status`, `created_at`, `content`, `thinking`, `tool_calls`, `exit_code`.
  - **No token counts or cost figures exist in local transcripts or SQLite records.** The IDE surface acts purely as a consumer of inference, not an accounting telemetry exporter.

### Axis 5: Billing, Accounting, and Costs
- **Account Mode (Inferred [E03, E04]):**
  - Google account Single Sign-On authenticating against `https://cloudcode-pa.googleapis.com` via internal Cloud Code / JetSki auth.
  - No `GEMINI_API_KEY` present in environment.
- **Attributable Charges (Unknown [E07, E08]):**
  - Zero financial or token quota metrics are exposed.
  - Per-attempt USD cannot be derived. Converting quota or request counts to USD without an official provider invoice is unjustified.

### Axis 6: Harness Compatibility Evaluation

| Harness Condition | Feasibility | Audit Findings & Prerequisites |
|---|---|---|
| **H0 (No added rules)** | **Partial / Candidate** | No user or project rules exist. However, 5 global plugins (41 skills) are loaded in `~/.gemini/config/plugins/`. True H0 baseline requires isolating or temporarily moving `~/.gemini/config/plugins/`. |
| **H1 (Fixed guidelines)** | **Feasible** | Can be delivered via a single root `GEMINI.md` or `AGENTS.md` in the target repository. Respects hierarchical path discovery. |
| **H2 (Bounded workflow)** | **Feasible (External)** | IDE natively supports planning and review modes. Turn bounds (`--max-turns`) and budget limits (`--max-budget-usd`) are absent from `agentapi` and must be enforced by an external watchdog. |
| **H3 (Loom Context-Only)** | **Feasible** | Loom guidelines and reference bundles can be committed as project rule files or context documents. |
| **H3 (Loom Native Pipeline)** | **Blocked** | Loom CLI is uninstalled (`which loom` returned 127). Furthermore, Loom v0.1.1 lacked pipeline commands and has no native Antigravity IDE execution adapter. |

### Axis 7: Export, Retention, and Security Boundaries
- **Filesystem & Network Isolation (Observed [E01, E04, E13]):**
  - No container or chroot boundary. Filesystem mutations occur directly in the active checkout.
  - Full network egress to Google Cloud endpoints. Browser restricted to allowlist.
- **Retention (Observed [E07, E08]):**
  - Local transcripts and SQLite conversation databases persist indefinitely in `~/.gemini/antigravity-ide/`.
  - Remote retention on Google Cloud Code servers is governed by Google Enterprise / Cloud terms.

---

## 3. The Three Largest Measurement and Control Gaps

1. **Zero Observable Token & Cost Telemetry in IDE Surface ([E07](file:///Users/oscarrieken/Projects/Rieken/guild-ledger/guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/evidence.md#e07-conversation-sqlite-database-inspection), [E08](file:///Users/oscarrieken/Projects/Rieken/guild-ledger/guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/evidence.md#e08-transcript-analysis-transcriptjsonl)):**  
   Neither local JSONL transcripts nor the SQLite conversation database records input tokens, output tokens, cached tokens, reasoning tokens, or dollar expenditure. Per-attempt USD cannot be derived from local telemetry.
2. **Absence of Backend Model Revision Pinning ([E04](file:///Users/oscarrieken/Projects/Rieken/guild-ledger/guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/evidence.md#e04-language-server-daemon-and-network-sockets), [E07](file:///Users/oscarrieken/Projects/Rieken/guild-ledger/guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/evidence.md#e07-conversation-sqlite-database-inspection)):**  
   The IDE and `agentapi` configure broad tier labels (`Gemini 3.8 Flash (High)`), but provide no mechanism to pin an immutable, dated snapshot ID or backend deployment hash to prevent silent model weight updates over time.
3. **Lack of Headless Batch Execution & External Spend Bounding ([E05](file:///Users/oscarrieken/Projects/Rieken/guild-ledger/guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/evidence.md#e05-cli-and-executable-inventory), [E14](file:///Users/oscarrieken/Projects/Rieken/guild-ledger/guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/evidence.md#e14-python-sdk-verification)):**  
   This surface is an interactive, attended IDE. While `agentapi` can initialize a conversation, it lacks headless streaming output, output schema constraints, turn limits, and budget enforcement mechanisms natively available in headless CLI tools.

---

## 4. Proposed Next Calibration Probe (Bounded — NOT Executed)

- **Objective:** Determine whether `agentapi new-conversation` can be programmatically launched from an external script in a disposable temporary directory, and test whether a freshly initialized conversation records token telemetry in its database.
- **Inputs:** Disposable directory (`/tmp/antigravity-probe-<timestamp>`), synthetic prompt (`{"action": "ping"}`), flag `--model=flash_lite`.
- **Expected Evidence:** Exit code, returned conversation ID, metadata response via `agentapi get-conversation-metadata <id>`, SQLite database schema and row inspection for token counts.
- **Execution Limits:** Exactly 1 `agentapi new-conversation` call and 1 `agentapi get-conversation-metadata` call.
- **Bounds:** 30 seconds maximum wall-clock time; $0 attributable spend.
- **Enforcement Mechanism:** External Python supervisor script invoking `subprocess.run(..., timeout=30)` with `SIGKILL` on timeout.
- **Overshoot Risks:** Language server background inference continuing after client process disconnects; unmetered quota deduction.

---

## 5. Traceability and Cross-Reference Index

| File | Relative Workspace Path | Purpose |
|---|---|---|
| **Audit Document** | [`guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/audit.md`](audit.md) | High-level synthesis, gaps, and disposition |
| **Full Report** | [`guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/report.md`](report.md) | Comprehensive 10-section narrative discovery report |
| **Capabilities Data** | [`guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/capabilities.json`](capabilities.json) | Valid JSON machine-readable capabilities matrix (v1-draft) |
| **Evidence Archive** | [`guild-ledger-research/docs/runtime-discovery/antigravity/20261021T053126Z/evidence.md`](evidence.md) | Itemized command records (E01–E16), links (D01–D06), and exclusions |
