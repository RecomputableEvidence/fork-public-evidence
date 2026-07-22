# Newcomer Walkthrough Forms v0.1

Status: `DRAFT_USABILITY_INSTRUMENT`

Classification intent: usability observation form. Completing this form does not validate Fork, approve the coherence change, establish reviewer competence, create admission standing, or replace exact-head technical review.

## Use boundary

Run these walkthroughs with participants who have not been coached through the target route. Record misunderstandings, dead ends, execution barriers, and unfavorable outcomes with the same care as successful completion.

Use a participant code rather than unnecessary personal information.

---

# Session cover sheet

- Session ID:
- Participant code:
- Date and time:
- Facilitator:
- Repository URL:
- Tested branch or exact commit:
- Root README blob, if known:
- Participant's self-described Git/GitHub familiarity:
  - [ ] None
  - [ ] Basic
  - [ ] Moderate
  - [ ] Advanced
- Operating system:
- Browser:
- Shell:
- Git version:
- Python version:
- PowerShell version or availability:
- Was the participant given any navigation coaching before the timer started?
  - [ ] No
  - [ ] Yes — describe:

## Session integrity

- [ ] The exact tested head was recorded.
- [ ] The participant began at the root README.
- [ ] No answer or route was supplied during a timed task.
- [ ] Technical failures were preserved rather than converted into user error.
- [ ] The facilitator distinguished observation from interpretation.

---

# Walkthrough A — Explain Fork in under three minutes

## Task shown to participant

> Starting from the repository front page, explain in plain language what Fork is, what problem it addresses, and at least one thing it does not claim to do.

- Timer start:
- Timer stop:
- Elapsed time:
- Completed within 3:00?
  - [ ] Yes
  - [ ] No

## Participant response

> 

## Observable route

- First link clicked:
- Additional links clicked:
- Did the participant remain on the root README?
- Terms that caused hesitation:
- Dead ends or circular routes:

## Boundary comprehension

Did the response correctly distinguish Fork from:

- [ ] runtime control or authorization;
- [ ] truth validation;
- [ ] compliance certification;
- [ ] legal sufficiency;
- [ ] production-readiness approval;
- [ ] inherited institutional authority.

## Misreadings preserved

Record exact or near-exact wording of any overread:

> 

## Facilitator classification

- [ ] Completed without material overread
- [ ] Completed with correctable ambiguity
- [ ] Not completed in time
- [ ] Material authority or claim overread
- [ ] Route failure
- [ ] Other:

---

# Walkthrough B — Find and run a verifier in under five minutes

## Task shown to participant

> Find the primary public verification command, run it from the correct location, and explain what its result does and does not establish.

- Timer start:
- Timer stop:
- Elapsed time:
- Found command within 5:00?
  - [ ] Yes
  - [ ] No
- Attempted execution within 5:00?
  - [ ] Yes
  - [ ] No

## Execution record

- Exact commit tested:
- Command copied or typed:

```text

```

- Command changed from the documented form?
  - [ ] No
  - [ ] Yes — describe:
- Exit code:
- High-level result:
- JSON output used?
  - [ ] No
  - [ ] Yes
- Failure or access barrier:

## Interpretation record

Participant's explanation of a pass, failure, or inability to execute:

> 

Did the participant identify that a pass is bounded structural evidence only?

- [ ] Yes
- [ ] No
- [ ] Not assessed because execution did not occur

Did the participant mistakenly infer:

- [ ] truth;
- [ ] compliance;
- [ ] approval;
- [ ] authorization;
- [ ] safety;
- [ ] production readiness;
- [ ] whole-repository completeness;
- [ ] no residual risk.

## Platform distinction

- PowerShell available?
- Fallback route found if needed?
- Did the participant distinguish named-verifier execution from manual reconstruction?

## Facilitator classification

- [ ] PASS — route and interpretation completed within scope
- [ ] FAIL — documented route or command did not work as presented
- [ ] UNRESOLVED — cause of execution barrier not established
- [ ] NOT_CHECKED — participant did not attempt execution

The classification above applies only to this walkthrough task.

---

# Walkthrough C — Find an appropriate starter task in under ten minutes

## Facilitator setup

