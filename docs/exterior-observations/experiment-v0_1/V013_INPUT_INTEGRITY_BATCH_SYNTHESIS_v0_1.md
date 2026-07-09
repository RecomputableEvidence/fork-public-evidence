# v0.1.3 Input-Integrity Batch Synthesis v0.1

Identifier: V013_INPUT_INTEGRITY_BATCH_SYNTHESIS_v0_1
Status: Draft
Classification: Exterior observance batch synthesis
Applies to: Exterior Observance Experiment v0.1.3

No endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied.

## Purpose

This document preserves the v0.1.3 input-integrity observance batch as an exterior observance record.

The batch is not treated as validation, endorsement, approval, certification, legal sufficiency, compliance sufficiency, audit sufficiency, production-readiness evidence, or consensus.

The batch is treated as evidence of heterogeneous access, retrieval, and interpretation behavior across LLM environments.

## Batch-level finding

The v0.1.3 packet exposed differentiated retrieval and interpretation behavior across LLM environments, including:

1. clean access failure with no substantive claim;
2. access failure followed by generic or conceptual analysis;
3. raw packet access with documentation-layer limitation;
4. direct multi-file access with artifact-level findings.

This heterogeneity is the observation.

Uniform review quality was not expected and is not claimed.

## Observed access and interpretation classes

| Class | Description | Preservation treatment |
|---|---|---|
| Clean access failure | The observer could not retrieve the packet and declined to assess the source text. | Preserve as access failure with zero retrieval fidelity. |
| Access failure plus conceptual substitution | The observer could not retrieve the packet but provided generic analysis, external citations, or design patterns. | Preserve as source-contamination pressure, not packet review. |
| Raw packet success, documentation-layer only | The observer retrieved the plaintext packet but did not inspect executable, schema, CSV, or repository layers. | Preserve as documentation-layer review with scope limitation. |
| Direct multi-file access | The observer accessed the packet and multiple linked artifacts and produced artifact-level findings. | Preserve as direct raw multi-file pass, bounded by execution status. |
| Second-order observance | The observer analyzed a synthesis or batch writeup rather than the packet itself. | Preserve as meta-analysis, not direct packet review. |

## Individual observation preservation

### Gemini

Classification:

```yaml
access_status: attempted_failed
retrieval_fidelity: zero
interpretation_scope: none
substantive_packet_review: false
source_contamination: false
recommended_preservation: access_mode_failure
```

Gemini reported failed retrieval, refused to assess the inaccessible packet, and requested pasted plaintext.

This is high-integrity access-failure behavior.

### Perplexity-like access-failure pass

Classification:

```yaml
access_status: attempted_failed
retrieval_fidelity: zero
interpretation_scope: conceptual_only
substantive_packet_review: false
source_contamination: true
recommended_preservation: source_contamination_after_failed_retrieval
```

The pass failed to retrieve the packet but generated generic conceptual analysis and unrelated external citations.

This is not evidence of packet inspection.

It is preserved as a pressure signal showing how failed retrieval can be laundered into apparent analysis.

### Copilot-like access-failure pass

Classification:

```yaml
access_status: attempted_failed
retrieval_fidelity: zero
interpretation_scope: conceptual_only
substantive_packet_review: false
source_contamination: partial
recommended_preservation: conceptual_only_after_failed_retrieval
```

The pass failed to retrieve the packet and provided generic control recommendations.

The recommendations may be useful as design pressure but are not evidence that v0.1.3 was inspected.

### Claude

Classification:

```yaml
access_status: performed
retrieval_fidelity: packet_only
interpretation_scope: documentation_layer_only
substantive_packet_review: true
source_contamination: false
recommended_preservation: raw_packet_success_documentation_layer_only
```

Claude retrieved the raw plaintext packet and explicitly bounded its pass as documentation-layer only.

It did not clone the repository, execute code, run schema validation, or inspect the data-layer artifacts outside the packet.

Key findings preserved as v0.1.4 pressure signals:

- analyst-output excerpting can itself be laundered into implied validation;
- divergent or contradictory coding across observers should be treated as a first-class pressure case;
- plaintext-only access cannot substitute for schema or data-layer inspection.

### Vibe-like direct multi-file pass

Classification:

```yaml
access_status: performed
retrieval_fidelity: multi_file
interpretation_scope: direct_raw_multi_file_review
substantive_packet_review: true
source_contamination: false
recommended_preservation: direct_file_review_with_artifact_boundary_findings
```

The pass reported direct raw access to multiple artifacts and identified artifact-level boundary gaps.

Key findings preserved as v0.1.4 pressure signals:

- artifact-level boundaries should travel with individual artifacts, not only with the packet;
- CSV artifacts should not receive comment rows that may break strict CSV consumers;
- JSON schemas may carry boundary descriptions where valid;
- sandbox cases should cover coding volume, synthesis boundaries, packet inclusion, analyst-output excerpting, divergent coding, and source contamination after failed retrieval.

## Synthesis conclusion

The v0.1.3 batch is successful as an input-integrity observance run because it surfaced differentiated behavior across LLM environments.

It does not validate Fork.

It does not validate the packet.

It does not establish reviewer consensus.

It supports a bounded v0.1.4 artifact-boundary hardening pass.

## Non-endorsement

No endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied.
