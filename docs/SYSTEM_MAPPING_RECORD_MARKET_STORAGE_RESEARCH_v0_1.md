# SYSTEM_MAPPING_RECORD Market Storage Research v0.1

## Purpose

This research note compares SYSTEM_MAPPING_RECORD against common storage patterns in market-leading data, AI, ML, observability, and governance platforms.

The purpose is not to claim that those systems are deficient. The purpose is to identify where Fork can sit beside existing trace, lineage, registry, evaluation, and audit-log systems without pretending to replace them.

## Naming relationship

SYSTEM_MAPPING_RECORD is the broader conceptual category: a downstream handoff record that declares whether upstream claim boundaries were preserved, narrowed, expanded, or left unresolved.

SYSTEM_MAPPING_RECEIPT is the concrete v0.1 artifact and checker implementation currently used to express that record structure in this repository.

This document uses SYSTEM_MAPPING_RECORD when discussing the architectural category and SYSTEM_MAPPING_RECEIPT when referring to the specific v0.1 receipt implementation.

## Research posture and vendor-language boundary

This document is a research scaffold over public documentation. It is not an exhaustive product analysis of any vendor product, standard, API, or platform.

The market-system analogies below are heuristic mapping aids. They do not assert product equivalence, native vendor support, vendor deficiency, or vendor-endorsed integration behavior.

This document does not claim that any platform cannot support claim-boundary metadata through extensions, custom schemas, tags, labels, metadata fields, artifacts, workflow integrations, governance policies, or third-party integrations.

## Working thesis

Traceability records what happened.

Lineage records where an artifact, dataset, model, or job came from.

A SYSTEM_MAPPING_RECORD records whether a downstream system stayed inside the upstream claim boundary, narrowed it, expanded it, or left it unresolved.

## Research boundary

This v0.1 document is a research scaffold.

It uses public documentation-level descriptions and should not be treated as a complete competitive analysis, legal conclusion, product certification, or procurement recommendation.

The table below records storage patterns observable from public documentation. It does not claim exhaustive feature coverage for any vendor.

## Market storage pattern summary

| Platform / standard | Publicly documented storage pattern | Strong at | Claim-boundary mapping gap to test | Fork fit |
| --- | --- | --- | --- | --- |
| Databricks Unity Catalog / MLflow Model Registry | Centralized governance for data and AI assets, model lifecycle management, access control, auditing, lineage, and model discovery. | Asset governance, lineage, audit, registry lifecycle. | Does not appear, from public docs alone, to encode per-claim downstream preserved/narrowed/expanded/unresolved handoff behavior. | Sidecar receipt attached to model, table, workflow, or governance artifact. |
| Microsoft Purview | Data map, scanning, metadata capture, cataloging, classification, and data lineage across data estate systems. | Metadata catalog, estate-level lineage, governance discovery. | Data lineage does not itself show whether a downstream consumer expanded an upstream governance claim. | Boundary receipt can complement lineage edges. |
| AWS Bedrock invocation logging | Model invocation logs can be stored in CloudWatch Logs, S3, or both when enabled. | Runtime invocation traceability and operational logging. | Invocation logs can show prompt/output/request metadata, but not necessarily downstream claim-boundary disposition. | Attach mapping receipt to logged invocation or workflow record. |
| Google Vertex AI ML Metadata | Tracks metadata produced by ML workflows and supports artifact lineage analysis. | ML workflow metadata, artifact lineage, reproducibility. | Artifact lineage does not itself show whether downstream governance claims stayed inside upstream boundaries. | Add claim-boundary receipt beside metadata artifact lineage. |
| LangSmith | Supports traces, datasets, experiments, evaluators, and evaluation workflows. | LLM trace inspection, datasets, evaluation results. | Traces/evals can show behavior and scores, but not necessarily explicit non-claim preservation or downstream expansion authority. | Attach SYSTEM_MAPPING_RECORD to trace/evaluation handoff. |
| Arize Phoenix | Traces AI applications via OpenTelemetry and captures paths requests take across LLM application components. | Observability, OpenTelemetry traces, debugging, evaluation. | Trace spans can show component flow, but not necessarily claim-boundary mapping semantics. | Convert selected spans into boundary handoff simulations. |
| W&B Registry | Manages and versions artifacts, tracks lineage, and promotes models through lifecycle stages. | Artifact lifecycle, versioning, lineage, model registry operations. | Registry lineage does not itself declare preserved/narrowed/expanded/unresolved claim handoff behavior. | Store receipt as artifact metadata or linked governance artifact. |
| OpenLineage | Defines runtime and design-time lineage events for jobs, datasets, and runs. | Standardized data lineage event model. | Lineage facets describe job/dataset/run relationships, not claim/non-claim inheritance boundaries. | SYSTEM_MAPPING_RECORD can complement lineage event graphs. |

