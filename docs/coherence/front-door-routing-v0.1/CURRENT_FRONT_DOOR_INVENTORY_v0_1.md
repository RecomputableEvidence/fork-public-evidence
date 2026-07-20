# Current Front-Door Inventory v0.1

Status: `DRAFT_COHERENCE_INVENTORY`

Change effect: orientation analysis only. This inventory does not amend Fork's claims, evidence, authority boundaries, experiment controls, admission standing, or historical records.

## Exact source

- Repository: `RecomputableEvidence/fork-public-evidence`
- Source commit: `1241c0084900f2c60f362205525464582e57b4a7`
- Source root-README blob: `bba793a057a4337b84c6fd8ac8473369ae8b7171`
- Source root-README length: 410 lines

## Present front-door shape

The current root README contains strong boundary language and many useful destinations, but it has accumulated multiple appended routing blocks. A new visitor is given a reviewer-first entry at the top, while proof, buyer, research, adversarial, experimental, and platform-specific routes appear later and are repeated in several forms.

## Present first-click destinations

| Current surface | Primary visitor intent | Present location or treatment | Routing observation |
|---|---|---|---|
| `docs/REVIEWER_START_HERE_v0_1.md` | External review | Top-level `Start here` and repeated later | Clear reviewer route; other roles are not equally visible. |
| `docs/REVIEWER_ROUTING_GUIDE_v0_1.md` | Additional reviewer routing | Early `Start Here` section | Adds reviewer choice but does not provide a role-neutral front door. |
| `docs/research/ACCOUNTABLE_HANDOFF_INTEROPERABILITY_POSITION_PAPER_v0_1.md` | Research context | Early research section | Useful but presented before the canonical proof path. |
| `docs/VERIFICATION_COMMANDS_v0_1.md` | Structural verification | Mid-page verification section | Verification is visible, but the one-command public verifier appears much later. |
| `docs/commercial/` | Commercial orientation | Mid-page commercial section | Broad directory route rather than a single bounded first action. |
| `docs/modular-surface/` documents | Architecture | Mid-page modular-surface block | Strong architecture route, but several paths are code-formatted rather than first-click links. |
| `docs/architecture/FORK_MATURITY_AND_TERMINOLOGY_BOUNDARY_v0_1.md` | Maturity boundary | Mid-page maturity block | Important limitation is not integrated with the initial value proposition. |
| `docs/recomputation/boundary-state-interop-v0.1.1/README.md` | Human recomputation | Mid-page sandbox section | Useful specialist route, not identified by visitor role. |
| `docs/exterior-observations/` | Exterior observations | Mid-page experiment section | Negative and interpretive evidence is visible but not indexed as one route. |
| `docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md` | Review interpretation | Later review-posture block | Critical anti-overread guidance appears after substantial architecture material. |
| `docs/commercial/BUYER_QUICK_START_GC_CISO_RISK_v0_1.md` | Governance or buyer review | Later buyer-facing block | Strong bounded destination; should be a top-level role route. |
| `docs/CURRENT_PROOF_SURFACE_v0_1.md` | Current proof index | Later proof-surface block | Canonical proof index appears after more than half of the README. |
| `scripts/verify_public_review_package_v0_1.ps1` | One-command verification | Later proof and quickstart blocks | Canonical verifier is repeated, but not placed immediately after the opening explanation. |
| `docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md` | Five-minute reviewer path | Later quickstart block | Appropriate canonical reviewer action; should be surfaced near the top. |
| `docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md` | Linux/macOS fallback | Later platform block | Important distinction is preserved but not connected directly to the primary command. |
| Longitudinal Day-0 adversarial cases and checkers | Negative evidence | Several later blocks | Findings are preserved, but visitors must scan multiple sections to locate them. |
| Longitudinal replay and schema-scope records | Limitations and replay | Several later blocks | High-value negative and bounded evidence is visible but fragmented. |
| `docs/experiments/FORK_EXPERIMENTAL_EXTENSION_PROTOCOL_v0_1.md` and state surfaces | Experimental standing | Final block | Current experiment orientation is separated from the opening research-status statement. |

## Coherence findings

### 1. The first route is role-specific rather than role-neutral

The top of the README sends every visitor to the reviewer path. Reviewers are well served, but contributors, governance readers, researchers, and first-time evaluators must infer their own route.

### 2. Proof is not presented immediately after the claim

The canonical public verifier and current proof-surface index exist and are repeatedly referenced, but the visitor encounters substantial doctrine and architecture before reaching them.

### 3. Boundaries are strong but repeated

The README repeatedly protects the same non-authority boundary. The repetition is substantively useful but creates a long front door and makes it harder to distinguish invariant language from surface-specific exclusions.

### 4. Negative evidence is preserved but distributed

Adversarial findings, schema limitations, temporal replay evidence, exterior observations, and unresolved experiment standing remain visible. They are not currently exposed through one clearly labeled limitations and negative-evidence route.

### 5. Several destinations are paths rather than links

Code-formatted repository paths are understandable to experienced GitHub users but create avoidable first-click friction for moderately computer-literate visitors.

### 6. Contribution has no equal first-click route

The root README does not presently provide one bounded contributor action comparable to the reviewer quickstart or buyer quickstart.

### 7. Current state and explanatory narrative can drift independently

The repository contains machine-readable state and sequence projections, while the README also carries narrative status statements. The front door should route to canonical state rather than duplicate fast-changing standing in prose.

## Proposed top-level routes

The replacement front door should expose these destinations before deep architecture:

1. Understand Fork in plain language.
2. Run the canonical public verifier.
3. Inspect one compact example artifact.
4. Review the current proof and limitations.
5. Choose a reviewer, contributor, governance-reader, or researcher path.
6. Ask a bounded question or file an observation.

## Preservation requirements

The coherence change must not:

- delete or rewrite the underlying evidence records;
- conceal adversarial findings, residuals, corrections, or unresolved states;
- convert a passing structural check into truth, approval, authorization, compliance, or readiness;
- replace canonical machine-readable state with README prose;
- describe a draft, candidate, or unadmitted artifact as admitted;
- alter Pair-001 execution standing or retry authority;
- use visual hierarchy to imply stronger standing than the source artifact establishes.

The intended operation is routing: keep the detailed surfaces, reduce first-click ambiguity, and direct each visitor to the smallest bounded artifact that supports the next action.