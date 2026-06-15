# State Transition Map

## Purpose

This file identifies workflow states that must remain separate.

Fork should not collapse states that have different institutional meanings.

For example:

- requested is not generated
- generated is not reviewed
- reviewed is not approved
- approved is not executed
- executed is not legally sufficient
- verified is not correct
- not checked is not pass

## State table

| State | Exists in workflow? | Recorded where? | Evidence available? | Notes |
|---|---|---|---|---|
| Requested | `[YES / NO / UNKNOWN]` | `[CLIENT_TO_COMPLETE / UNKNOWN]` | `[YES / NO / PARTIAL / UNKNOWN]` | `[CLIENT_TO_COMPLETE]` |
| AI generated | `[YES / NO / UNKNOWN]` | `[CLIENT_TO_COMPLETE / UNKNOWN]` | `[YES / NO / PARTIAL / UNKNOWN]` | `[CLIENT_TO_COMPLETE]` |
| Human reviewed | `[YES / NO / UNKNOWN]` | `[CLIENT_TO_COMPLETE / UNKNOWN]` | `[YES / NO / PARTIAL / UNKNOWN]` | `[CLIENT_TO_COMPLETE]` |
| Modified | `[YES / NO / UNKNOWN]` | `[CLIENT_TO_COMPLETE / UNKNOWN]` | `[YES / NO / PARTIAL / UNKNOWN]` | `[CLIENT_TO_COMPLETE]` |
| Approved | `[YES / NO / UNKNOWN]` | `[CLIENT_TO_COMPLETE / UNKNOWN]` | `[YES / NO / PARTIAL / UNKNOWN]` | `[CLIENT_TO_COMPLETE]` |
| Denied | `[YES / NO / UNKNOWN]` | `[CLIENT_TO_COMPLETE / UNKNOWN]` | `[YES / NO / PARTIAL / UNKNOWN]` | `[CLIENT_TO_COMPLETE]` |
| Escalated | `[YES / NO / UNKNOWN]` | `[CLIENT_TO_COMPLETE / UNKNOWN]` | `[YES / NO / PARTIAL / UNKNOWN]` | `[CLIENT_TO_COMPLETE]` |
| Executed | `[YES / NO / UNKNOWN]` | `[CLIENT_TO_COMPLETE / UNKNOWN]` | `[YES / NO / PARTIAL / UNKNOWN]` | `[CLIENT_TO_COMPLETE]` |
| Remediated | `[YES / NO / UNKNOWN]` | `[CLIENT_TO_COMPLETE / UNKNOWN]` | `[YES / NO / PARTIAL / UNKNOWN]` | `[CLIENT_TO_COMPLETE]` |
| Reported | `[YES / NO / UNKNOWN]` | `[CLIENT_TO_COMPLETE / UNKNOWN]` | `[YES / NO / PARTIAL / UNKNOWN]` | `[CLIENT_TO_COMPLETE]` |

## Collapsed states

List any states that are collapsed in existing systems.

Examples:

- approved and executed recorded as one event
- AI recommendation and human decision stored together
- review and approval not separated
- policy state not captured at decision time

`[CLIENT_TO_COMPLETE / NONE / UNKNOWN]`

## Required Fork evidence states

Select all likely needed:

- `[ ] PASS`
- `[ ] FAIL`
- `[ ] NOT_CHECKED`
- `[ ] PARTIAL`
- `[ ] STALE_CONTEXT`
- `[ ] OUT_OF_SCOPE`
- `[ ] SOURCE_UNAVAILABLE`
- `[ ] UNKNOWN`

## State-transition risks

`[CLIENT_TO_COMPLETE / NONE / UNKNOWN]`