# FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001

## AG4 — DIMENSIONAL EVALUATION ADMISSION

Status: `AG4_COMPLETE`

Capture: `CAPTURE_001_DIMENSIONAL_EVALUATION_ADMITTED`

Parent AG3 commit: `874947205b9cd1dac5f3268d9d6f25e1a97be7c1`

AG4 was explicitly authorized after AG3 completed. This gate evaluates the nine predeclared relation-edge objects using only the evidence boundary admitted through AG3. No new external source observation was introduced during AG4.

Ruleset: `FORK-RRD-001-AG4-EVAL-v0.1`

```text
EVALUATION
!= NEW_SOURCE_CAPTURE

EDGE_STATUS
!= GLOBAL_VERDICT
```

---

## 1. Evaluation method

Allowed result vocabulary remains exactly the AG0 vocabulary:

- `SUPPORTED`
- `CONTRADICTED`
- `UNRESOLVED`
- `INSUFFICIENT_EVIDENCE`
- `NOT_EVALUATED`
- `OUT_OF_SCOPE`

AG4 applies these distinctions:

- `SUPPORTED` means the admitted evidence directly supports the edge proposition at the named capture coordinate without an unadmitted bridge.
- `CONTRADICTED` means admitted evidence directly conflicts with the edge proposition.
- `UNRESOLVED` means relevant admitted evidence conflicts or remains ambiguous such that support or contradiction cannot be assigned.
- `INSUFFICIENT_EVIDENCE` means a required endpoint, source surface, or proposition-level observation is absent from the admitted evidence boundary.

In particular:

```text
INSUFFICIENT_EVIDENCE
!= CONTRADICTED

MISSING_EVIDENCE
!= EVIDENCE_OF_ABSENCE
```

---

## 2. AG4 results

### AG3-E01 — ARTIFACT_TO_RELEASE_OBJECT

Status: `SUPPORTED`

Scope: `SUPPORTED_FOR_CAPTURE_001_RELEASE_ASSOCIATION_ONLY`

AG1 independently bound the uploaded artifact as:

```text
google-workspace-cli-x86_64-pc-windows-msvc.zip
6275652 bytes
sha256:5e33f26556df86411959e0f07cd51caa87b4eaa413b14a385c9efd828b5b1739
```

AG2 observed release object `301345178` / tag `v0.22.1`, whose release body listed that filename, and release-asset object `381438738`, which reported the same filename, byte length, and SHA-256.

This supports the bounded release association for `CAPTURE_001`.

It does **not** establish build provenance, attestation validity, organizational approval, safety, or deployment authority.

---

### AG3-E02 — ARTIFACT_TO_PUBLISHED_DIGEST

Status: `INSUFFICIENT_EVIDENCE`

Scope: `CHECKSUM_ASSERTION_OBJECT_CONTENT_NOT_CAPTURED`

AG2 observed checksum asset `381438739` and its linkage from the release body, but did not capture the checksum file's 115-byte content. Therefore the actual digest assertion inside that checksum file is absent from the AG2 evidence boundary.

The GitHub-reported digest of the checksum-file object itself is not substituted for the assertion contained in that file.

```text
CHECKSUM_FILE_OBJECT_DIGEST
!= CHECKSUM_ASSERTION_CONTENT
```

---

### AG3-E03 — ARTIFACT_TO_ATTESTATION_SUBJECT

Status: `INSUFFICIENT_EVIDENCE`

Scope: `ATTESTATION_SUBJECT_UNBOUND`

AG2 observed that the release body stated release artifacts have GitHub Artifact Attestations and that the source workflow contained an `attest-build-provenance` step. No attestation bundle or decoded predicate was captured that binds the exact CAPTURE_001 artifact digest as an attestation subject.

```text
ATTESTATION_CONFIGURATION_PRESENT
!= ARTIFACT_BOUND_AS_ATTESTATION_SUBJECT
```

---

### AG3-E04 — ATTESTATION_TO_SOURCE_REPOSITORY

Status: `INSUFFICIENT_EVIDENCE`

Scope: `ATTESTATION_OBJECT_UNBOUND`

The release and workflow are observed in `googleworkspace/cli`, but no captured attestation object exists from which an attestation-to-repository assertion can be evaluated.

```text
REPOSITORY_HOSTS_RELEASE
!= ATTESTATION_ASSERTS_REPOSITORY
```

---

### AG3-E05 — ATTESTATION_TO_SOURCE_COMMIT

Status: `INSUFFICIENT_EVIDENCE`

Scope: `ATTESTATION_OBJECT_UNBOUND`

AG2 observed tag `v0.22.1`, commit `45ca45bfd418db07b02995e8510dd18ac45cb3a6`, the release workflow at that commit, and a successful release run with the same head SHA. No captured attestation predicate binds an attestation object to that commit.

