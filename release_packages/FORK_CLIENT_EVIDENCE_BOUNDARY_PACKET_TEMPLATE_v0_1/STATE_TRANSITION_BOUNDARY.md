# State Transition Boundary

## Purpose

This file defines workflow states that must remain separate in the evidence boundary.

Fork should not collapse states that have different institutional meanings.

## Required state distinctions

| State | Included? | Source system | Evidence artifact | Notes |
|---|---|---|---|---|
| Requested | `[YES / NO / UNKNOWN]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` |
| AI generated | `[YES / NO / UNKNOWN]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` |
| Human reviewed | `[YES / NO / UNKNOWN]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` |
| Modified | `[YES / NO / UNKNOWN]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` |
| Approved | `[YES / NO / UNKNOWN]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` |
| Denied | `[YES / NO / UNKNOWN]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` |
| Escalated | `[YES / NO / UNKNOWN]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` |
| Executed | `[YES / NO / UNKNOWN]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` |
| Remediated | `[YES / NO / UNKNOWN]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` |
| Reported | `[YES / NO / UNKNOWN]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` |

## Collapsed-state risks

List states that the client system collapses or fails to separate.

`[FORK_TO_COMPLETE / NONE / UNKNOWN]`

## Required evidence states

Select all required:

- `[ ] PASS`
- `[ ] FAIL`
- `[ ] NOT_CHECKED`
- `[ ] PARTIAL`
- `[ ] STALE_CONTEXT`
- `[ ] OUT_OF_SCOPE`
- `[ ] SOURCE_UNAVAILABLE`
- `[ ] UNKNOWN`

## Boundary decision

Select one:

- `[ ] STATE_TRANSITION_BOUNDARY_DRAFTED`
- `[ ] STATE_TRANSITION_BOUNDARY_REQUIRES_REVIEW`
- `[ ] STATE_TRANSITION_BOUNDARY_BLOCKED`
- `[ ] STATE_TRANSITIONS_UNKNOWN`

Reason:

`[FORK_TO_COMPLETE]`