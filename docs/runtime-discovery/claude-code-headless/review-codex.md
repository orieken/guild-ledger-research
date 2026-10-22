# Review: local Claude CLI and documented headless interface

Reviewer: Codex. Scope: the three discovery files in this folder, independently checked local version/help output and installed Loom help, the existing Loom source checkout, and selected official documentation. No extra model session, live probe, package installation, settings change, commit or push was performed. Original Claude files are preserved.

## Disposition

**Promising first runtime candidate; not yet an admitted benchmark profile.** The report correctly distinguishes an interactive local discovery session from a tested headless run. It identifies inherited personal instructions that would contaminate H0, exposes a recoverable Loom binary/source mismatch, and documents usage-accounting pitfalls. Headless output, clean-input behavior, actual spend limits, child accounting and interruption capture remain untested.

Checks: JSON parses; 36 capability entries contain the requested fields and allowed status values; evidence IDs are unique and every non-empty reference resolves. Seven capability entries have an empty evidence list, so valid structure does not yet mean complete evidence traceability.

## F01 · High · Correct the no-tools probe before execution

The proposed P1 suggests an empty `--allowedTools` list or unattended permission mode as a way to mitigate tool execution. Those are not equivalent to removing tools. The [CLI reference](https://code.claude.com/docs/en/cli-reference) distinguishes auto-approval rules (`--allowedTools`) from built-in availability (`--tools`); MCP needs its own control.

For the first metering probe, explicitly remove built-in and MCP tool access and verify the effective catalog. Do not rely on auto-permission defaults or an empty approval list. This review does not provide or run a complete launch command: auth, configuration, model and supervisor controls must be settled first.

## F02 · High · Choose one launch/auth profile across H0–H3

The report's H0 discussion proposes stripping discovery; H1 proposes a discovered `CLAUDE.md` or `.claude/settings.json`. That pairing is not yet a coherent common profile. Settings are not themselves a free-form instruction document. Modes that suppress automatic instruction discovery require another deliberate injection route.

The [headless guide](https://code.claude.com/docs/en/headless) documents bare-mode auth via API key or an explicit API-key helper, rather than ordinary subscription login, and explicit context flags. Therefore do not compare H0 in bare/API mode with H1 in a personal subscription session that loads global instructions.

Proposed policy: select a common launch mode, base prompt and account mode; apply it to every condition; add only the selected treatment through a declared, hashed channel. H2/H3 must receive their required capabilities explicitly. If the native Loom pipeline cannot use that profile, keep it native rather than changing only its baseline controls. Bare mode is one candidate, not the definition of H0 or a proven prerequisite.

## F03 · High · Reconcile installed Loom with the existing source checkout

Independent checks reproduce the installed `/opt/homebrew/bin/loom` as v0.1.1, with installer/tool commands but no `run`. However, the previously inspected source checkout at `/Users/oscarrieken/Projects/Rieken/ai-assistant-dot-files` already contains the pipeline executor and Claude/mock provider selector. Its HEAD remains `3a41006238a43bbd0920f3ef108091641b1be00e`, with local modifications/untracked inputs.

Conclusion: native execution is blocked by this **installed binary**, not established as absent from Loom. Do not redefine H3 as context-only simply to fit the old binary, and do not silently update the user's global installation.

Next zero-model work: select a clean source revision or archive intended changes, build a separate research-local executable, hash it, inspect its commands, and validate mock execution in a disposable workspace. This is proposed work, not performed by this review. Preserve both source identity and binary identity in the manifest.

## F04 · Medium · Fix evidence completeness and confidence labels

Seven capabilities have no `evidence_ids`: `tools.network` (observed), `metrics.usage_vs_modelusage`, `metrics.resume_accumulation`, `metrics.crash_zeroing`, `metrics.aggregate_local_usage`, `artifacts.interruption_survival`, and `harness.H1` (documented). Link the appropriate observation/docs or downgrade unsupported claims.

`cost.accounting_mode` is labeled observed while its own text calls it inferred from environment/doctor/credential-file indicators. Preserve that as inference unless an authorized non-sensitive auth-status readout establishes the method. The absence of one environment variable is not exhaustive proof of the active provider or billing path. No credential values are needed.

“No hooks active” is stronger than absence of hooks in one settings file if plugins/other instruction sources remain loaded. Distinguish “no hooks found in inspected settings” from runtime-confirmed effective hooks. The claimed ancestor-file location is also described as two directories above although the listed path is higher; the substantive risk is ancestor discovery, not that count.

## F05 · Medium · Repair internal probe definitions and bounds

P1 says it will examine bare-mode authentication, but its actual proposed command omits bare mode. Split authentication, structured output and isolation into distinct objectives. P3 assumes likely auth failure and initially supplies no budget enforcement; a failure expectation must not replace limits when execution could unexpectedly proceed.

The local top-level help captured during review does not list `--max-turns`, although the official reference documents it. This is a documentation/help discrepancy to verify on the pinned version, not evidence that the flag is unsupported. A one-turn limit also does not certify exactly one provider request or exclude auxiliary behavior.

Choose a tiny text-only response task with no command execution rather than an ambiguous “echo” request. Use a supervisor timeout, explicit model/effort, candidate limit enforcement and a stated overshoot allowance. The [CLI reference](https://code.claude.com/docs/en/cli-reference) describes dollar limits as estimated-spend checks that may overshoot and excludes restored session spend from a new invocation's cap. An attempt-level supervisor must account across all invocations.

## F06 · Medium · Preserve the boundary between transcript findings and headless evidence

The transcript schema and duplicate IDs were observed during an interactive session, not a `-p` execution. Its absence of a cost field does not prove that all interactive accounting sources lack cost or that the future headless adapter cannot capture it. The report mostly respects this distinction; retain it in the normalized profile.

Build test fixtures for duplicate records, final-versus-provisional usage, cumulative resume totals, cache TTL categories, child lineage, missing/error final results and partial captures. Reconcile a later actual exported result against those assumptions. No token total, complete list-price estimate or cost-per-success measurement is justified by the current schema inventory alone.

## F07 · Medium · The current directory is not an experimental isolation boundary

The report observes execution from the parent `guild-ledger/` folder with access to personal rules, home-level AGENTS instructions, sibling repositories and the ordinary user filesystem. This is appropriate for documenting the developer environment but not a benchmark launch template.

Run future attempts from materialized task workspaces with explicitly controlled configuration and separate evaluator/telemetry access. File-tool scoping does not by itself prove that shell execution cannot read other files. Do not remove or repair the user's global Loom symlinks/settings to manufacture a baseline; use an isolated profile/environment.

## Alignment after this review

| Component | Current state |
|---|---|
| Local Claude CLI | Version 2.1.304 and relevant flags independently observed |
| Actual headless metering | Not exercised; calibration still needed |
| Personal-context-free H0 | Candidate mechanisms documented; effective inputs unverified |
| H1 instruction injection | Design it to match the selected H0 launch mode |
| H2 bounded review | Enforcement/metering primitives available on paper; workflow not built |
| Loom context profile | Distinct treatment; not a substitute for native pipeline |
| Loom native pipeline | Installed binary lacks executor; source exists and needs reproducible local build/mock validation |
| Complete per-attempt billed USD | Not established by these reports |

## Recommended next steps

1. Correct the seven evidence references, confidence labels, and proposed probe text in a new revision; do not silently erase the current discovery record.
2. Select the common launch/auth/instruction-injection policy for the controlled harnesses.
3. Resolve the source-versus-installed Loom mismatch using a separate pinned research executable and mock provider, without replacing global tools.
4. Validate the supervisor/normalizer with zero-model fixtures.
5. Only then propose a separately authorized tiny live metering calibration with concrete controls, no tools, durable capture and explicit limit semantics. Test editing/child usage later, each as a separate admission check.

The two reports together establish useful differences between a Projects cloud session and a local developer CLI. They still do not establish a completed, isolated or correctly metered H0–H3 experiment.
