# Longitudinal Reconstruction Trial Day-0 Packet Receipt v0.1

Status: Day-0 packet receipt.
Trial: fork_longitudinal_reconstruction_trial_v0_1
Packet: LRT_DAY0_PACKET_v0_1

## 1. Purpose

This receipt records creation of the Day-0 packet for Fork's longitudinal reconstruction trial.

The Day-0 packet is the object that later Day-7, Day-30, and Day-90 replay attempts will test.

## 2. Packet Path

- docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/

## 3. Checker

- tools/check_longitudinal_reconstruction_day0_packet_v0_1.py

Run:

- python tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json

## 4. Packet Boundary

The Day-0 packet is a fixture for longitudinal reconstruction.

It preserves:

- request state;
- output state;
- human review state;
- boundary state;
- non-claims;
- expected reconstruction;
- environment manifest;
- artifact hashes;
- manifest hash sidecar;
- outer receipt.

It does not establish:

- truth;
- compliance;
- legal sufficiency;
- safety;
- authorization;
- approval;
- certification;
- endorsement;
- production readiness;
- institutional authority.

## 5. Current Limitation

The expected reconstruction provenance for v0.1 is author-declared fixture baseline, not independent external reviewer provenance.

This is intentional and must remain visible. Later Day-7, Day-30, and Day-90 replays should not treat this expected reconstruction as independent validation.

## 6. Future Work

Next stages:

- add pinned Day-0 replay checker;
- add current-checker drift comparison;
- add Day-7 replay receipt;
- add Day-30 replay receipt;
- add Day-90 replay receipt;
- add adverse longitudinal variants for packet tamper, manifest tamper, checker drift, and receipt overread.

## 7. Non-Authority Statement

This receipt does not validate Fork, certify Fork, approve Fork, establish legal sufficiency, establish compliance sufficiency, establish safety, establish production readiness, endorse Fork, or transfer authority.