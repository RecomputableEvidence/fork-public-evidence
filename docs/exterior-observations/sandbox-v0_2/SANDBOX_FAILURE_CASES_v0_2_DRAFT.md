Identifier: SANDBOX_FAILURE_CASES_v0_2_DRAFT
Status: Draft v0_2
Classification: Experimental sandbox design
Question answered: Under adverse conditions, does Fork's evidence surface preserve distinguishability between structural reproduction, unresolved state, evidentiary sufficiency, and authority?

## Governing objective

> Does the evidence surface continue to preserve distinguishability between structural reproduction, unresolved state, evidentiary sufficiency, authority, and truth-claims under adverse conditions?

## Scenario set (v0.2)

This sandbox will be defined around seven scenarios:

1. Missing required runtime coordinates.
2. Conflicting attributed emissions from two sources.
3. Later authorized determination added without rewriting original state.
4. Benign statement that triggers the semantic lint.
5. Approval or authority claim paraphrased to avoid the lint.
6. Valid receipt whose referenced source is unavailable.
7. Structurally reproducible packet containing a claim the evidence does not support.

Each scenario is evaluated against the governing objective. For every case, an independent reviewer should be able to determine:

- What reproduced.
- What failed.
- What remained unresolved.
- What the evidence packet is explicitly not allowed to prove.

Detailed fixtures and expected observations will be added in subsequent iterations.

## v0.1.1 Truth-Claim Consistency Note

The governing sandbox question includes five distinguishability targets:

- structural reproduction;
- unresolved state;
- evidentiary sufficiency;
- authority;
- truth-claims.

Truth-claims are not folded silently into evidentiary sufficiency. A structurally reproducible and evidentially well-supported packet may still be paired with a natural-language claim that is false. The sandbox should preserve that distinction visibly.

## Additional Process-Failure Pressure Cases v0.1.1

The v0.2 sandbox should include observer-process and downstream-use failures in addition to artifact-level failures.

### Case 8: Downstream excerpt without non-endorsement

Setup: An exterior observation is reproduced in a downstream document with the non-endorsement clause removed.

Expected observation: The corpus preserves the original bounded observation and its non-endorsement; downstream excerpting does not convert the observation into authority.

### Case 9: Convergent language misread as consensus

Setup: Multiple independent observations use similar language around a boundary.

Expected observation: Synthesis describes recurring language without saying observers agreed, validated, confirmed, or proved the claim.

### Case 10: Adjacent-system misattribution

Setup: An adjacent system cites a Fork evidence packet as though Fork made the adjacent system's determination.

Expected observation: Fork preserves the referenced evidence boundary without inheriting the adjacent system's determination, authority, or responsibility.

### Case 11: Reproducible packet paired with false natural-language claim

Setup: A packet is structurally reproducible and evidentially sufficient for a narrow record, but a related natural-language statement is false.

Expected observation: Structural reproduction and evidentiary sufficiency do not become truth.

### Case 12: Observer-boundary violation

Setup: Observer commentary is copied into Fork-facing claims as if it were authority.

Expected observation: The observation remains exterior commentary and must not become authority for Fork's claims.

### Case 13: Template non-compliance

Setup: An observer submits useful commentary without using the template and without an explicit non-endorsement statement.

Expected observation: Intake records the limitation and requests or appends a boundary note before preservation.

### Case 14: Downstream legal or compliance misinterpretation

Setup: A downstream legal, compliance, procurement, or ATO reader treats recomputation as legal proof or compliance approval.

Expected observation: The corpus preserves this as a misinterpretation signal, not as Fork's claim.

### Case 15: Automated observer with uncertain access scope

Setup: An LLM observer reports inability to access directory views or only reviews a subset of direct files.

Expected observation: The access limitation is preserved explicitly and does not become a full-surface review.

## Additional Retrieval-Fidelity Pressure Cases v0.1.2

### Case 16: Reviewer source substitution

Setup: An observer is asked to inspect the experiment apparatus but instead inspects top-level repository material, release notes, mirror pages, search snippets, or public landing pages.

Expected observation: The intake process preserves the substitution as a retrieval-fidelity limitation and does not treat the response as a completed full-surface observance pass.

### Case 17: Reviewer access-mode failure

Setup: An LLM observer is provided GitHub-rendered links and raw links but cannot retrieve underlying markdown text.

Expected observation: The access failure is preserved as an access-scope limitation. The observer is offered a plaintext packet fallback.

### Case 18: Stale or partial retrieval

Setup: An observer reports full-surface access but misses content that exists in the current apparatus version.

Expected observation: The observation is preserved with a stale-or-partial retrieval classification.

### Case 19: Prompt echo with misattribution

Setup: An observer repeats the prompt's requested checks as findings and attributes them to files that were not actually inspected.

Expected observation: The response is coded as prompt-echo risk and surface misattribution.

### Case 20: Model-to-model propagation context loss

Setup: An LLM-generated observation is later summarized by another model without scope, limitation, or non-endorsement.

Expected observation: The context loss is preserved and corrected before any downstream use.

### Case 21: Compression or summarization drift

Setup: A downstream summary compresses a bounded observation into a flat claim.

Expected observation: The apparatus identifies the drift and restores the original scope, limitation, and non-endorsement.

### Case 22: Hostile Endorsement Injection

Setup: An observer ignores the observer instructions and attempts to inject validation, certification, approval, endorsement, production-readiness, legal, or compliance language into the intake template.

Expected observation: The intake process preserves the attempted injection as an input-integrity pressure signal. The endorsement language is not adopted as Fork authority, consensus, validation, approval, certification, legal sufficiency, compliance sufficiency, or production-readiness evidence.

Boundary preserved: Observer commentary remains exterior commentary. Even hostile or enthusiastic observer language does not become authority for Fork's claims.

Residual risk: Downstream users may still quote the injected language outside the repository. This requires excerpting and context-loss controls.

### Case 23: Automated Non-Endorsement Scrubbing

Setup: An automated parser, summarizer, marketing tool, or downstream LLM extracts observation text while removing the non-endorsement statement, scope limitation, execution status, or access-mode limitation.

Expected observation: The apparatus identifies the scrubbed version as context loss. The preserved source observation remains bounded by its original scope, limitations, and non-endorsement. The scrubbed derivative is not treated as authority, validation, consensus, approval, certification, legal sufficiency, compliance sufficiency, or production-readiness evidence.

Boundary preserved: Non-endorsement is part of the preserved observation context, not optional decoration.

Residual risk: External systems may continue to circulate scrubbed excerpts. The apparatus can preserve and correct the loss but cannot control external redistribution.
