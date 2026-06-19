# SYSTEM_MAPPING_RECEIPT v0.1

## Purpose

A SYSTEM_MAPPING_RECEIPT records how a downstream consumer maps an upstream claim boundary.

It is designed for handoff situations where one system consumes, references, summarizes, routes, transforms, or operationalizes another system's claim boundary. The receipt records whether each consumed claim boundary was preserved, narrowed, expanded, or left unresolved.

The receipt is evidentiary. It is not an approval instrument.

## Core question

When a downstream system consumes an upstream record, what happened to the upstream boundary?

The receipt records whether the downstream consumer:

- preserved the upstream claim boundary;
- narrowed the upstream claim boundary;
- expanded the upstream claim boundary;
- carried unresolved pointers forward;
- dropped non-claims;
- added new downstream claims with separate authority references.

## Design principle

Boundary expansion should be visible enough that institutions cannot accidentally inherit claims no one actually made.

## Receipt behavior values

### PRESERVED

The downstream consumer retained the upstream claim boundary and preserved the relevant non-claims.

### NARROWED

The downstream consumer relied on a narrower portion of the upstream claim boundary without adding a broader claim.

### EXPANDED

The downstream consumer added a claim not present in the upstream record. Expansion requires an explicit authority reference and evidence references for each added claim.

### UNRESOLVED

The downstream consumer did not resolve one or more upstream pointers and carried that unresolved state forward.

### MIXED

The downstream consumer performed more than one boundary behavior across the per-claim records. MIXED requires per-claim boundary behavior records.

## Required receipt posture

A SYSTEM_MAPPING_RECEIPT must make boundary behavior explicit at the per-claim level.

A receipt must not silently convert unresolved pointers into resolved claims.

A receipt must not silently drop upstream non-claims.

A receipt must not add downstream claims without separate authority references.

## Non-claims

A SYSTEM_MAPPING_RECEIPT does not claim that the downstream system is:

- legally sufficient;
- compliant;
- safe;
- true;
- authorized;
- deployment-ready;
- clinically appropriate;
- financially correct;
- policy-approved;
- risk-accepted.

A SYSTEM_MAPPING_RECEIPT does not decide whether expansion is permitted. It records whether expansion was declared with sufficient structural references.

## Checker output vocabulary

The checker avoids approval-oriented output vocabulary.

Allowed result kinds for this checker are descriptive records, not approval signals:

- STRUCTURAL_MAPPING_RECORDED
- MAPPING_INCOMPLETE_RECORDED
- EXPANSION_AUTHORITY_GAP_RECORDED
- NON_CLAIM_DROP_RECORDED
- UNRESOLVED_POINTER_MAPPING_GAP_RECORDED

These result kinds must not be mapped to approval, compliance, safety, readiness, authorization, truth, waiver approval, deployment approval, or control effectiveness.

## Structural checks in v0.1

The v0.1 checker records structural mapping issues only.

It checks that:

- receipt type and version are present;
- source and consumer references are present;
- at least one boundary behavior record exists;
- MIXED declaration has mixed per-claim behavior;
- non-MIXED declaration matches per-claim behavior;
- expansion includes downstream added claims;
- each downstream added claim includes authority and evidence references;
- dropped non-claims are explicitly disclosed;
- preserved records do not drop non-claims;
- unresolved pointers are carried forward or resolved with evidence;
- unresolved pointers are not silently resolved.

## Scope boundary

This v0.1 artifact defines SYSTEM_MAPPING_RECEIPT structure and a deterministic checker.

It does not alter CBC, CCE, RGV, CCEC, claim-inheritance, or broader Fork governance semantics.

## v0.1 review hardening notes

### Receipt-declared coverage

The v0.1 receipt includes `source_claim_refs` and `source_non_claim_refs`.

The checker verifies receipt-declared coverage by requiring each declared upstream claim reference to appear in `boundary_behavior_records[].claim_ref`.

The checker also verifies that each declared upstream non-claim reference appears in either `preserved_non_claims` or `dropped_non_claims`.

This is an internal structural coverage check for the receipt. It does not independently fetch or validate the upstream source record. Independent upstream-manifest cross-checking is reserved for a later alignment harness.

### MIXED behavior

`MIXED` is an aggregate declaration only.

It is not a leaf-level result. A MIXED receipt requires per-claim `boundary_behavior_records` showing which claims were preserved, narrowed, expanded, or left unresolved.

Downstream consumers must not treat MIXED as approval, readiness, or a single flattened disposition. MIXED requires per-claim inspection.

### EXPANDED behavior

`EXPANDED` records require downstream added claims.

Each downstream added claim requires a non-empty `authority_ref` and at least one evidence reference.

The checker also rejects authority references that point back to Fork structural receipts, checker artifacts, schemas, or the consuming system itself. Fork records structural evidence boundaries; it does not provide substantive authority for downstream claim expansion.

### UNRESOLVED behavior

`UNRESOLVED` is a visible mapping state, not a default approval state.

A receipt carrying unresolved pointers can be structurally recorded as provisional mapping evidence, but unresolved pointers must not be silently treated as preserved, narrowed, expanded, approved, compliant, or resolved.

### Non-decisional result semantics

`STRUCTURAL_MAPPING_RECORDED`, `STRUCTURAL_MAPPING_PROVISIONAL_RECORDED`, and gap-recording result kinds are evidence records.

They may inform separate review, policy, or governance processes, but they do not themselves approve, reject, authorize, certify, or determine compliance.
