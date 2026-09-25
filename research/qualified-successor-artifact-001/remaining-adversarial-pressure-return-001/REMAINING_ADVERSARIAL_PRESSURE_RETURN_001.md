# QSA-001 v0.1 Remaining Adversarial Pressure Return 001

Target reference: `d18119105481d194298148a31715303c77a244bc`

Plan freeze: `b1be477d1d6ae12ea17c0b7e849aaddb1dd6d55d`

All A3-A10 probes were executed against isolated derivatives of the exact frozen reference package. The baseline package remained byte-identical after execution.

## Results

- A3: direct domain-separation replay rejected (`domain/type mismatch: p2-adoption`).
- A4: parent mutation rejected at signature verification; an independent direct parent comparison also failed.
- A5: successor-state mutation rejected at signature verification; recomputed mutated successor hash no longer matched the preserved build-mark successor hash.
- A6: qualification expiry mutation rejected at signature verification, but a diagnostic that consistently updated dependent hashes and suppressed only signature verification returned PASS despite `valid_until < adopted_at`. This preserves a bounded temporal-enforcement gap.
- A7: attempt to extend the chain to a third state was rejected by schema `maxItems=2`; direct stale-parent adoption semantics are therefore not exercisable in this reference fixture. This is a bounded representation/pressure gap.
- A8: the frozen P3 fixture already exercises EDITORIAL -> CONSTITUTIONAL escalation and is preserved as `P3_REJECTED_ROUTE_INVALID`; verifier PASS confirms that rejection fixture is required.
- A9: removing the P2 inspection receipt is rejected by schema as a missing required property.
- A10: after mutating the separate builder actor-binding relation, all 16 signed protocol objects still verified mathematically, while the full verifier rejected with `genesis actor-binding mismatch`.

## Disposition

```text
FULL_DECLARED_PRESSURE_MATRIX_EXECUTED
+ BOUNDED_FAILURES_PRESERVED
+ SUCCESSOR_REPAIR_CANDIDATES_IDENTIFIED
```

No frozen reference bytes were repaired or rewritten. Bootstrap is withheld pending a successor decision or an explicit bounded acceptance decision.
