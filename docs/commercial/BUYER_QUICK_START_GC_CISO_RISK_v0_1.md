# Buyer Quick Start for GC / CISO / Risk v0.1

Status: Buyer-facing orientation guide.  
Audience: General Counsel, CISO / security leadership, risk leadership, compliance leadership, audit-adjacent reviewers, and design-partner evaluators.  
Scope: Commercial first-read path for Fork's evidence-boundary posture.  
Classification: Orientation surface, not certification.

## Buyer note

Fork preserves reconstructable evidence context around AI-assisted artifacts that may later be relied upon.

Fork does not certify compliance, establish legal admissibility, establish legal sufficiency, replace institutional controls, operate detection systems, function as a GRC system, replace SIEM or logging platforms, or act as a runtime control plane.

## What Fork is

Fork is evidence-boundary infrastructure for AI-assisted workflows.

It preserves the context needed to reconstruct what was requested, what AI-assisted artifact was produced, what humans reviewed or changed, what was relied upon, what was not relied upon, what authority was referenced, what authority was not transferred, what non-claims were preserved, and whether a sealed record still structurally verifies later.

## What Fork is not

Fork is not a runtime control plane, policy engine, compliance oracle, legal-admissibility engine, legal-sufficiency engine, SIEM, security telemetry platform, GRC system, system-wide audit log, approval workflow, control-effectiveness assessment, production-readiness certification, or substitute for institutional decision authority.

This is the canonical buyer-facing non-claims list for this quick start. Later sections preserve the same non-claims and should not be read as narrowing them.

## Reliance boundary

A reliance boundary is the point at which an AI-assisted artifact is treated as something a person, team, workflow, or downstream record depends on.

Examples include citation in an approval memo, inclusion in a case file, use in a vendor-risk recommendation, attachment to a decision record, or reference during an investigation or risk review.

Fork does not decide what should be relied upon. Fork preserves the reconstructable context around what was in fact relied upon, what was not relied upon, and whether the sealed record still structurally verifies later.

Fork does not assess the quality, correctness, reasonableness, or sufficiency of any reliance decision.

## CISO / security distinction

Security leadership may use Fork to reconstruct the context around AI-assisted artifacts that were referenced during investigations, postmortems, risk reviews, or control-design discussions.

Fork does not integrate with, replace, operate, or evaluate SIEM, logging, GRC, compliance, detection, telemetry, or security-control systems unless separately implemented outside this buyer-facing posture.

## Legal-scope distinction

Fork does not establish legal admissibility or legal sufficiency.

Legal admissibility and legal sufficiency are separate legal determinations outside Fork's scope. Fork preserves reconstructable context; it does not decide whether that context is admissible, sufficient, persuasive, complete, or legally operative.

## Commercial maturity posture

This package describes an emerging evidence-boundary infrastructure pattern under active development with design partners.

It is not a completed enterprise compliance product, production control system, legal-admissibility engine, legal-sufficiency engine, audit certification package, or procurement-ready control framework.

## Recommended first-read path

Read these first:

1. [Buyer overview](BUYER_OVERVIEW_v0_1.md)
2. [Commercial README](README.md)
3. [Public review package index](../PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md)

Then, if the boundary posture is relevant, review the technical or recomputation materials through the public review index rather than treating the repository as a single undifferentiated review surface.

## What not to infer

Do not infer from Fork materials that:

- an AI-assisted decision was correct;
- an artifact was legally admissible;
- an artifact was legally sufficient;
- a reliance decision was reasonable;
- a reliance decision was correct;
- a reliance decision was sufficient;
- Fork assessed the quality, correctness, reasonableness, or sufficiency of any reliance decision;
- a control operated effectively;
- a compliance obligation was satisfied;
- an approval occurred;
- a reviewer endorsed the system;
- structural verification proves truth;
- recomputation proves production readiness;
- a preserved observation is a certification.

## Good buyer question

Where in our AI-assisted workflow might an artifact become relied upon, and what would a later reviewer need in order to reconstruct that reliance without trusting memory, screenshots, or a live system?