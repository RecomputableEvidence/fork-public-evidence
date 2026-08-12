# Fork Stage 1 exterior recomputation delivery branch

Standing: `EXTERIOR_RECOMPUTATION_DELIVERY_PACKET_CANDIDATE_NOT_ADMITTED_NOT_MERGE_AUTHORIZED`

This draft branch carries the complete additive patch and exterior-recomputation instructions. It intentionally does **not** install the Stage 1 implementation into the governed preservation branch.

## Bound coordinates

- repository: `RecomputableEvidence/fork-public-evidence`
- governed base: `preservation/clean-continuance-v0.1@1ae03971c680e361d2d81cefc8319dfccb50d8d3`
- delivery branch: `agent/complementary-evidence-sidecar-stage-1-exterior-recompute-v0-1`
- patch SHA-256: `5cc5e819df354bbec1f6691d7c37f02ea1b720a121b32cb9e8b42b59e021463c`

The exact exterior target is the tuple:

`(governed base commit, exact delivery-branch head, patch SHA-256)`

The branch name alone is not the review coordinate.

## Exterior recomputation

1. Resolve and record the exact draft-branch head.
2. Create a clean worktree or clone at the governed base commit.
3. Copy the compressed patch from this exact delivery head and decompress it without changing the resulting bytes.
4. Verify the patch SHA-256 before applying it.
5. Apply the patch without modifying it.
6. Run the Stage 1 and exterior-packet commands specified by the applied packet.
7. Return raw stdout, stderr, exit codes, environment, independence disclosure, exact coordinates, corrections, unresolved items, and one bounded disposition.

Example:

```bash
git fetch origin preservation/clean-continuance-v0.1 \
  agent/complementary-evidence-sidecar-stage-1-exterior-recompute-v0-1

git rev-parse origin/agent/complementary-evidence-sidecar-stage-1-exterior-recompute-v0-1

git worktree add --detach ../fork-stage1-recompute \
  1ae03971c680e361d2d81cefc8319dfccb50d8d3

cd ../fork-stage1-recompute
sha256sum ../FORK_STAGE1_COMPLEMENTARY_EVIDENCE_SIDECAR_EXTERIOR_RECOMPUTATION_PACKET_v0_1.patch.gz
gzip -dc ../FORK_STAGE1_COMPLEMENTARY_EVIDENCE_SIDECAR_EXTERIOR_RECOMPUTATION_PACKET_v0_1.patch.gz > ../FORK_STAGE1_COMPLEMENTARY_EVIDENCE_SIDECAR_EXTERIOR_RECOMPUTATION_PACKET_v0_1.patch
sha256sum ../FORK_STAGE1_COMPLEMENTARY_EVIDENCE_SIDECAR_EXTERIOR_RECOMPUTATION_PACKET_v0_1.patch
git apply --check ../FORK_STAGE1_COMPLEMENTARY_EVIDENCE_SIDECAR_EXTERIOR_RECOMPUTATION_PACKET_v0_1.patch
git apply ../FORK_STAGE1_COMPLEMENTARY_EVIDENCE_SIDECAR_EXTERIOR_RECOMPUTATION_PACKET_v0_1.patch
python tools/run_complementary_evidence_sidecar_stage_1_exterior_recomputation_v0_1.py --root .
python -m pytest -q tests/test_complementary_evidence_sidecar_stage_1_v0_1.py tests/test_complementary_evidence_sidecar_stage_1_exterior_packet_v0_1.py
```

Expected local result before exterior review: `26 passed`.

## Retained correction

The packet preserves a packaging correction: the original Stage 1 manifest test passed only in the isolated overlay and was not repository-integrated. The successor patch scopes manifest coverage explicitly and preserves the original receipt as historical evidence rather than rewriting it.

## Prohibited effects

This branch and packet do not authorize merge, admission, production use, a live pilot, provider calls, Pair-001 calls, runtime control, policy enforcement, system replacement, upstream blocking, truth promotion, approval inheritance, or authority transfer.
