# Fork Reviewer Quick Start v0.1

## Purpose

This file gives a cold external reviewer the shortest reproducible path through Fork's public evidence surface.

It is a convenience entry point. The authoritative reviewer guide remains:

```text
docs/REVIEWER_START_HERE_v0_1.md
```

## Boundary note

This repository provides a bounded, read-only evidence disclosure and verification surface.
It does not certify:

- legal admissibility
- production readiness
- security posture
- SOC 2, ISO, HIPAA, or regulatory compliance
- customer deployment
- commercial pilot approval
- AI-output correctness
- source completeness
- audit sufficiency
- risk acceptance
- institutional authority

A passing local verification result establishes only the bounded structural or integrity condition declared by the verifier.

## Minimal environment

Tested reviewer path:

- Git
- Python 3.11+
- No third-party Python packages required for `technical-disclosure/verify_public_disclosure.py`

The verifier dependency statement is kept in:

```text
technical-disclosure/requirements.txt
```

## Clone

From a shell:

```bash
git clone https://github.com/RecomputableEvidence/fork-public-evidence.git
cd fork-public-evidence
```

## Optional isolated Python environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r .\technical-disclosure\requirements.txt
```

Linux/macOS shell:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r ./technical-disclosure/requirements.txt
```

The requirements file is intentionally empty except for comments because the public disclosure verifier uses the Python standard library.

## Minimal package checks

From the repository root:

```bash
python ./tools/check_release_package.py ./release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1
python ./tools/check_release_package.py ./release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1

# Before checking the pilot discovery package, note:
# this verifies package structure and checksums only;
# it does not validate commercial pilot readiness.
python ./tools/check_release_package.py ./release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1
```

Expected result for each package check:

```text
RELEASE_PACKAGE_CHECK: PASS
```

## Public technical disclosure verification

From the repository root:

```bash
cd ./technical-disclosure
python ./verify_public_disclosure.py
cd ..
```

Expected bounded result:

```text
FORK_PUBLIC_TECHNICAL_DISCLOSURE_V0_1_1_PASS
GATES_FAIL: 0
```

`GATES_NOT_CHECKED` entries are preserved boundary outputs, not failures, unless a specific verifier document states otherwise.

## What to read next

After running the quick start, read:

- `docs/REVIEWER_START_HERE_v0_1.md`
- `docs/FORK_OPERATIONAL_BOUNDARY_MAP_v0_1.md`
- `docs/VERIFICATION_COMMANDS_v0_1.md`
- `docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md`
- `docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md`

## Interpretation rule

Do not treat this quick start as a product-readiness, compliance-readiness, security-readiness, customer-readiness, or deployment-readiness path.

It is only a bounded public-review path for recomputing and inspecting declared evidence-surface materials.
