# Authority and Policy Context Spec v0.1

## Purpose

The Authority and Policy Context section preserves the stated institutional context under which an AI-assisted claim, recommendation, memo, or workflow artifact was reviewed, accepted, or relied upon.

This section does not establish that the stated authority was sufficient, that the policy was adequate, or that the resulting reliance was legally, commercially, operationally, or regulatorily sufficient.

Its purpose is to prevent later reviewers from having to reconstruct the governance context from memory, surrounding systems, or unstated assumptions.

## Reviewer question

A reviewer should be able to answer:

Who accepted or relied on the claim, under what role or policy context, for what purpose, and did later use stay inside or move beyond that context?

## Required fields

A conformant reviewer-facing packet SHOULD expose the following fields when available:

| Field | Meaning |
|---|---|
| `accepted_by_role` | The role, group, or function that accepted or relied on the artifact. |
| `accepted_by_actor_or_group` | The named actor or group, if appropriate and permitted by privacy/security constraints. |
| `accepted_under_policy` | The policy, procedure, control, playbook, review process, or governance context asserted for the acceptance event. |
| `policy_version_or_reference` | The policy version, document reference, control ID, or process identifier if available. |
| `accepted_for_purpose` | The bounded purpose for which the artifact was accepted or relied upon. |
| `review_status` | The recorded review state, such as reviewed, modified, rejected in part, escalated, or unresolved. |
| `approval_status` | The recorded approval state, if any. Absence of approval must not be inferred as approval. |
| `authority_scope_statement` | A plain-language statement of the authority context asserted for the acceptance event. |
| `assumptions_and_unresolved_items` | Assumptions, open verification items, unresolved questions, or known gaps at the time of acceptance. |
| `authority_not_established` | Explicit statement that the record preserves stated authority context but does not establish authority sufficiency. |
| `downstream_authority_change` | Whether a later consumer narrowed, preserved, expanded, or attempted to expand the original authority context. |

## Required non-claim

Every reviewer-facing use of this section MUST preserve the following non-claim in substance:

This record preserves the stated authority and policy context associated with the review, acceptance, or reliance event. It does not establish that the reviewer had sufficient institutional authority, that the policy was adequate, that the review was complete, or that the resulting decision satisfied legal, compliance, audit, procurement, security, risk, executive, or regulatory requirements.

## Boundary behavior

If a downstream consumer uses the packet for a purpose outside the recorded authority or policy context, that use must be treated as a downstream authority-context change.

The change may be:

- `PRESERVED` - later use stays within the recorded authority and policy context.
- `NARROWED` - later use is more limited than the recorded authority and policy context.
- `EXPANDED` - later use attempts to rely beyond the recorded authority and policy context.
- `UNRESOLVED` - the later authority context cannot be determined from the packet.

Fork records the authority-context state and any downstream change. Fork does not decide whether the authority was valid, sufficient, legally effective, or institutionally adequate.

## Placement in reviewer artifacts

Authority and Policy Context SHOULD be visible in:

- Evidence Card
- Boundary Map
- Review Packet
- Non-Claim Panel
- Verification Receipt when the verification receipt lists packet sections or required panels

## Not established by this section

This section does not establish:

- legal authority;
- compliance satisfaction;
- audit sufficiency;
- procurement approval;
- security approval;
- production readiness;
- executive approval;
- regulatory adequacy;
- correctness of the AI-assisted output;
- completeness of the evidence base;
- adequacy of the policy or governance process;
- institutional authority beyond the recorded context.

## Policy Reference Non-Claim

Presence of a policy reference does **not** imply:

- policy applicability;
- policy approval;
- compliance determination;
- authority sufficiency;
- legal adequacy;
- operational readiness.

A policy reference records only that a policy context was asserted or referenced in the bounded workflow record.

Any determination that the policy was applicable, adequate, current, satisfied, or sufficient requires separate institutional authority.

## Required Structural Separation

Authority and policy context records should keep the following concepts structurally distinct:

| Field | Meaning | Non-Claim |
|---|---|---|
| Referenced policy | A policy was cited, asserted, or attached as context | Does not imply the policy applies |
| Recorded authority context | A role, actor, or process was recorded as part of the workflow context | Does not imply authority was sufficient |
| Validated applicability | A separate authorized process determined the policy applied | Not established by Fork unless separately recorded |
| Approved compliance status | A separate authorized process determined compliance status | Not established by Fork |
| Approved decision status | A separate authorized process approved a decision | Not established by Fork |

Fork records policy and authority context only as bounded evidence context. It does not validate, approve, certify, or complete that context.