```text
WORKFLOW_RUN_AT_COMMIT
!= ATTESTATION_TO_COMMIT_EDGE_ESTABLISHED
```

---

### AG3-E06 — SOURCE_COMMIT_TO_WORKFLOW_REFERENCE

Status: `SUPPORTED`

Scope: `SUPPORTED_FOR_NAMED_WORKFLOW_REFERENCE_AT_BOUND_COMMIT`

AG2 observed:

- `refs/tags/v0.22.1` resolving to commit `45ca45bfd418db07b02995e8510dd18ac45cb3a6`;
- `.github/workflows/release.yml` at that exact commit; and
- release workflow run `23554953556` reporting the same workflow path and head SHA.

This supports the bounded source-commit-to-workflow-reference relation.

It does not establish that this workflow produced the exact public release ZIP, nor does it establish attestation or issuer authority.

---

### AG3-E07 — CLAIMED_ISSUER_TO_ISSUER_AUTHORITY

Status: `INSUFFICIENT_EVIDENCE`

Scope: `CLAIMED_ISSUER_AND_AUTHORITY_INSTRUMENT_UNBOUND`

AG2 did not capture an attestation predicate identifying the claimed issuer in the edge's required sense, and no independent authority instrument was admitted from which issuer authority could be established.

```text
ACTOR_OBSERVED
!= ISSUER_AUTHORITY_ESTABLISHED

WORKFLOW_PERMISSION
!= ISSUER_AUTHORITY
```

No claim is made that any observed actor lacked authority.

---

### AG3-E08 — RELATION_TO_TEMPORAL_APPLICABILITY

Status: `SUPPORTED`

Scope: `SUPPORTED_FOR_CAPTURE_001_RECORD_COORDINATE_BINDING_ONLY`

AG0 required future standing to remain coordinate-bound. AG2 established the `CAPTURE_001` observation window, and AG3 instantiated the relation-edge set against that capture. AG4 therefore supports only that the statuses assigned here are applicable to the named `CAPTURE_001` evidence/record coordinate.

This does not establish persistence of any external relation before or after that coordinate.

```text
STANDING_AT_CAPTURE_001
!= STANDING_AT_LATER_CAPTURE

CURRENT_EVALUATION
!= HISTORICAL_OR_FUTURE_INHERITANCE
```

---

### AG3-E09 — RELATION_TO_SUPERSESSION_STATE

Status: `INSUFFICIENT_EVIDENCE`

Scope: `NO_BOUND_SUPERSESSION_SOURCE_ADMITTED`

The AG2 evidence set contains release, tag, commit, workflow-text, workflow-run, and asset observations, but no independently bounded source sufficient to establish whether any evaluated relation had been superseded at `CAPTURE_001`.

Release immutability and the absence of an observed supersession event are not treated as proof of non-supersession.

```text
NO_SUPERSESSION_EVENT_OBSERVED_IN_BOUND_SET
!= NON_SUPERSESSION_ESTABLISHED
```

---

## 3. Result distribution

```text
SUPPORTED                3
CONTRADICTED              0
UNRESOLVED                 0
INSUFFICIENT_EVIDENCE      6
NOT_EVALUATED              0
OUT_OF_SCOPE               0
```

The absence of a `CONTRADICTED` result is not itself evidence of broad correctness. The six `INSUFFICIENT_EVIDENCE` results are preserved as higher-resolution standing rather than silently completed by adjacency or expectation.

```text
NO_CONTRADICTED_EDGES
!= ARTIFACT_VERIFIED_GLOBALLY

INSUFFICIENT_EVIDENCE_PRESERVED
= RESOLUTION_GAIN_WHERE_INFERENCE_WOULD_OTHERWISE_FILL_THE_GAP
```

---

## 4. AG4 disposition

Admitted:

- one named AG4 evaluation ruleset;
- nine edge evaluations;
- three bounded `SUPPORTED` statuses;
- six bounded `INSUFFICIENT_EVIDENCE` statuses;
- explicit scope qualifiers and evidence references for every edge; and
- coordinate binding to `CAPTURE_001`.

Not admitted:

- a global `VERIFIED` result;
- artifact safety or correctness;
- checksum assertion validity for the uncaptured checksum file content;
- attestation validity;
- issuer authority;
- deployment authorization;
- runtime permission;
- provenance beyond the supported edge scopes;
- supersession or non-supersession beyond the admitted source set;
- any derived view;
- any selected view; or
- any downstream action.

AG5 remains `UNOPENED`.

```text
SUPPORTED_UNDER_BOUND_EVIDENCE
!= UNIVERSALLY_TRUE

EDGE_SUPPORTED
!= ARTIFACT_CERTIFIED

AG4_COMPLETE
!= AG5_AUTHORIZED
```
