# QSA-001 v0.1.1 successor reference

This is a bounded successor to the frozen QSA-001 v0.1 reference at `d18119105481d194298148a31715303c77a244bc`.

It implements only the repairs authorized by `QSA-001-v0.1.1-SUCCESSOR-REPAIR-AUTHORIZATION-001`:

- independent temporal qualification enforcement at submission, inspection, and adoption;
- a generalized canonical chain with three states so stale-parent adoption can be exercised;
- an explicitly segregated deterministic adversarial test-key path used only by `qsa_pressure.py` to construct validly signed negative fixtures.

The frozen v0.1 reference is not modified.

## Verify the successor baseline

```text
python -m pip install -r requirements.txt
python qsa_verify.py --compare-expected
```

## Run the successor regression and focused repair probes

```text
python qsa_pressure.py
```

The pressure harness covers baseline, A1-A12, and focused probes A4-R, A5-R, A6-R1, A6-R2, A6-R3, and A7-R.

## Non-claims

A PASS establishes only the declared mechanical checks of this reference fixture. It does not establish production readiness, formal security, external identity, universal authority, semantic truth, governance wisdom, legal compliance, or any empirical Fork hypothesis.

The deterministic private test material derivable inside `qsa_pressure.py` is intentionally public fixture material. It is not a production key or an external authority credential.
