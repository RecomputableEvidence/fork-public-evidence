# CSH successor hardening — 2026-10-26

Status: IN_FLIGHT implementation, no hosted execution or experimental promotion.

## Source continuity

Based on main `a420dfd74881f87c90007f1ad1b3a894d767cb26` plus the exact 12
changed-source files supplied in the user's review package, reported as local
commit `d970ebb0f579ef7182cf72a2c30dbc642894b957`. That local commit object was
not supplied; importing its files does not recreate its commit identity.
The Day-0 history and its earlier 696-pass/6-fail run remain distinguished from
the user's later 702-pass local run. The current change adds CSH hardening.

## Preserved finding and reproduction

`CSH_OFFLINE_FINDINGS_20261026.json` preserves 14 mocked predecessor preflight
observations, exact mock response bodies, predecessor code hashes, and a
packet-tamper observation. Reproduce with:

```
python scripts/reproduce_csh_offline_findings_v0_2.py --check
```

No provider requests occur. The predecessor accepts unrelated JSON, a length
finish, and prefixed model names; a top-level JSON array raises AttributeError.
The predecessor packet checker accepts a whitespace-tampered projection when
its materialization manifest is unchanged. These observations do not show
provider failure or a result for the experimental hypothesis.

## Successor contract

`tools/preflight_csh_s001_receivers_v0_2.py` requires HTTP 200, a JSON object,
one choice object, assistant text, finish_reason=stop, parsed content exactly
{"preflight":"ok"}, and a returned identity exactly in PERMITTED_MODELS.
Duplicate JSON members and non-JSON constants are rejected. Model policy begins
with each predecessor configuration's exact requested identity only. No substring
matching or automatically inferred aliases. Provider aliases can be considered
only through an explicit subsequent policy revision. Exact identity matching
is a returned-string check, not model attestation.

The successor CLI defaults to NOT_EXECUTED/exit 2. Live use requires explicit
--live, --provider, and a fresh --output-dir. Missing credentials are non-success.
Requests have no CSH corpus; there are no automatic retries. Exact request and
received response bytes are preserved locally, including HTTP-error bodies.
Request authorization headers are not written to receipts. Live raw responses
require inspection before publication; none are produced by this repair.

`tools/check_csh_s001_packet_binding_v0_2.py` recomputes actual SHA-256 values,
checks them against both manifest declarations and the preserved binding, rejects
duplicate/missing scenarios and unexpected paths, rejects symlinks, and checks
exact file population. Coordinated changes to bytes and manifest declarations
still fail against the preserved binding. It does not authenticate a modified
binding file, concurrent filesystem changes, or delivery to any receiver.

## CI and accounting

A new offline CI workflow exercises both successors, the recorded findings,
packet generation, Day-0 validation, and change accounting on Linux and Windows.
The predecessor's automatic PR-hosted observation job is disabled: opening a PR
must not send provider requests using repository secrets. Its explicit manual
legacy hosted workflow is preserved; it does not establish successor acceptance.
Old preflight and packet checker source bytes remain unchanged.

New governed tools are accounted as IN_FLIGHT without changing the coverage
base or deleting prior ledger entries. CSH G06/G07/G08/G11 remain unresolved.
Remote CI results must be read at the published candidate commit, not inferred
from the existence of workflow files or local passes.

## Local validation

773/773 tests passed locally (71 new hardening tests). The uploaded packet set
passed 20/20 successor checks. Raw full-suite output and source hashes are
preserved in `csh-hardening-local-20261026/`. Remote CI is pending publication.
