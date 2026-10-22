# How the experiment works

These diagrams describe the proposed system. They do not represent deployed infrastructure or completed experiments. See the linked specifications for the exact contracts and unresolved decisions.

## 1. Experiment matrix

Every prompt level is tested against every admitted harness for each task and repetition. The controlled track fixes the model configuration. Loom joins that track only if its selected profile supports the same conditions; its full native pipeline is a separately labeled comparison.

```mermaid
flowchart TD
    Tasks["3 canonical tasks<br/>T01 quest board<br/>T02 accept expedition<br/>T03 repair concurrency"] --> Matrix["Cross all task, prompt,<br/>harness and repetition levels"]
    P1["P1: brief"] --> Matrix
    P2["P2: detailed"] --> Matrix
    P3["P3: specification"] --> Matrix
    H0["H0: minimal agent"] --> Matrix
    H1["H1: fixed guidelines"] --> Matrix
    H2["H2: our harness"] --> Matrix
    H3["H3: compatible Loom profile"] --> Matrix
    Reps["3 fresh repetitions"] --> Matrix
    Model["1 pinned model configuration"] --> Matrix
    Matrix --> Schedule["108 scheduled attempts<br/>Randomized within blocks"]
    Schedule --> Run["Fresh workspace and session<br/>for every attempt"]
```

The count is a feasibility-pilot proposal, not an authorized spending plan. More models, profiles, or harnesses enlarge the schedule explicitly. See [prompt protocol](03-prompt-protocol.md).

## 2. Repository ownership and shared inputs

The harness repositories own their treatment packages. The research repository owns common task inputs and independent scoring. A harness repository never supplies its own acceptance verdict.

```mermaid
flowchart LR
    subgraph Research["guild-ledger-research"]
        Campaign["Frozen campaign<br/>Registry and schedule"]
        Common["Pinned starter<br/>Selected prompt and envelope"]
        Eval["Private evaluator<br/>Frozen criteria and fixtures"]
        Collector["Collector and archive"]
        Analysis["Analysis and posts"]
    end
    subgraph HarnessRepos["Four independently versioned harness repos"]
        H0["guild-ledger-baseline<br/>H0 package"]
        H1["guild-ledger-guidelines<br/>H1 package"]
        H2["guild-ledger-harness<br/>H2 package"]
        H3["guild-ledger-loom<br/>H3 package"]
    end
    Campaign --> Resolve["Resolve one scheduled attempt"]
    Common --> Resolve
    H0 --> Resolve
    H1 --> Resolve
    H2 --> Resolve
    H3 --> Resolve
    Resolve --> Attempt["One fresh workspace<br/>One selected harness"]
    Attempt --> Subject["Final or partial source artifact<br/>Trusted generation evidence"]
    Subject --> Eval
    Eval --> Report["Authoritative attempt report"]
    Report --> Collector
    Collector --> Analysis
```

Only the selected harness enters a given attempt. The four incoming package arrows represent alternatives. Previous generated code is never fed into the next repetition. See [repository architecture](02-repositories-and-isolation.md).

## 3. Prompt assembly and information boundaries

The supervisor selects inputs; the agent does not receive this whole research pack. In particular, P1 cannot discover P3 or the private target through repository access.

```mermaid
flowchart LR
    subgraph Available["Allowed inputs for one attempt"]
        Runtime["Recorded base runtime instructions"]
        Envelope["Shared task envelope<br/>Stack, interfaces and commands"]
        Prompt["Exactly one prompt<br/>P1 or P2 or P3"]
        Starter["Pinned starter<br/>Visible fixtures and checks"]
        Harness["Exactly one harness package<br/>Rules, tools and workflow"]
    end
    Runtime --> Assemble["Supervisor assembles inputs<br/>Records hashes and order"]
    Envelope --> Assemble
    Prompt --> Assemble
    Starter --> Assemble
    Harness --> Assemble
    Assemble --> Agent["Coding agent<br/>Fresh context and memory"]
    Agent --> Output["Code, assumptions<br/>and claimed verification"]
    subgraph Private["Outside agent access"]
        Target["Canonical requirement inventory"]
        Hidden["Private evaluation fixtures"]
        Other["Other prompt levels<br/>Previous run outputs"]
    end
    Target --> Evaluator["Independent evaluator"]
    Hidden --> Evaluator
    Output --> Evaluator
```

