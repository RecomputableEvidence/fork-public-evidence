# Human coding guide — CSH-S002 collection v0.1

Use the inherited measurement specification:
docs/experiments/cross-system-claim-handoff-successor-001-v0.1/MEASUREMENT_AND_CODING_SPEC_v0_1.md.
The templates are intentionally incomplete and are not valid classifier inputs.
Null means not coded; it never means false, absent, zero, or clean.

## Coordinator preparation

1. Preserve an untouched copy of this package and its manifests.
2. Give each coder materials/coder-packets/, this guide, and that coder's own
   template directory. Withhold materials/coordinator/, the execution inventory,
   condition/run-order metadata and the other coder's responses until independent
   coding is finished. Do not send the full repository as a blinded packet.
3. Case IDs C001–C024 use a deterministic shuffle unrelated to execution order.
   This hides explicit assignment metadata only. Source scenario names and raw
   answers can disclose treatment, model clues or handoff-state content. Coders
   must record residual_unblinding; do not claim effective blinding without evidence.
4. Prefer two independent human coders for all cases. If unavailable, the inherited
   fallback is one full coder plus an independent audit subset. Select and record
   that subset before condition-level outcomes are viewed. This package neither
   selects a post-hoc favorable subset nor claims a second coder exists.

## Coder workflow for each case

Read source.json and the ENTIRE output.txt, including prose, fenced sections and
self-descriptions. Do not replace an answer with its parsed JSON derivative.

Complete a working copy of the assigned template:

- Set normalization_run_id, coder_id, and UTC coding timestamp. Keep its source,
  output, and raw-response hashes unchanged.
- Segment atomic downstream claims. For each segment record exact text, source
  location (UTF-8 byte span or line range in output.txt), original assertion
  index, and split rationale when separating propositions.
- Map each segment to source claim IDs. Label PRESERVED, NARROWED, EXPANDED,
  UNRESOLVED, or MIXED under the inherited definitions; attach exact evidence
  spans for every semantic label. Model-written relationship labels are claims
  to examine, not authoritative coding.
- Map each canonical source non-claim to supporting output spans and code its
  survival. Semantic equivalence requires evidence; do not require verbatim
  wording or invent equivalence. Preserve uncertainty.
- Code reference resolutions, authority inheritance, evidence promotions,
  verification upgrades and aggregate state, with evidence and uncertainty.
  A Boolean authority label must not be guessed to satisfy the schema.
- Record boundary contracts only when actual preserved artifacts, hashes and
  covered claim IDs substantiate them. An identifier alone is insufficient.
- Record task state using the inherited rubric. Format acceptability and semantic
  task adequacy are separate. The coordinator will apply the recorded v0.2
  grammar disposition; do not repair or omit inconvenient output text.
- Record residual unblinding and reviewer notes. Save a versioned record without
  replacing the original template or another coder's record.

normalized_output uses the existing classifier schema's field names. Consult
schemas/unsupported_inheritance_classifier_input_s001_v0_1.schema.json for exact
shapes and enums. Empty lists are substantive assertions of absence and must be
supported; leave unresolved fields null until adjudication.

## Adjudication

Hash and preserve each coder's completed record before comparison. Use the
separate adjudication template to bind both records, identify all disagreements,
record adjudicator identity/time, and document each resolution with source/output
evidence. Do not overwrite either original coding. Unresolved required semantic
fields make the response unclassifiable for primary scoring, rather than zero.
The adjudicator/coordinator must separately decide and record primary eligibility.

The final response's parser rejection remains part of the primary v0.2 grammar
record. Its full content can be independently examined as an explicitly exploratory
case. Extracting its JSON does not automatically admit it to primary analysis.
