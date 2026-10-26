# Day-0 schema v0.2 repair ? 2026-10-26

Status: IN_FLIGHT local implementation; remote CI not yet established.

Base commit: a420dfd74881f87c90007f1ad1b3a894d767cb26.

## Scope

Adds a stronger Day-0 manifest schema, synthetic validation fixtures,
a separately named schema-bundle validator, and a dedicated CI workflow.
Clarifies the existing integrated validation in the reviewer-facing document.
Configures temporary freshness-test repositories to avoid automatic
line-ending conversion. The freshness checker's detection rules are unchanged.

The v0.2 fixture is synthetic test material, not a newly executed or resealed
Day-0 packet. The original schema, packet, and frozen v0.1 validator remain
preserved.

## Observed local results

User-supplied execution records report:
- Initial integrated validation: 47/47.
- Successor schema tests: 18/18.
- Original Day-0 packet checks: 27/27.
- Initial full regression: 696 passed, 6 failed.
- After separating the frozen validator and correcting temporary-repository
  Git configuration: 31/31 targeted tests passed.

The initial integration changed a validator bound by the CSH freezes.
The repair restores that validator and places the new integration in v0.2.
Three initial freshness-test failures involved LF/CRLF byte differences.
The outstanding standing-accounting failure is addressed by explicit
in-flight entries for the two new governed files.

These observations summarize supplied logs; they do not constitute a new
execution. A complete post-accounting regression remains to be observed.

## Remaining boundaries

Schema conformance does not establish file existence, actual artifact hashes,
unique artifact paths, complete artifact populations, or semantic correctness.
The original CSH baseline and successor execution gates are unchanged.
No hosted access, corpus execution, independent review, or release admission
is established by this change.

## Evidence locations reported by the user

- Initial run: C:\N\fork-day0-checks-20261026-075445
- Targeted repair run: C:\N\fork-day0-repair-checks-20261026-081437

These are local locations, not repository-admitted evidence attachments.

## Post-accounting local verification

User-supplied terminal output for the post-accounting run reports:
- Standing freshness: PASS, zero errors.
- Full regression: 702 passed in 283.31 seconds.
- Diff formatting: exit code 0.

Evidence location: `C:/N/fork-day0-accounted-checks-20261026-081806`.

This supplements the earlier failed run and targeted repair results; it does
not replace them. Remote CI remains unobserved. CSH hosted-access and execution
standing remain unchanged.
