# FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001

## AG2 — SOURCE OBSERVATION ADMISSION

Status: `AG2_PROCEDURE_COMPLETE`

Capture: `CAPTURE_001_SOURCE_OBSERVATION_SET_ADMITTED`

Parent AG1 commit: `bd53977185fce00f7a88b2b8bf85b0766b37a5db`

AG2 was explicitly authorized after AG1 passed. This record freezes the surrounding public source observations used by the demonstration without evaluating the predeclared relation edges.

Observation window: `2026-09-25T04:55:51Z` through `2026-09-25T04:57:52Z`.

---

## 1. Bound artifact carried forward from AG1

```text
google-workspace-cli-x86_64-pc-windows-msvc.zip
6275652 bytes
sha256:5e33f26556df86411959e0f07cd51caa87b4eaa413b14a385c9efd828b5b1739
```

Standing carried forward only:

`ARTIFACT_IDENTITY_ADMITTED_FOR_CAPTURE_001`

AG2 does not re-evaluate that byte identity.

---

## 2. Release surface observed

The GitHub release endpoint for `v0.22.1` reported:

- release id `301345178`;
- tag `v0.22.1`;
- release name `0.22.1`;
- target commitish `45ca45bfd418db07b02995e8510dd18ac45cb3a6`;
- `draft=false`;
- `prerelease=false`;
- `immutable=true`;
- published at `2026-03-25T17:37:35Z`.

The release body listed the selected Windows x64 ZIP and a checksum link for it. The release body also stated that artifacts in the release have GitHub Artifact Attestations and provided `gh attestation verify` instructions.

These are source observations only.

```text
RELEASE_PAGE_LISTS_ARTIFACT
!= ARTIFACT_TO_RELEASE_RELATION_EVALUATED

RELEASE_BODY_STATES_ATTESTATIONS_EXIST
!= ATTESTATION_BUNDLE_CAPTURED
```

---

## 3. Target asset metadata observed

GitHub asset id `381438738` reported:

- name `google-workspace-cli-x86_64-pc-windows-msvc.zip`;
- content type `application/zip`;
- state `uploaded`;
- size `6275652`;
- digest `sha256:5e33f26556df86411959e0f07cd51caa87b4eaa413b14a385c9efd828b5b1739`;
- created at `2026-03-25T17:37:33Z`;
- updated at `2026-03-25T17:37:34Z`.

AG1 independently bound identical filename, byte length, and SHA-256 from the uploaded bytes. AG2 preserves the source metadata separately and does not convert the match into a release-relation conclusion.

```text
SOURCE_METADATA_MATCHES_BOUND_IDENTITY
!= RELEASE_RELATION_STANDING
```

---

## 4. Checksum surface observed with limitation

GitHub asset id `381438739` reported:

- name `google-workspace-cli-x86_64-pc-windows-msvc.zip.sha256`;
- content type `application/octet-stream`;
- state `uploaded`;
- size `115` bytes;
- GitHub-reported digest of the checksum-file object: `sha256:36bf177d920055ed9923821303f23e4ac089b40b765686a0b8a56a826469b8b9`.

The release body linked that checksum asset to the selected ZIP.

The 115-byte checksum file content itself was **not captured** in AG2. Therefore the checksum assertion contained inside that file is not yet observed by this packet.

```text
CHECKSUM_ASSET_METADATA_PRESENT
!= CHECKSUM_ASSERTION_CONTENT_CAPTURED

CHECKSUM_LINK_PRESENT
!= CHECKSUM_ASSERTION_VALIDATED
```

---

## 5. Tag and source commit surfaces observed

The Git tag reference endpoint reported:

```text
refs/tags/v0.22.1
→ commit 45ca45bfd418db07b02995e8510dd18ac45cb3a6
```

The commit endpoint reported the same SHA with message:

`chore: release versions (#624)`

AG2 preserves these as source observations. Their relationship to the captured artifact remains for later edge evaluation.

---

## 6. Release workflow text observed at the source commit

At commit `45ca45bfd418db07b02995e8510dd18ac45cb3a6`, `.github/workflows/release.yml` was observed with the following relevant text surfaces:

