# FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001

## AG1 — DISPOSITION AFTER ATTEMPT 002

Status: `AG1_PASSED`

Capture: `CAPTURE_001_IDENTITY_BOUND`

This disposition is additive. It does not rewrite or erase `CAPTURE_001_AG1_ARTIFACT_IDENTITY_ATTEMPT_001` or the earlier `AG1_ARTIFACT_IDENTITY_ADMISSION.md` record, which correctly preserve the first acquisition-path failure.

---

## 1. Exact-byte acquisition

The selected artifact bytes were supplied through the conversation as:

`google-workspace-cli-x86_64-pc-windows-msvc.zip`

At `2026-09-25T04:49:30.302837Z`, the exact uploaded bytes were read only to compute byte length and SHA-256.

Locally observed identity:

- byte length: `6275652`
- SHA-256: `5e33f26556df86411959e0f07cd51caa87b4eaa413b14a385c9efd828b5b1739`

The archive was not extracted and no contained executable was run.

---

## 2. Identity comparison

Attempt 001 had preserved locator metadata from the selected release surface for asset id `381438738`:

- reported filename: `google-workspace-cli-x86_64-pc-windows-msvc.zip`
- reported byte length: `6275652`
- reported SHA-256: `5e33f26556df86411959e0f07cd51caa87b4eaa413b14a385c9efd828b5b1739`

Attempt 002 independently observed the uploaded byte length and computed SHA-256 from the acquired bytes.

Comparison:

- filename: `MATCH`
- byte length: `MATCH`
- SHA-256: `MATCH`

Disposition:

`ARTIFACT_IDENTITY_ADMITTED_FOR_CAPTURE_001`

This disposition binds the captured byte object by exact size and SHA-256 and records that those identity properties match the prior locator metadata associated with the frozen target name.

It does not yet evaluate the separately predeclared `ARTIFACT_TO_RELEASE_OBJECT` relation edge.

```text
BYTE_IDENTITY_BOUND
!= RELEASE_RELATION_EVALUATED

DIGEST_MATCH
!= CHECKSUM_ASSERTION_EVALUATED

DIGEST_MATCH
!= ATTESTATION_VERIFIED
```

---

## 3. Preservation boundary

The exact binary bytes are present in the source conversation attachment used for this capture but are not embedded into this Git repository by this disposition.

Therefore:

```text
ARTIFACT_IDENTITY_ADMITTED
!= REPOSITORY_CONTAINS_BINARY_COPY
```

The repository receipt preserves deterministic identity sufficient to recognize the captured byte object if the exact bytes are presented again.

---

## 4. AG1 standing

Admitted:

- exact captured artifact filename;
- exact captured byte length;
- locally computed SHA-256;
- identity match to the source-reported locator metadata preserved in Attempt 001; and
- `CAPTURE_001` artifact identity.

Not admitted:

- release-to-artifact relation standing;
- published checksum assertion standing;
- attestation standing;
- source repository, commit, or workflow relation standing;
- issuer authority;
- temporal applicability or supersession standing;
- any dimensional evaluation result beyond artifact identity;
- any derived view;
- any view selection; or
- any external action.

AG2 remains:

`UNOPENED`

```text
ATTEMPT_001_ACQUISITION_FAILURE
REMAINS_HISTORICAL_EVIDENCE

ATTEMPT_002_IDENTITY_SUCCESS
DOES_NOT_ERASE_ATTEMPT_001

AG1_PASSED
!= AG2_AUTHORIZED
```