## Source references

The following source references were used to frame this v0.1 research scaffold:

- Databricks documentation describes Models in Unity Catalog as extending Unity Catalog governance benefits to ML models, including centralized access control, auditing, lineage, and model discovery.
- Microsoft Purview documentation describes data lineage across different parts of an organization's data estate and different levels of data preparation.
- AWS Bedrock documentation describes model invocation logging destinations including Amazon S3 and CloudWatch Logs.
- Google Cloud documentation describes Vertex ML Metadata as supporting metadata tracking and artifact lineage analysis for ML workflows.
- LangSmith documentation describes evaluation workflows using datasets, evaluators, experiments, and traces.
- Phoenix documentation describes AI application tracing via OpenTelemetry.
- W&B documentation describes Registry as managing/versioning artifacts, tracking lineage, and promoting models through lifecycle stages.
- OpenLineage documentation describes runtime and design lineage event types for jobs, datasets, and runs.

## Research claim boundary

This document does not claim that market-leading systems cannot support claim-boundary metadata through extension, custom schemas, labels, tags, metadata fields, artifacts, or workflow integrations.

The narrower claim is:

Publicly documented storage primitives primarily emphasize traces, lineage, artifacts, evaluations, registries, metadata, and audit events. SYSTEM_MAPPING_RECORD tests a more specific handoff primitive: whether downstream use preserved, narrowed, expanded, or left unresolved an upstream claim boundary.

## Research questions for v0.2

1. Can SYSTEM_MAPPING_RECORD be represented as metadata in existing registry systems without losing non-claim semantics?
2. Can SYSTEM_MAPPING_RECORD be linked to OpenTelemetry spans without being collapsed into generic trace status?
3. Can SYSTEM_MAPPING_RECORD complement data lineage without pretending to be lineage?
4. Can SYSTEM_MAPPING_RECORD complement audit logs without becoming an approval or compliance finding?
5. Can unresolved pointers remain visible when downstream platforms prefer terminal success/failure states?
6. Can expansion authority references avoid circular reliance on structural evidence artifacts?


## Worked example: traceability and lineage without boundary mapping

A trace system may record that a downstream workflow step executed.

A lineage system may record that the downstream workflow consumed an upstream artifact.

Both records may be accurate.

The remaining boundary question is different: did the downstream system stay inside the upstream claim boundary?

Example:

- Upstream artifact claim: `claim:denial-letter-generated`
- Upstream non-claim: `does_not_claim_medical_correctness`
- Downstream statement: `ready_for_appeals_routing`

Traceability can show that the routing step happened.

Lineage can show that the routing step consumed the denial-letter artifact.

SYSTEM_MAPPING_RECORD asks whether the downstream `ready_for_appeals_routing` statement preserved the upstream boundary, narrowed it, expanded it with authority and evidence, or silently inherited a claim the upstream artifact did not make.

## Pre-tag review notes

The v0.1 research scaffold intentionally avoids vendor capability conclusions.

Preferred framing:

- public documentation emphasizes traceability, lineage, artifact, registry, evaluation, metadata, and audit-log storage;
- SYSTEM_MAPPING_RECORD tests a narrower claim-boundary handoff primitive;
- Fork can sit beside existing trace, lineage, registry, observability, and audit systems.

Avoided framing:

- any unsupported negative capability statement about a named platform;
- any exclusive-capability statement about Fork or claim-boundary handoffs;
- any statement that a market gap has been proven by this research scaffold.
