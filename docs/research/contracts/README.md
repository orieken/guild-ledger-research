# Summary contract notes

`run-record.schema.json` describes one attempt summary using JSON Schema Draft 2020-12. The example in `../examples/run-record.synthetic.json` is fabricated and must be rejected from real campaign datasets because `synthetic` is true.

JSON Schema validates shape, types, enum values, basic null handling, and nonnegative measurements. It cannot establish evidence authenticity or calculate all relationships. The future trusted validator must also enforce:

* All identity and provenance values match the frozen campaign and actual GitHub origin. No unresolved or placeholder hashes in real campaigns.
* Passed requirement/regression counts do not exceed totals; full-target criteria include the communicated critical subset.
* Artifact acceptance equals all assigned critical requirements passing. Top-level autonomous acceptance additionally requires completed generation and valid integrity. Missing evaluations produce null, and incomplete/invalid provenance is quarantined rather than accepted into analysis.
* Dates are ordered; elapsed durations match supervisor timing; agent-active plus gate-wait equals generation elapsed within declared clock tolerance. Human-active and queue time are separate quantities.
* The chosen comparison cost equals the selected reported/estimated total, with complete invocation coverage. Estimates require a verified pricing snapshot and the correct provider-native category mapping.
* Aggregated invocation usage is complete, subsets are not double counted, and tool counts come from trusted instrumentation. Unknown categories remain null.
* Referenced evidence exists, hashes match, the subject evaluated is the subject generated, and the selected evaluator revision matches the campaign.
* Recollection of an identical record is idempotent; changed bytes under the same attempt identity are quarantined. Retries are separate attempts with lineage.

Run records summarize evidence; they are not self-authenticating. The invocation, event, campaign, and evidence-manifest schemas are explicitly future implementation deliverables.
