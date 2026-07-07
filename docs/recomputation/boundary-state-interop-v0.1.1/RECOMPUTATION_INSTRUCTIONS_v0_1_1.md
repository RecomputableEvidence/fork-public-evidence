# Reproduction Instructions v0.1.1

These instructions are for human reviewers using the sandbox branch.

## Preferred runner

From the repo root:

`powershell
powershell -ExecutionPolicy Bypass -File scripts\run_boundary_state_human_recomputation_v0_1_1.ps1 
  -EvidencePacketZip docs\recomputation\boundary-state-interop-v0.1.1\evidence\boundary_state_interop_evidence_packet_v0_1_1.zip
`

The runner extracts the evidence packet into a local sandbox work directory, verifies top-level SHA256 entries, extracts the nested checker source artifact, runs canonical/adversarial/reviewer-regression suites, compares receipts when present, and writes a local recomputation receipt.

## Manual posture

A reviewer may ignore the runner and use the packet's own docs/REPRODUCTION_GUIDE_v0_1_1.md. If doing so, record exact commands and any deviations in HUMAN_REVIEWER_WORKSHEET_v0_1_1.md.

## Candidate payload posture

Candidate payloads under candidate-regression-payloads/ are not required tests. They are reviewer-generated triage material for future checker discussion.