# ADV_003 Post-Fix Recomputation Instructions v0.1

## Purpose

Independently recompute the first M87 × Fork remediation loop for:

- unmanifested packet-file addition detection; and
- packet-root-bound artifact hashing.

The historical v0.1 checker and Mac McFall / M87 source harness remain unchanged. This run evaluates the append-only successor checker and Fork-admitted repository-shaped derivative harness.

## Required revision

Run against the exact commit and artifact digests supplied in the accompanying transmission receipt. Do not substitute a mutable branch name for the commit SHA when recording the verdict.

## Environment

- Python 3.11 or later
- a fresh checkout of the identified commit
- an operating system and filesystem capable of creating a symbolic link for the symlink-substitution case
- no network access is required by the checker or harness

On Windows, enable Developer Mode or run in an environment with symbolic-link privilege. An inability to create the symlink fixture is a tool/environment error, not a passing or failing security result.

## Commands

From the repository root:

```text
python tools/check_longitudinal_reconstruction_day0_packet_v0_1_1.py --json
```

Expected: the clean canonical packet returns exit `0` with `failed: 0`.

Run the complete derivative harness and preserve its output:

```text
python tools/check_longitudinal_day0_adv_003_recomputation_v0_1.py --repo-root . --json > ADV_003_POST_FIX_RECOMPUTATION_v0_1.json
```

Expected process exit: `0`.

Expected summary:

```json
{
  "total": 7,
  "passed": 7,
  "failed": 0
}
```

Run the focused regression test:

```text
python -m pytest -q tests/test_longitudinal_day0_adv_003_v0_1.py
```

## Required outcome codes

The harness must emit all of the following:

- `CLEAN_PACKET_STILL_VERIFIES`
- `ADV_003_A_INVENTORY_ADDITION_DETECTED`
- `ADV_003_B_PACKET_ROOT_HASH_BASE_ENFORCED`
- `PACKET_ROOT_CONTROLS_ARTIFACT_RESOLUTION`
- `PATH_ESCAPE_REJECTED`
- `SYMLINK_SUBSTITUTION_REJECTED`
- `EXISTING_ADVERSARIAL_STANDING_UNCHANGED`

## Digest capture

Record the exact commit and artifact digests:

```text
git rev-parse HEAD
sha256sum tools/check_longitudinal_reconstruction_day0_packet_v0_1_1.py
sha256sum tools/check_longitudinal_day0_adv_003_recomputation_v0_1.py
sha256sum tests/test_longitudinal_day0_adv_003_v0_1.py
sha256sum ADV_003_POST_FIX_RECOMPUTATION_v0_1.json
```

PowerShell equivalent:

```powershell
& git rev-parse HEAD
Get-FileHash tools/check_longitudinal_reconstruction_day0_packet_v0_1_1.py -Algorithm SHA256
Get-FileHash tools/check_longitudinal_day0_adv_003_recomputation_v0_1.py -Algorithm SHA256
Get-FileHash tests/test_longitudinal_day0_adv_003_v0_1.py -Algorithm SHA256
Get-FileHash ADV_003_POST_FIX_RECOMPUTATION_v0_1.json -Algorithm SHA256
```

## Verdict rules

- `RECOMPUTED_POST_FIX_CONFORMING`: all seven cases reproduce, the focused regression passes, and recorded artifact digests match the transmission.
- `RECOMPUTED_POST_FIX_NON_CONFORMING`: one or more required cases execute but produce a contradictory result.
- `RECOMPUTATION_INCONCLUSIVE`: the exact commit/artifacts are unavailable, the output cannot be parsed, or an environment limitation prevents a required case from executing.

Do not convert an environment error into a conforming or non-conforming architecture conclusion.

## Append-only verdict

Return the unchanged output JSON, its SHA-256, environment details, exact commit SHA, and one of the bounded verdicts above. The verdict is appended to the historical limitation record; it does not erase or rewrite the pre-fix observation.

## Non-authority

This recomputation verifies bounded checker behavior only. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, institutional authority, or merge authority.
