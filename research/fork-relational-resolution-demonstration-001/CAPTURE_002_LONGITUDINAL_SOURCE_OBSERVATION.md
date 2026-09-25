# FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001

## CAPTURE_002 — LONGITUDINAL SOURCE OBSERVATION

Status: `CAPTURE_002_SOURCE_OBSERVATION_SET_ADMITTED_UNEVALUATED`

Parent AG5 commit: `c2fc1f4f8ede096be26d0dbf147d64022faac291`

Authorization received by user action: `OPEN_CAPTURE_002`

Observation window: `2026-09-25T05:52:25Z` through `2026-09-25T05:54:48Z`.

This record opens the second longitudinal capture reserved at AG0 and re-observes the same primary source surfaces used for `CAPTURE_001`, while preserving the existing artifact identity and evaluation grammar.

It does not open AG6, instantiate CAPTURE_002 relation-edge objects, or evaluate relation standing.

```text
CAPTURE_002_OPEN
!= AG6_OPEN

SOURCE_OBSERVED
!= RELATION_ESTABLISHED
```

## 1. Artifact identity carried forward

The identity-stable artifact remains:

```text
google-workspace-cli-x86_64-pc-windows-msvc.zip
6275652 bytes
sha256:5e33f26556df86411959e0f07cd51caa87b4eaa413b14a385c9efd828b5b1739
```

This identity is carried forward from the AG1/AG5 admitted record. The ZIP was not reacquired or rehashed during this CAPTURE_002 source-observation step.

```text
ARTIFACT_IDENTITY_CARRIED_FORWARD
!= ARTIFACT_REACQUIRED
```

## 2. Primary longitudinal comparability rule

The primary comparison uses only the field projections that CAPTURE_001 actually preserved. Fresh API fields that were not preserved in CAPTURE_001 are not retroactively imported into the earlier coordinate.

```text
NEWLY_OBSERVED_FIELD
!= RETROACTIVE_CAPTURE_001_OBSERVATION
```

This matters because mutable fields such as release-asset download counts are visible in the fresh API response but were not part of the original CAPTURE_001 projection. They are therefore excluded from the primary longitudinal comparison.

## 3. Re-observed primary surfaces

The following ten source surfaces were re-observed:

1. release metadata for `v0.22.1`;
2. target release-asset metadata;
3. checksum-asset metadata;
4. tag reference;
5. source commit;
6. release workflow text at the source commit;
7. release workflow run;
8. target-platform workflow job;
9. target-platform intermediate workflow artifact metadata; and
10. attestation-bundle surface/missingness.

Across the exact field projections preserved in CAPTURE_001, all ten surfaces matched their CAPTURE_001 values or preserved missingness states.

```text
COMPARABLE_SOURCE_SURFACES              10
MATCHED_ON_PRESERVED_FIELD_PROJECTION   10
CHANGED_ON_PRESERVED_FIELD_PROJECTION    0
```

This is only a source-field observation result.

```text
FIELD_STABILITY
!= RELATION_STANDING_STABILITY

SAME_SOURCE_FIELDS
!= SAME_WORLD_STATE
```

## 4. Specific preserved observations

The `v0.22.1` release still reported release id `301345178`, target commitish `45ca45bfd418db07b02995e8510dd18ac45cb3a6`, `draft=false`, `prerelease=false`, `immutable=true`, and the same creation/publication/update timestamps.

The release body still listed the selected Windows x64 ZIP and its checksum link, and still stated that release artifacts have GitHub Artifact Attestations.

The target release asset still reported:

```text
asset id 381438738
name google-workspace-cli-x86_64-pc-windows-msvc.zip
size 6275652
sha256:5e33f26556df86411959e0f07cd51caa87b4eaa413b14a385c9efd828b5b1739
```

The checksum asset still reported id `381438739`, size `115`, and object digest `sha256:36bf177d920055ed9923821303f23e4ac089b40b765686a0b8a56a826469b8b9`; its 115-byte assertion content was not captured.

The tag still resolved to commit `45ca45bfd418db07b02995e8510dd18ac45cb3a6`. The source commit still reported message `chore: release versions (#624)`.

The release workflow at that commit still contained the named `Release` workflow, tag-push trigger, attestation and OIDC write permissions for local build jobs, `actions/attest-build-provenance@43d14bc2b83dec42d39ecae14e916627a18bb661`, and release creation against `${{ github.sha }}`.

Workflow run `23554953556` still reported `status=completed`, `conclusion=success`, head branch `v0.22.1`, and head SHA `45ca45bfd418db07b02995e8510dd18ac45cb3a6`.

Job `68579090437`, `build-local-artifacts (x86_64-pc-windows-msvc)`, still reported `completed/success` on `windows-2022` at the same head SHA.

Intermediate workflow artifact `6107415008` still reported the same size and digest and remained `expired=true`.

## 5. Attestation surface remains unbound

The release body still points to GitHub's attestation surface and states that release artifacts have attestations. Fresh attempts to retrieve the repository attestation endpoint through the available connector were rejected because that endpoint is not exposed by the connector.

No attestation bundle bytes or decoded predicate were captured.

```text
ATTESTATION_CLAIM_PRESENT
!= ATTESTATION_BUNDLE_CAPTURED

CONNECTOR_ENDPOINT_UNAVAILABLE
!= ATTESTATION_ABSENT
```

## 6. Supplemental observation kept out of the primary comparison

A fresh query of the repository's `latest` release endpoint reported `v0.22.5`, release id `303852979`, target commitish `705fb0ecac6f4249679958f6325b809b63fdde17`, published `2026-03-31T18:53:24Z`.

CAPTURE_001 did not preserve the `latest` release endpoint. This observation is therefore recorded separately and is **not** treated as a CAPTURE_001-to-CAPTURE_002 delta.

Nor does a later release, by itself, establish supersession of any relation around the historical `v0.22.1` artifact.

```text
LATER_RELEASE_EXISTS
!= PRIOR_RELATION_SUPERSEDED

SUPPLEMENTAL_C2_OBSERVATION
!= RETROACTIVE_C1_SURFACE
```

## 7. CAPTURE_002 disposition

Admitted:

- opening of `CAPTURE_002` at a new observation coordinate;
- carried-forward identity of the already admitted artifact object;
- a fresh re-observation of the same ten primary source surfaces;
- field-level equality across the CAPTURE_001-preserved primary projections;
- preserved checksum-content missingness;
- preserved attestation-bundle missingness;
- a separately labeled latest-release observation that is excluded from the primary longitudinal comparison.

Not admitted:

- any CAPTURE_002 relation-edge standing;
- any claim that the relation graph is unchanged merely because source fields matched;
- any attestation validity claim;
- any checksum assertion validity claim;
- any issuer-authority relation;
- any supersession or non-supersession standing;
- any derived longitudinal view;
- AG6 derivation; or
- any downstream action.

```text
FIELD_EQUALITY
!= STANDING_EQUALITY

CAPTURE_002_SOURCE_OBSERVATION_COMPLETE
!= CAPTURE_002_EDGE_EVALUATION_AUTHORIZED

G1
DOES_NOT_REWRITE
G0
```

## 8. Next transition

`CAPTURE_002_RELATION_EDGE_INSTANTIATION` remains `UNOPENED`.

AG6 remains `UNOPENED`.
