# Open-candidate coordinate snapshot — 2026-08-05

This append-only candidate records the observed coordinates and bounded roles of
the eight open draft pull requests that were examined on 2026-08-05.

It is a temporal checkpoint, not a merge queue. An open pull request, a passing
check, a review, GitHub mergeability, or later chronology does not confer
admission, merge authorization, successor standing, authority, or execution
permission.

The source analysis described five governance lanes while enumerating six. This
record preserves that discrepancy and uses the computable count of six:

1. foundational correction;
2. exterior evidence;
3. interoperability experiment;
4. proof governance;
5. meta-evidence research; and
6. pre-pilot implementation.

The snapshot binds the exact governed tip and exact pull-request base and head
coordinates. It does not query GitHub at verification time. Later changes to a
pull request require a separate append-only successor snapshot; they do not
rewrite this observation.

On reviewed merge to `preservation/clean-continuance-v0.1`, the maximum standing
available to this record is:

`OPEN_CANDIDATE_COORDINATE_SNAPSHOT_ADMITTED_NO_SOURCE_PR_EFFECT`

Before reviewed merge, its standing remains:

`OPEN_CANDIDATE_COORDINATE_SNAPSHOT_CANDIDATE_NOT_ADMITTED`

The snapshot does not modify, admit, reject, supersede, close, merge, retarget,
or authorize any source pull request. It does not modify `main`, the governed
preservation ref, or repository settings merely by existing on its candidate
branch. Branch-protection settings remain a separate administrative act that
requires separate authorization.

## Recompute

```bash
python tools/check_open_candidate_coordinate_snapshot_v0_1.py --json
python -m pytest tests/test_open_candidate_coordinate_snapshot_v0_1.py -q
```

A conforming checker result establishes only internal conformance of the
committed snapshot to its declared coordinate and non-inheritance contract. It
does not establish that the observed pull-request state remains current.
