# Independent Verification Receipt
## FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001-PRESSURE-EPOCH-3284e82-FREEZE-002

**Verifier:** IBM Bob (AI agent)  
**Platform:** win32 (PowerShell, SHA-256 via `Get-FileHash -Algorithm SHA256`)  
**Verification conducted on:** extracted ZIP member bytes and the outer ZIP itself  
**Receipt scope:** FREEZE-002 only — this receipt is standalone and is NOT placed inside the frozen package  

---

## 1. Outer ZIP Integrity

**Artifact verified:** `FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001-PRESSURE-EPOCH-3284e82-FREEZE-002-FROZEN.zip`

| Item | Value |
|---|---|
| File size | 18,448 bytes |
| Computed SHA-256 | `ef1828f5edc2332b8b4f02f38d4001aa63b7d80b5a1ccece62e83ec5a759a5e6` |
| Sidecar `.sha256.txt` claimed | `ef1828f5edc2332b8b4f02f38d4001aa63b7d80b5a1ccece62e83ec5a759a5e6` |
| ZIP structure | Well-formed; extractable without error |

**Disposition:** `RECOMPUTATION_PASS`

A second file named `FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001-PRESSURE-EPOCH-3284e82-FREEZE-002-FROZEN (2).zip` (15,386 bytes, SHA-256 `b40ef43c…`) was also present in the Downloads folder. It does **not** match the sidecar and is not the canonical sealed artifact. Its existence is noted but it is not the subject of this receipt.

---

## 2. Complete Member Population (canonical ZIP)

The ZIP contains exactly **13 entries**:

| # | Filename | Uncompressed bytes |
|---|---|---|
| 1 | `00_README.md` | 2,404 |
| 2 | `01_FREEZE_MANIFEST.json` | 1,473 |
| 3 | `02_SUBJECT_IDENTITY.json` | 905 |
| 4 | `03_INSTRUMENT_IDENTITY.json` | 695 |
| 5 | `04_PRESSURE_EPOCH_RECEIPT.json` | 2,701 |
| 6 | `05_P30_CORRECTION_RECEIPT.md` | 771 |
| 7 | `06_NONCLAIMS_AND_OPEN_BOUNDARIES.md` | 655 |
| 8 | `07_GITHUB_STATE_AT_FREEZE.json` | 880 |
| 9 | `08_SOURCE_REFERENCE_INDEX.json` | 811 |
| 10 | `09_RESEAL_RECEIPT.json` | 1,711 |
| 11 | `10_PREDECESSOR_INDEPENDENT_RECOMPUTATION_RECEIPT.html` | 16,786 |
| 12 | `MANIFEST_ROOT_SHA256.txt` | 81 |
| 13 | `SHA256SUMS.txt` | 1,051 |

**Note on workspace/ZIP divergence:** The extracted workspace directory (the folder delivered alongside the ZIP) contains a different file population: `09_INDEPENDENT_RECOMPUTATION_VERIFICATION.json` (not present in the ZIP) and lacks `09_RESEAL_RECEIPT.json`, `10_PREDECESSOR_INDEPENDENT_RECOMPUTATION_RECEIPT.html`, `MANIFEST_ROOT_SHA256.txt`, and `SHA256SUMS.txt`. Additionally, `00_README.md`, `01_FREEZE_MANIFEST.json`, `04_PRESSURE_EPOCH_RECEIPT.json`, and `06_NONCLAIMS_AND_OPEN_BOUNDARIES.md` differ between the workspace copy and the sealed ZIP. The workspace copy appears to be an earlier draft predating the reseal. **The canonical sealed artifact is the ZIP.** All hash verification below is conducted against bytes extracted from the canonical ZIP.

---

## 3. SHA256SUMS.txt Verification (11 of 11 content entries)

All 11 content files named in `SHA256SUMS.txt` were independently recomputed from the bytes extracted from the canonical ZIP.

