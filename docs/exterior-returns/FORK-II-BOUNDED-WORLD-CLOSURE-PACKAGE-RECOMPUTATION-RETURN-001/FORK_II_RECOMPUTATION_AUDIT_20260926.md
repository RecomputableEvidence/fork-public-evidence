# Fork II Bounded-World Closure — Independent Package Audit and Recalculation

**Audit date:** 2026-09-26  
**Input:** `FORK_II_BOUNDED_WORLD_CLOSURE_20260926.zip`  
**Received archive SHA-256:** `1bba9be907ce5e2d6ba4ec5f801ccf189d73439ffc54b0921428eb68cc6efb20`

## 1. Scope

This audit recomputes only what can be established from the bytes supplied in the closure archive. The archive contains closure/orientation documentation and package checksums, but it does **not** contain the underlying bounded fixture population, deterministic receiver implementation, preregistered Run 001 specification, Run 002 repair declaration, KERNEL-002 manifests/fixtures, Run 003 hash ranges, or ten-artefact simulation implementation/output.

Therefore the audit separates:

1. **directly recomputable package facts** — checksums, JSON validity, arithmetic, artifact presence, and documentary consistency; from
2. **documented execution claims** — claims whose source evidence is not present in the archive and therefore cannot be independently rerun here.

## 2. Package integrity recomputation

- ZIP container test: **PASS**; no compressed-data errors.
- `SHA256SUMS.txt`: **8/8 listed files match**.
- All seven ordered artifacts listed in `README.md`: **present**.
- Current-standing JSON: **valid JSON**.
- `SHA256SUMS.txt` itself is not self-listed, which is normal for a checksum manifest.

This establishes byte-level internal consistency for the supplied package. It does **not** by itself establish provenance/authenticity of the package as a whole; an independently pinned archive hash, signed release/tag, or trusted repository coordinate is needed for that stronger claim.

## 3. Original-hypothesis pilot recomputation

### Run 001

Supplied table:

- unsupported inheritance: H0 = 10, H1 = 1
- false withholding: H0 = 0, H1 = 1
- negative probes: 10 per condition
- positive controls: 4 per condition

Recomputed:

- absolute unsupported-inheritance reduction = `10 - 1 = 9`
- relative reduction = `9 / 10 = 0.90 = 90.0%`
- H0 unsupported-inheritance rate = `10/10 = 100%`
- H1 unsupported-inheritance rate = `1/10 = 10%`
- primary criterion `U_H1 < U_H0`: **PASS** (`1 < 10`)
- false-withholding change, H1 − H0 = `1 - 0 = +1`
- H1 positive-control false-withholding rate = `1/4 = 25%`
- guardrail `false_withholding_H1 <= false_withholding_H0`: **FAIL** (`1 <= 0` is false)
- joint preregistered success: **FAIL**

The package's `90.0%` reduction and failed-guardrail disposition are arithmetically correct.

### Run 002

Supplied table:

- unsupported inheritance: H0 = 10, H1 = 0
- false withholding: H0 = 0, H1 = 0
- negative probes: 10 per condition
- positive controls: 4 per condition

Recomputed:

- absolute unsupported-inheritance reduction = `10 - 0 = 10`
- relative reduction = `10 / 10 = 1.00 = 100.0%`
- H0 unsupported-inheritance rate = `10/10 = 100%`
- H1 unsupported-inheritance rate = `0/10 = 0%`
- primary criterion `U_H1 < U_H0`: **PASS** (`0 < 10`)
- false-withholding change, H1 − H0 = `0 - 0 = 0`
- H1 positive-control false-withholding rate = `0/4 = 0%`
- guardrail `false_withholding_H1 <= false_withholding_H0`: **PASS** (`0 <= 0`)
- joint preregistered success: **PASS**

The package's `100.0%` reduction, `+0` false-withholding change, and bounded-success disposition are arithmetically correct.

## 4. Other count checks

The current-standing document reports:

- 26/26 FII fixtures
- 13/13 frozen controls
- 39/39 combined

The combined count is internally coherent because `26 + 13 = 39`.

The separately reported `22/22` predecessor baseline, `12/12` predecessor mutants, and `8/8` targeted successor faults are presented as separate populations/suites and do not create an arithmetic contradiction with 39/39.

Claims of `46/46` manifest-listed records, `22/22` predecessor fixture hashes, `36/36` simulation assertions, five rejected attacks, and Run 003 `0/17 -> 17/17` cannot be independently recomputed from this archive because their underlying records/implementations are absent.

## 5. Embedded hash references

The closure document names three SHA-256 values:

