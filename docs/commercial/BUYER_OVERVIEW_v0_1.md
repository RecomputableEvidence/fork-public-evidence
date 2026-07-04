# Fork

## Buyer Overview v0.1

**Recomputable Evidence for AI-Assisted Workflows**

---

## The problem

Organizations are rapidly adopting AI to produce business artifacts that influence decisions.

These artifacts may include vendor risk assessments, compliance summaries, audit documentation, leadership briefs, policy drafts, procurement recommendations, customer communications, and technical analyses.

Most AI governance solutions focus on governing model behavior, enforcing policy, monitoring runtime activity, or evaluating model performance.

A different problem emerges after an artifact is produced:

**Can a later reviewer independently reconstruct the basis on which this AI-assisted artifact became eligible for institutional reliance?**

If this artifact were challenged tomorrow by audit, legal, or a regulator, could the organization show what was actually relied upon, and what was not?

In many organizations, the answer is incomplete. Important context is often lost as artifacts move between people, teams, and systems.

Without this record, organizations often cannot answer basic audit or legal questions without reconstructing events from fragmented logs, emails, document versions, and recollection, introducing delay, uncertainty, and conflicting interpretations of what was actually relied upon.

---

## Introducing Fork

Fork is evidence-boundary infrastructure for AI-assisted workflows.

Fork does not govern model behavior. It preserves the evidence required to reconstruct reliance.

Fork creates tamper-evident, recomputable records that preserve the governance context surrounding AI-assisted artifacts.

Rather than determining whether an artifact is correct, compliant, or approved, Fork preserves enough context for later reviewers to independently reconstruct what occurred.

Fork records can preserve:

- workflow context
- AI-assisted outputs
- human review context
- evidence references
- claim boundaries
- explicit non-claims
- transition records across workflow handoffs
- CISO / security leadership
- downstream reliance events
- structural verification status

Structural verification means confirming that the preserved record is complete, internally consistent, and untampered within Fork's defined verification scope.

The result is a bounded evidence record that remains independently verifiable after the workflow continues.

---

## Why this matters

Organizations increasingly rely on AI-generated work long after the original interaction has ended.

Downstream reviewers frequently need to answer questions such as:

- What evidence supported this artifact?
- What claims were actually made?
- Which claims were intentionally excluded?
- What authority context applied?
- What changed during review?
- Did later systems preserve or expand the original claim?
- Can the record still be independently verified?

Fork is designed to preserve this reconstruction context without becoming the decision maker.

---

## What Fork is

Fork preserves the governance boundary surrounding AI-assisted work.

Fork helps organizations create recomputable evidence records that support later inspection and independent review.

Fork is designed to complement existing governance, compliance, security, and workflow systems rather than replace them.

---

## What Fork is not

Fork is not:

- a prompt firewall
- a runtime policy engine
- a model gateway
- a model evaluation platform
- an approval workflow
- a compliance automation platform
- a legal opinion
- a truth certification system

Fork does not determine whether reliance is justified.

Fork preserves the evidence required for others to evaluate that question.

---

## Example workflow

An organization uses AI to prepare a vendor-risk assessment.

A human reviewer edits the draft before it is shared with procurement and legal.

Fork can preserve:

- what was requested
- what AI produced
- what evidence was referenced
- what the reviewer accepted or modified
- what remained outside scope
- what transitioned downstream
- whether the resulting record still structurally verifies

The procurement process remains unchanged.

Fork preserves the evidence boundary surrounding the transition.

---

## Initial buyers

Fork is designed for organizations where AI-assisted artifacts influence operational decisions.

Typical stakeholders include:

- Chief Compliance Officers
- General Counsel
- Chief Risk Officers
- Internal Audit
- AI Governance teams
- Vendor Risk teams
- Enterprise Architecture
- Public-sector governance programs

---

## Why Fork is different

Most AI governance platforms focus on governing models.

Fork focuses on preserving the evidence boundary surrounding AI-assisted reliance.

Its primary concern is not model behavior.

Its primary concern is preserving the information needed to independently reconstruct why an AI-assisted artifact became part of institutional action.

---

## Current status

Fork is an active research and engineering project.

The public evidence repository includes executable specifications, validation tooling, governance simulations, and independently verifiable proof surfaces demonstrating the project's architectural approach.

The current focus is collaboration with design partners interested in evaluating reconstructable evidence for AI-assisted workflows.

---

## Discussion

Fork is seeking conversations with organizations interested in improving the reconstructability of AI-assisted decision workflows.

The objective is to understand where later reviewers need stronger evidence of what crossed a governance boundary, what remained in scope, and what requires fresh justification before reliance.
