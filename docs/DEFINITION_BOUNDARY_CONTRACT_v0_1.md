STATUS: INTERNAL_CONTRACT
DEPENDS_ON:
  - docs/CLAIM_BOUNDARY_CONTRACT_v0_1.md
  - docs/CLAIM_BOUNDARY_ENFORCEMENT_PHASE_2.md
  - docs/CLAIM_BOUNDARY_BINDING_v0_1.md

TITLE: Fork Definition Boundary Contract v0.1

1. Purpose

Fork must not silently convert observed identifiers into natural-person identity,
authority, meaningful review, or verified human presence.

Fork may preserve observed identifiers and undefined states.

Fork may only resolve undefined identity states when an approved definition
profile explicitly permits that resolution.

2. Core Definition

A Definition Boundary is an explicit constraint on what a system, artifact,
verifier, reviewer summary, or reconstruction layer is permitted to define,
classify, stabilize, or resolve.

Claim Boundaries constrain inference:
  What may this evidence establish?

Definition Boundaries constrain classification:
  What may this system define this thing as?

3. First Boundary Type: IDENTITY_UNDEFINED

Boundary type:
  IDENTITY_UNDEFINED

Under IDENTITY_UNDEFINED, Fork may observe identifiers and states, but it must
not define natural-person identity, verified human presence, or authorization.

Allowed observations include:
  - account_id
  - actor_label
  - system_user_id
  - workflow_role_label
  - approval_state
  - review_state
  - timestamp
  - source_event_id

Forbidden definitions include:
  - natural person identity
  - human presence
  - legal identity
  - verified identity
  - authorized reviewer
  - meaningful human review
  - actual person performed action

4. v0.1 Scanner Discipline

Definition Boundaries v0.1 intentionally start narrow.

The IDENTITY_UNDEFINED checker must:

  - Scan only the fields where Fork is making or permitting a definition.
  - Not scan the doctrine fields that list forbidden definitions.

Concretely, under IDENTITY_UNDEFINED:

  - The checker MUST scan:
      - definition_statement
      - allowed_definitions

  - The checker MUST NOT scan:
      - forbidden_definitions

This mirrors Claim Boundaries v0.1, which scan only claim_statement and
allowed_inferences, not forbidden_inferences.

5. First Failure Code

Failure code:
  DEFINITION_EXPANSION_DEFECT

Meaning:
  Under IDENTITY_UNDEFINED, the Definition Boundary payload attempted to define
  identity, human presence, authorization, or meaningful review beyond its
  allowed scope.

6. v0.1 Phrase Policy

Definition Boundary v0.1 does not attempt to detect all possible identity
overdefinition. It enforces a deliberately small, dangerous class.

Under IDENTITY_UNDEFINED, the checker rejects payloads whose
definition_statement or allowed_definitions contain identity-expanding phrases
such as:

  - natural person
  - human approved
  - person approved
  - identity verified
  - verified identity
  - authorized reviewer
  - reviewer was authorized
  - meaningful review
  - meaningful human review
  - employee approved
  - legal identity
  - actual human
  - Ryan approved

The checker must still allow observed-identifier phrases such as:

  - observed account_id
  - observed actor_label
  - observed approval_state
  - recorded system user
  - source event reports

7. v0.1 Invariant

Fork must preserve undefined identity states as undefined unless an approved
definition profile explicitly permits resolution.

Undefined is not a defect. It is an evidentiary state.

8. Architectural Position

In the Fork boundary stack:

  - Claim Boundary: prevents evidence from claiming too much.
  - Definition Boundary: prevents systems from classifying too much.
  - Reconstruction Boundary: will prevent later analysis from reconstructing too much.
  - Hypothesis Boundary: will prevent downstream reasoning from rewriting
    uncertainty as fact.

Definition Boundary v0.1 establishes:

  An observed account is not a verified human.
