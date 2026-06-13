# Fork Public Evidence

## Suggested Reading Path

For a first review, read the artifacts in this order:

1. **README** — what Fork establishes and does not establish.
2. **[Reading Guide: From Reconstructive Fidelity to Recomputable Evidence](docs/READING_GUIDE_RECONSTRUCTIVE_FIDELITY_TO_RECOMPUTABLE_EVIDENCE.md)** — how the reconstructive-fidelity doctrine maps to Fork's executable evidence posture.
3. **White Paper: _Reconstructive Fidelity in the Age of AI_** — the broader governance and evidentiary doctrine.
4. **v0.7 Release Notes** — the narrow recomputability receipt-binding milestone.
5. **Local Verification Script** — run `technical-disclosure/verify_public_disclosure.py` to inspect the public disclosure verification surface.
6. **Schemas, examples, tests, and tools** — review the executable evidence constraints in `schemas/`, `examples/`, `tests/`, and `tools/`.

This reading path is intended to prevent two common misreadings: treating Fork as only a theoretical governance paper, or treating the repository as a broad product-readiness claim. Fork's current public posture is narrower: bounded evidence preservation, explicit non-claims, and test-backed controls against specific forms of evidentiary overclaim.
Fork restricts what any artifact in the evidentiary chain may be treated as proving, for the purpose of authorized action.


Public evidence, technical disclosure, and canonical publication materials for Forkâ€™s work on reconstructive fidelity in AI-assisted workflows.

## Canonical white paper

**Reconstructive Fidelity in the Age of AI**  
*The Invariant Distance Principle and Why Governance Requires Evidence That Survives Institutional Change*

- Canonical article: https://SentinelQuantumAegis.github.io/fork-public-evidence/
- Repository copy: https://github.com/SentinelQuantumAegis/fork-public-evidence/blob/main/white-paper/Reconstructive_Fidelity_in_the_Age_of_AI_v1_0.md
- Technical disclosure release: https://github.com/SentinelQuantumAegis/fork-public-evidence/releases/tag/fork-public-disclosure-v0.1.1

## Public technical disclosure

Release: **Fork Public Technical Disclosure v0.1.1**

Outer ZIP SHA-256:

```text
1361dd12b1f249372f240cb5226cac289319bc6da4ce219ea47538a0716c1410
```

The disclosure contains a deterministic synthetic workflow fixture, selected schemas, an included verifier, granular gate results, explicit non-claims, and a detached outer-ZIP receipt.

## Established by the public disclosure

- Declared workflow-member eligibility and packet membership
- SHA-256 member-digest recomputation
- Canonical manifest-digest recomputation
- Public test-key HMAC binding recomputation
- Persisted-artifact verification
- Granular `PASS / FAIL / NOT_CHECKED` preservation
- No aggregate trust, validity, compliance, or admissibility verdict
- Mechanical semantic-authority non-promotion checks
- Explicit timestamp disclosure boundaries

## Not established

- Source truth or completeness
- Public signer identity or non-repudiation
- Legal admissibility
- Compliance or ethical correctness
- Third-party verifier independence
- Live institutional deployment
- Production readiness

## Local verification

See:

```text
technical-disclosure/README_VERIFY_PUBLIC_DISCLOSURE_v0_1_1.md
```

Then run:

```powershell
cd technical-disclosure
python .\verify_public_disclosure.py
```

## Release assets

The exact frozen ZIP and detached SHA-256 receipt are available in:

```text
receipts/
```

and through the tagged GitHub Release.

## Copyright

Copyright © 2026 Ryan Feller. All rights reserved.

Public availability permits inspection and verification of the disclosed artifacts. It does not grant a license to Forkâ€™s undisclosed implementation, trademarks, proprietary architecture, or controlled operating materials.
