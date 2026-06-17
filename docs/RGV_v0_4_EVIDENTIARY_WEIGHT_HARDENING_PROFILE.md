# RGV v0.4 Evidentiary-Weight Hardening Profile

## Status

Candidate non-breaking profile for RGV v0.3.

This profile does not reopen the RGV v0.3 repair path. It defines an optional v0.4 evidentiary-weight hardening layer that can be applied to RGV graph bundles and verifier results.

## Core distinction

The target is evidentiary weight, not legal sufficiency.

RGV v0.4 profile hardening can increase reconstructability, reproducibility, and handoff clarity without asserting legal sufficiency, admissibility, self-authentication, business-records status, compliance, safety, truth, or runtime authority.

## Dependency order

The profile sequence is intentionally ordered.

1. Canonicalization profile

Canonicalization is prerequisite to seals, digests, timestamp anchors, and reproducible cross-party verification.

For v0.4, the profile fixes `canonicalization_profile_id` to `RFC8785_JCS` as a const. Future schemes may be considered in later versions only after independent review. RGV v0.4 constrains the profile to RFC8785_JCS so JSON evidence objects have a declared canonical serialization target before seals, digests, timestamp anchors, or receipt envelopes are layered on top.

2. Seal / integrity binding

Seal binding must specify:

- seal scope;
- seal algorithm;
- declared method;
- sealed inclusion of the verifier version identifier;
- signer identity state;
- non-repudiation state.

For v0.4, `seal_algorithm` is fixed to `SHA256`.

The seal scope must explicitly choose one of:

- bundle only;
- verifier result only;
- bundle and result independently;
- compound bundle/result digest.

If a compound digest is used, the ordering convention must be declared.

3. Timestamp anchor

The timestamp anchor should anchor a sealed digest, not an unstable serialization.

The profile allows timestamp state to remain `NOT_ESTABLISHED` or `NOT_CHECKED`; absence must be recorded honestly rather than implied.

4. Provenance tier

Provenance is declared per CBC node. A graph bundle may contain nodes with different provenance tiers.

The bundle-level `minimum_provenance_tier` must equal the weakest declared CBC provenance tier. This prevents provenance laundering: a weak-provenance node cannot be made stronger merely by being co-located with stronger nodes.

5. Receipt envelope

Receipt envelopes remain separate handoff artifacts.

They are not embedded in the graph bundle because embedding the receipt inside the bundle creates circularity: the receipt seals the bundle, while the bundle would contain the receipt. Keeping the receipt envelope separate avoids fragile exclusion rules.

## Required non-claims

The profile must preserve these non-claims:

- This profile does not assert legal sufficiency, admissibility, self-authentication, or business-records status.
- This profile does not assert satisfaction of FRE 902(13) or FRE 902(14) absent a separate qualified certification.
- This profile does not assert satisfaction of FRE 803(6) business-records requirements.
- Signer identity and non-repudiation remain `NOT_ESTABLISHED` unless separately established.
- Declared canonicalization profile does not by itself prove independent RFC8785/JCS implementation conformance.

## Checker scope

`tools/check_rgv_evidentiary_weight_profile_v0_4.py` validates deterministic profile consistency only.

It does not verify legal sufficiency, admissibility, self-authentication, business-records status, truth, compliance, safety, runtime authority, cryptographic correctness, or independent RFC8785 implementation conformance.

## Build posture

This profile is designed to make future contribution easier, not harder.

It narrows the decision surface by declaring:

- dependency order;
- canonicalization const;
- seal algorithm;
- verifier version binding;
- honest establishment states;
- provenance anti-laundering rule;
- receipt-envelope separation.

Future contributors can harden the implementation against this contract without changing Fork's non-claims.
