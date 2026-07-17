# Consumer-Owned Claim Admission Control v0.1

**Control ID:** `FORK_CONSUMER_OWNED_CLAIM_ADMISSION_POLICY_v0_1`

**Status:** `PROPOSED_FOR_ADMISSION`

**Failure class addressed:** `CCF-001_AI_CHANGE_READINESS_PROMOTION`

## Purpose

This control separates a producer's representation about a candidate change from the evidence the repository consumer uses to decide whether the candidate is eligible for review. A passing structural result does not grant repository standing, approve a merge, establish semantic correctness, certify security, or determine producer intent.

## Trusted-base execution

The `pull_request_target` workflow executes the checker and policy from the pull request's base commit. Candidate Git objects may be fetched only after repository and commit identifiers are syntactically constrained. The candidate tree is never checked out into the working directory and no candidate script, dependency declaration, action, hook, test, or configuration is executed.

Candidate workflow and governance files are parsed as untrusted data. The gate fails closed on malformed or duplicate-key YAML/JSON, mutable action references, excessive token permissions, persistent checkout credentials, self-hosted runners, missing timeouts, unhashed Python installs, untrusted pull-request expressions embedded in shell scripts, symbolic links, submodules, unsafe paths, whitespace errors, or recurrence of a quarantined live-workflow digest.

## Byte-sealed instrumentation boundary

Two pre-existing CSH instrumentation workflows are already members of the immutable `CSH-AMEND-002` freeze. Rewriting those bytes inside this stage would destroy the very instrumentation identity that the experiment checker is required to preserve. The gate therefore recognizes only their two named paths at their two freeze-bound SHA-256 digests. It verifies the digest against the trusted freeze, applies a minimum no-write/no-secret/no-self-hosted boundary, and rejects any byte change. This is an exact-digest preservation rule, not a reusable security waiver.

Those preserved workflows do not satisfy every new supply-chain control. A separately reviewed, provenance-bound successor amendment is required before experiment execution. This stage neither creates that amendment nor starts, authorizes, or changes the experiment.

## Activation boundary

GitHub loads `pull_request_target` workflows from the repository default branch. This stacked development stage does not modify `main` or repository settings, so the gate is `IMPLEMENTED_DORMANT_UNTIL_PRESENT_ON_DEFAULT_BRANCH`. It must not be represented as an active required check until the preservation lineage is admitted to the default branch through separate authority, the workflow completes successfully there, and an administrator independently verifies its exact check name.

## Separation of responsibilities

The automated gate establishes only `REVIEW_ELIGIBLE_NOT_ADMITTED`. CODEOWNERS identifies accountable reviewers for control surfaces. The proposed branch ruleset binds required reviews and status checks only after a repository administrator independently verifies the check names and applies the setting through a separately authorized operation.

## Supply-chain treatment

New and non-sealed live workflows use full-length action commit SHAs recorded in `ACTION_PIN_REGISTRY_v0_1.json`. Python dependencies are installed from hash-locked requirement files. The two exact-digest CSH exceptions remain byte-identical pending their separately reviewed successor amendment. Dependabot may propose updates, but it receives no automatic merge authority.

## Experiment boundary

This control does not change the Cross-System Claim Handoff hypothesis, corpus, prompt packets, receiver bindings, parameters, run order, classifier, stopping rule, optimization embargo, or baseline execution state.

## Reference basis

- GitHub Secure use reference: <https://docs.github.com/en/actions/reference/security/secure-use>
- GitHub guidance for `pull_request_target`: <https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target>
