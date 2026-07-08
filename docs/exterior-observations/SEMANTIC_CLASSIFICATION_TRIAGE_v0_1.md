Identifier: SEMANTIC_CLASSIFICATION_TRIAGE_v0_1
Status: Draft v0_1
Classification: Research backlog
Question answered: What are the known and hypothesized pressure points for Fork's semantic authority-language lint, and how mature is our understanding of each?

## Status taxonomy

- Confirmed reproduction: Independently executed and reproduced across at least one external observation and internal fixture.
- Observed limitation: Identified in an exterior observation or internal test but not yet independently reproduced.
- Research question: Open investigation into possible classifier behavior or design alternative.
- Design constraint: Intentionally out of scope by doctrine; will not be "fixed" but must remain visible.

## Issues by maturity

Status | Issue | Description
---|---|---
Confirmed reproduction | AUTHORITY_PARAPHRASE_BYPASS | Authority semantics expressed indirectly to avoid lint flag
Confirmed reproduction | BENIGN_TECH_FALSE_POSITIVE | Neutral technical language triggering authority lint
Observed limitation | LONG_LIVED_ORG_CHANGE_DRIFT | Classifier not accounting for evolving organizational context over long-lived operations
Research question | CONTEXT_SENSITIVE_MATCHING | Whether multi-field patterns and subject scoping should be considered
Design constraint | NO_SEMANTIC_ORACLE | Fork must not become a semantic sufficiency or policy authority judge

## Separation of concerns

Confirmed and observed items are candidates for hardening and improved lint behavior. Research questions are where new fixtures or algorithms may be added. Design constraints are guardrails ensuring the classifier never mutates Fork into a policy engine, and must remain visible as explicit non-claims.
