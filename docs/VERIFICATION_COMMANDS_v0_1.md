# Fork Verification Commands v0.1

## Purpose

This document gives reviewers one command path for the public/reviewer package surface. It does not replace package-specific verification instructions. It consolidates them so external reviewers can reproduce the basic checks without searching the repository.

## Prerequisites

- Git.
- Python 3.
- Local clone of the repository.
- Optional: test dependencies required by the full repository test suite.

## Command syntax note

Commands below use PowerShell-compatible syntax and forward-slash paths where possible. Forward slashes work with Python on Windows and are also compatible with Linux/macOS shells.

If adapting older Windows examples, replace `.\` with `./` on Linux or macOS.

## Minimal package checks

From the repository root:

```powershell
python ./tools/check_release_package.py ./release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1
python ./tools/check_release_package.py ./release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1
```

Before checking the pilot discovery package, note: This verifies package structure and checksums only; it does not validate commercial pilot readiness.

```powershell
python ./tools/check_release_package.py ./release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1
```

Expected package-check outcome for each checked package:

```text
RELEASE_PACKAGE_CHECK: PASS
```

A package-check pass means required package control files are present and the package checksum file matches the package file bytes under the checker contract.

It does not mean the package proves legal admissibility, compliance satisfaction, production readiness, decision correctness, source completeness, runtime authority, or commercial pilot readiness.

## Public technical disclosure verifier

From the repository root:

```powershell
cd ./technical-disclosure
python ./verify_public_disclosure.py
cd ..
```

The public technical disclosure verifier checks the bounded synthetic disclosure surface described in:

- `technical-disclosure/README_VERIFY_PUBLIC_DISCLOSURE_v0_1_1.md`

## Full repository tests

When local dependencies are installed:

```powershell
python -m pytest
```

This command is broader than public package verification. Its result should be interpreted test-by-test according to the relevant checker and doctrine files.

A full test pass is not a production-readiness, compliance, legal, audit, model-safety, or decision-correctness claim.

## Optional checksum regeneration for package maintainers only

Do not use `--write` during external review unless intentionally updating package checksum files as a maintainer.

Maintainer regeneration pattern:

```powershell
python ./tools/check_release_package.py ./release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1 --write
python ./tools/check_release_package.py ./release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1

python ./tools/check_release_package.py ./release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1 --write
python ./tools/check_release_package.py ./release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1

python ./tools/check_release_package.py ./release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1 --write
python ./tools/check_release_package.py ./release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1
```

## Interpretation boundary

Verification commands establish only their declared structural or integrity condition.

They do not establish:

- source truth;
- source completeness;
- AI-output correctness;
- decision correctness;
- legal admissibility;
- compliance satisfaction;
- audit sufficiency;
- production deployment;
- client-specific suitability;
- runtime control;
- institutional authority;
- independent third-party verification;
- commercial pilot readiness.