The private nodes have no input path into the agent. Harness-generated plans/specifications can use only the allowed inputs, and their generation counts toward cost. See the [worked T02 prompts](prompts/T02/00-shared-envelope.md).

## 4. One attempt from dispatch to dataset

Actions coordinates work, but the supervisor captures generation usage. Evaluation runs after construction stops and does not return private failures for repair.

```mermaid
sequenceDiagram
    autonumber
    participant C as Research campaign
    participant H as Harness repo workflow
    participant S as Trusted supervisor
    participant A as Isolated agent
    participant E as Independent evaluator
    participant P as Report publisher
    participant R as Research collector
    C->>H: Dispatch frozen campaign and slot
    H->>S: Invoke pinned common workflow and harness revision
    S->>S: Verify inputs, limits and fresh state
    S->>A: Supply starter, selected prompt and harness
    loop During generation, within total limits
        A->>A: Edit code and run visible checks
        S->>S: Capture provider usage, tool events and checkpoints
    end
    A-->>S: Completion, request for help, limit or error
    S->>S: Freeze final or partial subject and stop evidence
    S->>E: Transfer exact subject hash for assessment
    E-->>P: Requirement results or evaluation error
    S-->>P: Manifest, subject and trusted generation telemetry
    P->>P: Validate and assemble versioned report
    P-->>R: Make report artifact available
    R->>P: Pull artifact and verify origin and digests
    R->>R: Archive and normalize once per attempt identity
```

A killed worker may never return normally. Durable supervisor checkpoints and the expected-slot ledger let collection identify missing evidence instead of silently losing the attempt. See [Actions plan](05-github-actions-plan.md).

## 5. Run lifecycle and unsuccessful outcomes

Construction status, evaluation status, and research validity are separate. An agent finishing does not imply acceptance; an acceptance failure is still useful data.

```mermaid
flowchart TD
    Slot["Scheduled slot"] --> Validate{"Inputs and limits valid?"}
    Validate -->|No| Config["Configuration error<br/>Do not launch agent"]
    Validate -->|Yes| Start["Start a distinct attempt"]
    Start --> Stop{"Construction stops"}
    Stop -->|Done| Completed["Generation completed"]
    Stop -->|Approval or answer required| Human["Needs human"]
    Stop -->|Spend or time ceiling| Limit["Budget or time limit"]
    Stop -->|Error or cancellation| Error["Record specific stop reason"]
    Completed --> Preserve["Preserve subject and trusted evidence"]
    Human --> Preserve
    Limit --> Preserve
    Error --> Preserve
    Preserve --> Assess["Assess available artifact independently"]
    Assess --> Verdict{"Evaluation completed?"}
    Verdict -->|Yes| Measured["Record requirement passes and failures<br/>Compute artifact and autonomous acceptance"]
    Verdict -->|No| Unknown["Acceptance unknown<br/>Record evaluation error or not run"]
    Measured --> Integrity{"Evidence valid and complete?"}
    Unknown --> Integrity
    Integrity -->|Yes| Dataset["Archive valid observation<br/>Include according to frozen analysis rules"]
    Integrity -->|No| Quarantine["Archive with incomplete or invalid status<br/>Resolve before analytical inclusion"]
    Config --> Ledger["Expected-slot ledger<br/>Retain every execution and replacement"]
    Dataset --> Ledger
    Quarantine --> Ledger
```

Autonomous success requires completed generation, passing assigned criteria, and valid evidence. A stopped attempt can have a passing partial artifact and still fail the autonomous endpoint. Infrastructure replacements receive new attempt IDs and preserve lineage. See [metrics contract](04-metrics-and-reporting.md).

