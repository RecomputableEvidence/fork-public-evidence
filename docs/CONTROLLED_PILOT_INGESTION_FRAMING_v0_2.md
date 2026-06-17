# Controlled Pilot Ingestion Framing v0.2

## Purpose

This pilot is designed to observe an existing AI-assisted, AI-adjacent, vendor-assisted, rules-assisted, or human-reviewed workflow without changing the underlying decision process.

Fork will act as an out-of-band evidence-boundary sidecar. It will preserve bounded records of what was requested, what evidence or artifacts were referenced, what outputs or determinations were produced, what human review occurred, what claims were made, what claims were not made, and whether the resulting evidence packet still structurally verifies.

Fork is closer to an evidentiary flight recorder than a co-pilot: it records how claims, limits, evidence references, and reliance moved, but it does not fly the plane.

## Pilot posture

Fork observes and preserves. It does not decide.

Fork does not certify that source material is true, complete, lawful, admissible, medically correct, procedurally sufficient, or compliant.

## Data boundary

Fork does not require the institution's primary workflow artifacts to leave the controlled environment in order to perform structural boundary preservation. Where appropriate, Fork may preserve structured references, hashes, timestamps, artifact identifiers, claim boundaries, non-claim boundaries, verification receipts, and graph-preservation results rather than exporting full source content.

## First ingestion mode

The recommended first ingestion mode is nightly batch export or append-only file drop from approved workflow sources.

This preserves Fork's out-of-band posture and avoids coupling the pilot to production runtime behavior.

## Free-text scope

Fork may preserve the existence, reference, hash, timestamp, and location of free-text fields. Fork does not perform NLP to decide whether free text contradicts a machine-readable boundary.

Required scope indicators:

- `nlp_scope: NOT_EVALUATED`
- `free_text_scope: NOT_EVALUATED_FOR_INFERENCE`

## Recommended first workflow

The recommended first controlled pilot candidate is prior authorization denial + internal appeals review.

## Pilot non-claims

The pilot does not claim production readiness across all workflows, legal admissibility, regulatory compliance, medical correctness, factual completeness, source truth, model quality, clinical safety, institutional approval, runtime authorization, or replacement of existing audit, legal, compliance, clinical, utilization-management, or appeal processes.
