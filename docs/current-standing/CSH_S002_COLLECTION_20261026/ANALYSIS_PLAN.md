# Analysis preparation — unscored CSH-S002 collection

## Populations and limits

All 24 planned requests were attempted. Parser v0.2 accepted 23, including the
first response carried by offline reparse; the final response failed its grammar.
The grammar repair occurred after observing the first response. Preserve that
change and the interruption in every report. The final JSON extraction is a
separate post-collection examination, not another grammar change or live rerun.

Primary v0.2 grammar-eligible population: at most 23 units, subject to completed
human normalization/adjudication. At most 11 complete H0/H1 pairs can be scored;
SIM_B_BOUNDARY_NARROWED / receiver B lacks a grammar-accepted H0 member. The
accepted H1 remains an unpaired observation. Do not impute the rejected member,
assign it zero, or drop it from the collection denominator.

Exploratory full-content examination may cover all 24 outputs, including the
final response's introductory prose and JSON. Any numerical analysis admitting
that response must be separately versioned and explicitly post hoc, with its
inclusion rationale and full-content coding preserved. No such inclusion or
semantic scores are generated here.

This is one replicate, six scenarios, two conditions, two model families through
one platform. No replication-based variance estimate or independent-platform
claim. Differences do not isolate structure from added information/salience.

## From reviewed coding to deterministic results

1. Preserve separate coder records and adjudication. Check all source/output
   hashes and evidence spans. These human adequacy checks are not established by
   passing the classifier's JSON schema.
2. Working copies of materials/coordinator/classifier-skeletons/ already bind the
   source scenario, original S002 unit ID, condition and raw response. Fill the
   classification_run_id, task_state, boundary_contracts and normalized_output
   ONLY from reviewed coding. Do not change the raw-output binding or source
   scenario to match the receiver's answer. Unresolved fields remain unclassifiable.
3. Run the inherited schema-validating classifier from the repository root:

```powershell
.\.venv\Scripts\python.exe tools/classify_unsupported_inheritance_s001_v0_1.py `
    C:\N\reviewed-classifier-input.json --output C:\N\classification.json --json
```

4. Create a new reviewed analysis file from materials/analysis/PRIMARY_PENDING.json.
   Retain all 24 rows, IDs, conditions, pairing keys and original capture status
   in the companion inventory. Only eligible, adjudicated, schema-valid records
   may be labeled COMPLETED_CLASSIFIABLE with classification and task_state
   populated. Keep the final rejected unit non-classifiable in primary analysis.
   Preserve unresolved coding as non-classifiable. Numeric zeros must come from
   actual classified coding, never placeholders.
5. Run the inherited analyzer:

```powershell
.\.venv\Scripts\python.exe tools/analyze_csh_s001_v0_1.py `
    C:\N\reviewed-primary-records.json --output C:\N\primary-analysis.json --json
```

6. Report attempted/accepted/coded/adjudicated/classifiable counts, exclusions and
   incomplete pairs alongside results. U counts rule findings; P counts unique
   claim IDs with claim-attributable promotion findings; A indicates any rule
   finding. None counts unique harms or establishes truth, authority or compliance.

materials/analysis/UNSCORED_SUMMARY.json is the current mechanical summary of
pending records: 24 rows, zero classifiable, no numerical U/P/A, no paired effect.
It demonstrates the current analysis state; it is not evidence of zero inheritance.
