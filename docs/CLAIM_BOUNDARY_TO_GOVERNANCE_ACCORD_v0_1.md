From Claim Boundary to Governance Accord v0.1

Status
Doctrine note.

This document explains the architectural progression from claim boundary preservation to governance-system interoperability.

Purpose
Fork's claim-boundary work is not intended to replace governance systems.
It is intended to preserve the evidentiary boundary between what was claimed, what was not claimed, what was relied on, what remained unresolved, and who remained locally accountable.

The progression is:
Claim Boundary Contract
→ Claim Inheritance Checker
→ Claim Consumption Event Contract
→ CCEC Governance Interoperability Profile

Each layer addresses a distinct failure mode.

1. Claim Boundary Contract
A Claim Boundary Contract records what a source artifact claims, does not claim, and leaves unresolved.
It answers:
What did this artifact actually assert?
It also preserves non-claims so that later systems cannot silently reinterpret a narrow source artifact as a broad assurance artifact.
A Claim Boundary Contract does not decide whether the source artifact is true, safe, compliant, legally sufficient, policy-satisfying, or institutionally authorized.

2. Claim Inheritance Checker
The Claim Inheritance Checker addresses downstream semantic expansion.
It answers:
Did a downstream artifact improperly inherit or expand a claim that the source artifact did not make?
This is the transitivity problem.
Examples of improper inheritance include treating:
structural integrity as truth;
human review as legal sufficiency;
policy attachment as compliance;
evidence availability as risk acceptance;
a bounded review as institutional authorization.
The checker does not approve or reject the underlying decision. It detects structural claim-boundary problems in synthetic controlled-pilot examples.

3. Claim Consumption Event Contract
A Claim Consumption Event Contract records receiving-side reliance.
It answers:
What did the receiving workflow treat the bounded source artifact as sufficient for?
The CCEC makes local reliance inspectable by recording:
the consumed source artifact;
the receiving workflow;
the relied claims;
the preserved non-claims;
the unresolved gaps;
the boundary effect;
the local reliance decision;
the decision owner;
the limitations that prevent the event from becoming an approval, truth, safety, compliance, legal sufficiency, policy satisfaction, risk acceptance, or authority oracle.
This does not eliminate claim consumption.
It eliminates silent, unbounded, non-accountable claim consumption.

4. CCEC Governance Interoperability Profile
A CCEC Governance Interoperability Profile defines how a surrounding governance system may reference a CCEC.
It answers:
What may travel into the surrounding governance system without silently transferring authority?
This is the accord layer.
A CCEC may be useful to a GRC register, audit evidence system, policy register, risk register, legal review queue, model governance system, evidence management system, procurement workflow, vendor-risk workflow, insurance workflow, or underwriting workflow.
But that usefulness creates a new risk: the external system may flatten a bounded CCEC reference into an approval-like or compliance-like status.
The interoperability profile prevents that collapse by making permitted and prohibited mappings explicit.

Accord principle
A contract unifies two or more parties in mutual accord.
A CCEC Governance Interoperability Profile defines the accord between:
the bounded CCEC record;
the external governance system;
the local owner accountable for downstream action;
the preserved non-claims;
the unresolved gaps.
The profile does not make Fork the governance system.
It does not make the external governance system a Fork verifier.
It defines the bounded field-level relationship between them.

What may travel
The following may travel as bounded references:
evidence reference;
boundary record reference;
local reliance record;
unresolved gap reference;
non-claim reference;
decision owner reference;
boundary effect reference;
source artifact reference;
receiving context reference.
These references are evidentiary.
They are not authority transfers.

What must not travel
The following must not travel by mapping:
approval status;
truth status;
safety status;
compliance status;
legal sufficiency status;
institutional authorization status;
policy satisfaction status;
risk acceptance status;
authority transfer;
claim expansion by mapping;
automated control decision.
A governance system may make its own local decision.
It may not inherit that decision from the CCEC.

Why this matters
Institutional AI governance is increasingly compositional.
Artifacts move across teams, tools, workflows, vendors, control systems, audit systems, risk systems, legal review channels, and executive reporting layers.
Without explicit claim-boundary preservation, a bounded artifact can become broader assurance than anyone actually provided.
Without claim-consumption recording, a receiving workflow can rely on an artifact without making that reliance inspectable.
Without interoperability constraints, a governance system can absorb a bounded reliance record and convert it into an approval-like status.
Fork's answer is not to control the runtime.
Fork's answer is to preserve the boundary.

Canonical progression
CBC:
what the source artifact claims and does not claim

Claim Inheritance Checker:
whether downstream text improperly expands or inherits claims

CCE / CCEC:
what the receiving workflow relied on locally

CCEC Governance Interoperability Profile:
how surrounding governance systems may reference the bounded reliance record without inheriting authority

Non-claims
This doctrine note does not claim that Fork determines:
truth;
safety;
compliance;
legal sufficiency;
institutional authority;
policy satisfaction;
risk acceptance;
production readiness;
governance adequacy.
It describes a structural evidence-boundary progression.

Canonical summary
Evidence may travel.
Non-claims and unresolved gaps must travel with it.
Reliance remains local.
Authority remains local.
A governance accord allows surrounding systems to reference bounded records without absorbing powers the records never claimed.