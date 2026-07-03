# Scenario 08 Transition Graph

```text
[System A: Prior Review Authority]
  creates bounded record at T1
  supports: record integrity, prior scope, prior authority context
  does not support: current authority after validity change
        |
        | S08-B01
        | PRIOR_VALIDITY_RECORDED
        | AUTHORITY_CONTEXT_BOUNDED_TO_T1
        v
[System B: Validity Change Source]
  records revocation / expiry / supersession / narrowing at T2
  effect: current reliance requires revalidation
        |
        | S08-B02
        | VALIDITY_STATE_CHANGED
        | PRIOR_AUTHORITY_NOT_CURRENT_AUTHORITY
        v
[System C: Downstream Reliance Actor]
  attempted expansion at T3:
  prior validity -> current validity
        |
        v
[Failure Event]
  record_support: NOT_SUPPORTED
  required: current authority / current evidence / current policy-state revalidation
```
