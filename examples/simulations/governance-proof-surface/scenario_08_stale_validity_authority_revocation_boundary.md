# Scenario 08 — Stale Validity / Authority Revocation Boundary

## Scenario ID

`SCENARIO_08_STALE_VALIDITY_AUTHORITY_REVOCATION_BOUNDARY`

## Summary

A bounded claim, authority context, policy reference, evidence basis, or role permission was valid at an earlier time.

Later, one or more validity conditions changed:

- the authority was revoked;
- the role changed;
- the time window expired;
- the policy version changed;
- the evidence basis was superseded;
- the allowed purpose narrowed;
- the operating environment changed.

A downstream actor attempts to reuse the prior Fork-preserved record as if the earlier validity state remained current.

Fork records that prior validity does not establish current validity. It preserves the stale-validity boundary and required revalidation.

## Systems

### System A — Prior Review Authority

Creates or relies on a bounded record during an earlier valid window.

### System B — Validity Change Source

Records a later validity-changing event such as revocation, expiry, policy change, evidence supersession, or role change.

### System C — Downstream Reliance Actor

Attempts to rely on the prior record after the validity state changed.

## Boundary under test

```text
valid at T1
≠ valid at T2
```

Scenario 08 tests whether prior validity is silently promoted into current validity after revocation, expiry, supersession, or narrowing.

## Expected failure mode

`STALE_VALIDITY_RELIANCE_ATTEMPT`

The downstream actor treats the earlier record as if it still supports current authority, policy satisfaction, evidence sufficiency, approval eligibility, compliance posture, legal sufficiency, external acceptance, or execution eligibility.

## Fork result

Fork records the stale-validity reliance attempt and preserves required revalidation.

Fork does not decide whether the earlier claim was true, whether the current claim is valid, whether the revocation was correct, whether an external authority should accept the record, or whether execution is allowed.

## Verification

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_08_stale_validity_authority_revocation_v0_1.ps1
```
