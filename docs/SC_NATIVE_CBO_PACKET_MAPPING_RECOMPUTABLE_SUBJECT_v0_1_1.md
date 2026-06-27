# SC Native CBO Packet Mapping v0.1.1 ? Recomputable Subject

## Status

Draft adapter hardening patch.

This patch extends the SC-native CBO packet mapping so a packet may include a recomputable digest subject rather than only pending or present metadata.

It remains a sandboxed collaboration artifact. It does not declare integration, compatibility, interoperability, endorsement, approval, certification, safety, compliance, admissibility, authorization, runtime participation, governance validation, invariant validation, causal validation, or truth.

## Purpose

v0.1 supported mapping an SC-native emitted continuity packet into Fork's normalized CBO minimum packet envelope.

v0.1.1 adds support for a recomputable subject:

- `canonicalization_method`
- `digest_subject`
- `digest_value: sha256:RECOMPUTE_FROM_DIGEST_SUBJECT`

The adapter may now compute the digest from the exported subject payload and place the computed digest into the normalized Fork CBO envelope.

## Boundary Rule

A successful recomputation means only that Fork recomputed the exported digest subject according to the declared canonicalization method.

It does not mean Fork validated:

- SC governance authority;
- causality;
- semantic meaning of SC-declared invariant references;
- runtime execution;
- safety;
- compliance;
- authorization;
- admissibility;
- approval;
- truth.

## Supported Canonicalization

The only supported v0.1.1 canonicalization method is:

`UTF8_JSON_MINIFIED_SORTED_KEYS`

This means:

1. take `digest_subject.payload`;
2. serialize JSON with sorted keys and compact separators;
3. encode the serialized JSON as UTF-8;
4. compute SHA-256 over those bytes.

Equivalent Python expression:

`json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")`

## Digest Instruction

The SC-native value:

`sha256:RECOMPUTE_FROM_DIGEST_SUBJECT`

is treated as an instruction to compute the digest from the exported digest subject.

It is not treated as a final declared digest.

The normalized Fork envelope receives:

- `digest_algorithm: sha256`
- `digest_value: <computed lowercase sha256 hex>`
- `digest_status: PRESENT`

## Seal Reference Preservation

If the SC-native metadata includes `seal_ref`, the adapter preserves it as:

`integrity_metadata.seal_refs`

inside the normalized Fork envelope.

This preserves seal reference visibility without converting the seal into a Fork authority claim.

## Design Principle

The adapter strengthens recomputability without expanding authority.

Fork may recompute the exported subject.

Fork does not validate the issuer's governance, causality, invariant semantics, runtime execution, safety, compliance, authorization, admissibility, approval, or truth.
