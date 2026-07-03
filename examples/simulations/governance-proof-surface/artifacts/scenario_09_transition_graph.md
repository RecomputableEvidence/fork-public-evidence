# Scenario 09 Transition Graph

```text
[System A: Revocation Source]
  records validity-changing event
        |
        | S09-B01
        | VALIDITY_CHANGE_RECORDED
        | NOT_AUTOMATICALLY_GLOBAL
        v
[System B: Intermediate State Holder]
  visibility: NOT_CONFIRMED
  consumption: NOT_CONFIRMED
        |
        | S09-B02
        | VISIBILITY_GAP_RECORDED
        | LOCAL_NON_AWARENESS_NOT_CURRENT_VALIDITY
        v
[System C: Downstream Reliance Actor]
  attempts reliance using stale or partial state
        |
        | S09-B03
        | SPLIT_STATE_RELIANCE_ATTEMPT_RECORDED
        | CURRENT_REVALIDATION_REQUIRED
        v
[Failure Event]
  failure_mode: REVOCATION_VISIBILITY_GAP
```
