# Configuration Output Targets

## Purpose

This file identifies what Fork should be able to produce if the returned discovery packet is reviewable.

## Desired Fork outputs

- [x] client evidence boundary packet
- [x] source-system map
- [x] evidence artifact map
- [x] state transition map
- [x] sidecar bridge specification
- [x] normalizer requirements
- [x] packet manifest requirements
- [x] verification result requirements
- [x] reviewer report requirements
- [x] acceptance criteria
- [x] implementation blockers
- [x] pilot-ready implementation scope
- [ ] other: Not used

## Reviewer audiences

- [x] legal
- [x] compliance
- [x] audit
- [x] risk
- [x] security
- [x] GRC
- [x] enterprise AI governance
- [x] workflow owner
- [x] technical integration owner
- [x] executive sponsor
- [ ] external reviewer
- [ ] other: Not used

## Required verification states

- [x] PASS
- [x] FAIL
- [x] NOT_CHECKED
- [x] PARTIAL
- [x] STALE_CONTEXT
- [x] OUT_OF_SCOPE
- [x] SOURCE_UNAVAILABLE
- [ ] UNKNOWN

## Candidate bridge pattern

- [x] manual export bridge
- [x] file-drop bridge
- [ ] watch-folder bridge
- [ ] API pull bridge
- [x] hybrid reference bridge
- [ ] unknown
- [ ] not yet selectable

Reason:

Manual export and file drop are sufficient for the initial synthetic pilot. Hash-only and external-pointer handling are needed for restricted vendor attachments.

## Implementation blockers

None

## Success criteria for discovery

Fork can draft a client evidence boundary that separates captured evidence, hashed references, external pointers, source unavailable items, explicit non-claims, state transitions, and institutional response ownership.