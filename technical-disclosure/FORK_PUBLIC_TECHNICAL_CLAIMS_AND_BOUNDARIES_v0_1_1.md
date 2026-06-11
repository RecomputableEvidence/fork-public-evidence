# Fork Public Technical Claims and Boundaries v0.1.1

*Public disclosure appendix to “Reconstructive Fidelity in the Age of AI”*

**Document class:** Public Architecture and Governance Note — Technical Appendix  
**Version:** 0.1.1  
**Status:** Patched Successor Public Disclosure Candidate  
**Fixture basis:** Declared synthetic reference corpus — no production or client data  
**Public disclosure build time:** 2026-06-11T18:49:54Z  
**Synthetic event-time semantics:** Fixed synthetic fixture times; not actual disclosure times  
**Production readiness:** NOT_ESTABLISHED

---

## Purpose

This appendix is the public technical anchor for Reference [4] in the white paper. It discloses only the capabilities and boundaries that the published fixture and verifier allow an external reviewer to recompute.

## Publicly Established Capabilities

The public fixture and `verify_public_disclosure.py` establish:

- explicit eligible workflow-member declaration;
- canonical SHA-256 member digests;
- canonical manifest-digest recomputation;
- HMAC-SHA-256 binding using a published non-secret test key;
- verification from persisted artifact bytes without invoking construction functions;
- granular PASS / FAIL / NOT_CHECKED gate states;
- recursive rejection of prohibited aggregate verdict fields;
- layered bundle inventory with a detached outer-ZIP receipt;
- mechanically reproduced semantic authority non-promotion checks.

The public fixture does **not** establish append-only persistence over time.

## Membership Eligibility Rule

`MEMBERSHIP_ELIGIBILITY_RULE: EXPLICIT`

Eligible workflow-member classes:

- `SOURCE_ASSERTION`
- `AI_OUTPUT`
- `HUMAN_REVIEW_RECORD`
- `INSTITUTIONAL_DISPOSITION`

Excluded control-plane classes:

- `PACKET_MEMBERSHIP`
- `PACKET_MANIFEST`
- `SEAL_BINDING`
- `TIMESTAMP_ANCHOR`

The verifier scans all JSON artifacts in `PUBLIC_REFERENCE_FIXTURE/`, classifies them by `_fork_artifact_class`, and fails if any eligible workflow artifact is present but undeclared.

## Claim-to-Gate Mapping

| Public capability | Gate | Result |
|---|---|---|
| Explicit eligible workflow membership | GATE_PUBLIC_001 | PASS |
| Member SHA-256 digests | GATE_PUBLIC_002 | PASS |
| Canonical manifest digest | GATE_PUBLIC_003 | PASS |
| Public test-key HMAC binding | GATE_PUBLIC_004 | PASS |
| Persisted-artifact recomputation | GATE_PUBLIC_005 | PASS |
| Granular state preservation | GATE_PUBLIC_006 | PASS |
| Append-only persistence | GATE_PUBLIC_006 sub-check | NOT_CHECKED |
| No aggregate trust verdict | GATE_PUBLIC_007 | PASS |
| Layered export inventory and digests | GATE_PUBLIC_008 | PASS |
| Semantic authority non-promotion | GATE_PUBLIC_009 | PASS — MECHANICALLY_REPRODUCED_GATE |
| Timestamp disclosure boundary | GATE_PUBLIC_010 | NOT_CHECKED |

## Timestamp Disclosure Boundary

| Sub-check | Result |
|---|---|
| TIMESTAMP_METADATA_RECORD_PRESENCE | PASS |
| RFC3161_REQUEST_RESPONSE_PAIR_PRESENCE | NOT_ESTABLISHED |
| MESSAGE_IMPRINT_OR_DIGEST_RELATIONSHIP | NOT_CHECKED |
| CERTIFICATE_TRUST_CHAIN_VALIDATION | NOT_CHECKED |
| INDEPENDENT_TIME_OF_EXISTENCE | NOT_ESTABLISHED |

The bundle contains `timestamp_anchor.json` as a metadata record. It does not contain `.tsq` or `.tsr` bytes and therefore makes no public RFC 3161 validation or independent time-of-existence claim.

## Semantic Non-Promotion

`SEMANTIC_NON_PROMOTION_METHOD: MECHANICALLY_REPRODUCED_GATE`

The included verifier checks that:

- the source record remains a `SOURCE_ASSERTION` with source truth `NOT_CLAIMED`;
- the AI output is not represented as an institutional decision;
- recorded human review is not promoted to policy satisfaction by Fork;
- institutional disposition meaning remains institution-defined;
- operative state is not promoted to a Fork-determined state.

## Time Coordinates

The release separates four temporal concepts:

| Coordinate | Meaning |
|---|---|
| SYNTHETIC_EVENT_TIME | Fixed timestamps inside the synthetic workflow fixture |
| FIXTURE_GENERATION_TIME | Synthetic construction coordinates retained for deterministic demonstration |
| VERIFICATION_EXECUTION_TIME | `2026-06-11T18:49:54Z` for this successor verification result |
| PUBLIC_DISCLOSURE_BUILD_TIME | `2026-06-11T18:49:54Z` for this release candidate |

Every fixture artifact states that its event timestamp is synthetic and is not the actual disclosure time.

## Bundle Integrity Layers

1. `SHA256SUMS.txt` hashes every ordinary disclosed file except itself and the public disclosure manifest.
2. `PUBLIC_DISCLOSURE_MANIFEST_v0_1_1.json` inventories the same ordinary files and records the SHA-256 of `SHA256SUMS.txt`.
3. `FORK_PUBLIC_TECHNICAL_DISCLOSURE_BUNDLE_v0_1_1.zip.sha256` is a detached receipt published outside the ZIP and anchors the complete ZIP, including the public disclosure manifest.

The public manifest does not hash itself. This is an explicit recursion-avoidance boundary, not an omitted claim.

## Public HMAC Key

```text
FORK_PUBLIC_DISCLOSURE_V0_1_1_NON_SECRET_TEST_KEY
```

- KEY_CONFIDENTIALITY: NOT_CLAIMED
- SIGNER_IDENTITY: NOT_ESTABLISHED
- NON_REPUDIATION: NOT_ESTABLISHED
- PURPOSE: DETERMINISTIC_PUBLIC_RECOMPUTATION_OF_THE_DECLARED_BINDING_METHOD

## Explicit Non-Claims

This disclosure does not establish:

- source truth or completeness;
- public signer identity or non-repudiation;
- append-only persistence over time;
- RFC 3161 request/response pair presence;
- independent time of existence;
- legal admissibility;
- compliance or ethical correctness;
- third-party verifier independence;
- live institutional deployment;
- production readiness.

## Public Bundle Inventory

```text
FORK_PUBLIC_TECHNICAL_CLAIMS_AND_BOUNDARIES_v0_1_1.md
PUBLIC_DISCLOSURE_MANIFEST_v0_1_1.json
SELECTED_PUBLIC_VERIFICATION_RESULT_v0_1_1.json
README_VERIFY_PUBLIC_DISCLOSURE_v0_1_1.md
verify_public_disclosure.py
SHA256SUMS.txt
PUBLIC_REFERENCE_FIXTURE/
SELECTED_PUBLIC_SCHEMAS/
```

The detached outer-ZIP receipt is published beside, not inside, the ZIP.

## Controlled Disclosure

The complete internal gate registry, full implementation package, operational scripts beyond the public verifier, internal release package, and client-operator materials remain under controlled disclosure.

*Soli Deo Gloria*