- fixture population: `f187f612473fdd6340f9cef3e7525fb21d532229cddc78279884b8b59a53583e`
- Run 001 preregistered specification: `dc0ab5c4b0676c43afe31e9c7c87fff3134b24bcf378e7095fab1de080090b54`
- Run 002 repair declaration: `3b551c26433dca0d9b3ec876c69f2ed67b27e5193b0d85bdb9af32a91017f4a9`

No file in the supplied archive hashes to any of these values. The hashes therefore function as **external content-addressed references**, not locally verifiable evidence in this package.

As a result, this archive alone cannot verify the claims that Run 001 and Run 002 used the same exact fixture bytes, that the Run 001 specification was actually frozen before execution, or that the Run 002 change was restricted to the declared repair scope.

## 6. Cross-document consistency

The following key states are consistent across the closure/current-standing/public/successor surfaces:

- bounded closure: `SUPPORTED_IN_BOUNDED_MECHANISTIC_PILOT__CLOSED`
- external behavioral validation: `NOT_ESTABLISHED`
- Run 001: preserved failed predecessor / failed instrument run
- Run 002: bounded mechanistic support
- successor: `OPENED_NOT_EXECUTED`
- standing inheritance into successor: `NONE`
- simulation: no repository mutation / no standing promotion

No substantive contradiction was found in these core states.

## 7. Reproducibility and interpretation findings

### A. Run 002 is a repaired same-fixture successor, not independent replication

Run 002 follows observed Run 001 defects and reuses the same fixture population. That is suitable for demonstrating that the repaired deterministic instrument satisfies the bounded cases, but it is not independent evidence of generalization. The package mostly handles this correctly by limiting standing to a bounded mechanistic pilot and explicitly withholding external empirical validation.

A stronger independent validation would need either a held-out fixture population, a separately implemented receiver, external receivers, or some combination of those, with the protocol frozen before seeing result-bearing outputs.

### B. Aggregate tables are insufficient for inferential statistics

The archive provides aggregate counts but not probe-by-probe paired outcomes. Because the setting is described as a deterministic fixed fixture population rather than a random sample, ordinary inferential p-values/confidence intervals would also require additional sampling assumptions not stated in the package. No statistical-significance claim should be inferred from the 10-case counts alone.

### C. The package is internally integrity-checked but not self-authenticating

`SHA256SUMS.txt` proves that the listed files match the checksum manifest shipped beside them. An attacker or editor could, in principle, change both files and checksums together. For repository-grade provenance, pin the received archive hash or commit/tag in a separately trusted channel, ideally with signature/attestation.

### D. Two wording/status ambiguities should be cleaned up

1. The public surface says “external behavioral validation remains unopened in the successor,” while the successor object is explicitly `OPENED_NOT_EXECUTED`. This is understandable as “validation execution has not begun,” but `NOT_BEGUN` or `NOT_EXECUTED` would avoid the apparent state collision.
2. The ten-artefact simulation is called `SUPPORTED_WITH_OPEN_SEAMS` in current standing and `BOUNDED_PRESSURE_ONLY` in the closure. Both surfaces agree on `NO_STANDING_EFFECT`, so this is not a substantive contradiction, but machine-readable consumers would benefit from one canonical `status` plus a separate `evidence_role` field.

### E. “Ten-artefact handoff world” is slightly under-specified in the public case

The closure explicitly establishes ten negative probes plus four positive controls. The companion simulation explicitly establishes ten artefact lineages. The public phrase “ten-artefact handoff world” can therefore blur the pilot fixture count with the companion simulation lineage count unless the omitted fixture population establishes that there are exactly ten artefacts. A safer public phrase would be “frozen deterministic bounded handoff fixture” or “ten-negative-probe bounded handoff fixture.”

## 8. Bottom line

**Directly recomputed result:** the supplied closure package is byte-integral and internally arithmetically consistent. Run 001 correctly fails the stated joint criterion because its false-withholding guardrail fails; Run 002 correctly satisfies the stated criterion and guardrail on the supplied aggregate table.

**What is not established by recomputation from this archive:** the underlying executions, fixture identity, preregistration timing, repair-scope exclusivity, KERNEL-002 execution/recomputation totals, Run 003 hash behavior, and ten-artefact simulation behavior. Those remain documentary claims until the referenced source objects are supplied or independently retrieved from an authenticated repository coordinate.

Accordingly, the package supports the narrow statement it itself emphasizes: **a bounded documentary/mechanistic closure is internally coherent; external behavioral validation and independent execution-level reproduction are not established by this archive.**
