# Scope and Non-Claims

## In scope

This object defines and tests a typed representation for:

- subject identity at the semantic layer;
- positive claims and their declared basis;
- explicit non-claims;
- evidence references and disclosure/access state;
- authority-transfer state as a declared field;
- unresolved state;
- revalidation requirements;
- predecessor linkage without semantic inheritance.

## Out of scope

This object deliberately excludes:

- canonical byte encoding;
- cryptographic digests of handoff objects;
- issuer signatures or signer identity;
- institutional authorization validation;
- trusted timestamps;
- transparency-log inclusion;
- external-witness receipts;
- proof of event-population completeness;
- legal, compliance, safety, production, procurement, or governance conclusions.

## Non-inheritance boundary

The following implications are prohibited:

```text
TYPED != TRUE
SCHEMA_VALID != CORRECT
REFERENCE_PRESENT != EVIDENCE_AVAILABLE
EVIDENCE_AVAILABLE != EVIDENCE_SUFFICIENT
CLAIM_BASIS_DECLARED != BASIS_VERIFIED
AUTHORITY_TRANSFER_ASSERTED != AUTHORITY_VALID
PREDECESSOR_LINKED != PREDECESSOR_STANDING_INHERITED
UNRESOLVED_LIST_EMPTY != COMPLETE
REVALIDATION_LIST_PRESENT != REVALIDATION_PERFORMED
SEMANTIC_CORE_PASS != CRYPTOGRAPHIC_INTEGRITY
SEMANTIC_CORE_PASS != INDEPENDENT_WITNESSING
```

## Construction rule

No field in this semantic-core object may be interpreted as a cryptographic or institutional trust signal unless a later separately bounded object defines and qualifies that property.

## v0.1.1 interpretation-boundary regression

The packaged `VALID_004_DECLARED_TRUTH_BOUNDARY.json` intentionally demonstrates that a structurally consistent positive `TRUTH` claim with `claim_basis: DECLARED` can return `PASS`. That behavior is not truth adjudication. The explicit promotion `VALIDATOR_PASS != TRUTH_ESTABLISHED` is therefore preserved as a required interpretation boundary.
