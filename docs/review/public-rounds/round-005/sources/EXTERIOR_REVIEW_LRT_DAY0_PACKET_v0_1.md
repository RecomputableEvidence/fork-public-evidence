# Exterior Review: Longitudinal Reconstruction Day-0 Packet v0.1

Status: Exterior access-path review, execution receipt, adversarial boundary-pressure observation.
Reviewer: Claude (Anthropic), acting as an outside reviewer with no repository write access.
Repo: RecomputableEvidence/fork-public-evidence
Reviewed object: `docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/`

Scope statement, as instructed by the review requester: this document does not assess Fork as production-ready, legally sufficient, compliant, safe, approved, certified, endorsed, or authoritative. It answers one bounded question: does the Day-0 packet preserve enough evidence for a future reviewer to reconstruct the declared Day-0 state without inheriting the author's authority. Every command below was executed in a fresh clone in a disposable Linux container; nothing here is an opinion about Fork's merit.

## Commit hash reviewed

- HEAD short: `03f25f0`
- HEAD full: `03f25f0e52109e8545c188c2bcc329fac4f701f7`
- Commit date: 2026-07-09 23:19:48 -0700
- Subject: Add longitudinal reconstruction Day-0 packet
- Branch: main, tracking origin/main, working tree clean.
- Packet manifest generated_from_base_commit: `e4555b93e8ce25d974de1c6a300049021862ba90`
- Reviewer confirmed the generated_from_base_commit is HEAD's immediate parent, distance 1.

## Environment

| Item | Value |
|---|---|
| OS | Linux container, Ubuntu 24.04.4 LTS, kernel 6.18.5 |
| Shell | bash 5.2.21 |
| Python | 3.12.3 |
| Git | 2.43.0 |
| PowerShell / pwsh | Not present |

## Public quickstart

Structurally sufficient, but primary verifier path is PowerShell-only. Linux/macOS reviewers without pwsh lack a documented one-command fallback equivalent to `scripts/verify_public_review_package_v0_1.ps1`.

## Expanded verifier

The PowerShell verifier did not run because pwsh was unavailable.

The reviewer manually reconstructed the verifier's checks:

- 50/50 required paths present;
- boundary-pressure checker: 4/4 default, 4/4 adversarial;
- Round 004 checker: 4/4;
- Day-0 checker: 27/27;
- git diff --check and git diff --cached --check: exit 0.

This must be recorded as manual reconstruction, not a verifier run.

## Day-0 checker

The reviewer executed:

- `python3 tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json`

Result:

- 27/27 passed;
- 0 failed.

Mechanism-level findings:

- Artifact hashes, manifest sidecar, outer receipt binding, expected reconstruction hash, environment manifest hash, and boundary statement hash are real byte-level SHA-256 checks.
- Non-authority language checks are lexical substring checks, not semantic or negation-aware checks.
- generated_from_base_commit is field-presence only; the checker does not call git to confirm the commit exists or is an ancestor.
- The manifest schema is declared and required-present by public verifier path coverage, but the Day-0 checker does not load or enforce the schema.
- Evidence records and receipts receive file-presence and aggregate byte-hash coverage, but not field-level or lexical assertions of their own.

## Manifest, sidecar, and outer receipt

The binding chain was understandable:

- artifact bytes to manifest artifact_hashes;
- manifest bytes to packet_manifest.sha256;
- manifest bytes to packet_manifest_outer_receipt.json packet_manifest_sha256.

Both manifest bindings matched on recomputation.

## Expected reconstruction provenance

The expected reconstruction is clearly marked author-declared, not independent.

However, it is narrower than the protocol section 8 bar. The protocol describes independent hand-authorship, separate implementation, or LLM-generated independently reviewed ground truth, with named artifacts such as source_event_sequence.json and ground_truth_review_receipt.md. The Day-0 packet does not ship those named artifacts and does not claim those methods.

## Future Day-7/30/90 needs

- pinned Day-0 replay checker;
- Day-7, Day-30, Day-90 replay receipts;
- independent expected-reconstruction provenance;
- protocol section 8 named artifacts if the trial intends to conform to that structure;
- external anchoring for the manifest chain;
- field-name reconciliation between protocol and manifest/checker;
- adverse longitudinal fixtures for payload tamper, manifest tamper, policy drift, missing historical reference, and receipt overread.

## Overclaim and overread risk

Direct overclaim in current text was low.

Findings:

- CURRENT_PROOF_SURFACE_v0_1.md still stated Day-0 fixture not yet implemented, while a later appended section stated the Day-0 packet is now present.
- PUBLIC_REVIEW_QUICKSTART_v0_1.md contained the same stale-status contradiction.
- Receipt-overread risk exists if a future reviewer treats byte verification of evidence records as semantic content verification.

## Adversarial cases executed

### Case A: Coordinated re-seal

In a disposable copy, the reviewer edited `receipts/day0_expected_reconstruction_provenance_receipt.json` to falsely claim independent provenance, recomputed that file hash into packet_manifest.json, recomputed packet_manifest.sha256, recomputed packet_manifest_outer_receipt.json, and ran the unmodified Day-0 checker.

Result:

- 27/27 passed;
- 0 failed.

Interpretation:

The checker cannot distinguish never-tampered from tampered-and-consistently-resealed because checks are relative to the current manifest, not to a hash pinned outside the packet at original sealing time.

Suggested outcome codes:

- MANIFEST_INTERNALLY_CONSISTENT_BUT_UNANCHORED
- SEMANTIC_CONTENT_CHANGE_UNDETECTED_BY_LEXICAL_CHECK
- ROOT_OF_TRUST_SCOPE_LIMIT_CONFIRMED

### Case B: Keyword-present authority assertion

The reviewer imported the checker's own has_boundary_terms function and tested it against a sentence containing all required boundary terms while asserting authority rather than disclaiming it.

Result:

- zero missing terms;
- same pass verdict as the real boundary statement.

Interpretation:

The non-authority check is keyword-presence only. It is not semantic or negation-aware.

## Summary

The Day-0 packet passed its checker and is structurally inspectable. The review found useful next-boundary work: cross-platform verifier parity, stale-status repair, protocol-vs-artifact reconciliation, schema enforcement clarification, coordinated re-seal adversarial testing, and lexical-limit documentation or tests.

No item above establishes that Fork is true, compliant, legally sufficient, safe, authorized, approved, certified, endorsed, production-ready, or institutionally authoritative.