# Prompt and harness protocol

Updated comparison definitions: [C1–C4 protocol](10-comparison-protocol.md). Full-target functional acceptance is now the common product endpoint; communicated conformance is the implementation diagnostic. Process wording in the shared envelope and prompt drafts still needs the treatment-separation cleanup described there.

Visual companions: [experiment matrix](07-system-diagrams.md#1-experiment-matrix) and [prompt assembly](07-system-diagrams.md#3-prompt-assembly-and-information-boundaries).

## Question

Does increasing prompt completeness improve outcomes, and how does that improvement interact with a harness? The experiment changes prompt information and workflow, while holding task, stack, common interfaces, base model configuration, and limits constant in the controlled track.

This is not a test of prompt word count alone. Record word/token counts, but define levels by disclosed requirements.

## Prompt assembly

The trusted runner assembles:

```text
provider/runtime instructions             recorded version/hash where accessible
condition instruction package             H0/H1/H2/H3 only
shared task envelope                      identical within a task
assigned prompt body                      exactly one of P1/P2/P3
starter repository and visible fixtures    identical within a task
```

Record file hashes and injection order. Runtime-specific placement may differ, but it must be declared. A framework may not choose a different prompt variant for itself. Do not run the experiment from this design chat: it already contains the complete target and all conditions.

The envelope contains the mechanical stack, paths, invocation commands, interface routes/transport schemas, fixed dependency configuration, file allowlist, and budget/clarification policy. It does not contain omitted product rules. This means P1 is a short product brief within a fixed engineering environment; it is not an unconstrained one-sentence request to invent an entire architecture.

## Three levels

| Level | Content | Intended uncertainty |
|---|---|---|
| P1 | Goal, happy path, desired user outcome | Many domain rules unspecified |
| P2 | Main rules, common failures, persistence and interaction expectations | Some edge semantics unspecified |
| P3 | Numbered rules, explicit boundaries, error mapping, examples, exclusions | Implementation choices remain, behavior is well defined |

The [T01 task package](../../benchmarks/T01/README.md) now has a runnable starter, visible tests and draft P1–P3 prompts. It remains unfrozen pending independent full-target evaluation and input disclosure review. The [T02 prompt folder](prompts/T02/) contains one complete worked set. Task-specific starter paths and commands are proposed contracts until the starter is implemented and verified.

## Information disclosure and scoring

Use an immutable requirement inventory and classify exposure before any attempts. For the draft T02 set:

| Requirement | P1 | P2 | P3 |
|---|---|---|---|
| R01 successful persisted acceptance | Explicit | Explicit | Explicit |
| R02 UI acceptance and result | Explicit | Explicit | Explicit |
| R03 inclusive party-size rules | Unspecified | Explicit | Explicit |
| R04 every-member minimum level | Unspecified | Explicit | Explicit |
| R05 unknown identifiers | Unspecified | Unspecified | Explicit |
| R06 open quests only | Unspecified | Explicit | Explicit |
| R07 one active expedition per party | Unspecified | Explicit | Explicit |
| R08 exact item-input validation | Unspecified | Unspecified | Explicit |
| R09 Go reservation and persisted link | Explicit | Explicit | Explicit |
| R10 insufficient stock leaves no acceptance/allocation | Unspecified | Explicit | Explicit |
| R11 normalized persisted idempotent replay | Unspecified | Unspecified | Explicit |
| R12 same-key different-body conflict | Unspecified | Unspecified | Explicit |
| R13 finite timeout and unavailable mapping | Unspecified | Unspecified | Explicit |
| R14 UI pending/duplicate/preserve behavior | Unspecified | Explicit | Explicit |
| R15 accessible feedback | Unspecified | Unspecified | Explicit |
| R16 preserve existing browse/party behavior | Explicit | Explicit | Explicit |
| R17 common engineering interface | Envelope | Envelope | Envelope |
| R18 exact domain error mappings | Unspecified | Unspecified | Explicit |

Finalize this table with an independent read of the actual prompt text and starter. Information can leak through existing code, schemas, filenames, tests, or service documentation. Record those channels; do not label a requirement unspecified if the starter already states it. The initial table concerns prompt disclosure and is not proof of total information exposure.

For each attempt report:

* **Communicated conformance:** all critical requirements explicitly available in that condition, including the envelope and verified starter information. Denominators differ across prompt levels, so compare harnesses within a level; report denominators alongside cross-level plots.
* **Full-target acceptance:** all critical requirements in the frozen complete task target, with the same denominator across levels. This measures product fit under incomplete instructions; it is not purely implementation competence.
* Non-critical quality dimensions separately, including R15 and maintainability review.

Agent assumptions do not change the denominator after execution. A general phrase such as “handle errors” is not evidence that an exact status code was communicated. Freeze criterion-to-input mappings before measuring results.

## Clarification policy

Primary trial: no live human answers. The common instruction asks agents to record assumptions and proceed when possible. If a runtime requires an answer or gate approval to continue, record `needs_human` and stop. Do not grant some conditions extra requirements through chat.

A later clarification study can use a fixed oracle answering from the canonical requirement inventory, with all questions, disclosed facts, human/model costs, and time recorded. It is a separate treatment because it changes available information.

## Harness instructions

H0 adds no project-specific guidelines beyond the common envelope. Base runtime behavior is still present and must be documented. Fresh global configuration is essential.

H1 proposed fixed text:

> Inspect the supplied repository before editing. Make a short plan. Implement the requested scope and record assumptions. Add appropriate tests and run the available checks. Review your changes for defects. Finish with a concise summary of changes, verification, and unresolved issues.

H2 proposed workflow, bounded within one attempt budget:

1. Extract requirements only from available inputs; list assumptions without fetching the private target.
2. Plan affected components and visible verification.
3. Implement and run selected visible checks.
4. Review the diff against the extracted requirements with the same model configuration; allow at most two review/repair rounds.
5. Run the complete visible suite and report evidence.

Freeze instruction text, review roles/context, check catalog, and stop logic before the pilot. If model-generated specifications/tests are created, their generation and tokens are part of H2 cost. Every controlled harness receives access to the same visible verification tools; H2 differs in the required workflow. A later sensor ablation may vary tool access explicitly.

H3 references a frozen Loom profile, not “whatever the current install does.” Verify generated instructions/tools, runtime compatibility, gate policy, retrieval corpus, model routing, and reporting. Documentation alone does not prove the controlled profile can execute.

## Run schedule

For each task/model/repetition block, randomize the 12 prompt/harness cells and retain the schedule seed. Use fresh workspaces and sessions per attempt. Dependency-cache policy is identical; provider prompt-cache behavior is measured rather than assumed identical.

Limits are campaign values shared across controlled cells: total generation spend, wall-clock runtime, maximum tool calls, and any token ceiling supported by the runtime. All child calls count. A bounded repair loop does not reset limits. No extra attempt is granted because a favorite harness nearly passed.

The proposed 108-attempt feasibility pilot validates mechanics; revisions informed by it require a new protocol version. Main-study sizes depend on pilot variability and a declared minimum meaningful effect. Keep tuning tasks separate from held-out evaluation tasks.

## Freeze checklist

Before paid execution, complete and hash: actual starter bundles; reference passes and flawed-variant checks; three prompt sets; disclosure maps; manifests; model/runtime configuration; budgets and pricing; schedule; independent evaluator; infrastructure rerun rule; metrics schema; analysis contrasts; review rubric; evidence retention settings. Freeze content, not just mutable release names.
