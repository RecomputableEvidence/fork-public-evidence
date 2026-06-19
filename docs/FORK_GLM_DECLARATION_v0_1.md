# Fork GLM Declaration v0.1

This package publishes a repo-local Governance Layer Manifest declaration for Fork.

The declaration is intended to make Fork's governance boundaries inspectable by GLM-style tooling:

- what Fork claims;
- what Fork explicitly does not claim;
- where Fork sits on the timing axis;
- where responsibility remains local;
- how Fork composes with adjacent layers;
- what downstream expansion risks are declared.

## Files

- `.well-known/governance-layer-manifest.json`
- `glm/fork_governance_layer_manifest_v0_1.json`
- `schemas/fork_glm_declaration_v0_1.schema.json`
- `tools/check_fork_glm_declaration.py`
- `tests/test_fork_glm_declaration_v0_1.py`
- `output/fork_glm_declaration/fork_glm_declaration_v0_1_check_output.json`

## Boundary

Fork is evidence-boundary infrastructure for AI-assisted governance workflows.

Fork does not validate truth, safety, compliance, legal sufficiency, policy satisfaction, risk acceptance, control effectiveness, deployment readiness, admissibility, or institutional authority.

Fork may preserve and inspect declared authority references. Authority remains local.

## Timing placement

Fork declares itself as a GLM `cross_cutting` layer because its constructs apply across multiple governance surfaces:

- at-bind claim-boundary declaration;
- post-bind claim consumption;
- post-bind / post-closure composition review;
- cross-cutting governance interoperability.

Fork is not a runtime gate, runtime approval system, policy engine, compliance oracle, or host-platform scoring system.

## Digest

The manifest includes a repo-local SHA-256 digest computed from canonical JSON with sorted keys and compact separators, excluding `manifest_digest` itself to avoid self-reference.
