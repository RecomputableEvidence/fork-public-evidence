# Access and Interpretation Classification v0.1.4

Identifier: ACCESS_INTERPRETATION_CLASSIFICATION_v0_1_4
Status: Draft
Classification: Exterior observance classification guidance
Applies to: Exterior Observance Experiment v0.1.4 candidate

No endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied.

## Purpose

This document classifies observer access and interpretation behavior so failed retrieval, conceptual substitution, packet-only review, multi-file review, and second-order observance are not collapsed into a single undifferentiated review category.

## Required classification fields

Recommended fields for each observation record:

```yaml
access_status: unknown
retrieval_fidelity: unknown
access_mode:
  github_rendered: unknown
  raw: unknown
  plaintext_packet: unknown
  repository_clone: unknown
  pasted_content: unknown
interpretation_scope: unknown
substantive_packet_review: unknown
source_contamination: unknown
execution_status: not_performed
schema_or_data_layer_inspected: unknown
non_endorsement_preserved: unknown
recommended_preservation: unknown
```

## Access status vocabulary

| Value           | Meaning                               |
|----------------|----------------------------------------|
| not_performed  | No retrieval was attempted.           |
| attempted_failed | Retrieval was attempted and failed. |
| performed      | Retrieval succeeded.                  |
| partial        | Some artifacts were retrieved and others failed. |
| unknown        | Access status cannot be determined from the observation. |

## Retrieval fidelity vocabulary

| Value           | Meaning                               |
|----------------|----------------------------------------|
| zero           | No source content was retrieved.       |
| prompt_only    | The observer relied only on the user's prompt. |
| plaintext_packet | The plaintext packet was retrieved or pasted. |
| packet_only    | The packet was inspected, but linked data/schema/repository layers were not. |
| multi_file     | Multiple linked artifacts were inspected directly. |
| repository_clone | The repository was cloned or otherwise inspected as a repository. |
| executable     | Code, schemas, or checks were executed. |
| unknown        | Fidelity cannot be determined.         |

## Interpretation scope vocabulary

| Value                     | Meaning                                |
|---------------------------|----------------------------------------|
| none                      | No substantive analysis was performed. |
| conceptual_only           | Analysis is generic or design-oriented and not source-grounded. |
| documentation_layer_only  | Markdown/plaintext documentation was reviewed, but schema/data/executable layers were not inspected. |
| data_schema_layer         | CSV, JSON, schema, or structured data artifacts were inspected. |
| direct_raw_multi_file_review | Multiple raw files were reviewed directly. |
| second_order_observance   | The observer reviewed a synthesis or batch writeup rather than the source packet. |
| unknown                   | Interpretation scope cannot be determined. |

## Source contamination

Source contamination occurs when an observer fails to retrieve the requested artifact but still produces analysis that appears source-aware by substituting:

- generic governance patterns;
- unrelated external citations;
- inferred architecture;
- prior context;
- unrelated standards;
- broad design advice;
- fabricated access claims.

Source contamination must not be treated as packet review.

It may be preserved as an input-integrity pressure signal.

## Preservation classification

| Classification                             | Use when |
|-------------------------------------------|---------|
| access_mode_failure                       | Retrieval failed and no substantive source claim was made. |
| source_contamination_after_failed_retrieval | Retrieval failed but analysis continued using generic or unrelated sources. |
| conceptual_only_after_failed_retrieval    | Retrieval failed and the response offered generic design advice. |
| raw_packet_success_documentation_layer_only | Packet was retrieved and reviewed, but only at documentation layer. |
| direct_file_review_with_artifact_boundary_findings | Multiple files were reviewed and artifact-local boundary issues were identified. |
| second_order_observance_not_packet_review | A batch synthesis or prior writeup was reviewed rather than the packet. |
| execution_or_schema_validation_performed  | The observer executed checks, validated schema, or inspected machine-readable artifacts directly. |
| unknown                                   | Insufficient information to classify. |

## Anti-collapse rule

Do not collapse the following into the same category:

- failed retrieval and packet review;
- packet review and repository review;
- documentation-layer review and schema/data-layer review;
- conceptual design advice and source-grounded observation;
- repeated observations and consensus;
- coded observations and audit rigor;
- packet inclusion and sufficiency;
- analyst participation and endorsement.

## Non-endorsement

No endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied.
