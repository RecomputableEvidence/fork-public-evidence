# M87 × Fork ADV_003 first recomputation loop

## Status

Append-only Fork admission surface for an exterior adversarial finding filed by Mac McFall / M87 on 17 July 2026.

The source materials registered under `source/` are preserved from the direct transmission. Fork does not silently correct, normalize, re-render, or replace them. The two PDF source artifacts are registered by exact SHA-256 and retained as direct-channel source attachments; the repository source register does not convert their contents into a Fork-authored restatement.

The Fork-authored successor checker, derivative harness, tests, and recomputation instructions are separate artifacts. They do not amend the submitted source record.

A model-assisted exact-head review of predecessor head `c15c105f7277494b335d1d038bda58c1dbc78b16` reproduced the principal packet-root and exact-inventory protections but identified a noncanonical-path normalization gap. The correction is preserved separately in [ADV_003 canonical-path correction v0.1](ADV_003_CANONICAL_PATH_CORRECTION_v0_1.md). Fresh exact-head recomputation and independent review remain required.

## Source finding

`LRT_DAY0_ADV_003_UNMANIFESTED_ADDITION_v0_1` records that the Day-0 v0.1 checker:

1. verified hashes only for manifest-listed artifacts and did not compare the actual packet file inventory against the declared set; and
2. resolved repository-relative manifest artifact paths against process working directory rather than the supplied `--packet-root`.

The first property allowed an unmanifested file to coexist with a passing packet. The second made scratch-copy hash isolation partial. The findings are related but independently testable.

## Source anchor

The observation was made against a GitHub main-branch ZIP export, not a Git checkout:

- archive name: `fork-public-evidence-main.zip`
- SHA-256: `76aa04a498a1fa886df864323f6cdeead95d1c23dbb20fd362580f45ca22d0fd`
- newest internal file mtime reported by the exterior observer: `2026-07-15T22:53:00Z`

The archive digest is the anchor of record. Any Git commit mapping remains a separate attribution unless archive bytes are compared with the candidate tree.

## Fork response

The historical checker `tools/check_longitudinal_reconstruction_day0_packet_v0_1.py` remains unchanged.

The append-only successor is:

- `tools/check_longitudinal_reconstruction_day0_packet_v0_1_1.py`

The Fork-admitted derivative harness is:

- `tools/check_longitudinal_day0_adv_003_recomputation_v0_1.py`

It verifies:

- clean packet still passes;
- an unmanifested addition fails;
- a manifested scratch-copy mutation fails;
- artifact hashes resolve beneath the supplied packet root rather than process cwd;
- path escape fails;
- symlink substitution fails;
- ADV_001 and ADV_002 historical limitation standings remain unchanged;
- dot and dot-dot path segments fail;
- duplicate and trailing separators fail;
- Windows drive-qualified, drive-relative, and UNC forms fail;
- POSIX UNC-style, backslash, and mixed-separator forms fail.

The path-representation cases recompute the mutated manifest sidecar and outer receipt before execution. Rejection therefore depends on the canonical-path contract rather than stale binding metadata.

## Finding classifications

- F-01 / ADV_003: `MATERIAL`
- F-03 / intake checksum recomputation: `MODERATE`
- F-02 / stale top-level checksum: `MINOR`

Only ADV_003 is remediated in this loop. F-02 and F-03 remain separate observations.

## Non-authority

This surface records checker behavior and bounded recomputation only. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority. Exterior submission, Fork admission, a passing checker, or an independent recomputation verdict confers no execution or merge authority.
