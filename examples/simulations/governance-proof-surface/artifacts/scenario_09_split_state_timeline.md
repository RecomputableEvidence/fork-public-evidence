# Scenario 09 Split-State Timeline

```text
T1 — Prior validity state exists.
T2 — Validity-changing event recorded in System A.
T3 — System B has not consumed the change.
T4 — System C relies on local or intermediate state.
T5 — Fork records visibility gap and split-state reliance.
```

## Split-state invariant

```text
recorded_in_A does not imply visible_in_B
visible_in_B does not imply consumed_by_C
not_visible_locally does not imply still_valid_currently
```

Fork preserves visibility and consumption state. It does not decide negligence, excuse, authorization, compliance, legal sufficiency, acceptance, correctness, or execution eligibility.
