# Fork CAD Candidate Local Validation v0.1

Status: `LOCAL_RECOMPUTATION_NOT_INDEPENDENT_REVIEW`

Candidate branch: `research/conversational-authority-drift-v0-1`

Base commit at branch creation: `1241c0084900f2c60f362205525464582e57b4a7`

Commands executed against a disposable local candidate tree:

```text
python tools/check_fork_cad_candidate_v0_1.py --root <candidate-root>
python -m unittest discover -s tests -p 'test_*.py' -v
```

Observed result:

```text
PASS: Fork CAD candidate v0.1 structural checks
Ran 3 tests
OK
```

Covered negative controls:

- unknown source reference is rejected;
- canonicalization flag set to true is rejected.

Non-claims:

- this is not an independent human review;
- this is not GitHub Actions evidence;
- this is not repository admission;
- this does not verify the private source bytes from a fresh clone;
- this does not validate the technical claims inside Fracture;
- this authorizes zero provider calls and has no Pair-001 effect.
