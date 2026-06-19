# SYSTEM_MAPPING_RECORD Simulation Harness v0.1

## Purpose

The SYSTEM_MAPPING_RECORD simulation harness tests claim-inheritance-less handoffs under controlled synthetic scenarios.

The harness does not simulate production systems. It creates synthetic upstream boundaries, downstream mappings, and expected structural outcomes so the repository can test whether boundary behavior is visible.

## Core test question

When a downstream system consumes an upstream claim boundary, did it:

- preserve the upstream boundary;
- narrow the upstream boundary;
- expand the upstream boundary;
- drop an upstream non-claim;
- launder an unresolved pointer into a resolved claim?

## Simulation classes

### CLEAN_PRESERVE

The downstream mapping repeats only what the upstream record claimed and preserves upstream non-claims.

Expected result kind:

`SIMULATION_MAPPING_RECORDED`

### SAFE_NARROWING

The downstream mapping uses a smaller subset of the upstream claim boundary and preserves or explicitly handles upstream non-claims.

Expected result kind:

`SIMULATION_MAPPING_RECORDED`

### EXPLICIT_EXPANSION_WITH_AUTHORITY

The downstream mapping adds a new claim with authority and evidence references.

Expected result kind:

`SIMULATION_MAPPING_RECORDED`

### UNSAFE_EXPANSION_WITHOUT_AUTHORITY

The downstream mapping adds a new claim without authority or evidence references.

Expected result kind:

`SIMULATION_EXPANSION_GAP_RECORDED`

### NON_CLAIM_DROP

The downstream mapping omits or fails to preserve/drop an upstream non-claim.

Expected result kind:

`SIMULATION_NON_CLAIM_DROP_RECORDED`

### UNRESOLVED_LAUNDERING

The upstream boundary includes an unresolved pointer, and the downstream mapping treats it as resolved without resolution evidence.

Expected result kind:

`SIMULATION_UNRESOLVED_POINTER_GAP_RECORDED`

## Non-decisional boundary

The simulation harness records structural simulation outcomes only.

It does not claim that a downstream system is approved, compliant, safe, correct, authorized, production-ready, or legally sufficient.

## Market-system analogue

Each simulation includes a market-system analogue field showing how a conventional platform might store the same handoff as:

- a trace span;
- an audit log row;
- a lineage edge;
- a model registry artifact;
- an evaluation record;
- metadata attached to a workflow event.

The analogue is illustrative. It is not a vendor integration and does not claim that the named market system behaves in that exact way.

## v0.1 limitation

The v0.1 harness validates synthetic simulation fixtures and expected structural outcomes.

It does not ingest real Databricks, Purview, Bedrock, Vertex, LangSmith, Phoenix, W&B, OpenLineage, OpenTelemetry, or MLflow records.
