# Proof Path Selection v0.1

Status: `DRAFT_COHERENCE_SELECTION`

Change effect: routing selection only. This document does not change what any checker establishes, does not admit an artifact, and does not promote experimental or execution standing.

## Exact source basis

- Repository base: `1241c0084900f2c60f362205525464582e57b4a7`
- Current proof-surface index: `docs/CURRENT_PROOF_SURFACE_v0_1.md`
- Reviewer quickstart: `docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md`

## Selected canonical verifier

Primary public verifier:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
```

Structured output:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1 -Json
```

Expected high-level signal at a conforming exact head:

```text
PUBLIC_REVIEW_PACKAGE_VERIFY_PASS
```

### Selection rationale

This verifier is selected for the front door because it is already identified as the primary public verifier by:

- the root README;
- `docs/CURRENT_PROOF_SURFACE_v0_1.md`;
- `docs/REVIEWER_START_HERE_v0_1.md`;
- `docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md`.

It is PowerShell 5.1 compatible, supports JSON output, checks the declared public-review package, and invokes multiple bounded structural checkers. It is therefore a better newcomer entry than selecting an isolated specialist checker without context.

### Verifier boundary

A passing result means only that the verifier's declared required paths and bounded checks succeeded at the tested checkout. It does not establish:

- truth or correctness of an underlying AI-assisted workflow;
- legal or compliance sufficiency;
- safety or security certification;
- authorization or approval;
- production or procurement readiness;
- institutional authority;
- admission of a draft or candidate artifact.

For Linux or macOS environments without PowerShell, use:

- `docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md`

Manual reconstruction is useful review evidence, but it is not identical to executing the named verifier artifact.

## Selected example artifact

Primary example:

- `docs/review/boundary-pressure/fixtures/valid/BPR_RR_VALID_001_receipt_preserved_as_structural_v0_1.json`

Associated case explanation:

- `docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md`

Direct checker:

```powershell
python tools/check_boundary_pressure_review_cases_v0_1.py --json
```

### Selection rationale

The selected fixture is compact enough to inspect without prior architectural knowledge and demonstrates a central Fork distinction:

> A recomputation receipt may show that a bounded structural replay occurred without replacing the underlying artifact or becoming truth, approval, compliance, legal sufficiency, authorization, or production readiness.

The fixture makes the distinction explicit through:

- a declared receipt role;
- an underlying-artifact reference;
- affirmative preservation controls;
- prohibited inheritance controls;
- expected outcome codes;
- a non-authority statement.

It is already inside a machine-checked fixture family invoked by the selected public verifier.

## Optional contrast artifact

After reading the valid example, a reviewer may inspect:

- `docs/review/boundary-pressure/fixtures/invalid/BPR_RR_INVALID_001_receipt_upgraded_to_validation_v0_1.json`

The contrast should be used to understand a rejected overread, not to imply that rejection validates every property of the valid fixture.

## Artifacts not selected as the first example

### Longitudinal Day-0 packet

The packet is materially important but too large for a sixty-second first inspection. It remains a later proof route.

### Sequence Surface and Pair-001 state

These surfaces are current and important, but their authority, retry, and execution distinctions require more context than a newcomer example should assume.

### PR #84 conversational-authority-drift candidate

PR #84 is excluded from the front-door example because it is frozen for exact-head exterior review and remains a draft candidate without admission or publication effect.

## Front-door placement

The README should present the selected verifier first, followed immediately by the compact example artifact and a bounded interpretation statement. Deeper proof, experiment, and architecture routes should follow after the visitor has seen one executable path and one inspectable record.