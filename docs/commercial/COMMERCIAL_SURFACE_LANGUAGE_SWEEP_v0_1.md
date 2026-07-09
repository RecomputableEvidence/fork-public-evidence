# Commercial Surface Language Sweep v0.1

Status: Language sweep report.  
Scope: README, docs/commercial, and public review index.  
Interpretation: A listed term is not automatically a defect. Buyer-facing uses of these terms should be checked for nearby boundary qualifiers.

## Terms to watch

- audit log
- audit trail
- evidence store
- control evidence
- compliance evidence
- verification
- structural verification
- receipt-binding
- non-repudiation
- production boundary
- production-ready
- validated
- certified
- approved
- trusted
- guarantee
- proof
- reliance
- AI-assisted reliance
- legal admissibility
- legal sufficiency
- SIEM
- GRC

## Replacement pattern

Prefer bounded phrases such as:

- sealed reliance record;
- context-preserving record;
- evidence-boundary record;
- reconstructable reliance context;
- context around AI-assisted artifacts that may later be relied upon;
- structural verification for reconstructability;
- evidence hand-off boundary;
- review surface.

## Specific guidance from buyer-surface review round 002

Avoid using "AI-assisted reliance" when the phrase may imply that Fork validates or approves reliance. Prefer "context around AI-assisted artifacts that may later be relied upon."

Use "legal admissibility" and "legal sufficiency" only when explicitly denying both or distinguishing them as separate legal determinations outside Fork's scope.

Avoid "proof surface." Prefer "review surface" or "evidence-boundary surface."

Keep SIEM, logging, GRC, compliance, detection, telemetry, and security-control systems in negated or contrastive sentences. Avoid placing Fork beside those terms in a way that implies integration, replacement, operation, or evaluation.

## Review note

This sweep is intended to reduce buyer misclassification risk.

It does not establish compliance, non-compliance, legal sufficiency, legal insufficiency, admissibility, inadmissibility, security sufficiency, production readiness, or control effectiveness.

## Round 003 CISO exception guidance

Do not qualify the core CISO / security denial with trailing exception language.

Preferred buyer-facing sentence:

Fork does not integrate with, replace, operate, or evaluate SIEM, logging, GRC, compliance, detection, telemetry, or security-control systems.

Any future integration, adapter, export, or customer-specific implementation would require a separate artifact, separate review, and separate claims. It should not be implied by the Buyer Quick Start.
