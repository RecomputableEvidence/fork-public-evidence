# Human Recomputation Sandbox v0.1.1

## Review question

Can an independent human reviewer reconstruct and recompute the Boundary-State Interoperability v0.1.1 evidence packet, distinguish structural reproduction from semantic adequacy, and record any residual ambiguity without expanding the authority of the original checker or receipt?

## Review objects

- Boundary-State Interoperability Evidence Packet v0.1.1.
- Boundary-State Interoperability Checker v0.1.1.
- Frozen Boundary-State Interoperability Profile v0.1.4.
- Exterior verification report filed in exterior-receipts/.
- Candidate reviewer regression payloads derived from human adversarial review.

## Reviewer actions

A reviewer may:

1. Verify hashes and source artifact integrity.
2. Re-run the canonical, adversarial, and reviewer-regression suites.
3. Compare fresh outputs against packaged receipts.
4. Inspect whether accepted outcomes are computed independently of expected values.
5. Test determinism across PYTHONHASHSEED conditions.
6. Articulate semantic concerns that remain outside structural reproduction.
7. Propose additional candidate regression payloads.

## What counts as a useful human recomputation receipt

A useful receipt should identify:

- environment used;
- artifact paths and SHA256 hashes;
- exact commands run;
- reproduced counts;
- receipt comparison result;
- any local deviations;
- semantic observations that did not affect structural reproduction;
- any candidate payloads proposed for future triage.

## Boundary rule

A successful recomputation does not mean the checker establishes legal sufficiency, compliance sufficiency, safety, truth, production readiness, or reliance sufficiency. It means the bounded structural evidence reproduced under the reviewer's stated conditions.