# viewer-hardening-v0.1.2

This package adds structural hardening for the static AHI viewer:

- `scripts/check_ahi_viewer_v0_1.ps1`
- `docs/viewer/ahi-viewer-v0_1/schema/scenarios_bundle.schema.json`
- `examples/simulations/governance-proof-surface/scenario_registry.schema.json`

The checker verifies required viewer files, deterministic bundle posture, scenario count alignment, posture enum discipline, artifact-path existence, selected-field shape, checker-coverage shape, JavaScript safety constraints, non-authority posture language, and optional deterministic rebuild behavior.

It does not approve, certify, score, authorize, or judge correctness.
