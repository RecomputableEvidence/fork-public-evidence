# Verification Instructions

## Prerequisites

- Git
- Python 3
- Local clone of the repository

## Check this package

From the repository root:

```powershell
python .\tools\check_release_package.py .\release_packages\FORK_TECHNICAL_VALIDATION_PACKET_v0_1
```

Expected result:

```text
RELEASE_PACKAGE_CHECK: PASS
```

## Regenerate this package checksum file

From the repository root:

```powershell
python .\tools\check_release_package.py .\release_packages\FORK_TECHNICAL_VALIDATION_PACKET_v0_1 --write
python .\tools\check_release_package.py .\release_packages\FORK_TECHNICAL_VALIDATION_PACKET_v0_1
```

## Interpretation

A PASS result means the package checksum file matches the current package file bytes and required package control files are present.

A PASS result does not mean:

- the AI output was correct
- a workflow was legally valid
- a compliance obligation was satisfied
- a source system was complete
- a client deployment is production-ready
- hidden vendor behavior can be replayed

## Reviewer note

Technical reviewers should distinguish:

- package integrity
- schema validity
- example validity
- verifier behavior
- evidence-state semantics
- declared non-claims

These are related but not interchangeable.