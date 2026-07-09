# Retrieval Fidelity Guide v0.1.2

Identifier: RETRIEVAL_FIDELITY_GUIDE_v0_1_2
Status: Draft
Classification: Instrumentation guidance

## Purpose

This guide records how observers should report what they actually accessed.

The Exterior Observance Experiment must distinguish:

- requested files;
- files actually inspected;
- access method used;
- failed access modes;
- stale or partial retrieval;
- source substitution;
- prompt echo;
- conclusions grounded in adjacent surfaces.

## Required access-mode reporting

Each LLM or automated observer should report:

- GitHub-rendered link access: succeeded / failed / not attempted
- raw link access: succeeded / failed / not attempted
- plaintext packet access: succeeded / failed / not attempted
- repository clone: succeeded / failed / not attempted
- pasted-content access: succeeded / failed / not attempted

## Retrieval fidelity classifications

Use these classifications when appropriate:

- access_mode_failure
- plaintext_packet_required
- source_substitution
- stale_or_partial_retrieval
- prompt_echo_risk
- surface_misattribution
- retrieval_scope_unclear
- retrieval_fidelity_sufficient

## Source substitution

Source substitution occurs when an observer is asked to inspect the experiment apparatus but instead inspects:

- top-level README material;
- release notes;
- project landing pages;
- mirror repositories;
- search snippets;
- generated summaries;
- adjacent documentation.

Source substitution is useful observance data, but it must not be treated as a full-surface observance pass.

## Stale or partial retrieval

A stale or partial retrieval occurs when an observer claims to inspect the surface but misses expected current content.

The intake process should preserve the observation while marking the retrieval limitation.

## Non-endorsement

Retrieval success or failure does not imply endorsement, validation, certification, approval, production readiness, legal sufficiency, or compliance sufficiency.
