# S002 frozen execution and coding handoff v0.1

This freeze succeeds the candidate preparation document without replacing it.
The unchanged PLAN.json intentionally retains its historical CANDIDATE_NOT_FROZEN
and corpus_execution_enabled=false fields. FREEZE.json binds that plan and grants
it a new execution role only through the separate opt-in runner. Source S001
identities remain in reused packets; new requests and records use S002 unit IDs.

## Execution contract

Exactly 24 frozen requests, one attempt each, serial, no fallback or retry.
Both neutral receipts passed at 2026-10-26 17:31 UTC, with reported combined
USD cost 0.00003. Preserve the full USD 0.06 neutral reservation for admission.
Each corpus request reserves USD 0.03 before sending; reservations are not
recycled. Full planned gross commitment is USD 0.78 within USD 1.00. Actual cost
is reported separately; an overrun is charged in full and stops subsequent calls.
This cannot constrain an in-flight bill or spending in other tools or checkouts.

A persistent .csh-s002-campaign-v0-1 directory in the repository root is created
atomically before execution. It is never removed or reset by the runner. It
blocks repeated and concurrent campaigns even with different output directories.
Missing credentials and failed offline verification do not claim the campaign.
After an interruption, retain the marker and all files: no automatic resumption,
retry, or deletion. A separately reviewed recovery instrument would be required.
Filesystem durability depends on the host filesystem; flushed local files do not
constitute an external transaction or provider billing receipt.

Requests use the official pinned SDK, exact frozen UTF-8 wire bodies, no history,
empty tools, and tool_choice=none. The HTTP request hook compares URL, method and
bytes before transport. Neutral responses echoed tool_choice=auto despite the
request's none; retain this discrepancy without claiming internal enforcement.
Returned tools, retrieval results, non-message/non-reasoning output, or reported
tool invocations stop execution. No raw headers or key are saved.

Non-200 responses, malformed JSON, incomplete responses, identity mismatch,
missing/invalid cost, cost above reservation, non-object answer JSON, or an
execution error stop the campaign. No selective reruns. This conservative stop
rule can leave a partial population; report that population and all missing units.
Successful transport/JSON is COMPLETED_PENDING_CODING, never automatic research
classification or a claim that the transfer record is semantically complete.

## Human normalization and analysis

1. Verify response.bin and output.txt against each receipt. response.bin is the
   preserved raw-output binding; output.txt is extracted text, not an independent
   source. Preserve failed or incomplete responses alongside successful ones.
2. Follow the SHA-bound S001 MEASUREMENT_AND_CODING_SPEC_v0_1.md, including separate
   coding and adjudication records. The generated coding-handoff.json deliberately
   leaves normalized_output, reviewer and adjudication null. Do not infer their
   values from PASS or accept model-written self-labels as independent review.
3. For each codeable unit, create an input satisfying the bound S001 classifier
   input schema. Use the S002 unit ID as receiver_run_id and a distinct S002
   classification_run_id; retain the classifier's existing method ID. Map H0 to
   control_h0 and H1 to instrumented_h1. Use the source scenario's truth record,
   supplied non-claims and unresolved references from the bound packet builder;
   do not construct these from the receiver answer. Bind the exact response.bin.
   Record task_state, normalized_output and substantiated boundary_contracts
   following the inherited rubric, with reviewer evidence and disagreements.
4. Run tools/classify_unsupported_inheritance_s001_v0_1.py on each reviewed input.
   Its schema permits S002 receiver IDs; its method remains the reused S001
   deterministic method. Classification is a function of supplied coding, not
   verification of the coding's truth.
5. Copy analysis-pending.json to a new reviewed analysis file. Only after coding
   and schema validation, set eligible rows to COMPLETED_CLASSIFIABLE and insert
   classification and task_state. Keep every other row non-classifiable and
   U/P/A absent/null. Do not edit the original capture or pending records.
6. Run tools/analyze_csh_s001_v0_1.py on that reviewed file. Preserve S002 pairing
   keys and all 24 rows. Report classifiable denominators and missing pairs;
   summary differences apply only to complete pairs. No replicate variance or
   independent-platform claim is justified by this one-replicate pilot.

Regression fixtures exercise the pending-analysis path (24 rows, zero numeric
scores) and a synthetic schema-valid S002 pair through the inherited classifier
and analyzer. These checks establish format compatibility, not human coding.
