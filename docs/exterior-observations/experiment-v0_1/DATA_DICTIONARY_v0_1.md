# Data Dictionary v0.1

Identifier: DATA_DICTIONARY_v0_1
Status: Draft

## Observation fields

| Field | Meaning |
|---|---|
| identifier | Stable observation record identifier |
| observer | Name, role, or anonymized label |
| date | Date observation was received |
| interaction_type | Type of contribution |
| scope_requested | What was asked of the observer |
| scope_performed | What the observer actually did |
| execution_performed | Whether the observer executed code or recomputation steps |
| artifacts_reviewed | Files, branches, docs, or sandbox elements reviewed |
| endorsement | Whether endorsement was provided; default should be none |
| limitations | Stated limits of the observation |
| attribution_preference | Named, role-only, anonymous, or private |
| permission_to_preserve | Whether the observation may be preserved |
| classification | Analytical tags assigned to the observation |

## Interaction types

| Type | Meaning |
|---|---|
| technical recomputation | Observer executed code or recomputation workflow |
| architectural observation | Observer interpreted system architecture |
| governance observation | Observer interpreted governance or authority boundary |
| interoperability observation | Observer mapped Fork to adjacent systems |
| semantic pressure observation | Observer identified language or classifier pressure |
| upstream admission observation | Observer identified execution-entry or admission boundary |
| downstream procurement observation | Observer identified procurement, ATO, or external review boundary |
| scope declination | Observer declined or bounded participation |
| consulting scope signal | Observer indicated further work requires formal engagement |

## Coding dimensions

| Dimension | Meaning |
|---|---|
| evidence_authority_distinction | Whether observer distinguished evidence from authority |
| recomputation_sufficiency_distinction | Whether observer distinguished recomputation from sufficiency |
| truth_claim_boundary | Whether observer treated truth-claims as external to preservation |
| semantic_pressure | Whether observer identified semantic classifier pressure |
| upstream_admission_mapping | Whether observer mapped Fork to governed execution or admission |
| downstream_review_mapping | Whether observer mapped Fork to procurement, ATO, or review packaging |
| role_separation | Whether observer preserved boundaries between projects or roles |
| failure_case_candidate | Whether observer proposed a testable failure case |
| misunderstanding | Whether observer revealed a misunderstanding useful for refinement |
