# Observation Intake Template v0.1

identifier:
observer:
date:
interaction_type:
  - technical recomputation
  - architectural observation
  - governance observation
  - interoperability observation
  - semantic pressure observation
  - upstream admission observation
  - downstream procurement observation
  - scope declination
  - consulting scope signal
scope_requested:
scope_performed:
execution_status:
artifacts_reviewed:
endorsement: none
limitations:
attribution_preference:
permission_to_preserve:
classification:
  - boundary interpretation
  - semantic pressure surface
  - upstream admission
  - downstream procurement
  - role separation
  - consulting scope signal
  - failure-case proposal

## 1. Observation

[Observer text here.]

## 2. Boundary interpretation

What does Fork appear to preserve?

What does Fork appear not to claim?

Where does evidence remain distinct from authority?

Where does structural recomputation remain distinct from truth-claim sufficiency?

## 3. Misunderstandings or ambiguity

What was unclear?

Which terms created confusion?

Which claims felt too broad?

## 4. Pressure cases

What failure cases should Fork test?

## 5. Adjacent-system mapping

Which neighboring systems or functions does Fork appear to touch?

Which responsibilities should remain outside Fork?

## 6. Non-endorsement

No endorsement, certification, approval, validation, production-readiness conclusion, legal conclusion, or compliance conclusion is implied.

## Taxonomy Clarification v0.1.1

`interaction_type` describes the mode of engagement.

`classification` describes the analytical content of the observation.

These fields should not be treated as a single taxonomy.

## Access Mode Reporting v0.1.2

Observers should report access mode results explicitly:

```yaml
execution_status: not_performed
access_modes:
  github_rendered: succeeded
  raw: failed
  plaintext_packet: not_attempted
  repository_clone: not_attempted
  pasted_content: not_attempted
artifacts_requested:
  - EXPERIMENT_PROTOCOL_v0_1.md
  - OBSERVER_INSTRUCTIONS_v0_1.md
artifacts_inspected:
  - EXPERIMENT_PROTOCOL_v0_1.md
```

`execution_status` is not the same as access status.

Missing execution status, unknown execution status, failed retrieval, and not-performed execution must remain distinguishable.

## Active Non-Endorsement Attestation v0.1.3

Observers should actively acknowledge the non-endorsement boundary when submitting an observation.

Recommended structured field:

```yaml
non_endorsement_attestation:
  acknowledged: true
  statement: "By submitting this observation, the observer acknowledges that no endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied."
```

This attestation is an intake boundary. It does not make the observation authoritative. It records that the observer understands the observation is exterior commentary and not authority for Fork's claims.
