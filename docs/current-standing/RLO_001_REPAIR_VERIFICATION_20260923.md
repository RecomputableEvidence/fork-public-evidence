# RLO-001 verification and standing repair

Verified against main `4e80ee7f33ac890c4101d741cf3da93522d2fd33` and PR #165 head `e3eabe49a7aa4eb9ec3fa451e16bae671fada19b`. Scope: the attached assessment's RLO-001 preservation → standing successor → bounded freshness sequence, plus the directly verified CI dependency mismatch.

## Findings

| Verification point | Disposition |
| --- | --- |
| Canonical standing route still v0.7 despite PR #164 | Confirmed from pinned bytes |
| Current structural checker can pass despite lag | Reproduced: 11/11 pass before repair |
| PR #163/#164 changed CSH-S001 state | Confirmed by Git history and the admitted gate/freeze records |
| Does the PR #160 base label mean PR #161 is unrepresented? | Not adopted: v0.7 already incorporates its corrections despite naming PR #160 as base |
| PR #165 Mistral/OpenAI responses | Confirmed as recorded branch evidence; open/unmerged via GitHub API; no independent provider rerun |
| Do the narrower freezes establish a fully frozen experiment? | Not adopted: narrower freezes exist, but G06/G07/G08/G11 remain unsatisfied |
| Evidence CI and admission gate use different dependency specifications | Confirmed and repaired using requirements-proof-surface.txt in both |
| Broad AI-speed thesis, actual reviewer reliance, or downstream harm | Not established by this bounded observation |

The public-site redesign, citation/licensing choices, provider replacement, and comparative experiment execution are outside this preservation-and-standing repair. No licensing terms, credentials, provider selections, frozen experiments, or closed historical objects are changed.

## Implementation

1. Preserve RLO-001, exact source copies, source identities, SHA-256 manifest, and pre-repair checker output in commit `55fb18508824a4a4efe6651dc01326506686f200`.
2. Add v0.8 as predecessor-plus-delta, bind v0.7 unchanged, and update the canonical routing surfaces.
3. Add explicit recognized-path transition accounting to the required admission workflow; remove path filters from the standing workflow.
4. Preserve admitted, in-flight, blocked, and partial-freeze distinctions. Do not convert PR #165 access errors into comparative results.

## Local verification

- Complete regression suite: **681 passed**, including 10 freshness/preservation regression cases (Python 3.12, repository dependency bounds).
- Current-state routing: **11/11 passed** after repair.
- Recognized transition accounting and RLO preservation: **PASS**.
- Historical v0.1/v0.2/v0.3/v0.4 standing checkers: **PASS**.
- Frozen CSH execution instrumentation: **PASS**.
- Fork Meta-Evidence package and integrated registry: **PASS**.
- Lens Shift, UEM, and Stacked Cadence admission verifiers: **PASS**.
- Governed LF and Git whitespace checks: **PASS**.
- No diff to original `admissions/`, `docs/experiments/`, or predecessor v0.1–v0.7 registers.

GitHub CI is a separate execution record; this note reports local results only. Merge should preserve the observation commit's ancestry; squash would discard a required preservation coordinate. Passing freshness accounting does not establish semantic completeness or authorize execution.

## Hosted Windows finding and additive repair

On initial PR #166 head `88834443c74f1f38f5012bf59aa9f21d4df0ac19`, the Windows proof-surface job `107052416949` completed with **679 passed, 2 failed**. Both failures arose when the new verifier attempted `git show` on a deeply nested preserved source; the second failure could not reach its intended assertion because that lookup failed first. Ubuntu and the required admission gate passed at that head.

A subsequent code-only lookup repair resolves paths from the committed tree and reads the resulting blob ID with `git cat-file blob`, avoiding Git's path/revision disambiguation. RLO-001, its manifest, all source copies, and v0.8 remain unchanged. Later CI results do not erase this initial cross-platform failure.
