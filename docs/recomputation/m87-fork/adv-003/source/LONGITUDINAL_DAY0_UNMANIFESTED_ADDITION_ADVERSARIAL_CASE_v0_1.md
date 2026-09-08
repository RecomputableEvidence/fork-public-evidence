# Longitudinal Day-0 Unmanifested-Artifact-Addition Adversarial Case v0.1

Status: Adversarial case (exterior observation).
Case ID: `LRT_DAY0_ADV_003_UNMANIFESTED_ADDITION_v0_1`
Filed by: Mac McFall / M87, exterior observer, 17 July 2026.
Source: M87-side exocortex repo audit of `fork-public-evidence` during bilateral architecture review.
Relation to prior cases: sibling to `LRT_DAY0_ADV_001_COORDINATED_RESEAL_v0_1` and `LRT_DAY0_ADV_002_LEXICAL_NON_AUTHORITY_LIMIT_v0_1`; records a distinct and simpler checker-coverage limit.

## 1. Purpose

This case converts an exterior-audit finding into a reproducible adversarial check.

The case asks:

Does the current v0.1 Day-0 packet checker detect an UNMANIFESTED file added to a packet
evidence directory, or does it verify only the artifacts the manifest already lists?

## 2. Expected current observation

Under the current v0.1 Day-0 checker (`tools/check_longitudinal_reconstruction_day0_packet_v0_1.py`),
a packet with one extra, unmanifested evidence file is expected to pass unchanged (`failed == 0`).

That is not treated as validation. It is treated as a confirmed coverage limitation:

- the Day-0 checker verifies presence, hash continuity, manifest binding, and boundary-statement
  presence for the artifacts the manifest enumerates;
- it does not perform a directory-inventory completeness sweep of the packet;
- therefore, a party able to write a file into the packet can add unmanifested content that a
  reviewer may mistake for packaged evidence, while the packet still verifies.

## 3. Distinction from ADV_001 (coordinated re-seal)

- `ADV_001` mutates a **manifested** file and re-seals every internal binding (receipt hash,
  manifest, sidecar, outer receipt). It requires full re-sealing capability.
- This case (`ADV_003`) **adds an unmanifested file** and changes no bindings at all. It requires
  no re-sealing. The two limits are independent: closing the root-of-trust gap in ADV_001 does not
  close this one, because this content is never referenced by any binding the checker consults.

## 4. Mutation performed in disposable scratch copy

The adversarial checker:

1. Copies `docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/` into a temporary
   repository-shaped directory. The source packet is never mutated.
2. CONTROL: runs the unmodified Day-0 checker on the clean scratch copy.
3. MUTATION: writes one new file, `evidence/day0_injected_extra_v0_1.json`, into the packet.
   The manifest, sidecar (`packet_manifest.sha256`), and outer receipt are NOT touched.
4. Runs the unmodified Day-0 checker on the mutated scratch copy.

## 5. Observed outcome (recorded 17 July 2026, subject commit adjacent to `fd93d05`)

- CONTROL: `passed = 27, failed = 0`.
- MUTATION: `passed = 27, failed = 0` — the injected file is not detected.
- `limitation_reproduced: true`.

Outcome codes:

- `MANIFEST_LISTED_ARTIFACTS_ONLY_CONFIRMED`
- `UNMANIFESTED_ADDITION_UNDETECTED`
- `NO_DIRECTORY_INVENTORY_COMPLETENESS_SWEEP`
- `PACKET_STILL_VERIFIES_WITH_INJECTED_EVIDENCE`

## 6. Relevance to a stated Fork property

The bilateral comparison record (M87 source "M87 Runtime Systems vs Fork Evidence Surface")
attributes to Fork the property that a "manifest inventory verifies completeness." This case
shows that, for the Day-0 checker at v0.1, manifest inventory verifies the completeness of
*listed* artifacts but does not verify that the packet contains *only* listed artifacts.
Recommend narrowing that language to "manifest inventory verifies listed-artifact integrity;
directory-completeness sweep not implemented in v0.1" until a checker upgrade lands.

## 7. Non-claim

This case does not show the clean Day-0 packet was altered. It records checker coverage scope
only. It does not establish truth, compliance, legal sufficiency, safety, authorization,
approval, certification, endorsement, validation, production readiness, procurement approval,
or institutional authority. Being filed by an exterior observer, it carries no authority over
Fork's claims and is offered for Fork's own Round process to accept, refine, reject, or preserve.

## 8. Run command

From repository root:

- `python check_day0_unmanifested_addition_adversarial_case_v0_1.py --json`

Exit `0` = limitation reproduced (control passes and injection undetected);
exit `1` = injection detected or control failed (gap may already be closed — re-inspect);
exit `3` = tool error.

## 9. Candidate remediation (non-binding)

Add a directory-inventory check to the Day-0 checker: enumerate files under the packet root,
compare against the manifest's declared file set, and emit a failing result for any packet file
not present in the manifest (allowing an explicit ignore list for the manifest/sidecar/outer
receipt themselves). This converts "listed-artifact integrity" into "packet-inventory
completeness" and closes the gap without affecting the root-of-trust work tracked by ADV_001.

## 10. Boundary statement

This case records checker-scope behavior only, as observed on the date and subject commit noted
in Section 5. It is bounded evidence, not certification, and confers no authority.
