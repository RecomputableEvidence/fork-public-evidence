# Third-Party Remote Mapping Verification v0.1

Status: Verification Procedure  
Version: v0.1  
Verifier: `tools/verify_remote_mapping_system_v0_1.py`

## Purpose

This procedure verifies the public remote GitHub snapshot for AI Governance Mapping System v0.1 without trusting the caller's local working tree.

It exists to upgrade evidence from:

```text
local terminal output
```

to:

```text
fresh remote clone + commit checkout + expected file verification + content sentinel checks + SHA-256 manifest output
```

## Default target

Repository:

```text
https://github.com/RecomputableEvidence/fork-public-evidence.git
```

Commit:

```text
9d96961
```

Expected commit message:

```text
Add AI governance mapping system v0.1
```

## What the verifier checks

The verifier checks:

* Git is available.
* The public repository can be cloned.
* Commit `9d96961` can be checked out.
* The commit subject matches the expected message.
* The changed-file set matches the expected AI Governance Mapping System v0.1 file set.
* Required dependency documents exist.
* Core doctrine phrases are present.
* Generic lane examples are explicitly marked as not named third-party mappings.
* SHA-256 hashes are computed for the checked files.
* A JSON verification result is emitted.

## What the verifier does not prove

This verifier does not prove:

* legal sufficiency,
* compliance sufficiency,
* market adoption,
* third-party endorsement,
* standard status,
* production interoperability,
* runtime enforcement,
* or the correctness of Fork as a commercial product.

It verifies only the remote repository snapshot and the declared v0.1 mapping-system artifact surface.

## Run

From the repository root:

```powershell
python .\tools\verify_remote_mapping_system_v0_1.py
```

Optional explicit form:

```powershell
python .\tools\verify_remote_mapping_system_v0_1.py `
  --repo-url "https://github.com/RecomputableEvidence/fork-public-evidence.git" `
  --commit "9d96961" `
  --output ".\remote_mapping_system_v0_1_verification_result.json"
```

## Expected pass output

```text
REMOTE_MAPPING_SYSTEM_V0_1_VERIFICATION_PASS
```

## Result artifact

The verifier writes:

```text
remote_mapping_system_v0_1_verification_result.json
```

The JSON result includes:

* verifier name,
* verifier version,
* timestamp,
* repository URL,
* requested commit,
* resolved commit,
* commit subject,
* check results,
* file list,
* file sizes,
* SHA-256 hashes,
* overall PASS / FAIL state.

## Boundary

This is a remote snapshot verifier.

It is stronger than pasted terminal output.

It is weaker than an independently signed third-party attestation.

It is appropriate for verifying that the public GitHub repository contains the expected AI Governance Mapping System v0.1 commit and files.