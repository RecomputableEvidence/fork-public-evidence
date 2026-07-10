# Public Review Round 005 Synthesis v0.1

Status: Initial synthesis.
Round: Longitudinal Day-0 Packet Accessibility, Reconstruction Boundary, and Replay Readiness Review.

## 1. Review received

One exterior review has been filed:

- Claude exterior access-path review, execution receipt, manual verifier reconstruction receipt, Day-0 packet inspection, and adversarial reconstruction observation.

Reviewed commit:

- 03f25f0e52109e8545c188c2bcc329fac4f701f7

Reviewed object:

- docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/

## 2. Positive confirmations

The review confirmed:

- Day-0 checker executed and passed 27/27.
- Boundary-pressure checker passed 4/4 default and 4/4 adversarial.
- Round 004 checker passed 4/4.
- Manifest, sidecar, and outer receipt binding chain was understandable.
- Expected reconstruction is visibly author-declared, not independent.
- Direct overclaim in the Day-0 packet artifacts was low.

## 3. Findings

The review surfaced several concrete boundary and accessibility findings:

1. The primary public verifier path is PowerShell-only.
2. The reviewer manually reconstructed the verifier behavior because pwsh was unavailable.
3. Read-first documentation contains stale Day-0 status contradictions.
4. The Day-0 checker performs real byte and hash checks, but several assertions are lexical or field-presence only.
5. The manifest schema is declared and required-present, but not mechanically enforced by the Day-0 checker.
6. Expected reconstruction provenance is honestly disclosed as author-declared, but narrower than protocol section 8.
7. Coordinated re-seal with falsified provenance passed the unmodified Day-0 checker 27/27.
8. Non-authority checking can be gamed with keyword-present authority-asserting language.
9. Evidence-file hash verification can be overread as semantic content verification.

## 4. Engineering implications

The next work should not proceed directly to Day-0 replay.

First-order response sequence:

1. Fix stale Day-0 status contradictions.
2. Add or document cross-platform verifier parity.
3. File coordinated re-seal as an adverse longitudinal case.
4. File lexical non-authority checker limitation as a boundary-pressure case.
5. Clarify schema-present versus schema-enforced.
6. Then build Day-0 replay checker and replay receipt.

## 5. Non-authority statement

This synthesis records exterior review findings. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, or institutional authority.
<!-- FORK_ROUND005_STATUS_AND_VERIFIER_FALLBACK_RESPONSE:START -->

Round 005 response: status repair and verifier fallback
Response receipt:
docs/review/public-rounds/round-005/ROUND005_RESPONSE_STATUS_AND_VERIFIER_FALLBACK_v0_1.md
Public verifier fallback:
docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md
This response fixes stale Day-0 status language and documents manual public-verifier reconstruction for reviewers who cannot execute the PowerShell verifier.

<!-- FORK_ROUND005_STATUS_AND_VERIFIER_FALLBACK_RESPONSE:END -->
