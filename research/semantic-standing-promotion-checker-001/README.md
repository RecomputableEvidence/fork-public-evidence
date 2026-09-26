# FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001

Status: `CANDIDATE_RESEARCH_OBJECT__NOT_EMPIRICALLY_QUALIFIED__NOT_GOVERNANCE_ADOPTED`

## Purpose

Explore a bounded, non-destructive checker for unsupported semantic-standing promotions in AI-generated text.

The source text remains byte-preserved. Findings are emitted as sidecar evidence. The checker is not a policy oracle, semantic adjudicator, governance authority, or general claim about LLM behavior.

## Candidate execution surface

```text
python tools/check_semantic_standing_promotions.py \
  --source ai_output.md \
  --standing-envelope standing.json \
  --evidence-registry evidence.json \
  --transition-registry authorized_transitions.json \
  --assertions normalized_assertions.json \
  --json
```

`--assertions` is intentionally separate from the mechanical verifier. v0.1 does not pretend that deterministic Python can infer standing semantics from arbitrary prose. A normalized assertion sidecar supplies the claim vector; the checker verifies that vector against evidence-backed state and transition records. If the sidecar is omitted, the checker returns `INDETERMINATE` rather than guessing.

## Governing boundaries

- `PROMOTION_DETECTED != SOURCE_REWRITTEN`
- `CHECKER_FINDING != FINAL_SEMANTIC_ADJUDICATION`
- `AUTHORIZED_TO_TRANSITION != TRANSITION_OCCURRED != TRANSITION_IS_EFFECTIVE`
- `REGISTRY_ENTRY != PROOF_OF_TRANSITION`
- `SUPPORTED_WITHIN_DECLARED_TRANSITION != UNIVERSALLY_CORRECT`
- `OBSERVED_LOCAL_BEHAVIOR != UNIVERSAL_SYSTEM_PROPERTY`

## Mechanical transition gate

A normalized assertion is supported by a declared transition only when the checker can bind:

1. exact subject identity (`object_id`, `version`, SHA-256),
2. exact standing dimension,
3. asserted state to `to_state`,
4. authorization status,
5. occurrence status,
6. effectivity status,
7. temporal alignment,
8. evidence bytes to declared hashes,
9. asserted scope to declared scope,
10. absence of conflict with explicit non-effects,
11. declared transition basis.

The positive internal label is `SUPPORTED_WITHIN_DECLARED_TRANSITION`, not a generic semantic-validity verdict.

## Candidate outputs

When `--output-dir` is supplied, the checker creates:

```text
source/original_ai_output.<ext>
analysis/promotion_findings.json
analysis/promotion_receipt.json
disposition/reviewer_decision.json
```

The reviewer-decision record remains `PENDING_AUTHORIZED_DISPOSITION`; the checker does not adjudicate its own findings.

## Initial corpus target

The candidate manifest preserves six intended specimen classes: bounded candidate language, canonicality promotion, cross-object promotion, temporal-state error, legitimate authorized transition, and accurate negative control. The manifest is not itself an executed or qualified corpus.

## Candidate success criterion

Within a frozen test population, identify declared prohibited standing promotions without falsely rejecting explicitly authorized state transitions, while preserving each source specimen unchanged.

Construction of this object establishes no repository admission, empirical qualification, governance adoption, production readiness, or generalized property of language models.
