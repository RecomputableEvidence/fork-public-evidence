# LS-MDRC-002 freeze 001: source search and representation reconciliation 002

Recorded 2026-09-23. This is an additive follow-up to PR #167, merged at
`3b45ac293efaa0d1765c653dc934b10fe657759b`. It preserves reconciliation 001 and
the original PR #162 package at `ca28599b7ca411060e1fc3667ef97596244ed9bb` unchanged.

**Disposition: PARTIAL_EXPLANATION_WITH_UNRESOLVED_FREEZE_ACCOUNTING.**

## What the additional evidence establishes

The user supplied the Bob playground repository archive and subsequently the CSH
workspace archive and other candidate source records. Their exact archive/file
identities are recorded in FINDINGS.json. The full workspace archives are not
published by this observation; public readers can independently reproduce the
receipt transformation below from the pinned public Git blob. Archive search
findings remain bounded observations requiring the identified archives to repeat.

The test-receipt discrepancy now has an exact byte-representation explanation:
the committed receipt has LF line endings; replacing each LF with CRLF produces
SHA-256 `c246327a96573c2c702293cb5b2efc56db8efd734077a5f13cf8f7edb76f9077`, exactly
the value declared in the original manifest and freeze receipt. This is a derived
representation, not recovery of an original filesystem instance. It establishes
the digest relationship, not the historical conversion event or freeze chronology.
The committed LF receipt still does not match the original manifest literally.

The uploaded workspace receipt records a later timestamp than the committed
receipt. Its 222 result records match by unique test ID; timestamps and result
ordering differ. This comparison used existing bytes and did not execute tests.

The uploaded workspace manifest differs from the committed manifest only by CRLF
line endings. Neither representation matches the manifest hash declared by the
freeze receipt. That remaining mismatch may be stale accounting or an earlier
manifest version; its cause is not established.

## Bounded source search outcome

- The playground ZIP contains the construction package. Its Git object database
  search covered 9,458 objects, including 3,777 blobs; neither expected historical
  digest was found as an existing blob. No exact match was found among ZIP members.
- The CSH workspace ZIP contains the separate work leading to PR #161. Its object
  search covered 9,424 objects, including 3,749 blobs; neither expected digest was
  found. No LS-MDRC/LS-MDRM references were found in the examined blobs or searched
  working files.
- The public technical disclosure bundle, semantic-standing checker pressure
  receipt, SE-003 freeze, and supplied CSH transcript identify other work. They did
  not supply the LS-MDRC-002 normative instruction §§1–24.
- The named HO-001, HO-002, and HO-003 content filenames were not found in the two
  repository archives. No sealed holdout content was opened or instantiated.
- The user reported searching and accepted reconciliation as warranted. This is
  not an assertion that every filesystem, conversation, or backup was searched.

The original package is available. The unresolved issue is agreement between
its contents, declared bindings, population accounting, and source requirements.
Failure to locate the specification here does not prove that it never existed.
Likewise, absence of named holdout content does not, without the specification,
establish that those files were required at this construction stage.

## Disposition

Retain the original package, preservation branch, and reconciliation 001. Keep
PR #162 unmerged under its current unqualified construction-closure description.
Preserve the line-ending explanation as a narrowing of the earlier receipt
identity uncertainty, while retaining the unresolved manifest binding and count
discrepancies. Pause further source hunting unless a specific new source becomes
available. Any later evidence can be recorded additively.

This record neither declares the research invalid nor authorizes MEASURE,
holdout opening, resealing, or a new successor. A successor is not automatically
required. A later admission decision must state explicitly whether it admits
historical evidence with limitations or qualifies a construction package; those
are different claims.

## Reproduce the receipt digest relationship

Run from a repository clone containing the original commit. The command reads
Git bytes and performs a transformation in memory; it writes no package files.

```python
import hashlib
import subprocess

blob = "bdaedbd7b37703d164915308555ab8cca95abc5e"
original = subprocess.check_output(["git", "cat-file", "blob", blob])
assert b"\r" not in original
assert hashlib.sha256(original).hexdigest() == (
    "4d4d89c77693b75442ef1d782e59bbf4827cf8468fb3b7582fa19d10019f03a4"
)
derived = original.replace(b"\n", b"\r\n")
assert hashlib.sha256(derived).hexdigest() == (
    "c246327a96573c2c702293cb5b2efc56db8efd734077a5f13cf8f7edb76f9077"
)
print("Digest relationship verified; original files unchanged.")
```

FINDINGS.json records the exact observed and derived digests. SHA256SUMS covers
this README and FINDINGS.json, excluding itself. It is not a replacement for the
historical package manifest. No package test suite was rerun for this follow-up.
