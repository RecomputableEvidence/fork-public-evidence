# Fork Public Disclosure v0.1.2 — Repository Successor

Status: `CANDIDATE_REPOSITORY_SUCCESSOR_NOT_YET_DETACHED_BUNDLE_RELEASE`

## Why v0.1.2 exists

Fork Public Disclosure v0.1.1 is preserved as the historical predecessor. Its Windows verification instructions contain control-character corruption in two path fragments. A later candidate repaired those bytes in place, but because the README is part of the v0.1.1 integrity inventory, that legitimate edit correctly caused the v0.1.1 verifier to fail with a bundle-file digest mismatch.

v0.1.2 therefore does not rewrite or re-seal v0.1.1 in place. It is a versioned successor.

## Successor construction

This repository successor contains the exact v0.1.1 verification payload as an inherited layer plus a v0.1.2 overlay:

- corrected v0.1.2 verification instructions;
- a successor relationship manifest;
- a stdlib-only successor verifier;
- the comments-only requirements file;
- no semantic promotion of the underlying synthetic fixture;
- no reuse of a v0.1.1 detached bundle receipt as a v0.1.2 receipt.

The inherited `verify_public_disclosure.py` remains the v0.1.1 semantic/integrity verifier. The v0.1.2 wrapper runs that verifier first and then checks the successor-specific repair and lineage conditions.

## Repository recomputation

From the repository root:

Linux/macOS:

```bash
cd technical-disclosure/v0.1.2
python3 verify_public_disclosure_v0_1_2.py
```

Windows PowerShell:

```powershell
Set-Location .\technical-disclosure\v0.1.2
python .\verify_public_disclosure_v0_1_2.py
if ($LASTEXITCODE -ne 0) { throw "PUBLIC_DISCLOSURE_V0_1_2_VERIFICATION_FAILURE" }
```

Expected successor conclusion after fresh execution:

```text
FORK_PUBLIC_TECHNICAL_DISCLOSURE_V0_1_2_REPOSITORY_SUCCESSOR_PASS
```

## Detached bundle boundary

No detached v0.1.2 ZIP receipt is claimed by this repository candidate.

A future detached v0.1.2 bundle release must:

1. freeze the complete v0.1.2 bundle bytes;
2. generate a new v0.1.2 outer ZIP digest/receipt;
3. publish that receipt beside the v0.1.2 ZIP;
4. never reuse the v0.1.1 ZIP receipt as v0.1.2 evidence.

Until that separately occurs, this surface is a repository successor candidate only.

## What successful recomputation would establish

Successful execution would establish that:

- the inherited v0.1.1 payload still verifies under its own original verifier;
- the v0.1.2 instructions contain no `0x0b` or `0x0c` control bytes;
- the successor manifest binds the exact preserved predecessor and exact failed repair candidate;
- the requirements file remains comments-only and adds no dependency.

## What it does not establish

It does not establish source truth, workflow completeness, append-only persistence, RFC 3161 validation, independent time of existence, signer identity, non-repudiation, legal admissibility, compliance, third-party independence, live institutional deployment, production readiness, admission, pilot authorization, execution authority, or institutional authority.