- workflow name `Release`;
- push trigger for version-like tags;
- local artifact build job permissions including `attestations: write`, `contents: read`, and `id-token: write`;
- an `Attest` step using `actions/attest-build-provenance@43d14bc2b83dec42d39ecae14e916627a18bb661`;
- attestation subject path `target/distrib/*${{ join(matrix.targets, ', ') }}*`;
- host logic that sets `RELEASE_COMMIT` from `${{ github.sha }}`;
- release creation command using `gh release create ... --target "$RELEASE_COMMIT" ... artifacts/*`.

These observations establish only what the workflow text contained at that commit.

```text
WORKFLOW_TEXT_PRESENT
!= WORKFLOW_EXECUTED_FOR_THIS_ARTIFACT

ATTEST_STEP_PRESENT
!= CAPTURED_ARTIFACT_ATTESTED
```

---

## 7. Release workflow run and target-platform job observed

GitHub Actions run `23554953556` reported:

- name `Release`;
- head branch `v0.22.1`;
- head SHA `45ca45bfd418db07b02995e8510dd18ac45cb3a6`;
- workflow path `.github/workflows/release.yml`;
- event `push`;
- status `completed`;
- conclusion `success`;
- run number `1185`.

Within that run, job `68579090437` was observed as:

`build-local-artifacts (x86_64-pc-windows-msvc)`

with `head_sha=45ca45bfd418db07b02995e8510dd18ac45cb3a6`, `status=completed`, `conclusion=success`, and runner label `windows-2022`.

The same run's artifact listing showed intermediate workflow artifact `artifacts-build-local-x86_64-pc-windows-msvc` (id `6107415008`) as expired at the observation coordinate. Its workflow metadata pointed to the same tag branch and head SHA.

That intermediate artifact is not treated as byte-identical to the public release ZIP.

```text
WORKFLOW_RUN_SUCCESS
!= ARTIFACT_PROVENANCE_ESTABLISHED

INTERMEDIATE_ARTIFACT_METADATA
!= PUBLIC_RELEASE_ARTIFACT_IDENTITY
```

---

## 8. Attestation surface limitation

The release body points to GitHub's repository attestation surface and states that release artifacts have attestations. However, the available GitHub connector did not permit retrieval through the repository attestations REST endpoint during AG2, and no attestation bundle bytes or decoded predicate were admitted.

Standing:

`ATTESTATION_SURFACE_CLAIM_OBSERVED`

but:

`ATTESTATION_BUNDLE_NOT_CAPTURED`

Therefore no attestation-subject, repository, commit, workflow, signer, issuer, or authority edge is evaluated at AG2.

---

## 9. Source-preservation limitation

The AG2 packet preserves structured field projections, source URLs, capture scope, and explicit missingness. It does **not** claim independent byte-for-byte preservation of every HTTP response body returned by GitHub.

```text
SOURCE_FIELD_PROJECTION_PRESERVED
!= COMPLETE_HTTP_RESPONSE_BYTES_FROZEN
```

This limitation remains first-class rather than being silently collapsed.

---

## 10. AG2 disposition

Admitted:

- the bounded `CAPTURE_001` source-observation set;
- release metadata observation;
- target release-asset metadata observation;
- checksum-asset metadata observation with content missingness preserved;
- tag reference observation;
- source commit observation;
- release workflow text observations at the source commit;
- release workflow-run observation;
- target-platform build-job observation;
- intermediate workflow-artifact metadata observation; and
- the release-body attestation claim with attestation-bundle missingness preserved.

Not admitted:

- `ARTIFACT_TO_RELEASE_OBJECT` standing;
- `ARTIFACT_TO_PUBLISHED_DIGEST` standing;
- `ARTIFACT_TO_ATTESTATION_SUBJECT` standing;
- `ATTESTATION_TO_SOURCE_REPOSITORY` standing;
- `ATTESTATION_TO_SOURCE_COMMIT` standing;
- `SOURCE_COMMIT_TO_WORKFLOW_REFERENCE` standing;
- issuer authority;
- temporal applicability or supersession standing;
- checksum assertion validity;
- attestation validity;
- any derived view;
- any view selection; or
- any external action.

AG3 remains `UNOPENED`.

```text
SOURCE_OBSERVED
!= RELATION_ESTABLISHED

AG2_PROCEDURE_COMPLETE
!= SOURCE_SURFACES_COMPLETE

AG2_COMPLETE
!= AG3_AUTHORIZED
```
