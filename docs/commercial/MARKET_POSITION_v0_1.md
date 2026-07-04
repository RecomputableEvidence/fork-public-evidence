# Market Position v0.1

# Where Fork Fits

## The AI governance stack

Modern AI governance consists of multiple architectural layers.

### Model Layer

- Foundation models
- Fine-tuned models
- Evaluation

### Runtime Layer

- Guardrails
- Policy enforcement
- Prompt filtering
- Security

### Workflow Layer

- Human review
- Business processes
- Approvals
- Documentation

### Evidence Layer

- Governance reconstruction
- Claim-boundary preservation
- Transition-state preservation
- Recomputable evidence

Fork operates in the Evidence Layer.

Existing layers govern behavior and process.

The evidence layer preserves what must survive after those processes complete.

Fork's purpose is not to govern model behavior or institutional policy.

Fork's purpose is to preserve what crossed governance boundaries so later reviewers can independently reconstruct the basis for reliance.

---

## Architectural principles

Fork is:

- read-only
- fail-open
- out-of-band
- independently verifiable
- composable with existing governance systems

Fork intentionally avoids becoming:

- a policy engine
- an approval authority
- a compliance oracle
- a runtime controller
- a truth certification service

---

## Core differentiation

Many platforms answer:

**How should AI behave?**

Fork answers:

**Can we independently reconstruct why this AI-assisted artifact became part of institutional action?**

Fork does not govern model behavior.

Fork preserves the evidence required to reconstruct reliance.

That distinction allows Fork to complement existing governance investments rather than compete with them.

Fork is designed to sit alongside existing governance, GRC, and workflow systems without requiring replacement or centralization.
