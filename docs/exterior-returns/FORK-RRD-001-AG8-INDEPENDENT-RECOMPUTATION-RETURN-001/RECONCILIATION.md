# FORK-RRD-001-AG8-INDEPENDENT-RECOMPUTATION-RETURN-001

Status: `REPOSITORY_ADMITTED_EXTERIOR_RETURN`

This object admits an exterior independent recomputation return for the already closed `FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001` object. It does not append to, reopen, or mutate the closed research object.

## Bound source coordinate

- closure commit: `a560de8e1e34ff8ec10da6c4b6ec1fe3f91e5160`
- closure parent: `27fc31e307307164ec3c8026473ce7ce0d007c17`
- closed-object standing: `CLOSED_HISTORICAL_EVIDENCE`

```text
EXTERIOR_RETURN_ADMISSION
!= CLOSED_OBJECT_REOPENED
```

## Independent recomputation result

The successful return directory is `RETURN-20260925-002411`. The unmodified receipt reports:

```text
Checks: 55/55 PASS
OVERALL MATCH: TRUE
```

The return was produced on Windows 11 with Python 3.14.0 and Git 2.52.0.windows.1. It performed no fresh external observation, artifact reacquisition/rehash, target execution, or runtime control.

## Exact source identities

- `returns.zip`: `645df4be1a4e1d6a4a286fc63085f76adcfd0bf5306cd71e426a4197b9a5ff02` (6038 bytes)
- successful receipt: `470bc0b590ca26cfbd9dd359c188b772d8e5865e06b2ee25cc42ab5ff0ce7476` (22257 bytes)
- successful console: `4a5a963b954ae63af2eed81e9c0bee210a2d55e1e462d6c4aaba821ac05c100e` (730 bytes; UTF-16)
- successful return manifest: `4a191b756ca433e5f2fa8963580e936d30d46e56d37d02a08c486834b7ff84bd` (347 bytes)
- source package recomputation script: `7b9450521e01edcab7b4e192060110e1f39ecb516c072c6769b9398ff5033696` (16341 bytes)

The return manifest's script hash matches the exact script from the issued recomputation package. The script bytes are not embedded inside the returned archive.

```text
RETURN_MANIFEST_SCRIPT_IDENTITY
= SOURCE_PACKAGE_SCRIPT_IDENTITY

SCRIPT_HASH_BOUND
!= SCRIPT_BYTES_EMBEDDED_IN_RETURN
```

## Procedural chronology

The source archive preserves an empty directory named `RETURN-20260925-001906` and the successful `RETURN-20260925-002411` directory. The preceding operator transcript records that an earlier run failed before recomputation because the supplied repository path was not a usable Git repository; the successful run followed creation of a fresh clone. The failed console transcript is not embedded in the returned archive.

The successful receipt internally identifies itself as:

`FORK-RRD-001-AG8-INDEPENDENT-RECOMPUTATION-ATTEMPT-001`

That internal harness identifier is preserved exactly. The exterior admission separately records the actual operator-visible chronology without rewriting the source receipt.

```text
SOURCE_RECEIPT_INTERNAL_ATTEMPT_ID
= ...ATTEMPT-001

ACTUAL_OPERATOR_SEQUENCE
= EARLIER_PROCEDURAL_FAILURE
  THEN SUCCESSFUL_RECOMPUTATION

IDENTIFIER_ORDINAL_MISMATCH
!= RECOMPUTATION_RESULT_MISMATCH
```

## Admission disposition

```text
INDEPENDENT_RECOMPUTATION_MATCH
= REPOSITORY_ADMITTED

CHECKS
= 55/55 PASS

OVERALL_MATCH
= TRUE
```

The following are not admitted by this return:

- fresh external verification;
- general system validation;
- new edge standing;
- authority change;
- action authorization;
- reopening of the closed AG8 object.

```text
RECOMPUTATION_OF_FROZEN_RECORD
!= FRESH_EXTERNAL_VERIFICATION

INDEPENDENT_RECOMPUTATION_MATCH
!= GENERAL_SYSTEM_VALIDATION

EXTERIOR_RETURN_ADMISSION
!= CLOSED_OBJECT_REOPENED
```
