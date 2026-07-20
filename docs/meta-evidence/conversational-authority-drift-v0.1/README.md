# Fork Conversational Authority Drift Candidate v0.1

Status: `CANDIDATE_NOT_ADMITTED`

This candidate adds a bounded meta-evidence case format for inspecting whether an AI-assisted exchange preserves the standing, provenance, and role of supplied context artifacts.

The candidate does not determine whether an underlying invention is technically correct. It records what material was supplied, what a reviewer said about that material, which statements were supported or contradicted by the preserved record, and what remains unresolved.

## Initial case

`CAD_004_CLAUDE_SOURCE_ROLE_BINDING` records a review sequence in which:

- a Markdown source artifact was visibly attached;
- the reviewer later read and analyzed that artifact;
- the reviewer nevertheless stated at other points that the artifact had not been supplied or was unavailable;
- a companion text file's evidentiary role was repeatedly mischaracterized;
- useful technical findings were still produced from the actual source;
- the user corrected the source-role mapping and required the same scrutiny to be applied to the reviewer, Fork, and the user.

The case preserves both the valid findings and the reviewer-side errors. It does not treat the exchange as uniformly correct or uniformly defective.

## Boundaries

This candidate:

- publishes no raw private conversation artifact;
- records only filenames, byte lengths, SHA-256 digests, source roles, bounded claims, and non-claims;
- makes no prevalence or novelty claim;
- creates no provider call authority;
- does not affect Pair-001 standing or execution;
- does not admit the case into the preservation lineage merely by existing in a pull request;
- does not canonize the candidate classifications.

See `FORK_CAD_RESEARCH_PROTOCOL_v0_1.md` and the case record for the exact method.
