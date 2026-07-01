# Outreach Path Assignment Guide v0.1

## Purpose

This guide helps assign each outreach target to the correct Fork external path.

The goal is to avoid sending a generic pitch.

Each target should receive one path:

- Public reviewer
- Advisor / design partner
- Enterprise bounded workflow PoV

## Path assignment decision tree

### Step 1 -- Is the person being asked to critique the public evidence surface?

Assign:

`PUBLIC_REVIEWER`

Use when the person is likely to care about:

- technical reproducibility;
- evidence preservation;
- governance semantics;
- open-source credibility;
- verifier behavior;
- white-paper argument;
- claim-boundary rigor.

Primary ask:

Can you review whether the evidence boundary and recomputation path hold?

Do not ask for purchase, procurement, or deployment.

### Step 2 -- Is the person being asked to pressure-test enterprise fit?

Assign:

`ADVISOR_DESIGN_PARTNER`

Use when the person is likely to care about:

- buyer psychology;
- operational feasibility;
- workflow fit;
- governance adoption;
- legal-tech or GRC integration;
- design-partner signal;
- enterprise failure modes.

Primary ask:

Can you help stress-test whether this framing holds up in real workflows?

Do not lead with price.

### Step 3 -- Is the person close to an enterprise budget, workflow, or risk owner?

Assign:

`ENTERPRISE_POV`

Use when the person is likely to care about:

- AI risk exposure;
- legal defensibility;
- audit evidence;
- compliance reconstruction;
- model risk;
- enterprise workflow review;
- paid PoV scoping.

Primary ask:

Can we assess whether one bounded AI-assisted workflow is a fit for a 90-day PoV?

Do not pitch platform rollout.

## Role-to-path mapping

| Role / Persona         | Default path            | Notes                                  |
|------------------------|-------------------------|----------------------------------------|
| AI governance researcher | Public reviewer       | Ask for critique, not purchase.        |
| Open-source assurance reviewer | Public reviewer | Anchor on verifier and non-claim boundary. |
| Legal-tech founder     | Advisor / design partner | Ask where buyer framing breaks.      |
| GRC product leader     | Advisor / design partner | Ask about integration semantics and misread risk. |
| Former GC / CCO        | Advisor / design partner | Ask whether the buyer frame is legible. |
| Current GC / CCO       | Enterprise PoV         | Anchor on bounded reconstruction and exposure control. |
| Head of AI Risk        | Enterprise PoV         | Anchor on one workflow and reviewability. |
| Model risk leader      | Enterprise PoV         | Anchor on evidence handoff and reconstruction. |
| Audit innovation lead  | Enterprise PoV         | Anchor on what can be reconstructed later. |
| CTO / CISO sponsor     | Enterprise PoV         | Anchor on read-only, out-of-band, fail-open posture. |

## Trigger examples

Use triggers to avoid cold generic outreach.

Examples:

- published AI governance policy;
- launched internal GenAI program;
- discussed AI auditability publicly;
- posted about model risk;
- mentioned compliance evidence gaps;
- investing in legal-tech / GRC tooling;
- AI incident or regulatory pressure;
- procurement of AI governance tooling;
- new AI risk leadership role;
- public AI principles without technical evidence path.

## Asset selection by path

### Public reviewer

Send one of:

- `REVIEWER_QUICK_START_v0_1.md`
- `docs/REVIEWER_START_HERE_v0_1.md`
- `docs/VERIFICATION_COMMANDS_v0_1.md`
- `white-paper/Reconstructive_Fidelity_in_the_Age_of_AI_v1_0.md`

### Advisor / design partner

Send one of:

- `docs/WORKED_EXAMPLE_VENDOR_RISK_AI_ASSISTED_DECISION_RECORD_v0_1.md`
- `docs/ENTERPRISE_DISCOVERY_POV_PACKET_v0_1.md`
- `docs/BOUNDED_WORKFLOW_POV_SCOPE_TEMPLATE_v0_1.md`
- `docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md`

### Enterprise PoV

Send one of:

- `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/ENTERPRISE_DISCOVERY_POV_v0_1.md`
- `docs/ENTERPRISE_DISCOVERY_POV_PACKET_v0_1.md`
- `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/NEXT_STEPS.md`
- `docs/BOUNDED_WORKFLOW_POV_SCOPE_TEMPLATE_v0_1.md`

## Path misassignment risks

| Mistake                                   | Risk                               |
|-------------------------------------------|------------------------------------|
| Sending enterprise PoV material to a researcher | Looks salesy; lowers credibility. |
| Sending full repo to a buyer first        | Too much cognitive load.           |
| Asking buyer for review                   | Avoids commercial motion.          |
| Asking advisor for purchase               | Burns relationship.                |
| Asking reviewer for endorsement           | Looks premature.                   |
| Leading with compliance                   | Invites overclaim scrutiny.        |
| Leading with price before workflow        | Makes scope feel arbitrary.        |

## Required target fields

Each target entry should include:

- Target:
- Organization:
- Role hypothesis:
- Path:
- Trigger:
- Why now:
- Why Fork:
- Asset anchor:
- Message variant:
- Status:
- Next action:

## Status values

Use these exact status values:

- IDENTIFIED
- RESEARCHING
- READY_TO_SEND
- SENT
- FOLLOWED_UP
- REPLIED_CURIOUS
- REPLIED_NOT_NOW
- REPLIED_WRONG_PERSON
- INTRO_REQUESTED
- MEETING_BOOKED
- MEETING_HELD
- QUALIFIED
- DISQUALIFIED
- CLOSED_NO_RESPONSE

## Reply signal values

Use these exact reply signal values:

- NO_RESPONSE
- CURIOSITY
- ASKED_FOR_REPO
- ASKED_FOR_EXAMPLE
- ASKED_FOR_PRICE
- ASKED_FOR_SECURITY
- ASKED_FOR_LEGAL
- ASKED_FOR_INTEGRATION
- REFERRED_TO_OTHER_PERSON
- NOT_RELEVANT
- TOO_EARLY
- PILOT_INTEREST

## Assignment rule

A target is first-wave eligible only when all are true:

- Path assigned
- Trigger identified
- Asset anchor selected
- Low-risk ask defined
- Non-claim risk understood
- Priority score >= 15