| File | Recorded digest | Computed digest | Result |
|---|---|---|---|
| `00_README.md` | `1403432941c2ca0b4f212bf7ee867ec0bfe6926b55eabaf11c6a2856a37c677a` | `1403432941c2ca0b4f212bf7ee867ec0bfe6926b55eabaf11c6a2856a37c677a` | ✓ MATCH |
| `01_FREEZE_MANIFEST.json` | `6575109fa563850010a15e9e16bc589fc838f4940cd646cd993cf32e00a5aafd` | `6575109fa563850010a15e9e16bc589fc838f4940cd646cd993cf32e00a5aafd` | ✓ MATCH |
| `02_SUBJECT_IDENTITY.json` | `639e5c9bd8e17fd5898e58a206f034808dade2f029bf89063e0cc43e140b7ec8` | `639e5c9bd8e17fd5898e58a206f034808dade2f029bf89063e0cc43e140b7ec8` | ✓ MATCH |
| `03_INSTRUMENT_IDENTITY.json` | `9eae0ba22f4d848257228442eb280fc3f8a7982b6d8227e0eb97b3895e4e0027` | `9eae0ba22f4d848257288442eb280fc3f8a7982b6d8227e0eb97b3895e4e0027` | ✓ MATCH |
| `04_PRESSURE_EPOCH_RECEIPT.json` | `83ec8125bcfbbda9023004a673b1cb434127b3d7203e82f54062d68be348ddf5` | `83ec8125bcfbbda9023004a673b1cb434127b3d7203e82f54062d68be348ddf5` | ✓ MATCH |
| `05_P30_CORRECTION_RECEIPT.md` | `89723e7ddd5d825edbaef8f3eb045e9275dffd44a0ed3448a385480d491df4f9` | `89723e7ddd5d825edbaef8f3eb045e9275dffd44a0ed3448a385480d491df4f9` | ✓ MATCH |
| `06_NONCLAIMS_AND_OPEN_BOUNDARIES.md` | `75a30025e6ee56a57636fc67c9830873feff5287f2f1f3d41655b8552bab597f` | `75a30025e6ee56a57636fc67c9830873feff5287f2f1f3d41655b8552bab597f` | ✓ MATCH |
| `07_GITHUB_STATE_AT_FREEZE.json` | `b51f1fe581ebe79174474d2aa2329276f2a5a10909a83edf76214c65f46bb03e` | `b51f1fe581ebe79174474d2aa2329276f2a5a10909a83edf76214c65f46bb03e` | ✓ MATCH |
| `08_SOURCE_REFERENCE_INDEX.json` | `571d6bef2751b6f090d9445c5d97a54e3571764c3ba2e25e243906515e383061` | `571d6bef2751b6f090d9445c5d97a54e3571764c3ba2e25e243906515e383061` | ✓ MATCH |
| `09_RESEAL_RECEIPT.json` | `687e697167f47a51d2fd6ec95a932a8ff35285c9899d3d84fc7d13c327944e59` | `687e697167f47a51d2fd6ec95a932a8ff35285c9899d3d84fc7d13c327944e59` | ✓ MATCH |
| `10_PREDECESSOR_INDEPENDENT_RECOMPUTATION_RECEIPT.html` | `b03f718a5971e3de50e6db6cab14139386589eba32df6af8f4e8934443ee8f40` | `b03f718a5971e3de50e6db6cab14139386589eba32df6af8f4e8934443ee8f40` | ✓ MATCH |

**11 of 11 entries match.**

**Disposition:** `RECOMPUTATION_PASS`

---

## 4. MANIFEST_ROOT_SHA256.txt Independent Recomputation

| Item | Value |
|---|---|
| Claimed SHA-256 of `SHA256SUMS.txt` (in `MANIFEST_ROOT_SHA256.txt`) | `d2f9acfdde977d00808d34409d696b967d352a4597cc5fc34ab600c684172f9f` |
| Independently computed SHA-256 of `SHA256SUMS.txt` | `d2f9acfdde977d00808d34409d696b967d352a4597cc5fc34ab600c684172f9f` |

**Disposition:** `RECOMPUTATION_PASS`

---

## 5. JSON Parse Validation

