# Repository-Hygiene / Publication-Readiness Successor Object — Inventory v0.1

**Status:** CANDIDATE — inventory-only successor. Admission is effective only on merge of the associated admission PR. Until then, this object changes no standing.

## Observation coordinate

Repository observations in this inventory are bounded to:

- branch: `main`
- commit: `d7af7fabc14f87df52384c21b22ac47094c7151c`
- tree: `877673093e289c62af35a71bd0b6c643d5508825`
- repository state: merge of PR #179
- observation date: `2026-09-24`

This observation coordinate does **not** move the representational horizon of `FORK_CURRENT_WORK_REGISTER_v0_9`, which remains bounded through PR #178 at commit `115992d750f0e893d07b61dbb6d584c87dc64d5d`.

`INVENTORY_OBSERVATION_COORDINATE != CURRENT_STANDING_REGISTER_HORIZON`

## Purpose

To freeze, in one bounded inventory, residuals identified by convergent exterior review and repository inspection on 2026-09-24 so that any later hygiene or publication-readiness work preserves the evidence for why a change was considered, rather than erasing that evidence through the change itself.

## Boundary

This object **inventories**. It does not:

- fix any item;
- assign priority or order among items;
- modify any workflow, schema, branch, tag, or standing record;
- admit, qualify, close, merge, or reopen any PR or research gate;
- convert exterior review commentary into authority for Fork's claims;
- authorize repository cleanup, branch deletion, schema relocation, license change, verifier replacement, attestation, archival publication, or experiment execution.

## Inventory of residuals

### R1 — Public-governance surface

- **R1.1** No standard machine-recognized root `LICENSE` file is present, and GitHub reports `Other / NOASSERTION`. `COPYRIGHT.md` already establishes an all-rights-reserved bounded public-inspection, citation, technical-review, and recomputation posture. Whether to adopt or add a standard code/content license remains unresolved.
- **R1.2** No root `SECURITY.md` or repository-native vulnerability-disclosure channel is established.
- **R1.3** No current root contribution policy or explicit maintainer/review-boundary statement is established on `main` at this coordinate.
- **R1.4** No `.github/CODEOWNERS` file is present. Decision boundary: CODEOWNERS must not be added merely to simulate independent review that does not exist.
- **R1.5** GitHub Issues and Discussions are disabled, and `.github/` contains workflows only; no repository-native structured exterior-observation intake is established.

### R2 — Repository topology

- **R2.1** Two schema roots are present: singular `schema/`, containing `observed-evidence-packet.schema.json`, and the larger governed `schemas/` population. A reference/binding audit has not yet established whether the singular path is historical-only, still active, or safely relocatable. No relocation is authorized by this inventory.
- **R2.2** Parallel top-level content surfaces including `spec/`, `docs/`, `research/`, and `reports/` are present. Their semantic overlap, historical necessity, and reviewer-routing burden have not yet been audited as one bounded topology question.
- **R2.3** The repository exposes 205 branches at this observation coordinate. No repository-wide branch lifecycle classification (`active / preserved / closed / superseded`, or another frozen vocabulary) is established. v0.9's dated open-PR snapshot does not confer a branch-lifecycle classification.
- **R2.4** Exterior review reported a population of 118 tags. This inventory does not treat that count as repository-bound fact until a separately preserved tag-population snapshot is made. No semantic distinction between evidence-boundary tags and convenience tags is currently admitted by this object.

### R3 — Publication / recomputation hardening

- **R3.1** The named public verifier entry point remains PowerShell. Linux/macOS public-verifier reconstruction is documented separately, while an existing Python verification core already executes on Ubuntu and Windows in CI. The residual is therefore public-entry-point unification, not absence of cross-platform verification logic.
- **R3.2** No macOS CI runner coverage is established for the integrated proof-surface verifier at this coordinate.
- **R3.3** No Fork-wide release manifest is admitted that binds one publication package to a specific subject commit, standing coordinate, schema/verifier identities, expected-result identity, limitations, and release checksum coordinates.
- **R3.4** No release-package artifact attestation layer (for example GitHub artifact attestations / Sigstore-style provenance) is established by this inventory.
- **R3.5** No SBOM is established for a bounded Fork research-release verification toolchain.
- **R3.6** No externally archived/citable release coordinate such as a DOI is established by this inventory.
- **R3.7** No governed research-object packaging layer such as RO-Crate is established by this inventory. Research-object packaging is distinct from an archival DOI or citation coordinate.

### R4 — Scientific progression (conditional; no new lineage)

- **R4.1** `CSH-S001-v0.1` remains the already-defined candidate for the controlled test of `E[U | H=1] < E[U | H=0]`. Existing narrower measurement/coding and execution-record freezes retain their own scope. Hosted access remains blocked; receiver registry and run order remain unfrozen; corpus execution is not established. No parallel successor experiment is created by this inventory.
- **R4.2** The residual recorded here is only completion or disposition of the already-existing CSH-S001 gates if their prerequisites become satisfied. It is not authorization to execute them and not a definition of a new study.

## Preserved non-equivalences

This inventory explicitly rejects the following inferences:

- `MANY_BRANCHES != BAD_EVIDENCE_PRACTICE`
- `POWERSHELL_PUBLIC_ENTRY_POINT != WINDOWS_ONLY_REPOSITORY`
- `NO_ARTIFACT_ATTESTATION != TRUST_IS_MERELY_ASSERTED`
- `DIGEST_VERIFIED != PROVENANCE_ATTESTED != SEMANTICALLY_CORRECT`
- `INVENTORY_ADMITTED != ITEM_DISPOSITIONED != CHANGE_AUTHORIZED`

The Run 003 LF/CRLF serialization event remains preserved evidence of a diagnosed serialization failure, misleading unconditional shell output, clarified byte convention, and recovered recomputation. This inventory does not reinterpret that event as evidence of inadequate tooling.

## Non-claims

- Inventory presence does not imply deficiency admission beyond the recorded bounded observation.
- Listing an item does not authorize any change to it.
- Admission of this object would not validate, qualify, endorse, or adopt any exterior review.
- Exterior review commentary remains exterior observation, not authority or standing.
- Absence of an item at this coordinate does not establish that the item is universally required.
- Repository hygiene does not strengthen any research result.
- Publication provenance does not establish semantic correctness, truth, authority, compliance, legal sufficiency, deployment readiness, or institutional approval.

## Next evidence-bearing gate — inventory admission only

If the associated admission PR is merged, this inventory is admitted only as a bounded record of the residual surface observed at the coordinate above.

Admission assigns **no R-item disposition** and authorizes **no repository change**.

Any later per-item decision must occur in a separately named disposition successor that preserves the inventory and may record one of the following only after its own review boundary is established:

- `FIX`
- `DEFER`
- `PRESERVE_AS_HISTORICAL`
- `REJECT_WITH_REASON`

No disposition is made here.

`INVENTORY_ADMITTED != ITEM_DISPOSITIONED != CHANGE_AUTHORIZED`
