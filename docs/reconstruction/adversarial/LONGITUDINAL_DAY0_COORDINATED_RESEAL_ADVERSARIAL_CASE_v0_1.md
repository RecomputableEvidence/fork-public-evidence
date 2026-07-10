# Longitudinal Day-0 Coordinated Re-Seal Adversarial Case v0.1

Status: Adversarial case.
Case ID: `LRT_DAY0_ADV_001_COORDINATED_RESEAL_v0_1`
Source: Public Review Round 005.

## 1. Purpose

This case converts the Round 005 coordinated re-seal finding into a reproducible adversarial check.

The case asks:

Can the Day-0 checker distinguish an originally sealed packet from a scratch-copy packet whose provenance receipt was falsified and then consistently re-sealed by recomputing the receipt hash, packet manifest, manifest sidecar, and outer receipt?

## 2. Expected current observation

Under the current v0.1 Day-0 checker, the coordinated re-sealed scratch packet is expected to pass.

That is not treated as validation.

It is treated as a confirmed root-of-trust limitation:

- the Day-0 checker verifies internal consistency relative to the current manifest and outer receipt;
- it does not verify an external original-sealing anchor;
- therefore, a party able to alter the packet and recompute all internal bindings can produce a self-consistent packet that still passes.

## 3. Mutation performed in disposable scratch copy

The adversarial checker:

1. Copies `docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/` into a temporary repository-shaped directory.
2. Edits `receipts/day0_expected_reconstruction_provenance_receipt.json`.
3. Changes provenance from author-declared baseline to independent external reviewer provenance.
4. Recomputes that receipt's SHA-256.
5. Patches the new receipt hash into `packet_manifest.json`.
6. Recomputes `packet_manifest.json`.
7. Patches the new manifest hash into `packet_manifest.sha256`.
8. Patches the new manifest hash into `packet_manifest_outer_receipt.json`.
9. Runs the unmodified Day-0 checker against the scratch copy.

## 4. Expected outcome codes

- `MANIFEST_INTERNALLY_CONSISTENT_BUT_UNANCHORED`
- `COORDINATED_RESEAL_CONFIRMED`
- `ROOT_OF_TRUST_SCOPE_LIMIT_CONFIRMED`
- `SEMANTIC_CONTENT_CHANGE_UNDETECTED_AFTER_CONSISTENT_RESEAL`

## 5. Non-claim

This adversarial case does not show that the clean Day-0 packet was altered.

It shows that the current v0.1 checker does not distinguish clean original sealing from coordinated re-sealing unless an external root of trust exists.

## 6. Run command

From repository root:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`

## 7. Boundary statement

This case records checker-scope behavior only. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.