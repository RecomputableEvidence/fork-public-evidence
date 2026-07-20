# Fork CAD Candidate Local Validation v0.1

Status: `HISTORICAL_LOCAL_VALIDATION_SUPERSEDED_BY_LATER_HEAD`

Candidate branch: `research/conversational-authority-drift-v0-1`

Validated exact head: `2b67a2e98430addcef3a1bfccc92233327a7f954`

Base commit at branch creation: `1241c0084900f2c60f362205525464582e57b4a7`

Commands executed against a disposable local candidate tree:

```text
python tools/check_fork_cad_candidate_v0_1.py --root <candidate-root>
python -m unittest discover -s tests -p 'test_*.py' -v
```

Observed result at the validated head:

```text
PASS: Fork CAD candidate v0.1 structural checks
Ran 3 tests
OK
```

Covered negative controls at that head:

- unknown source reference is rejected;
- canonicalization flag set to true is rejected.

The candidate advanced after this local run. The later head adds supplemental sources, model-self-report boundaries, an observable-event register, and additional negative controls. This historical result must not be represented as validation of the later head.

Non-claims:

- this is not an independent human review;
- this is not GitHub Actions evidence;
- this is not repository admission;
- this does not verify the private source bytes from a fresh clone;
- this does not validate the technical claims inside Fracture;
- this authorizes zero provider calls and has no Pair-001 effect.
