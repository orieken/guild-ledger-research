# Repositories, ownership, and isolation

Visual companion: [repository ownership and shared inputs](07-system-diagrams.md#2-repository-ownership-and-shared-inputs).

## Decision: separate harness repos, shared benchmark

The user's proposed separate repos are useful for reviewing harness changes and onboarding GitHub frameworks. The main risk is four independently evolving applications or evaluators. Avoid that by making each repository a thin harness package around the same immutable task inputs.

Proposed names are suggestions; no repositories exist as a result of this document.

```text
guild-ledger-research/                  # trusted control plane, initially private
  protocol/                            # preregistration and decision log
  tasks/<task>/<version>/               # canonical agent-visible bundles
  prompts/<task>/<version>/             # shared envelope + P1/P2/P3
  evaluation/                          # private cases; never agent-mounted
  schemas/                             # run records, events, campaign manifests
  harness-registry/                     # repository + immutable revision + profile
  .github/workflows/                    # shared generation/reporting orchestration
  collector/                           # pull, validate, archive, deduplicate
  analysis/                            # derived tables/plots and fixed analysis plan
  posts/                               # drafts and claim-to-evidence index

guild-ledger-<condition>/               # one of the four treatment repositories
  harness.yaml                         # profile, version, source references
  adapter/                             # prepare, invoke, collect, teardown
  config/                              # condition-specific rules/tools
  .github/workflows/                    # thin caller of pinned shared workflow
  README.md                            # human docs, excluded from H0 workspace
```

Generated code lives in per-attempt artifacts, optionally mirrored to output-only branches after collection. A task checkout is never the latest output branch. Repository names and their READMEs are hidden from blinded reviewers where practical.

## Single sources of truth

| Asset | Owner | Rule |
|---|---|---|
| Product target and requirement inventory | Research | Freeze before scoring; private full target |
| Starter and mechanical interfaces | Research | Same content hash across the compared cells |
| P1/P2/P3 text | Research | Same prompt hash for a level/task across harnesses |
| Condition instructions/tools | Harness repo | Immutable commit and resolved asset hashes |
| Evaluation suite and scoring | Research | Agent cannot read or modify |
| Usage and event capture | Trusted supervisor + runtime adapters | Never rely on model-written totals |
| Analysis and published results | Research | Reproducible derivation, no manual editing of measurements |

A reusable workflow is pinned to a full commit. It explicitly fetches benchmark assets and harness assets at their resolved revisions; it must not assume checking out the caller repository also checks out research assets. See [GitHub reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).

## Harness manifest contract to implement

```yaml
id: H2
profile: controlled
version: 0.1.0
adapter_protocol: guild-ledger-adapter/1
runtime: TBD
source_revision: RESOLVE_TO_FULL_COMMIT
instructions: [config/workflow.md]
development_tools: [shell, editor, visible-tests]
model_policy: campaign-pinned
memory_policy: fresh-per-attempt
network_policy: declared-allowlist
review_round_limit: 2
human_gate_policy: halt-and-record
usage_adapter: TBD
```

This is a planning example with unresolved fields; it is not an executable manifest. Before admission, resolve dependencies, external framework revision, configuration hashes, model policy, license, setup time, service needs, supported platforms, and whether child invocations can all be metered.

## Controlled versus native profiles

H0–H2 use one base runtime/model setting and total attempt limits. H2's review calls count inside the same budget, including any separate reviewer context. H3 can join this track only if the selected Loom profile supports the same configuration and task information.

Loom's full delivery pipeline may route models and stop at gates. Preserve that behavior in a `native` profile and label the comparison accordingly. Do not auto-approve human gates to make a benchmark finish. Compare assisted runs separately with actual human minutes and waiting time.

## Isolation requirements

* Supervisor reads the campaign and materializes a clean attempt directory from the starter archive, not by cloning all research files into an agent-readable checkout.
* Agents receive only the selected envelope, task prompt, visible task assets, and declared treatment package. No full specification, alternate prompt levels, hidden tests, previous outputs, or user-wide Loom memory.
* Resolve symlinks and inspect archives for traversal before materialization. Pin dependency lockfiles and cache policy.
* Generation, evaluation, and publishing run under separate credentials/process boundaries. Hidden tests on the same readable filesystem as an agent are not hidden.
* During evaluation, execute generated code in a restricted disposable application environment. Keep test source and answer keys in an external test process, with only bounded read-only observation channels to application state.
* The trusted supervisor captures hashes, process exit/limit events, provider usage, and final code. Agent-written evidence is supplemental.
* Do not expose model/provider credentials to generated code during evaluation, and do not expose repository-write credentials to either generated application or agent tools.

## Run identity

A campaign freezes all resolved inputs and an ordered schedule. An attempt record includes campaign ID, slot ID, attempt ID, task/prompt/harness/profile/model IDs, all revisions/hashes, tool/runtime versions, environment digest, repetition index, randomization block, and limits.

The scheduled slot identifies the intended experimental cell/repetition. Each actual invocation has a distinct attempt ID. A CI rerun or infrastructure retry creates a new attempt linked to the same slot and original attempt; it never overwrites history. Only the preregistered selection rule determines which infrastructure replacement is analyzed. Agent failures are not replaced.

Capture workflow ID, repository, workflow run ID, run attempt, workflow definition revision, and subject artifact hash. GitHub run IDs alone do not identify an experimental cell.

## Adding another GitHub framework

1. Register its source URL, immutable revision, license, supported runtime, and proposed profile.
2. Implement the common adapter lifecycle and verify usage from every model invocation.
3. Audit task information, state persistence, gates, and available development checks.
4. Exercise fake-provider success, failure, needs-human, timeout, and collection cases.
5. Add it to a new frozen campaign alongside contemporaneous baseline cells.

No evaluator fork is permitted just to accommodate a harness's output. Adapt its output to the common launch/artifact contract, or explicitly declare incompatibility.
