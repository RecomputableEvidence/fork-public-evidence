# FORK-SCTD-TF00-LOSSLESS-CONTROL-EXECUTION-001-v0.1-CANDIDATE

**Program:** Fork Semantic Compression and Transferal Deviation (SCTD)  
**Execution family:** `TF-00 — LOSSLESS_TRANSFER_CONTROL`  
**Chain ID:** `SCTD-TF00-FSCOPY-001`  
**Execution status:** `PERFORMED`  
**Control disposition:** `PASS`  
**Repository admission:** `NOT_PERFORMED`  
**Governance standing effect:** `NONE`

## Bound inputs

```text
T0_SHA256 = 40279366bcce014a5dfb281e4d4c787a39c1cc07c379b5cea7622175368b30f1
T0_BYTES  = 37255
HARNESS_SHA256 = 62cc0291a4c04a0d937944b33bceffddfc48e4a789b0c848e0f6e11f3b677ec1
REPLICATES = 2
GENERATIONS_PER_REPLICATE = 10
```

The executed transformation was a binary local-filesystem stream copy. No text decoding, newline conversion, Markdown rendering, syntax integration, summarization, or model-mediated rewriting was intentionally performed.

## Observed chain

```text
R01: T0 -> A01 -> A02 -> A03 -> A04 -> A05 -> A06 -> A07 -> A08 -> A09 -> A10
R02: T0 -> A01 -> A02 -> A03 -> A04 -> A05 -> A06 -> A07 -> A08 -> A09 -> A10
```

All 20 successor artifacts produced the same SHA-256 as T0. Every successor was checked both against its immediate predecessor and against T0.

```text
D1 = EXACT
D2 = PRESERVED_BY_EXACT_BYTE_IDENTITY_CONTROL
D3 = PRESERVED_BY_EXACT_BYTE_IDENTITY_CONTROL
D4 = PRESERVED_WITHIN_REGISTERED_LEDGER_BY_EXACT_BYTE_IDENTITY_CONTROL
D5 = PRESERVED_BY_EXACT_BYTE_IDENTITY_CONTROL
```

## Deterministic replication

The same declared transformation was executed twice from T0, satisfying the preregistered deterministic-control rerun requirement. Both 10-generation chains remained byte-identical to T0 throughout.

## Fail-closed self-test

A separate temporary copy of `R01/A05` was changed at one byte without changing file length. The verifier returned `FAIL` with exit code `2`. The temporary mutation was destroyed after the self-test; no preserved run artifact was modified.

This self-test establishes only that the verifier detects this tested one-byte integrity deviation. It does not establish completeness against every possible corruption or adversarial manipulation.

## Bounded interpretation

The result establishes a working no-change baseline for the executed local-filesystem transfer mechanism. It does **not** establish that syntax-integration, rich-text transfer, AI-mediated compression, summarization, model-to-model transfer, or any TF-01+ operation is lossless.

```text
TF00_CONTROL_BASELINE = ESTABLISHED_WITHIN_EXECUTED_SCOPE
TF01_SYNTAX_INTEGRATION = NOT_EXECUTED
TF02_STRUCTURAL_COMPRESSION = NOT_EXECUTED
TF03_SEMANTIC_COMPRESSION = NOT_EXECUTED
TF04_MIXED_RECONSTRUCTION = NOT_EXECUTED
SCTD_PATTERN_DEMONSTRATION = NOT_ESTABLISHED
SCTD_GENERALIZATION = NOT_ESTABLISHED
```
