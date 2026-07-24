# Exterior recomputation envelope — PR #91 linear replay v0.2

**Target:** `PR91_LINEAR_REPLAY_V0_2`
**Standing before review:** `UNRESOLVED_PENDING_EXTERIOR_RECOMPUTATION`

This envelope asks a reviewer to recompute PR #91 from its exact Git objects.
It does not ask for endorsement, admission, merge authorization, or agreement
with Fork's interpretation.

## 1. Independence disclosure

Before acquisition, record:

- reviewer identity and affiliation;
- relationship to Fork or its author;
- all prior exposure to Fork, PR #91, PR #92, or adjacent review material;
- one classification: `ARMS_LENGTH_DISCLOSED`,
  `PRIOR_EXPOSURE_DISCLOSED`, or `NOT_INDEPENDENT_AUTHOR_ASSISTED`.

Prior exposure does not invalidate a review, but it must remain visible.

## 2. Exact target

- repository: `RecomputableEvidence/fork-public-evidence`
- pull request: `#91`
- branch: `agent/longitudinal-recomputation-replay-v0-2`
- head commit: `e848ea0825bafc1aa3754d89e719d71b5a9f3982`
- head tree: `0b5f11eb6c1cd8c90b4cacce2a747045da917741`
- predecessor commit: `f955834681d2f2ee257276acbf68afde0ae0e69d`
- predecessor tree: `52ca08a41173e031ade01b9b6ec529cc80776380`

Stop and classify acquisition as unresolved if either acquired coordinate
differs. Do not substitute a moving branch tip.

```bash
git clone --filter=blob:none --no-checkout \
  https://github.com/RecomputableEvidence/fork-public-evidence.git
cd fork-public-evidence
git fetch --no-tags origin \
  refs/heads/agent/longitudinal-recomputation-replay-v0-2
git checkout --detach e848ea0825bafc1aa3754d89e719d71b5a9f3982
git rev-parse HEAD
git rev-parse HEAD^{tree}
```

## 3. Isolated dependency surface

Create a fresh environment and record the OS, interpreter version, dependency
installation exit code, and lock-file digests.

```bash
python -m venv .venv-fork-review
python -m pip install --require-hashes \
  -r requirements-proof-surface.lock.txt
python --version
python -m pip freeze
```

Expected lock digests are comparison values, not observations:

- `requirements-proof-surface.lock.txt`:
  `188768b6b1167c0f556482d72be7a6fc1d938afc086c870c071e46510c0f4387`
- `requirements-claim-admission.lock.txt`:
  `b7c60b29661c5cd5ffaba6651962f3db20c9612fb06accfcc9dc03b0efd5d5ab`

## 4. Raw recomputation

Preserve stdout, stderr, exit code, SHA-256, and byte size for each output.

```bash
python tools/check_longitudinal_recomputation_v0_2.py --json
python tools/check_longitudinal_recomputation_v0_2.py --derive-projection
python tools/check_longitudinal_recomputation_v0_2.py \
  --as-of bac40d9bdbd7f6b4927a676fef8def70756ad9d5
python tools/check_longitudinal_recomputation_v0_2.py \
  --diff-from bac40d9bdbd7f6b4927a676fef8def70756ad9d5 \
  --diff-to f955834681d2f2ee257276acbf68afde0ae0e69d
python -m pytest tests/test_longitudinal_recomputation_v0_2.py -q
```

The reviewer should independently inspect the bounded inventory:

```bash
git rev-list --reverse --ancestry-path \
  bac40d9bdbd7f6b4927a676fef8def70756ad9d5..f955834681d2f2ee257276acbf68afde0ae0e69d
git diff-tree --no-commit-id --name-only -r \
  bac40d9bdbd7f6b4927a676fef8def70756ad9d5 \
  f955834681d2f2ee257276acbf68afde0ae0e69d
```

## 5. Required challenges

At minimum, record whether the executable tests reject:

1. an omitted interval event;
2. a stale review head;
3. silent admission or execution promotion;
4. unreconciled concurrency;
5. a committed projection that diverges from the reducer.

Do not rewrite an adverse result into conformance. Preserve it as a finding.

## 6. Comparison values

Only after recording raw observations, compare:

- checker status: `LONGITUDINAL_STATE_REPRODUCED`;
- focused tests at the exact target: 16 passed;
- state-vector SHA-256:
  `9ce7d9b07df71481eb3020152084dce6e58b8172d7cea9f11d8bb6ec11f7a496`;
- changed dimensions: artifact, verification, review, unresolved, temporal
  closure;
- preserved dimensions: admission, authority, execution.

A mismatch may establish `REPRODUCED_WITH_CORRECTION_REQUIRED`,
`NOT_REPRODUCED`, or `UNRESOLVED_INCOMPLETE`. Expected values must not replace
observed commands, outputs, exit codes, and digests.

## 7. Return record

Complete
`EXTERIOR_RECOMPUTATION_RECEIPT_TEMPLATE_PR91_v0_1.json`, attach or transmit
the raw outputs, and compute `integrity.receipt_payload_sha256` over canonical
JSON after removing that one field.

The template's empty arrays do not disclose their item shapes. Use:

- `schemas/fork_longitudinal_exterior_recomputation_receipt_v0_1.schema.json`;
- `tools/check_longitudinal_exterior_recomputation_return_v0_1.py`.

Validate the completed return and its artifacts before transmission:

```bash
python tools/check_longitudinal_exterior_recomputation_return_v0_1.py \
  --schema \
    schemas/fork_longitudinal_exterior_recomputation_receipt_v0_1.schema.json \
  --receipt path/to/completed-receipt.json \
  --artifact-root path/to/return-directory \
  --json
```

Do not widen or replace the registered object shapes. Preserve richer metadata
as raw artifacts and refer to it from the compact `observed_result` or
`evidence` fields.

The receipt must retain `NO_ADMISSION_OR_EXECUTION_EFFECT`: provider calls,
Pair-001 calls and repetitions remain zero; admission, merge authorization,
publication, authority transfer, and execution permission remain `NONE`.
