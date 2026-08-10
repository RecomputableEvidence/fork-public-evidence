# Fork CAD Review Sequence v0.1

Status: `PROCEDURE_CANDIDATE_NOT_ADMISSION`

## Stage 1 — Known technical reviewer

Use a reviewer who has already demonstrated artifact-level recomputation and understands Fork's non-claim, exact-head, and append-only boundaries.

Purpose:

- detect packet defects quickly;
- verify the private source digests;
- run the checker and tests correctly;
- identify repository-specific boundary violations;
- return actionable corrections.

The reviewer must not receive an expected verdict beyond the declared review questions.

## Stage 2 — Candidate amendment

If Stage 1 finds defects:

- preserve the review unchanged;
- amend the candidate branch append-only where possible;
- record any withdrawn or superseded candidate language;
- obtain a new exact head;
- rerun all workflows;
- do not reuse the prior verdict as approval of the amended head.

## Stage 3 — New independent reviewer

After the packet is stable, use a reviewer with limited or no prior Fork exposure.

Purpose:

- test whether the method is understandable without oral history;
- detect hidden assumptions familiar reviewers may overlook;
- assess whether source roles and non-claims travel cleanly;
- challenge favorable interpretations and terminology.

Do not select this reviewer primarily for publicity. Review competence and independence control the evidentiary value; audience reach is a separate benefit.

## Stage 4 — Reconciliation without consensus laundering

Compare the two reviews at claim level:

- same source package?
- same exact head?
- same claim boundaries?
- same source-role interpretation?
- same verdict or preserved disagreement?

Do not average or collapse divergent findings into consensus. Preserve each review and any adjudication separately.

## Stage 5 — Admission decision

Only after exact-head review is complete should the maintainer decide whether to:

- amend and rereview;
- retain privately;
- close as not reproduced;
- merge the review surface without admission;
- perform a separate append-only admission act.

Merge, admission, publication, outreach, and endorsement remain non-equivalent.
