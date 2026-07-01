# CBC / CCE v0.2.2 Enforcement Repair

## Status

Repair note: `CBC_CCE_v0_2_2_ENFORCEMENT_REPAIR`

Base commit:

- `4cbe52e` -- Add CBC and CCE v0.2.2 final precision hardening patch

## Purpose

This repair restores strict boundary-effect enforcement that was present in v0.2.1 but softened during v0.2.2 drift-closure work.

This is not a doctrine change.

It preserves v0.2.2's final hardening while re-closing three relational enforcement surfaces before v0.3 graph verification.

## Repaired surfaces

### PRESERVED

A `PRESERVED` CCE must not contain boundary-change fields.

It cannot contain:

- `narrowing_reason`;
- `expansion_reason`;
- `new_claim_reference`;
- `new_claim_boundary_contract_id`;
- `authorizing_party`;
- `additional_evidence_refs`.

### NARROWED

A `NARROWED` CCE must include a `narrowing_reason`.

It cannot contain expansion fields.

### EXPANDED

An `EXPANDED` CCE must include:

- `expansion_reason`;
- `new_claim_reference`;
- `new_claim_boundary_contract_id`;
- `authorizing_party`;
- `additional_evidence_refs`.

## Additional precision edits

The CCE expanded-claim non-claim now uses "direction and destination of expansion" instead of "vector of expansion."

The limited internal review example now uses "applicable internal review process" rather than "stated internal review process."

The CBC partial verification posture now says partial scopes must not be used to "assert or suggest" completeness.

## Relationship to v0.3

v0.3 stateless relational graph verification should build on this repaired v0.2.2 surface.

Boundary-effect semantics must be strict before graph traversal begins.
