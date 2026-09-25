# FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001

## AG1 — ARTIFACT IDENTITY ADMISSION

Status: `AG1_ATTEMPTED_NOT_PASSED`

Capture: `CAPTURE_001_OPENED_INCOMPLETE`

Parent AG0 commit: `883e4aad6667b06a9e4d2eb6a5d23f435afcfe68`

AG1 was explicitly authorized after AG0. This record performs only the bounded acquisition / exact-byte identity step.

No AG2 source-observation admission, relation-edge evaluation, attestation verification, derivation, view selection, installation, execution, policy decision, consequence selection, or runtime intervention is opened by this record.

---

## 1. Locator observation

A fresh locator observation of the selected release surface was bounded inside the following UTC interval:

- start: `2026-09-25T04:40:52.181313969Z`
- end: `2026-09-25T04:40:57.825558504Z`

Locator source:

`https://api.github.com/repos/googleworkspace/cli/releases/tags/v0.22.1`

The source reported a release object for `v0.22.1` and an asset with the frozen target name:

`google-workspace-cli-x86_64-pc-windows-msvc.zip`

Locator-only metadata observed for that asset:

- asset id: `381438738`
- reported content type: `application/zip`
- reported asset state: `uploaded`
- reported size: `6275652` bytes
- reported digest: `sha256:5e33f26556df86411959e0f07cd51caa87b4eaa413b14a385c9efd828b5b1739`
- browser download URL: `https://github.com/googleworkspace/cli/releases/download/v0.22.1/google-workspace-cli-x86_64-pc-windows-msvc.zip`

These are source-reported locator properties only. They are not promoted to locally recomputed artifact identity.

```text
REPORTED_ASSET_DIGEST
!= LOCALLY_COMPUTED_ARTIFACT_DIGEST

ASSET_METADATA_OBSERVED
!= ARTIFACT_BYTES_ACQUIRED
```

---

## 2. Exact-byte acquisition attempt

The exact artifact bytes were not acquired by the available execution environment.

Observed acquisition-path limitations:

1. direct binary retrieval through the available download path did not produce the artifact bytes;
2. direct container `curl` could not resolve the external GitHub host because the execution container has no outbound DNS/network access; and
3. the available GitHub connector explicitly supports UTF-8/JSON repository-resource responses and does not expose arbitrary release-asset binary bytes through its generic fetch action.

This is an acquisition-path limitation, not a finding about the target artifact.

```text
ACQUISITION_FAILURE
!= TARGET_ARTIFACT_FAILURE

PUBLIC_DOWNLOAD_URL_PRESENT
!= DOWNLOAD_SUCCEEDED
```

---

## 3. AG1 identity disposition

Required AG1 identity properties remain unavailable:

- acquired exact artifact bytes: `NO`
- frozen byte copy: `NO`
- locally observed byte length: `UNAVAILABLE`
- locally computed SHA-256: `UNAVAILABLE`

Therefore:

`ARTIFACT_IDENTITY_NOT_ADMITTED`

Reason:

`EXACT_ARTIFACT_BYTES_NOT_ACQUIRED`

The source-reported byte length and source-reported digest are preserved as locator metadata but do not satisfy AG1's requirement for exact-byte acquisition and independent local identity computation.

```text
AG1_ATTEMPTED
!= AG1_PASSED

CAPTURE_001_OPENED
!= CAPTURE_001_COMPLETE
```

---

## 4. Standing after this attempt

Admitted by this AG1 attempt:

- `CAPTURE_001` is opened;
- the selected target release surface was observed sufficiently to locate the frozen target name;
- the bounded locator observation interval and retrieval path are preserved; and
- the failed artifact-acquisition attempt is preserved as procedural evidence.

Not admitted:

- target artifact byte identity;
- a locally computed artifact digest;
- release-to-artifact relation standing;
- checksum/digest relation standing;
- attestation standing;
- source repository / source commit / workflow relation standing;
- issuer authority;
- temporal applicability or supersession standing;
- any derived view; or
- any external action.

AG2 remains:

`UNOPENED`

```text
ARTIFACT_IDENTITY_NOT_ADMITTED
!= ARTIFACT_IDENTITY_CONTRADICTED

AG1_RESULT
!= AG2_AUTHORIZATION
```

---

## 5. Continuation requirement

AG1 can proceed only if the exact selected artifact bytes are acquired and frozen under this capture, after which the observed byte length and locally computed SHA-256 can be recorded and compared only as an identity operation.

No checksum assertion, attestation assertion, provenance claim, authority claim, or other relation edge should be evaluated while completing that byte-acquisition step.
