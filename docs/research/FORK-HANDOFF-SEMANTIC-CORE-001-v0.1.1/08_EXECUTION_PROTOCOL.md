# Execution Protocol

## Preconditions

1. Use this package without modifying fixtures, schema, invariants, prohibited promotions, coverage map, or validator.
2. Record Python and `jsonschema` versions.
3. Disable Python bytecode generation during qualification execution.
4. Run semantic fixtures, unit tests, and package-closure verification before producing a disposition.

## Commands

```bash
PYTHONDONTWRITEBYTECODE=1 python -B 06_REFERENCE_VALIDATOR.py --fixtures
PYTHONDONTWRITEBYTECODE=1 python -B -m unittest discover -s 07_TESTS -v
PYTHONDONTWRITEBYTECODE=1 python -B 15_CLOSURE_VERIFICATION.py
```

## Pass condition

- all 4 valid fixtures return `PASS`;
- all 15 adversarial fixtures return `FAIL`;
- 19/19 fixture expectations match;
- all 15 declared semantic invariants have explicit packaged adversarial fixture coverage with their expected failure code observed;
- the declared-`TRUTH` boundary fixture returns `PASS` while `VALIDATOR_PASS != TRUTH_ESTABLISHED` remains explicit;
- the unit test suite returns zero failures/errors;
- package file inventory is exhaustive;
- every hash-bound manifest entry and every entry listed in `SHA256SUMS` verifies;
- no `.pyc` or `__pycache__` content exists in the package;
- no claim of independent witnessing, cryptographic integrity, authority validity, truth establishment, compliance, or production readiness is emitted by the validator.

## Failure preservation

Any failure or mismatch is evidence and must be preserved. Do not mutate v0.1.1 in place after qualification. Any repair after freeze must be a separately versioned successor.