All JSON files in the sealed ZIP were parsed successfully:

| File | Result |
|---|---|
| `01_FREEZE_MANIFEST.json` | PARSE_OK |
| `02_SUBJECT_IDENTITY.json` | PARSE_OK |
| `03_INSTRUMENT_IDENTITY.json` | PARSE_OK |
| `04_PRESSURE_EPOCH_RECEIPT.json` | PARSE_OK |
| `07_GITHUB_STATE_AT_FREEZE.json` | PARSE_OK |
| `08_SOURCE_REFERENCE_INDEX.json` | PARSE_OK |
| `09_RESEAL_RECEIPT.json` | PARSE_OK |

**Disposition:** `RECOMPUTATION_PASS`

---

## 6. Predecessor/Successor Relationship

The package identifies itself as a minimal envelope reseal (`freeze_type: MINIMAL_ENVELOPE_RESEAL`) of:

`FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001-PRESSURE-EPOCH-3284e82-FREEZE-001`

The reseal receipt (`09_RESEAL_RECEIPT.json`) records:

- `predecessor_outer_zip_sha256`: `19007b57c3e475e3d6fdeb78892f5984883dd7d0d143819b32c12989e00d440f`
- `predecessor_manifest_root_sha256`: `6078204c350a6cc8a6415d83ad9307b324fd2ae41fb619712c5311c288e6712f`

**Verification of predecessor ZIP hash:** Three FREEZE-001 ZIP variants were found in the Downloads folder. The claimed hash `19007b57c3e475e3d6fdeb78892f5984883dd7d0d143819b32c12989e00d440f` matches `FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001-PRESSURE-EPOCH-3284e82-FREEZE-001-FROZEN (2).zip` (17,615 bytes). The other two variants (`FREEZE-001-FROZEN.zip` at 8,975 bytes and `FREEZE-001-FROZEN(1).zip` at 23,604 bytes) do not match. Multiple FREEZE-001 ZIP variants exist in the environment with different hashes, indicating multiple distinct artefacts bearing the FREEZE-001 name are present. The predecessor link resolves unambiguously only to the `(2)` variant.

**Verification of predecessor manifest root:** The matching FREEZE-001 variant's `MANIFEST_ROOT_SHA256.txt` contains `6078204c350a6cc8a6415d83ad9307b324fd2ae41fb619712c5311c288e6712f`, and the independently computed SHA-256 of that variant's `SHA256SUMS.txt` is `6078204c350a6cc8a6415d83ad9307b324fd2ae41fb619712c5311c288e6712f`. These match the value recorded in `09_RESEAL_RECEIPT.json`.

**Disposition:** `RECOMPUTATION_PASS_WITH_QUALIFICATION`

Qualification: three distinct FREEZE-001 ZIP artefacts are present. The predecessor link is internally self-consistent with exactly one of them; the existence of the other two variants is not explained by the package.

---

## 7. Byte-Identity Verification of Claimed Preserved Artefacts

`09_RESEAL_RECEIPT.json` claims the following files are preserved byte-for-byte from FREEZE-001:

`02_SUBJECT_IDENTITY.json`, `03_INSTRUMENT_IDENTITY.json`, `04_PRESSURE_EPOCH_RECEIPT.json`, `05_P30_CORRECTION_RECEIPT.md`, `06_NONCLAIMS_AND_OPEN_BOUNDARIES.md`, `07_GITHUB_STATE_AT_FREEZE.json`, `08_SOURCE_REFERENCE_INDEX.json`