The route under test should expose `docs/coherence/front-door-routing-v0.1/STARTER_TASKS_v0_1.md` from the root contributor row and contributor role path. Do not reveal that destination or provide navigation coaching before or during the timer. Record failure to locate it as route evidence rather than participant error.

## Task shown to participant

> Find a bounded contribution or adversarial-testing task that matches your skills. Explain what files or surfaces it would affect, what evidence you would produce, and what you must not change.

- Timer start:
- Timer stop:
- Elapsed time:
- Task identified within 10:00?
  - [ ] Yes
  - [ ] No

## Selected task

- Starter-task ID, if found:
- Task title or proposed task:
- Route used to find it:
- Why it matches the participant:
- Expected effort:
- Required tools or environment:
- Files or surfaces in scope:
- Files or surfaces excluded:
- Evidence required for completion:
- Expected checker or review path:
- Admission effect:
- Provider-call effect:
- Experiment-execution effect:

## Contribution-boundary comprehension

Did the participant understand that they should:

- [ ] begin from an exact base;
- [ ] preserve the original failure or negative evidence;
- [ ] keep the PR draft when files change;
- [ ] avoid combining unrelated change classes;
- [ ] state non-claims;
- [ ] avoid interpreting merge or CI as admission where a separate act is required.

## Observed friction

- Could the participant find the starter-task register without entering an undifferentiated docs directory?
- Could the participant select a real task without inventing one?
- Was the task bounded enough to begin?
- Were prerequisites visible?
- Was a prohibited change explicit?
- Missing information:

## Facilitator classification

- [ ] Suitable bounded task found
- [ ] Task found but scope ambiguous
- [ ] No task found
- [ ] Proposed task would mutate protected standing
- [ ] Contribution surface absent or incomplete

---

# Walkthrough D — Identify boundaries and non-claims at a glance

## Task shown to participant

> Without running code, identify what Fork does not claim to do and distinguish PASS, FAIL, UNRESOLVED, and NOT_CHECKED.

- Observation window used:
- Time to first correct non-claim:
- Time to distinguish all four statuses:

## Non-claims identified by participant

1. 
2. 
3. 
4. 

## Status definitions given by participant

- PASS:
- FAIL:
- UNRESOLVED:
- NOT_CHECKED:

## Visual and language accessibility

- Were full status labels visible?
- Was meaning dependent on color?
- Were definitions reachable in one click?
- Did any success presentation obscure a blocked, unresolved, or not-checked dimension?
- Could the participant distinguish lifecycle standing such as `CANDIDATE_NOT_ADMITTED` from a verification result?

## Facilitator classification

- [ ] Boundaries and statuses legible at a glance
- [ ] Boundaries found but status distinctions unclear
- [ ] Statuses found but non-claims unclear
- [ ] Material success overread
- [ ] Not enough information on front door

---

# Cross-session observation log

Use one row per observed event. Do not collapse repeated misunderstandings into one favorable aggregate.

| Session ID | Task | Elapsed time | Observed event | Evidence or participant wording | Classification | Proposed correction | Correction owner | Retest required |
|---|---|---:|---|---|---|---|---|---|
| | | | | | | | | |

## Allowed classifications

- `ROUTE_SUCCESS`
- `DEAD_END`
- `BROKEN_LINK`
- `TERM_AMBIGUITY`
- `STATUS_OVERREAD`
- `AUTHORITY_OVERREAD`
- `MISSING_PREREQUISITE`
- `PLATFORM_BARRIER`
- `COMMAND_FAILURE`
- `UNRESOLVED_CAUSE`
- `NOT_CHECKED`
- `OTHER_PRESERVED_OBSERVATION`

---

# Session disposition

- What succeeded:
- What failed:
- What remained unresolved:
- What was not checked:
- Negative evidence preserved at:
- Proposed corrections:
- Corrections that would require a separate normative or implementation PR:
- Does this session authorize merge?
  - [ ] No
- Does this session admit or publish the coherence surface?
  - [ ] No
- Does this session change Fork's claims, authority, experiment standing, or historical record?
  - [ ] No

## Facilitator attestation

> This record reports observed usability behavior at the identified repository head. It is not an endorsement, certification, approval, admission act, authority transfer, or claim that the participant independently verified every referenced artifact.
