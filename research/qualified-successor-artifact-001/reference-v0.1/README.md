# QSA-001 v0.1 four-outcome reference package

This is the smallest reference implementation authorized by the QSA-001 v0.1 conceptual freeze.

It demonstrates:

- P0 metadata-only preservation with a proposal commitment and proposal mark;
- P1 material-observation preservation without canonical mutation;
- P2 authorized successor adoption with a build mark;
- P3 rejection when an EDITORIAL declaration is inspected as CONSTITUTIONAL impact.

The committed `reference-package/` directory is a deterministic, self-contained fixture. Its `INDEX.json` names the components reconstructed by the verifier before schema and cryptographic validation. Reference keys are deterministic test keys and MUST NOT be treated as production keys, external identity proof, or universal authority.

## Verify

```text
python -m pip install -r requirements.txt
python qsa_verify.py --compare-expected
```

Expected terminal result begins:

```text
QSA-001 reference verification: PASS
```

The machine-readable receipt is reproduced with:

```text
python qsa_verify.py --json
```

## Non-claims

A verification PASS establishes the bounded mechanical checks emitted by the verifier. It does not establish semantic truth, moral legitimacy, policy wisdom, universal authority, legal compliance, or any empirical Fork hypothesis.
