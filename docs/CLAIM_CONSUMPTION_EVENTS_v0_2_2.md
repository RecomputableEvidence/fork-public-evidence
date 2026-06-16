# Claim Consumption Events v0.2.2

## Status

Version: `CCE_v0_2_2`

CCE v0.2.2 is the final precision hardening patch in the CCE v0.2 line.

It preserves CCE v0.2.1's edge model and closes residual integration-layer drift surfaces before graph-level verification work.

## Purpose

A Claim Consumption Event is a downstream consumption edge.

It records how a CBC was consumed. It never becomes a claim-boundary node.

## Required CCE non-claims

CCE v0.2.2 requires five baseline CCE non-claims:

- source truth is not asserted;
- legal, contractual, regulatory, or compliance sufficiency is not asserted;
- runtime enforcement or authorization is not asserted;
- source completeness is not asserted;
- the CCE does not become the expanded claim-boundary node.

## Expansion semantics

A CCE can record an expansion, but it does not hold the expanded claim.

Any expanded downstream claim must be represented as a separate CBC and referenced by the CCE.

The CCE records the direction and destination of expansion. It does not assert that the new boundary is true, sufficient, complete, or locally validated unless the reference-resolution state records local resolution.

## Pointer resolution

`LOCAL_RESOLVED` means the referenced CBC was present in the local bundle and structurally validated.

`EXTERNAL_POINTER` means the pointer is external and is not claimed to have been inspected locally.

`NOT_RESOLVED` means an expansion pointer was recorded but not resolved and must be carried as an unresolved unknown.

`NOT_APPLICABLE` means no new boundary exists for the edge type. It differs from `NOT_RESOLVED`: no resolution was expected for a preserved or narrowed edge.

## Downstream output typing

The `downstream_output.artifact_type` field is constrained to bounded output types.

Overclaiming labels such as deployment approval, compliance certification, production authorization, or legal sufficiency are not valid CCE output types.

## Source assurance

Source assurance profiles describe how evidence was obtained or represented.

They do not assert source truth, factual correctness, legal sufficiency, safety, compliance, deployment readiness, or source completeness.

Assurance limitations cannot be used to smuggle absolute truth language.
