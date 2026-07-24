# Exterior recomputation envelope — PR #92 causal replay v0.3

**Target:** `PR92_CAUSAL_RECONCILIATION_V0_3`
**Standing before review:** `UNRESOLVED_PENDING_EXTERIOR_RECOMPUTATION`

This envelope asks a reviewer to recompute PR #92 from its exact Git objects
without treating registry order or a committed projection as authority.

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
- pull request: `#92`
- branch: `agent/longitudinal-causal-reconciliation-v0-3`
- head commit: `353c1b8159cfe0b4e1f3710b11a3c7f1aeb1bc84`
- head tree: `a85af6ef1c7db88dcddbc709944d9872320cdb96`
- predecessor commit: `e848ea0825bafc1aa3754d89e719d71b5a9f3982`
- predecessor tree: `0b5f11eb6c1cd8c90b4cacce2a747045da917741`

Stop and classify acquisition as unresolved if either acquired coordinate
differs. Do not substitute a moving branch tip.

```bash
git clone --filter=blob:none --no-checkout \
  https://github.com/RecomputableEvidence/fork-public-evidence.git
cd fork-public-evidence
git fetch --no-tags origin \
  refs/heads/agent/longitudinal-causal-reconciliation-v0-3
git checkout --detach 353c1b8159cfe0b4e1f3710b11a3c7f1aeb1bc84
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
python tools/check_longitudinal_causal_reconciliation_v0_3.py
python tools/check_longitudinal_causal_reconciliation_v0_3.py \
  --coordinate 5150ece4c29cea38cfe5e25daeb781423c680834
python tools/check_longitudinal_causal_reconciliation_v0_3.py \
  --compare-left c879242c4dafad68bdd8e7bcf2466e4169351969 \
  --compare-right 5150ece4c29cea38cfe5e25daeb781423c680834
python -m pytest tests/test_longitudinal_causal_reconciliation_v0_3.py -q
```

Independently derive the bounded causal inventory and both-parent deltas:

```bash
git rev-list --reverse --topo-order \
  0bac4f60986e0be4da53d6b69c49aab1f7e73e7d \
  ^5fbabbd486d4e863d23e0096600185ada92539a6 \
  ^c6bb2df424193e7ef043ee3c0436bf97ba10fc6e
git show -s --format=%P 97abe21daed2daec8a608851467875df42a99f0a
git show -s --format=%P 0bac4f60986e0be4da53d6b69c49aab1f7e73e7d
git diff-tree --no-commit-id --name-only -r \
  97abe21daed2daec8a608851467875df42a99f0a^1 \
  97abe21daed2daec8a608851467875df42a99f0a
git diff-tree --no-commit-id --name-only -r \
  97abe21daed2daec8a608851467875df42a99f0a^2 \
  97abe21daed2daec8a608851467875df42a99f0a
```

Repeat the per-parent comparison for closure
`0bac4f60986e0be4da53d6b69c49aab1f7e73e7d`.

## 5. Required challenges

At minimum, record whether the executable tests reject:

1. a missing frontier event;
2. an altered per-parent Git delta;
3. a missing dimension-level merge decision;
4. `REQUIRE_EQUAL` over divergent parent states;
5. a forged parent or result digest;
6. silent admission promotion;
7. an overbroad explicit join;
8. a divergent committed projection.

Also record whether shuffled registry order leaves the derived projection
unchanged. Do not rewrite an adverse result into conformance.

## 6. Comparison values

Only after recording raw observations, compare:

- checker status: `CAUSAL_RECONCILIATION_REPRODUCED`;
- focused tests at the exact target: 18 passed;
- state-vector SHA-256:
  `356a64ee2dd317d752c5cbba2457942de4baa0506b9a0a2b119dce45a6f831c1`;
- closure node digest:
  `28f504cdc071bd0b15767a3c41fc4511ae1bd7455bfef4d362c01eff8ca403d7`;
- active event head:
  `0bac4f60986e0be4da53d6b69c49aab1f7e73e7d`;
- admission, authority, review inheritance, and execution remain absent.

Expected values must not replace observed commands, outputs, exit codes, and
digests. A mismatch may establish `REPRODUCED_WITH_CORRECTION_REQUIRED`,
`NOT_REPRODUCED`, or `UNRESOLVED_INCOMPLETE`.

The reviewer should separately assess whether the frontier is semantically
complete and whether `REQUIRE_EQUAL`, `SELECT_PARENT`, and `EXPLICIT_JOIN`
cover the declared reconciliation surface without implicit promotion.

## 7. Predecessor manifest correction

Confirm that PR #92 preserves
`docs/state/longitudinal-recomputation-v0.2/PACKAGE_MANIFEST_v0_2.json`
unchanged at SHA-256
`d2bbfc8fa6ec31872071706a85a036164baeb93de4a57287d2d790164463f4fa`,
while v0.2.1 removes moving shared dependencies from immutable membership.

## 8. Return record

Complete
`EXTERIOR_RECOMPUTATION_RECEIPT_TEMPLATE_PR92_v0_1.json`, attach or transmit
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
