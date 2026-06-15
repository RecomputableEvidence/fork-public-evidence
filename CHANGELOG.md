# Changelog

<!-- FORK_CHANGELOG_AI_GOVERNANCE_MAPPING_RECORD_V0_2_2 -->

## AI Governance Mapping Record checker hardening v0.2.2

Final stabilization patch.

Added:

- static machine-readable error codes for failed checks;
- local multi-hop safe-handoff cycle detection within one record;
- parser-boundary fuzz fixtures and tests;
- large-record performance smoke test;
- normalized output comparison guidance;
- documentation overclaim-language regression coverage.

Preserved:

- v0.2.1 duplicate ID detection;
- v0.2.1 safe-handoff self-reference rejection;
- v0.2.1 combined failure-mode reporting;
- v0.2.1 schema version mismatch handling;
- v0.2.1 malformed/non-object/empty input handling;
- v0.2.1 missing schema failure behavior;
- v0.2.1 Unicode-aware restricted-claim bypass detection;
- v0.2, v0.1, and semantic alignment regression coverage.

Non-claims: v0.2.2 is not a policy engine, legal sufficiency checker, compliance checker, audit substitute, decision validator, runtime controller, cross-record DAG compiler, external artifact resolver, or semantic intent engine.
