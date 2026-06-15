# AI Governance System Mapping Record Template v0.1

Status: Template
Version: v0.1
Parent architecture: AI Governance Mapping System v0.1

## Instructions

Use this template to describe an AI-governance system before integration or artifact handoff.

The purpose is to prevent silent claim inheritance by making claims, non-claims, artifacts, authority boundaries, verification models, and handoff rules explicit.

Do not use this template to claim adoption, certification, legal sufficiency, compliance sufficiency, or interoperability.

## 1. Record metadata

```yaml
record_version: "v0.1"
record_status: "DRAFT | SELF_DECLARED | REVIEWED | SUPERSEDED"
system_id: ""
system_name: ""
system_owner: ""
record_author: ""
created_at: ""
updated_at: ""
```

## 2. System function

Describe the system's primary function.

```text
SYSTEM_FUNCTION:
-
```

## 3. Pipeline position

Where does the system sit?

Examples:

* runtime anchoring,
* pre-execution governance,
* execution control,
* inference telemetry,
* continuation validity,
* admissibility-before-bind,
* authorization-context continuity,
* evidence preservation,
* evidentiary reconstruction,
* compliance review,
* audit review,
* legal interpretation,
* risk acceptance,
* remediation,
* reporting.

```text
PIPELINE_POSITION:
-
```

## 4. Supported claims

What does the system affirmatively claim within its own boundary?

```text
SUPPORTED_CLAIMS:
-
```

For each claim, specify where possible:

```yaml
claim_type: ""
claim_statement: ""
scope: ""
verification_method: ""
assurance_level: "CRYPTOGRAPHIC | DETERMINISTIC | HEURISTIC | ASSERTED"
authority_basis: ""
limitations:
  - ""
```

## 5. Explicit non-claims

What does the system explicitly refuse to claim?

```text
EXPLICIT_NON_CLAIMS:
-
```

Examples:

* no AI correctness claim,
* no decision correctness claim,
* no legal admissibility claim,
* no compliance satisfaction claim,
* no audit sufficiency claim,
* no source completeness claim,
* no institutional authority claim,
* no runtime control claim.

## 6. Emitted artifacts

What artifacts does the system produce?

```text
EMITTED_ARTIFACTS:
-
```

Examples:

* receipt,
* hash,
* trace ID,
* manifest,
* verdict,
* policy version,
* authority assertion,
* runtime output reference,
* reviewer action,
* verification result,
* evidence packet,
* public-log reference.

## 7. Consumable artifacts

What artifacts may the system consume from upstream or adjacent systems?

```text
CONSUMABLE_ARTIFACTS:
-
```

## 8. Verification model

How does the system verify its native claims?

```text
VERIFICATION_MODEL:
-
```

Examples:

* cryptographic hash recomputation,
* manifest verification,
* public-log lookup,
* schema validation,
* deterministic policy evaluation,
* runtime telemetry inspection,
* human assertion,
* audit review.

## 9. Authority boundary

What authority does the system have?

What authority does it lack?

```text
AUTHORITY_BOUNDARY:
-
```

Minimum rule:

```text
A system may verify an artifact without having authority to assert downstream claims about it.
```

## 10. Dependency boundary

What dependencies must remain available, referenced, or declared?

```text
DEPENDENCY_BOUNDARY:
-
```

## 11. Unknowns

What remains unknown even if the system operates correctly?

```text
UNKNOWNS:
-
```

## 12. Failure states

What failures can this system surface?

```text
FAILURE_STATES:
-
```

Examples:

* verification failure,
* unsupported claim type,
* authority mismatch,
* dependency inconsistency,
* missing non-claims,
* missing unknowns,
* transitivity violation,
* opaque claim consumption,
* evaluation creep,
* evidence unavailable,
* not checked,
* unresolved conflict.

## 13. Safe handoff surfaces

What may safely pass to another system?

```text
SAFE_HANDOFFS:
-
```

For each handoff, specify:

```yaml
artifact: ""
allowed_downstream_use: ""
claims_that_may_be_preserved:
  - ""
claims_that_require_reverification:
  - ""
claims_that_must_not_transfer:
  - ""
non_claims_that_must_travel:
  - ""
unknowns_that_must_travel:
  - ""
dependencies_that_must_travel:
  - ""
```

## 14. Prohibited claim inheritance

Which claims must not be inherited by downstream systems?

```text
PROHIBITED_CLAIM_INHERITANCE:
-
```

## 15. Re-verification requirements

Which claims may only be reattached after local downstream verification?

```text
RE_VERIFICATION_REQUIREMENTS:
-
```

## 16. Institutional dependencies

Which claims remain dependent on human, institutional, legal, audit, compliance, or risk authority?

```text
INSTITUTIONAL_DEPENDENCIES:
-
```

## 17. Mapping summary

Complete the summary in bounded language.

```text
This system proves:
-

This system does not prove:
-

This system emits:
-

A downstream system may preserve:
-

A downstream system must not infer:
-

Authority remains with:
-
```

## 18. v0.1 declaration

This mapping record is a placement artifact.

It does not certify the system.

It does not establish legal sufficiency.

It does not establish compliance sufficiency.

It does not establish production interoperability.

It exists to make claim boundaries explicit before artifact handoff.