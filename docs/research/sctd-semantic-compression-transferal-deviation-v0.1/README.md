# SCTD — Semantic Compression and Transferal Deviation v0.1

Status: `ACTIVE_EMPIRICAL_RESEARCH_CANDIDATE_NO_ADMISSION_OR_PRODUCT_EFFECT`

This dedicated research surface preserves the SCTD preregistration, immutable T0 source, execution harness, TF-00 lossless-control evidence, longitudinal dataset, and verifier pressure observations.

It is repository-visible research. Repository visibility does not confer admission, product standing, general validation, or execution authority.

## Current bounded result

The registered TF-00 filesystem-copy lossless control executed two deterministic replicates of ten generations each. All 20 successor artifacts were byte-identical to T0.

```text
T0 SHA-256 = 40279366bcce014a5dfb281e4d4c787a39c1cc07c379b5cea7622175368b30f1
T0 bytes   = 37255
TF-00      = PASS
```

A one-byte mutation of a temporary test copy was rejected by the TF-00 verifier. That observation is a bounded fail-closed pressure result; it is not completeness against every corruption class.

## What TF-00 does not establish

```text
TF00_PASS
  != TRANSFER_COMPRESSION_PATTERN_DEMONSTRATED
  != SEMANTIC_DRIFT_PATTERN_DEMONSTRATED
  != GENERAL_TRANSFER_ROBUSTNESS
  != PRODUCT_CAPABILITY
```

TF-01 and later transfer/compression pressure families remain future research work.

## Surface layout

- `transport/` — exact base64 text transports for the preregistration and TF-00 execution-cycle ZIP packages, with per-segment and decoded-package digests.
- `materialize_sctd_packages.py` — reconstructs and verifies both exact ZIP packages.
- `SCTD_CURRENT_STANDING_v0_1.json` — current bounded research standing.
- `SCTD_REPOSITORY_BINDING_v0_1.json` — exact source-package and repository-placement bindings.
- `NO_ADMISSION_OR_PRODUCT_EFFECT_v0_1.json` — explicit non-effects.

The exact execution ZIP includes the local Python bytecode cache produced during execution. Its presence in the bound package does not make bytecode cache output a governed SCTD semantic artifact.
