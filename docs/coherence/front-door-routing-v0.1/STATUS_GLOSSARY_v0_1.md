# Status Glossary v0.1

Status: `DRAFT_PRESENTATION_GLOSSARY`

Scope: front-door and visitor-orientation presentation only.

This glossary does not replace artifact-specific schemas, verdict codes, state projections, admission records, experiment contracts, or checker outputs. When a canonical artifact uses a more specific status, quote that status exactly and use this glossary only to explain the general presentation category.

## Core rule

> A status describes what was established within a declared scope. It must never be presented as establishing a broader property that was not checked.

## Four primary presentation states

| State | Plain-language meaning | Required interpretation | Prohibited overread |
|---|---|---|---|
| **PASS** | Every declared check in the referenced verification scope succeeded. | Name the checker, exact head, scope, and expected result. | Truth, correctness, approval, authorization, compliance, legal sufficiency, safety, production readiness, endorsement, or repository-wide completeness. |
| **FAIL** | At least one declared check in the referenced verification scope did not succeed. | Preserve the failing result, affected check, observed evidence, and whether other checks remained unaffected. | The entire repository, hypothesis, artifact family, or unrelated claim is false or invalid. |
| **UNRESOLVED** | Available evidence does not support a conclusive classification within the declared question. | Preserve competing explanations, missing evidence, access limits, and the next permitted discriminating action. | Permission to assume the favorable result, infer a cause, continue execution, or silently choose a branch. |
| **NOT_CHECKED** | The relevant property was not evaluated by the cited process. | State which property was outside scope and what separate check or authority would be required. | PASS, FAIL, closure, residual acceptance, or evidence that no problem exists. |

## Presentation requirements

Every visible status must use:

1. the complete textual label;
2. a short definition or linked glossary;
3. the named scope or checker;
4. the exact head or artifact version when available;
5. explicit non-claims where overread is plausible.

Color may supplement the label but must not carry meaning by itself. A visitor must be able to distinguish all states in monochrome, screen-reader output, copied text, and printed form.

Recommended neutral symbols:

- `PASS` — `✓`
- `FAIL` — `✗`
- `UNRESOLVED` — `?`
- `NOT_CHECKED` — `—`

Symbols must always appear beside the full label.

## Relationship to Fork-specific standing

Fork contains statuses that are not reducible to the four verification states. Examples include:

- `CANDIDATE_NOT_ADMITTED`;
- `REVIEW_ELIGIBLE_NOT_ADMITTED`;
- `STRUCTURALLY_READY_EXECUTION_BLOCKED`;
- `DRIFT_CLASSIFIED_RETRY_NOT_AUTHORIZED`;
- `BLOCKED_PROVIDER_VALIDATION_FAILED`;
- `PUBLISHED_BUT_NOT_EXECUTION_AUTHORITY`.

These are standing, lifecycle, control, or experiment-state expressions. They must remain verbatim. Do not relabel them as `PASS`, `FAIL`, `UNRESOLVED`, or `NOT_CHECKED` unless a specific canonical mapping is declared by the governing artifact.

### Examples

#### Passing verifier with blocked execution

A structural verifier can be `PASS` while the experiment remains `STRUCTURALLY_READY_EXECUTION_BLOCKED`. The pass establishes bounded structural conformance; it does not authorize execution.

#### Green CI with an unexamined property

A workflow may be `PASS` while a separate manifest or semantic property is `NOT_CHECKED`. Green CI must not be presented as coverage of a surface that the workflow did not evaluate.

#### Repeated provider error with unknown cause

Observed requests may be classified and preserved while cause remains `UNRESOLVED`. Repetition does not authorize an assumed cause or retry.

#### Correctly rejected invalid fixture

A checker may `PASS` because it correctly rejected an invalid fixture. That pass does not approve the fixture or establish the underlying claim as true.

## Composite display pattern

When more than one dimension matters, display them separately:

```text
Structural verification: PASS
Admission standing: CANDIDATE_NOT_ADMITTED
Execution standing: STRUCTURALLY_READY_EXECUTION_BLOCKED
Cause classification: UNRESOLVED
Provider calls performed by this change: 0
```

Do not collapse these dimensions into one green badge or a single phrase such as "Fork passed."

## Historical and superseded results

Earlier results must be labeled with their exact head and temporal standing. A later successful run may supersede an earlier run for merge reliance, but it does not erase the earlier failure or retroactively validate a later head.

Recommended forms:

- `PASS — exact head <sha>`
- `FAIL — preserved historical run <id>`
- `SUPERSEDED_FOR_MERGE_RELIANCE — preserved as history`
- `NOT_CHECKED — outside workflow scope`

## Front-door invariant

The front door must make favorable and unfavorable states equally legible. `UNRESOLVED`, `FAIL`, `NOT_CHECKED`, blocked standing, residuals, and historical corrections may not be hidden behind a success summary or relegated to styling that implies lower importance.