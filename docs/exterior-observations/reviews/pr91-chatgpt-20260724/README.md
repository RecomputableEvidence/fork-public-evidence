# PR #91 ChatGPT/Codex exterior recomputation — preserved return

## Standing

- substantive disposition:
  `REPRODUCED_WITH_CORRECTION_REQUIRED`;
- original return-package integrity: `VALID`;
- original receipt conformance against the PR #93 schema:
  `EXTERIOR_RECOMPUTATION_RECEIPT_NONCONFORMING`;
- normalized successor conformance:
  `EXTERIOR_RECOMPUTATION_RETURN_CONFORMS`;
- admission, merge, publication, authority, and execution effects: `NONE`.

The original receipt and ZIP are preserved byte-for-byte. The normalized
successor is additive and does not replace, silently repair, or reinterpret
either original.

## Preserved originals

| Artifact | SHA-256 | Bytes |
|---|---|---:|
| `ORIGINAL_EXTERIOR_RECOMPUTATION_RECEIPT_PR91_CHATGPT_20260724_v0_1.json` | `51d8249fe85fff34d288c1bfd7198639eecbd11e6fc4ae4872666fe63fcfacb9` | 53,662 |
| `ORIGINAL_FORK_PR91_EXTERIOR_RECOMPUTATION_CHATGPT_20260724_v0_1.zip` | `cb37f93be096d80f0f8ec5bc6082829ba4273bc1b214608da341949d46625155` | 94,901 |

The original receipt carries payload digest
`3a8b0629076513584f47b999594b04224638f837ac201eca96d870fbe43f1bdb`.
Its ZIP carries a 115-entry package manifest and binds 105 raw artifacts plus
35 execution metadata records.

## Reproduced observations

- exact head:
  `e848ea0825bafc1aa3754d89e719d71b5a9f3982`;
- exact tree:
  `0b5f11eb6c1cd8c90b4cacce2a747045da917741`;
- checker: `LONGITUDINAL_STATE_REPRODUCED`;
- state-vector SHA-256:
  `9ce7d9b07df71481eb3020152084dce6e58b8172d7cea9f11d8bb6ec11f7a496`;
- focused suite: 16 passed;
- clean-checkout full suite: 726 passed, 3 skipped;
- adversarial challenges: 10 of 10 rejected with their required finding code.

## Corrections retained

1. PR #91's public description reported 776 full-suite passes. The exact-target
   return independently collected 726 tests and observed 726 passed,
   3 skipped.
2. Creating `.venv-fork-review` inside the checkout caused the optional
   line-ending test to inspect reviewer-created `bin/Activate.ps1` and report
   its CRLF bytes. Moving only the virtual environment outside the checkout
   produced the clean full-suite result.
3. The reviewer read mutable PR metadata before local execution, so the run is
   not represented as blind.
4. The concurrency challenge produced the required
   `CONCURRENT_SUCCESSOR_UNRECONCILED` and the additional
   `EVENT_REGISTRY_DUPLICATE`; both remain visible.
5. The original rich receipt used execution, finding, measurement, and
   adversarial shapes that were not accepted by PR #93's compact v0.1 schema.
   That first-use portability defect is preserved rather than erased.

## Mechanical normalization

`tools/normalize_longitudinal_exterior_recomputation_return_v0_1.py`:

- verifies the registered original receipt and ZIP digests;
- recomputes and verifies the original receipt payload seal;
- maps all 35 execution records to the registered compact execution shape;
- maps all ten adversarial observations without changing their booleans;
- maps the four original findings and adds one normalization finding;
- drops only measurement extensions unavailable in schema v0.1;
- preserves the target, disclosure, environment, disposition, effects,
  non-claims, and original reviewer attestation;
- binds the normalized successor directly to both preserved originals; and
- computes a new canonical payload digest.

It performs no recomputation command and confers no new review independence.

## Validation

```bash
python tools/check_longitudinal_exterior_recomputation_return_v0_1.py \
  --receipt \
    docs/exterior-observations/reviews/pr91-chatgpt-20260724/EXTERIOR_RECOMPUTATION_RECEIPT_PR91_CHATGPT_20260724_NORMALIZED_v0_1_1.json \
  --artifact-root \
    docs/exterior-observations/reviews/pr91-chatgpt-20260724 \
  --json
```

Expected status:
`EXTERIOR_RECOMPUTATION_RETURN_CONFORMS`.

This validation establishes conformance of the normalized return container. It
does not convert package validation into substantive recomputation, erase the
recorded corrections, or authorize admission or merge.
