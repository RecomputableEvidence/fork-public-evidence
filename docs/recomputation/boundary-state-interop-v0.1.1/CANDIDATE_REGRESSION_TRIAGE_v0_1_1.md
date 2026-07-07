# Candidate Regression Triage v0.1.1

This note files the exterior report's Q5/Q6 findings as triage candidates rather than normative checker failures.

## Q6 residual paraphrase bypass candidates

The exterior report describes five schema-valid paraphrases that were accepted by the unmodified checker while carrying reliance/no-further-review semantics to a human reader:

1. thumbsup_asfinal
2. checkpoint_noholdback
3. comfortable_asis
4. shipit_nonotes
5. bar_met

These should be reviewed as possible future regression payloads.

## Q5 false-positive candidates

The exterior report describes four schema-valid benign technical metadata sentences that were rejected because trigger words appeared in unrelated technical senses:

1. JSON-schema compliant.
2. URI authority component.
3. Syntactically correct JSON.
4. Boolean true flag.

These should be reviewed as possible precision tests before broadening free-text semantic linting.

## Triage rule

Do not wire these payloads into required CI until the project decides whether the intended checker posture is strict phrase-list linting, context-scoped linting, or explicitly best-effort semantic linting.