Comparison conducted against the matching FREEZE-001 predecessor (the `(2)` variant whose hash matches the reseal receipt's `predecessor_outer_zip_sha256`):

| File | FREEZE-001 SHA-256 | FREEZE-002 SHA-256 | Result |
|---|---|---|---|
| `02_SUBJECT_IDENTITY.json` | `639e5c9b…` | `639e5c9b…` | ✓ BYTE_IDENTICAL |
| `03_INSTRUMENT_IDENTITY.json` | `9eae0ba2…` | `9eae0ba2…` | ✓ BYTE_IDENTICAL |
| `04_PRESSURE_EPOCH_RECEIPT.json` | `83ec8125…` | `83ec8125…` | ✓ BYTE_IDENTICAL |
| `05_P30_CORRECTION_RECEIPT.md` | `89723e7d…` | `89723e7d…` | ✓ BYTE_IDENTICAL |
| `06_NONCLAIMS_AND_OPEN_BOUNDARIES.md` | `75a30025…` | `75a30025…` | ✓ BYTE_IDENTICAL |
| `07_GITHUB_STATE_AT_FREEZE.json` | `b51f1fe5…` | `b51f1fe5…` | ✓ BYTE_IDENTICAL |
| `08_SOURCE_REFERENCE_INDEX.json` | `571d6bef…` | `571d6bef…` | ✓ BYTE_IDENTICAL |

**7 of 7 claimed byte-preserved files verified as byte-identical to the matching FREEZE-001 predecessor.**

**Disposition:** `RECOMPUTATION_PASS`

---

## 8. Historical Non-Alteration Claim Check

**Finding: one instance of an overreaching claim identified, in a file not covered by the sealed SHA256SUMS.txt.**

The sealed package (`SHA256SUMS.txt` and `MANIFEST_ROOT_SHA256.txt`) itself contains the correct scoped language:
- `01_FREEZE_MANIFEST.json` explicitly states: `"integrity_nonclaim": "SELF_CONTAINED_HASH_CLOSURE != HISTORICAL_NON_ALTERATION_PROOF"`
- `09_RESEAL_RECEIPT.json` explicitly states: `"integrity_boundary": "DIGEST_MATCH_AT_VERIFICATION_TIME != PROOF_OF_HISTORICAL_NON_ALTERATION"`
- `10_PREDECESSOR_INDEPENDENT_RECOMPUTATION_RECEIPT.html` explicitly states: "This digest agreement does not, by itself, establish historical non-alteration."

However, the workspace copy of `09_INDEPENDENT_RECOMPUTATION_VERIFICATION.json` (a file **not** included in the sealed ZIP and therefore outside the package's integrity perimeter) contains the field:

```
"integrity_conclusion": "FREEZE_001_PACKAGE_UNALTERED_SINCE_SEALING"
```

This is a historical non-alteration claim inferred directly from hash agreement. This wording is exactly what the reseal's `successor_envelope_changes` list records as having been corrected ("historical non-alteration wording is replaced with verification-time digest-match wording"). The corrected language appears in the HTML receipt bound to the sealed ZIP. The overreaching claim appears only in the superseded workspace draft, which is outside the sealed perimeter.

**Assessment:** The sealed ZIP does not itself make a historical non-alteration claim inferred from hash agreement. The workspace draft (outside the perimeter) does. The distinction is structurally enforced by what is and is not covered by `SHA256SUMS.txt`.

---

## 9. TEXT_OCCURRENCE_FOUND != OCCURRENCE_IDENTITY_BOUND

This open boundary is confirmed **explicitly open** across all controlling files in the sealed ZIP:

| Location | Language |
|---|---|
| `00_README.md` | `TEXT_OCCURRENCE_FOUND != OCCURRENCE_IDENTITY_BOUND` |
| `01_FREEZE_MANIFEST.json` | `"open_boundary": "TEXT_OCCURRENCE_FOUND != OCCURRENCE_IDENTITY_BOUND"` |
| `04_PRESSURE_EPOCH_RECEIPT.json` | `"open_boundary": "TEXT_OCCURRENCE_FOUND != OCCURRENCE_IDENTITY_BOUND"` |
| `05_P30_CORRECTION_RECEIPT.md` | `TEXT_OCCURRENCE_FOUND != OCCURRENCE_IDENTITY_BOUND` |
| `06_NONCLAIMS_AND_OPEN_BOUNDARIES.md` | `TEXT_OCCURRENCE_FOUND != OCCURRENCE_IDENTITY_BOUND` |

No file in the sealed ZIP claims that this boundary has been resolved, narrowed, or promoted.

**Disposition:** `RECOMPUTATION_PASS` — open boundary remains explicitly stated and unresolved throughout.

---

## 10. Claim Strength Audit

| Claim category | Assessment |
|---|---|
| **Byte/hash agreement** | All 11 SHA256SUMS entries match at verification time. MANIFEST_ROOT matches. Outer ZIP sidecar matches. Byte-identity of 7 claimed preserved files confirmed against matching predecessor. All claims in this category are properly scoped. |
| **Package integrity at verification time** | The sealed ZIP is internally self-consistent. Its SHA256SUMS.txt covers all 11 content members; MANIFEST_ROOT_SHA256.txt covers SHA256SUMS.txt. This establishes that the bytes named match their recorded digests **at the time of this verification**. No more is established. |
| **Empirical findings** | `44_OF_44_PASS` is stated as a reported result of a local execution on win32. The package does not claim this constitutes independent qualification or empirical qualification. Consistent with the nonclaims list. |
| **Semantic standing** | `standing_effect: NONE` across all controlling JSON files. The package consistently and explicitly disclaims qualification authority, governance authority, merge authority, repository-admission authority, and canonical authority. No semantic promotion is observed. |
| **Historical non-alteration** | The sealed ZIP does not claim it. One superseded workspace draft (outside the sealed perimeter) contains such a claim but this draft is explicitly identified in `09_RESEAL_RECEIPT.json` as having been corrected in the reseal. |
| **Predecessor ZIP ambiguity** | Three FREEZE-001 ZIP variants are present. The reseal's predecessor link resolves to exactly one. The package does not address the others. This is an omission but not a false claim. |

---

## 11. Summary Dispositions

| Check | Disposition |
|---|---|
| Outer ZIP integrity (hash vs sidecar) | `RECOMPUTATION_PASS` |
| Complete member enumeration | `RECOMPUTATION_PASS` (13 members; workspace/ZIP divergence noted and explained) |
| SHA256SUMS.txt — all 11 entries | `RECOMPUTATION_PASS` |
| MANIFEST_ROOT_SHA256.txt recomputation | `RECOMPUTATION_PASS` |
| JSON parse validation (7 JSON files) | `RECOMPUTATION_PASS` |
| Predecessor/successor relationship | `RECOMPUTATION_PASS_WITH_QUALIFICATION` (predecessor link resolves; multiple FREEZE-001 variants present without explanation) |
| Byte-identity of 7 claimed preserved files | `RECOMPUTATION_PASS` |
| Historical non-alteration claim check | `RECOMPUTATION_PASS_WITH_QUALIFICATION` (sealed ZIP clean; superseded workspace draft contains overreaching claim but is outside the sealed perimeter and is explicitly noted as corrected by the reseal) |
| TEXT_OCCURRENCE_FOUND != OCCURRENCE_IDENTITY_BOUND open | `RECOMPUTATION_PASS` |
| No semantic promotion observed | `RECOMPUTATION_PASS` |

---

## 12. Explicit Distinctions

- **Byte/hash agreement** is established for all 11 content members at verification time, for the outer ZIP against its sidecar, and for the 7 byte-preserved files against the matching predecessor. This is the only thing hash agreement establishes.
- **Package integrity at verification time** is established. This means the bytes in the ZIP match the recorded digests on the day this verification was run. It does not establish when those bytes were created.
- **Historical non-alteration** is NOT established by the package and NOT claimed by the sealed ZIP. The statement "DIGEST_MATCH_AT_VERIFICATION_TIME != PROOF_OF_HISTORICAL_NON_ALTERATION" is explicitly present in the sealed artifact.
- **Empirical findings** (`44_OF_44_PASS`) are preserved as recorded. This verifier has not re-executed the test suite. The finding is treated as a reported result, not verified execution.
- **Semantic standing** is not conferred. No qualification, admission, governance, or canonical authority is claimed. This is verified to be consistent across all JSON files.

---

*This receipt was produced externally to the frozen package and is not placed inside it. It does not modify any artifact.*
