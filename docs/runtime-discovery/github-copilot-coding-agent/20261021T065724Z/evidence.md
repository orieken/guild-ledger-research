# Evidence ledger

Captured: 2026-10-21T06:57:24Z. “Observed” refers only to this active session and the checks below. Documentation references describe their named GitHub surface, not proof of this runtime's behavior. No credentials, hidden prompt text, private reasoning, personal data, or unrelated logs are reproduced.

## E01 — active session metadata and exposed tool surface

Used the session metadata tool for the current session. It returned a session title, `inProgress` status, working directory, creation/modification timestamps, and session URI. The report omits the URI. Runtime identity is supplied as “AI assistant using Copilot SDK in VS Code”; this is the exact product/surface label available to the assistant, not a build/version or backend attestation.

**Not exposed in that result:** application/extension/SDK version, selected model, backend revision, request IDs, token counters, billing, retention controls, task cancellation, or an exportable raw tool-event log.

## E02 — local OS and repository checks

From the workspace parent:

```text
pwd
/Users/oscarrieken/Projects/Rieken/guild-ledger
```

The parent is not a Git repository. In the research checkout, read-only checks returned:

```text
git rev-parse --show-toplevel
/Users/oscarrieken/Projects/Rieken/guild-ledger/guild-ledger-research

git status --short --branch
## No commits yet on main...origin/main [gone]
?? README.md
?? docs/
?? repositories.json

git branch --show-current
main
```

No files were staged. Existing untracked state predates the three documents in this discovery.

## E03 — platform and execution environment

Read-only command:

```text
sw_vers
ProductName: macOS
ProductVersion: 26.6.2
BuildVersion: 25G83

uname -a
Darwin Mac 25.6.0 Darwin Kernel Version 25.6.0: Fri Jul 31 19:18:53 PDT 2026; root:xnu-12377.161.14~5/RELEASE_ARM64_T6031 arm64
```

These results are observed for the shell that ran the command; they do not identify the model-inference host.

## E04 — absent runtime and billing telemetry

The current-session metadata and read-only checks used for this report did not expose a runtime build number, model label or backend revision, request-level usage, cost ledger, or provider telemetry export. This is a bounded absence claim about the inspected interfaces—not proof that no such information exists in an administrator console or another authorized export.

No model run was launched to test logging, billing, cancellation, or model pinning.

## E05 — operations exercised in this discovery

Observed successful operations: workspace file reads/search; shell execution of read-only OS, Git, and GitHub metadata commands; retrieval of official web documentation; direct writing of the requested documentation files. There was no application build/test, GitHub Actions run, benchmark, external agent launch, Loom execution, or additional model/cloud task initiated.

The assistant's visible tool interaction is not a complete provider-level usage/event ledger. Tool listing alone was not treated as evidence of exercise.

## E06 — instruction/configuration discovery

A bounded file search in the intended research checkout for:

```text
AGENTS.md
.github/copilot-instructions.md
*.instructions.md
*.agent.md
*.prompt.md
```

returned no matches. The research README and the user-provided runtime-discovery prompt were read. No organization settings, home-directory configuration, hidden prompts, memory, or unrelated files were inspected.

This is not a claim that mandatory platform instructions or organization policy are absent. Their text/effective context is not exported here.

## E07 — hosted repository and PR-base check

Read-only command:

```text
gh repo view orieken/guild-ledger-research --json nameWithOwner,url,defaultBranchRef,isPrivate,visibility
```

returned repository name `orieken/guild-ledger-research`, public visibility, and an empty `defaultBranchRef.name`. A credential/account status check was not included in this report.

```text
git ls-remote --symref origin HEAD
```

returned no output and exit status 0. `git remote show origin` reported `HEAD branch: (unknown)`. This confirms no currently advertised remote HEAD/default branch for this checkout; a normal base-branch PR could not be opened. No branch, commit, push, or PR was created.

## D01 — GitHub Copilot on GitHub.com overview (documented, separate surface)

Retrieved 2026-10-21: [GitHub Copilot on GitHub.com](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github). It distinguishes GitHub.com agentic experiences and cloud agent from Copilot in IDEs. The page documents cloud sessions, branches, logs, customizations, and model selection. It is reference material only; this discovery is not a GitHub.com cloud-agent task.

## D02 — Copilot cloud-agent environment setup (documented, separate surface)

Retrieved 2026-10-21: [Configure the development environment](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment). It describes an ephemeral environment powered by GitHub Actions and a repository `copilot-setup-steps.yml` workflow. These setup mechanisms were not observed in the local SDK session.

## D03 — cloud-agent session progress and stopping (documented, separate surface)

Retrieved 2026-10-21: [Managing agent sessions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents). The article documents monitoring session progress/logs, steering, stopping sessions, and that cloud-agent stopping ends the GitHub Actions run while preserving commits already pushed. No claim is made that the same controls or persistence apply to this session.

## D04 — cloud-agent task workflow and PR (documented, separate surface)

Retrieved 2026-10-21: [Research, plan, and iterate on code changes with Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/research-plan-iterate). The page describes a GitHub.com cloud-agent flow with a branch and PR creation. This session instead changed a local checkout with no remote base branch.

## D05 — official billing reference (documented, limited applicability)

Retrieved 2026-10-21: [Requests in GitHub Copilot (legacy)](https://docs.github.com/en/copilot/reference/copilot-billing/request-based-billing-legacy/copilot-requests). The page explicitly applies to certain subscribers remaining on legacy request-based billing after June 1, 2026; it describes GitHub Copilot request accounting for those plans. It does not establish the billing mode or charge for this Copilot SDK session, so no units or amounts are imputed.

## What was not tested

- A fresh or resumed agent task, prompt re-delivery, task setup, cancellation, timeout, or changed-file export.
- Runtime/model version selection, backend pinning, context isolation, compaction, memory, repository/org policy injection, or hooks.
- Any H0, H1, H2, H3, or Loom-enabled code-generation run.
- Usage export, input/output/cache/reasoning tokens, request/call IDs, child/reviewer calls, retries, failure attribution, or token/tool event timing.
- Account billing mode, premium/credit use, attributable USD, Actions compute, or cost reconciliation.
- Retention/deletion/export policy or administrator controls.
- CI, installation, settings changes, deployment, merge, commit, or push.

Normal platform processing of this documentation task is not a zero-cost benchmark. Unknown measurements remain unknown, not zero.
