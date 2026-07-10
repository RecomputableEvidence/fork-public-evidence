# Round 005 Response: Coordinated Re-Seal Adversarial Case v0.1

Status: Engineering response receipt.
Round: Public Review Round 005.
Response class: Adversarial case filing.

## 1. Finding addressed

Round 005 demonstrated that a coordinated re-seal could falsify expected reconstruction provenance, recompute the mutated receipt hash into the manifest, recompute the manifest sidecar and outer receipt, and still pass the current Day-0 checker.

This response preserves that finding as a reproducible adversarial case.

## 2. Added artifacts

- `docs/reconstruction/adversarial/README.md`
- `docs/reconstruction/adversarial/LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL_CASE_v0_1.md`
- `docs/reconstruction/adversarial/fixtures/LRT_DAY0_ADV_001_coordinated_reseal_v0_1.json`
- `schemas/longitudinal_day0_adversarial_case_v0_1.schema.json`
- `tools/check_longitudinal_day0_adversarial_cases_v0_1.py`

## 3. Interpretation

A pass in this adversarial checker means:

- the clean Day-0 packet still passes;
- the checker successfully created a scratch-copy coordinated re-seal;
- the unmodified Day-0 checker still accepted the re-sealed scratch copy;
- the root-of-trust limitation is therefore reproduced.

It does not mean the adversarially mutated packet is valid, truthful, compliant, authorized, approved, certified, endorsed, safe, production-ready, or institutionally authoritative.

## 4. Current limitation preserved

The Day-0 checker verifies internal consistency and byte continuity relative to the current manifest and outer receipt.

It does not verify an external original-sealing anchor.

## 5. Future response options

Future work may add:

- external anchoring;
- signed release evidence;
- transparency-log anchoring;
- pinned manifest hash outside the packet;
- checker behavior that classifies coordinated re-seal as a separate condition.

## 6. Non-authority statement

This response records an adversarial checker-scope limitation. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.