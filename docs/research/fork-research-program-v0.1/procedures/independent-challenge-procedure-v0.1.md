# Fork Independent Challenge Procedure v0.1

```yaml
artifact:
  name: Fork Independent Challenge Procedure
  version: "0.1"
  status: PROVISIONAL_PROCEDURE
  instantiated_at: "2026-08-06"
```

## 1. Purpose

This procedure defines the minimum declaration and preservation requirements for an independent challenge used in considering advancement from `PROVISIONAL_RESEARCH_BASELINE` to `INDEPENDENTLY_VALIDATED_BASELINE`.

It does not guarantee independence, truth, correctness, completeness, or institutional acceptance. It makes the asserted basis for independence and the resulting challenge inspectable.

## 2. Preconditions

Before a challenge may begin, the challenge record **MUST** identify:

- exact candidate-model version;
- repository identity, commit SHA, and tree digest;
- baseline-manifest digest;
- normative artifact, schema, profile, rule, procedure, and fixture digests;
- declared corpus tranche;
- challenge scope and exclusions;
- originating implementation, if any; and
- declared advancement criteria.

A challenge initiated while repository binding is unresolved may be preserved as a preliminary observation, but it **MUST NOT** support advancement to `INDEPENDENTLY_VALIDATED_BASELINE`.

## 3. Challenger declaration

Each challenger **MUST** disclose:

- stable identity or declared pseudonymous identity;
- organization or affiliation, if any;
- financial, employment, authorship, implementation, and governance relationships relevant to the challenged artifacts;
- prior access to originating source code, fixtures, expected outputs, or private guidance;
- tools and implementations used;
- assistance received; and
- limitations on independence.

Independence **MUST NOT** be inferred solely from organizational separation or the use of a different model or tool.

## 4. Permitted challenge modes

```yaml
challenge_mode:
  - INDEPENDENT_CLASSIFICATION
  - INDEPENDENT_RECOMPUTATION
  - ADVERSARIAL_CORPUS_CHALLENGE
  - REDUCTION_REVIEW
  - CLEAN_ROOM_IMPLEMENTATION
```

The selected mode and its limitations **MUST** be explicit. Results from one mode **MUST NOT** silently inherit the standing of another.

## 5. Procedure declaration

The challenger **MUST** preserve:

- procedure identity and version;
- environment and dependency versions;
- input and output digests;
- profile identities and versions;
- instructions supplied to human or model evaluators;
- random seeds or nondeterminism controls where applicable;
- raw results;
- deviations from the declared procedure; and
- enough information to reproduce the challenge within the declared scope.

## 6. Classification and disagreement

Every challenge classification **MUST** be recorded as a `classification_event`. Multiple results **MUST** remain separately attributable.

Disagreement **MUST** be classified, when possible, as one or more of:

```yaml
agreement_state:
  - AGREEMENT
  - PARTIAL_AGREEMENT
  - MATERIAL_DISAGREEMENT
  - PROFILE_DIVERGENCE
  - PROCEDURAL_DIVERGENCE
  - UNRESOLVED
```

No majority vote or evaluator prestige rule may automatically establish the governing result.

## 7. Minimum advancement record

Any governance action advancing a version to `INDEPENDENTLY_VALIDATED_BASELINE` **MUST** preserve:

- the declared corpus evaluation and its completion status;
- the reduction review and retained negative results;
- all qualifying independent challenges;
- all known conflicts and limitations;
- material disagreements and unresolved questions;
- clean-room implementation results if required by the declared scope;
- the exact scope in which advancement is granted; and
- an attributable standing-transition authorization.

The advancement decision is procedural standing for that version and scope. It does not establish universal correctness, completeness, legal validity, institutional acceptance, or permanent finality.

## 8. Failure and partial completion

Failed, constrained, partially completed, and non-reproduced challenges **MUST** be preserved. Their preservation does not imply that the model failed; their diagnosis and disposition remain separate events under RFC 0.

