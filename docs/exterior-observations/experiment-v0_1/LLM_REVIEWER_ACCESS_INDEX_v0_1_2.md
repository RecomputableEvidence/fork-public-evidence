# LLM Reviewer Access Index v0.1.2

Identifier: LLM_REVIEWER_ACCESS_INDEX_v0_1_2
Status: Draft
Classification: Portable access support for LLM and automated reviewers

## Purpose

Some LLM and automated reviewers cannot reliably inspect GitHub directory views, GitHub-rendered file pages, or raw GitHub links.

This index supports multiple access modes:

1. GitHub-rendered links
2. raw GitHub links
3. plaintext review packet
4. repository clone
5. pasted content

If one access mode fails, the failure should be recorded as observance data.

## Primary fallback

Use the plaintext review packet if GitHub-rendered or raw links fail:

* GitHub-rendered:
  [https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/LLM_PLAINTEXT_REVIEW_PACKET_v0_1_2.md](https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/LLM_PLAINTEXT_REVIEW_PACKET_v0_1_2.md)

* Raw:
  [https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/LLM_PLAINTEXT_REVIEW_PACKET_v0_1_2.md](https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/LLM_PLAINTEXT_REVIEW_PACKET_v0_1_2.md)

## Machine-readable manifest

* GitHub-rendered:
  [https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/manifest.v0.1.2.json](https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/manifest.v0.1.2.json)

* Raw:
  [https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/manifest.v0.1.2.json](https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/manifest.v0.1.2.json)

## Intake schema

* GitHub-rendered:
  [https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/schema/observation_intake_v0_1_2.schema.json](https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/schema/observation_intake_v0_1_2.schema.json)

* Raw:
  [https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/schema/observation_intake_v0_1_2.schema.json](https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/schema/observation_intake_v0_1_2.schema.json)

## Core files

| Artifact                 | GitHub file                                                                                                                                                                                                                                                                                                                        | Raw file                                                                                                                                                                                                                                                                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Next-pass request        | [https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/NEXT_PASS_LLM_OBSERVANCE_REQUEST_v0_1_2.md](https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/NEXT_PASS_LLM_OBSERVANCE_REQUEST_v0_1_2.md)       | [https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/NEXT_PASS_LLM_OBSERVANCE_REQUEST_v0_1_2.md](https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/NEXT_PASS_LLM_OBSERVANCE_REQUEST_v0_1_2.md)       |
| Experiment Protocol      | [https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/EXPERIMENT_PROTOCOL_v0_1.md](https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/EXPERIMENT_PROTOCOL_v0_1.md)                                     | [https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/EXPERIMENT_PROTOCOL_v0_1.md](https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/EXPERIMENT_PROTOCOL_v0_1.md)                                     |
| Observer Instructions    | [https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/OBSERVER_INSTRUCTIONS_v0_1.md](https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/OBSERVER_INSTRUCTIONS_v0_1.md)                                 | [https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/OBSERVER_INSTRUCTIONS_v0_1.md](https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/OBSERVER_INSTRUCTIONS_v0_1.md)                                 |
| Intake Template          | [https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/templates/OBSERVATION_INTAKE_TEMPLATE_v0_1.md](https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/templates/OBSERVATION_INTAKE_TEMPLATE_v0_1.md) | [https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/templates/OBSERVATION_INTAKE_TEMPLATE_v0_1.md](https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/templates/OBSERVATION_INTAKE_TEMPLATE_v0_1.md) |
| Data Dictionary          | [https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/DATA_DICTIONARY_v0_1.md](https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/DATA_DICTIONARY_v0_1.md)                                             | [https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/DATA_DICTIONARY_v0_1.md](https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/DATA_DICTIONARY_v0_1.md)                                             |
| Coding Guide             | [https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/CODING_GUIDE_v0_1.md](https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/CODING_GUIDE_v0_1.md)                                                   | [https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/CODING_GUIDE_v0_1.md](https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/CODING_GUIDE_v0_1.md)                                                   |
| Analysis Plan            | [https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/ANALYSIS_PLAN_v0_1.md](https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/ANALYSIS_PLAN_v0_1.md)                                               | [https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/ANALYSIS_PLAN_v0_1.md](https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/ANALYSIS_PLAN_v0_1.md)                                               |
| Sandbox Failure Cases    | [https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/sandbox-v0_2/SANDBOX_FAILURE_CASES_v0_2_DRAFT.md](https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/sandbox-v0_2/SANDBOX_FAILURE_CASES_v0_2_DRAFT.md)                         | [https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/sandbox-v0_2/SANDBOX_FAILURE_CASES_v0_2_DRAFT.md](https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/sandbox-v0_2/SANDBOX_FAILURE_CASES_v0_2_DRAFT.md)                         |

## Non-endorsement

This access index does not assert endorsement, validation, certification, approval, production readiness, legal sufficiency, or compliance sufficiency.