## 6. Development feedback versus independent scoring

Agent-visible tests help construction. The private evaluator measures behavior against frozen expectations. Those feedback loops have different roles.

```mermaid
flowchart LR
    subgraph Development["Agent-visible development environment"]
        Inputs["Selected task inputs"] --> Implement["Implement or revise"]
        Implement --> Visible["Run visible checks"]
        Visible --> Decide{"Continue within limits?"}
        Decide -->|Yes| Implement
        Decide -->|No| Freeze["Freeze subject"]
    end
    Freeze --> App["Isolated generated application"]
    subgraph Assessment["Trusted independent assessment"]
        Hidden["Private tests and fixtures"] --> Checks["API, browser and bounded state checks"]
        Checks --> Results["Requirement-level results"]
    end
    Checks -->|Exercise and observe| App
    Results --> Report["Research report<br/>No private feedback to coding session"]
```

For H2, review/repair rounds are bounded. H0 and H1 may still choose to run visible checks through their base runtime; all controlled conditions have the same declared verification tools. Source secrecy requires process/filesystem boundaries, not merely a private repository.

## 7. Metrics provenance and research ingestion

Every headline number traces to evidence from the system that actually observed it. The agent's summary is not authoritative usage or acceptance data.

```mermaid
flowchart TD
    Provider["Provider and runtime<br/>Invocation usage and charge"] --> Telemetry["Trusted generation telemetry"]
    Supervisor["Supervisor<br/>Timings, tool calls, limits and stops"] --> Telemetry
    Human["Intervention record<br/>Active minutes and gate decisions"] --> Telemetry
    Evaluator["Independent evaluator<br/>Criterion results and regressions"] --> Assemble["Report assembler"]
    Telemetry --> Assemble
    Manifest["Frozen manifest<br/>Versions, hashes and pricing"] --> Assemble
    Assemble --> Bundle["Versioned metrics bundle<br/>JSON, source, events and evidence manifest"]
    Bundle --> Summary["GitHub job summary<br/>Human-readable view"]
    Bundle --> Pull["Research collector pulls<br/>Registered repos and workflows"]
    Pull --> Verify{"Origin, schema, hashes<br/>and identity valid?"}
    Verify -->|No| Quarantine["Quarantine with reason"]
    Verify -->|Yes| Dedup{"Already archived?"}
    Dedup -->|Same identity and bytes| Noop["No duplicate insertion"]
    Dedup -->|Same identity, changed bytes| Quarantine
    Dedup -->|New attempt| Archive["Durable raw archive<br/>Normalized research tables"]
    Archive --> Analysis["Cost, quality, reliability<br/>Missingness and uncertainty"]
    Analysis --> Posts["Plots and posts<br/>Claims linked to evidence"]
```

Missing usage stays unknown. Failed attempts retain their costs. Unknown evaluations stay distinct from known coding failures. Archive evidence before Actions artifact expiration. See the [summary schema](contracts/run-record.schema.json).

## 8. Extending the benchmark with another harness

Adding a framework changes the treatment registry and campaign, while preserving the shared task and evaluator contracts.

```mermaid
flowchart LR
    Source["GitHub framework<br/>Pinned revision and license"] --> Adapter["Implement common adapter<br/>Declare tools, models, gates and memory"]
    Adapter --> Admit["Admission checks<br/>Isolation, usage coverage and stop limits"]
    Admit --> DryRun["Fake-provider dry run<br/>Success and failure paths"]
    DryRun --> Registry["Register versioned harness profile"]
    Registry --> Campaign["Freeze a new campaign<br/>Same task/evaluator versions for comparison"]
    Campaign --> Compare["Run new harness plus<br/>contemporaneous baseline cells"]
    Compare --> Collect["Collect through the same metrics contract"]
    Collect --> Analyze["Compare within compatible<br/>model, prompt and profile groups"]
```

Native multi-model workflows remain separate from controlled same-model comparisons. New results do not silently replace older records or inherit an old model configuration by name alone.
