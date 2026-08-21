# FORK-SCTD-EXECUTION-HARNESS-001-v0.1-CANDIDATE

**Status:** `CANDIDATE_IMPLEMENTATION — TF-00 EXECUTABLE`  
**Bound protocol:** `FORK-SCTD-PREREGISTERED-PROTOCOL-001-v0.1-CANDIDATE`  
**Bound protocol SHA-256:** `acaf4fd0909cd32f4ccb6583e54c119c739991cbcdb6a304850a9a13791bb8a3`  
**Bound T0 SHA-256:** `40279366bcce014a5dfb281e4d4c787a39c1cc07c379b5cea7622175368b30f1`  
**Harness SHA-256 at execution:** `62cc0291a4c04a0d937944b33bceffddfc48e4a789b0c848e0f6e11f3b677ec1`  
**Repository admission:** `NOT_PERFORMED`

## Purpose

This harness implements only the first preregistered control family, `TF-00 — LOSSLESS_TRANSFER_CONTROL`. It performs raw binary filesystem transfers without text decoding or normalization and records each successor as an immutable artifact with a structured receipt.

It is deliberately not a TF-01/TF-02/TF-03 semantic evaluator. Exact byte identity is sufficient for this control to assert preservation of the artifact-resident syntax, structure, registered propositions, and standing tokens. If byte identity fails, D2-D5 are not inferred by this harness.

## Executed chain design

```text
CHAIN_ID = SCTD-TF00-FSCOPY-001
REPLICATES = 2
GENERATIONS_PER_REPLICATE = 10

R01: T0 -> A01 -> A02 -> ... -> A10
R02: T0 -> A01 -> A02 -> ... -> A10
```

The two repetitions satisfy the preregistered requirement that a deterministic transformation be rerun at least twice from the same input. Every generation receives both an adjacent comparison and a T0-relative comparison.

## Fail-closed control behavior

A generation passes only when:

```text
INPUT_SHA256 == OUTPUT_SHA256
and OUTPUT_SHA256 == T0_SHA256
and INPUT_BYTE_COUNT == OUTPUT_BYTE_COUNT
and OUTPUT_BYTE_COUNT == T0_BYTE_COUNT
```

If the equality fails, TF-00 is a control failure and the harness refuses to promote D2-D5 to preserved.

## Commands

From the package root:

```bash
python3 harness/sctd_harness.py run-tf00 \
  --config config/tf00_lossless_control.json \
  --package-root .

python3 harness/sctd_harness.py verify \
  --config config/tf00_lossless_control.json \
  --package-root .
```

## Standing

```text
HARNESS_IMPLEMENTATION = CANDIDATE
TF00_EXECUTION = PERFORMED
TF00_GENERALIZATION = NOT_ESTABLISHED
TF01_PLUS_EXECUTION = NOT_PERFORMED
REPOSITORY_ADMISSION = NOT_PERFORMED
GOVERNANCE_STANDING = UNCHANGED
```
