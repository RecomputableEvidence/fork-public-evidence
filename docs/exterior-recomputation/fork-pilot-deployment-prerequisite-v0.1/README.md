# Fork pilot deployment prerequisite — computable implementation candidate

Standing: `PILOT_DEPLOYMENT_PREREQUISITE_IMPLEMENTATION_CANDIDATE_NOT_ADMITTED_NOT_PILOT_AUTHORIZED`

This delivery packet reconstructs a byte-identical source ZIP containing a bounded, local, read-only Fork sidecar implementation for a single-workflow shadow pilot prerequisite.

## Reconstruct

From this directory:

```bash
python materialize_fork_pilot_prerequisite_v0_1.py --extract ./reconstructed
```

The materializer fails closed if any segment, aggregate Base64 stream, decoded archive, ZIP member count, CRC, or extraction path does not match the manifest.

Expected archive:

- bytes: `41,395`
- SHA-256: `fc8deb027678099d0da353684166c91991d4451ae60e54e9969310055a9636b2`
- members: `28`

## Implementation scope

The reconstructed package provides strict JSON/JSONL file-drop ingestion, content-addressed artifacts, an append-only event hash chain, explicit observation-gap records, state reconciliation, deterministic evidence-bundle export, independent bundle verification, tests, schemas, Docker/Compose examples, and pilot intake/security gates.

It contains no provider calls, live network adapter, runtime control, policy enforcement, authority inference, approval function, compliance determination, or automatic pilot authorization.

## Required gates before a real pilot

1. Exterior recomputation of this exact candidate.
2. Named workflow and accountable workflow owner.
3. Approved data classification, retention, deletion, and access boundaries.
4. Client-approved deployment image/runtime and security review.
5. Shadow-mode authorization with rollback and incident procedures.
6. Separately reviewed admission and pilot authorization acts.

CI success, local tests, reconstruction, or merge do not themselves satisfy these gates.
