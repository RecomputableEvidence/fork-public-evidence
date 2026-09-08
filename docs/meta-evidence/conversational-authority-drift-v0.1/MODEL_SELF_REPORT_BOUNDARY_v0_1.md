# Model Self-Report Boundary v0.1

Status: `CANDIDATE_NOT_ADMITTED`

## Rule

A model may be quoted as the source of a statement about its own output. That statement does not, by itself, establish the model's hidden causal process, internal state, durable belief revision, memory change, rollback, or claim-standing transition.

## Required fields

When a case preserves a model's explanation of its own behavior, record:

- `statement_origin` — the attributed system or speaker;
- `observable_text` — the exact or bounded statement preserved;
- `source_reference` — the artifact or span containing the statement;
- `self_report_status` — `ATTRIBUTED_MODEL_SELF_REPORT`;
- `mechanism_verified` — `false` unless independently established by an authorized method;
- `causal_standing` — normally `UNRESOLVED`;
- `later_revision_or_withdrawal` — any subsequent narrowing, objection, or withdrawal.

## Prohibited inheritance

Do not convert a model self-report into:

- a verified mechanism label;
- a correction receipt proving internal reset;
- a transition log asserting settled hidden-state changes;
- provider-wide behavioral evidence;
- a favorable or unfavorable model ranking;
- an execution, admission, or authority event.

## Observable events remain recordable

The following may be recorded when source-bound:

- the model emitted an initial statement;
- the model later emitted narrower replacement language;
- the model later disputed or withdrew its own explanation;
- the replacement text conflicts with or supersedes a prior public statement at the textual level;
- an analyst overinterpreted the revision and later corrected that interpretation.

These are textual or artifact events. They do not establish an internal cognitive transition.

## Actor terminology

Use `statement_origin`, `source_speaker`, or `attributed_system` for transcript attribution.

Reserve `actor` for externally observable acts such as creating a file, submitting a review, executing a command with a preserved receipt, changing a repository object, or posting a correction. Even then, record the visible act rather than an inferred mental process.

## Pair-001 boundary

The CAD candidate is an exploratory, correction-bearing review thread with tools and memory potentially enabled. It is not the frozen, no-correction, pre-registered Pair-001 execution surface and must not be represented as executing or extending Pair-001.
