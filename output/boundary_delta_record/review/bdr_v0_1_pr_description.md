# Boundary Delta Record v0.1 — hardened technical review candidate

## Summary

This PR adds Boundary Delta Record v0.1 as a narrow mechanical inspection artifact for Fork.

BDR v0.1 inspects declared boundary transitions and determines whether the record is structurally inspectable under finite v0.1 rules. It is designed to make declared boundary expansion and transition mismatch visible without becoming a semantic, policy, risk, compliance, safety, legal, or approval interpreter.

## Current branch evidence

- Branch: $Branch
- HEAD: $HeadFull
- Tree: $Tree
- Mismatch fixture hash: $FixtureHash

Recent commits:

`	ext
3237682 Relax BDR v0.1 review gate to current branch HEAD
ce92c23 Add BDR v0.1 technical review scripts
e1612fa Harden BDR non-inference and transition compatibility
`

Mismatch fixture history:

`	ext
730e906 Enforce BDR transition rule compatibility
`

## Core locks

BDR v0.1 is constrained by:

- declared inputs only
- opaque references only
- finite transition vocabulary
- finite transition kind / transformation rule compatibility map
- binary outcome only: INSPECTABLE / NOT_INSPECTABLE
- no natural-language inference
- no scoring, severity, confidence, risk, approval, or policy judgment
- authored structural_outcome is recomputed and not trusted as authoritative

## Hardened behavior

The checker emits explicit non-inference limitations:

- does_not_infer_scope_from_text
- does_not_infer_authority_from_text
- does_not_infer_evidence_requirements_from_text
- requires_declared_transitions
- treats_references_as_opaque_tokens

The adversarial mismatch fixture returns:

- NOT_INSPECTABLE
- TRANSITION_KIND_RULE_MISMATCH

The valid preserved fixture returns:

- INSPECTABLE

## What BDR v0.1 does not claim

BDR v0.1 does not determine truth, safety, compliance, legal sufficiency, approval, admissibility, risk, severity, or upstream completeness. NOT_INSPECTABLE is a structural inspection outcome only.

## Review ask

Please review this PR against one narrow question:

> Does BDR v0.1 mechanically expose declared boundary expansion and transition mismatch without becoming a semantic, policy, risk, or governance interpreter?

## Deferred backlog

Deferred outside this v0.1 branch:

- schema/checker enum parity tests
- canonicalization tests
- reviewer harness script hardening
- schema/checker authority relationship clarification
- declared requires_* / transferred_* model
- cross-record or bundle-level verification
