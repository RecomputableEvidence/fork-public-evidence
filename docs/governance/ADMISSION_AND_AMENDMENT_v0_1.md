# Fork Admission and Amendment Procedure v0.1

Status: Repository governance procedure.  
Normative force: Maintainer-governed procedure for admission, publication, historical correction, supersession, and current-state projection.  
Scope: Public artifacts in `fork-public-evidence`.  
Non-claim: This procedure does not certify truth, security, compliance, legal sufficiency, production readiness, or institutional authority.

## Purpose

This procedure separates contribution activity from the acts that change an artifact's repository standing.

It governs:

- submission;
- verification;
- review;
- merge;
- admission;
- freeze or publication;
- amendment;
- supersession;
- historical preservation;
- current-state projection.

## Lifecycle separation

The following are distinct events:

1. **Submission** — a contributor proposes a change.
2. **Verification** — identified checks are executed against identified inputs and rules.
3. **Review** — a reviewer inspects the bounded surface and records findings or disposition.
4. **Merge** — repository history incorporates a commit.
5. **Admission** — an explicit governing record grants a defined artifact a defined repository standing.
6. **Publication or freeze** — an explicit record identifies a release, corpus, experiment state, or other public reference point.

No earlier event implies a later event.

In particular:

- verification does not imply review;
- review does not imply endorsement;
- merge does not imply admission unless a controlling procedure explicitly says it does;
- admission does not imply truth, correctness, compliance, legal sufficiency, safety, production readiness, or authority transfer;
- publication does not resolve recorded residuals or unresolved conditions.

## Admission record requirements

An admission or publication act must be append-only and attributable.

The governing record should identify, as applicable:

- admission or publication identifier;
- date and responsible repository role;
- artifact names and versions;
- exact commit SHA, tree reference, content digest, or other immutable coordinates;
- governing specification, schema, or procedure;
- required verification commands;
- exact successful check runs, receipts, or outputs;
- reviewer identity or pseudonymous participant identifier where permitted;
- review independence and any conflicts or prior authorship;
- admitted scope;
- explicit exclusions and non-claims;
- unresolved conditions, limitations, and residuals;
- relationship to prior admissions, amendments, or superseded records;
- publication phase or standing granted by the act.

An admission record must not claim more than the cited verification and review evidence supports.

## Independence and review standing

Independent review means only that the reviewer is sufficiently separate from the contribution activity for the governing procedure's stated purpose.

The record should disclose material prior authorship, direct implementation participation, or other conflicts relevant to the review claim.

Independent review is not:

- endorsement;
- certification;
- security assessment;
- legal approval;
- compliance determination;
- production approval;
- authority transfer.

A review receipt records what was accessed, executed, inspected, or not observed. Failed retrieval, partial access, or unexecuted commands must remain explicit.

## Historical preservation rule

A published, admitted, frozen, cited, or historically relied-upon artifact must not be silently rewritten to match a later interpretation or current implementation state.

When a defect is discovered, preserve distinguishability among:

- the original historical artifact;
- the defect observation;
- the correction or superseding artifact;
- the current-state projection;
- the admission or publication standing of each record.

Historical continuity is evidentiary continuity. It does not create authority continuity.

## Amendment procedure

A historical correction or amendment should proceed through the following bounded sequence.

### 1. Preserve the original

Preserve the original artifact byte-for-byte where feasible, or preserve an immutable digest and sealed representation when the original cannot remain in its prior path.

Do not replace the original before its prior state is independently recoverable.

### 2. Record the defect

Create an attributable defect record that identifies:

- the affected artifact and version;
- exact path, line, field, block, commit, or digest coordinates;
- when and how the defect was observed;
- whether the defect is syntactic, structural, semantic, procedural, historical, or mixed;
- affected verification results or downstream references;
- conditions that remain unknown.

Do not infer intent from malformed content unless separately evidenced and within scope.

### 3. Create the correction

Add a corrective artifact, replacement version, amendment, or repair commit under the applicable contract.

The correction must state:

- what changed;
- what did not change;
- whether the correction is backward compatible;
- whether prior outputs remain valid;
- what must be recomputed;
- whether a new version is required.

### 4. Declare the relationship

Classify the relationship between the records, using the vocabulary required by the governing surface. Typical relationships include:

- corrected by;
- amended by;
- superseded by;
- preserved as historical;
- invalid for current use but retained;
- projected into current state;
- unresolved pending further evidence.

Do not use “superseded” when both records retain distinct valid scopes.

### 5. Recompute independently

Run the correction's applicable verification procedure from identified inputs and a published commit or immutable artifact set.

Where independent recomputation is required, the verifier should not rely solely on the correction author's unsealed local output.

A successful recomputation verifies only the bounded checker or integrity condition.

### 6. Admit the amendment separately

When the original artifact was admitted, frozen, canonical, or published, admit the correction through a separate append-only admission or amendment record.

The admission record must identify the original and corrected coordinates and state the standing of each.

## Current-state projections

A current-state projection summarizes or computes the present standing of an artifact set without altering the historical records from which it is derived.

A projection must identify:

- projection time or source commit;
- source records;
- governing projection rules;
- excluded or unavailable records;
- unresolved residuals;
- derived status;
- non-claim that the projection does not rewrite prior state.

A projection may be updated by adding a new projection. Do not mutate an earlier projection when historical reproducibility matters.

## Frozen specifications and preregistered experiments

Do not modify a frozen specification, preregistration, canonical fixture set, or sealed experiment input in place after the freeze point.

Changes after freeze require one of:

- an explicit amendment that preserves the frozen original;
- a new version;
- a new experiment phase or run;
- a defect record and separately admitted correction.

Instrumentation changes that could affect an experiment result must be separated from execution of that experiment. A repaired instrument should produce a new execution record unless the governing preregistration explicitly provides another procedure.

## Generated and derived records

Generated records must identify their source inputs and generation procedure.

Do not manually edit a generated receipt unless manual authorship is explicitly permitted by its schema or governing procedure.

If regeneration changes unrelated fields:

1. stop the admission process;
2. identify the source of nondeterminism or hidden state;
3. preserve the unexpected output when it is relevant evidence;
4. repair or document the condition;
5. rerun the bounded verification path.

## Residuals and unresolved conditions

Admission and publication records must preserve known residuals.

A residual may be:

- resolved by a later attributable record;
- narrowed by new evidence;
- reclassified under an explicit governing rule;
- retained as unresolved;
- shown to be outside the admitted scope.

A residual must not disappear merely because a newer artifact exists.

## Minimal admission checklist

Before an admission or publication act, confirm:

1. The artifact coordinates are immutable and exact.
2. The governing contract and change class are identified.
3. Required checks were executed against the admitted commit or artifact set.
4. Successful outputs and failures are recorded accurately.
5. Independent review requirements are satisfied or explicitly unresolved.
6. Historical records remain recoverable.
7. Current-state projections remain distinct from historical state.
8. Claims, non-claims, authority limits, and unresolved conditions remain explicit.
9. The admission record is append-only.
10. The record does not convert verification into endorsement, certification, or authority.

## Relationship to other repository documents

- Contribution entry point: [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md)
- Change classes: [`CHANGE_CLASSIFICATION_v0_1.md`](CHANGE_CLASSIFICATION_v0_1.md)
- Local recomputation: [`../verification/LOCAL_RECOMPUTATION_v0_1.md`](../verification/LOCAL_RECOMPUTATION_v0_1.md)
- Repository review posture: [`../review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md`](../review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md)

A more specific frozen specification, experiment preregistration, schema, registry procedure, or publication contract controls when it imposes stricter or more specific requirements.
