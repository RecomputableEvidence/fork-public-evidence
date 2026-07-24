# Longitudinal exterior recomputation and interoperability v0.3.1

**Standing:** `REVIEW_PACKAGE_CANDIDATE_NO_REVIEW_RESULT`
**Exact predecessor:** PR #92 head
`353c1b8159cfe0b4e1f3710b11a3c7f1aeb1bc84`, tree
`a85af6ef1c7db88dcddbc709944d9872320cdb96`

## Purpose

This successor freezes feature expansion and makes the next evidentiary gate
portable. It supplies exact-target envelopes and machine-checkable receipt
templates for separate recomputation of:

1. PR #91's bounded linear replay v0.2; and
2. PR #92's frontier-bounded causal reconciliation v0.3.

The package contains no completed reviewer receipt and makes no claim that
either target has been independently reproduced.

## Reviewer route

Send one envelope and its matching template:

- `EXTERIOR_RECOMPUTATION_ENVELOPE_PR91_v0_1.md`
- `EXTERIOR_RECOMPUTATION_RECEIPT_TEMPLATE_PR91_v0_1.json`
- `EXTERIOR_RECOMPUTATION_ENVELOPE_PR92_v0_1.md`
- `EXTERIOR_RECOMPUTATION_RECEIPT_TEMPLATE_PR92_v0_1.json`

The targets should be reviewed in order: PR #91 before PR #92. The complete
stack coordinates are recorded in `STACK_REVIEW_COORDINATES_v0_1.json`.

## Package and receipt checks

Validate this package:

```bash
python tools/check_longitudinal_exterior_recomputation_package_v0_3_1.py
```

Validate a returned receipt without converting its disposition:

```bash
python tools/check_longitudinal_exterior_recomputation_package_v0_3_1.py \
  --receipt path/to/returned-receipt.json
```

Receipt conformance establishes only that the result is consistently recorded
against the exact target. `REPRODUCED_WITH_CORRECTION_REQUIRED`,
`NOT_REPRODUCED`, and `UNRESOLVED_INCOMPLETE` remain valid evidence outcomes.

## Acceptance benchmark

Feature work should remain paused until:

- at least one exact-head receipt exists for PR #91;
- at least one separately disclosed exact-head receipt exists for PR #92;
- raw outputs and their digests are preserved;
- any findings are answered append-only rather than rewritten; and
- admission or merge is considered as a separate, bottom-up decision.

## Boundary

This package performs no provider call, Pair-001 call or repetition, readiness
decision, retry authorization, admission, publication, merge authorization,
authority transfer, or execution request. Package conformance is not review,
truth, correctness, compliance, legal sufficiency, safety, or institutional
authority.
