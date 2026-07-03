Fork

Fork is evidence-boundary infrastructure for AI-assisted workflows. It preserves a reviewer-operable record of what was requested, what AI produced, what humans reviewed or changed, what evidence was referenced, what was explicitly not claimed, and whether the sealed packet still verifies later.

Fork does not certify truth, compliance, safety, legal sufficiency, model quality, or vendor approval. It preserves what the record can legitimately be said to establish, and what it explicitly does not establish.

What Fork is

Fork is designed to preserve the evidence boundary around AI-assisted institutional work.

It provides reviewer-facing artifacts for AI-assisted workflows, including:

- Evidence Card
- Boundary Map
- Verification Receipt
- Review Packet
- Non-Claim Panel

Fork helps reviewers answer:

> When an AI-assisted output became a basis for action, what exactly did the organization rely on, and does that record still verify?

What Fork is not

Fork is not:

- an AI governance platform;
- a compliance automation system;
- a model monitoring or observability tool;
- a runtime policy engine;
- an explainability or truth-certification system;
- a replacement for GRC, legal judgment, audit judgment, or governance programs.

Fork does not:

- certify legal sufficiency;
- establish regulatory compliance;
- declare vendor approval;
- prove model correctness;
- guarantee safety;
- transfer authority from one record to another.

Fork's doctrine is:

> Preservation without inheritance.

Golden workflow

The current golden workflow is:

> AI-assisted vendor-risk recommendation → internal decision memo → downstream reliance attempt.

This workflow demonstrates the moment an AI-assisted artifact becomes eligible for institutional reliance and the downstream risk that a bounded record may be silently expanded into a broader claim.

See:

- examples/vendor-risk/

Reviewer artifacts

Reviewer-facing artifacts are defined under:

- docs/reviewer-artifacts/

The current artifact set includes:

- Fork Evidence Card
- Fork Boundary Map
- Fork Verification Receipt
- Fork Review Packet
- Fork Non-Claim Panel

Pilot

The current buyer-facing pilot is:

> One bounded AI-assisted workflow. One sealed evidence packet. One verification path. One reviewer-facing closeout report.

See:

- docs/pilots/FORK_RELIANCE_EVIDENCE_PILOT_v0_1.md

Proof surface

Technical and proof-layer materials live under:

- docs/proof/

The proof surface may document schemas, checkers, fixtures, receipts, reproducibility materials, and boundary discipline. These mechanisms support the reviewer-facing product surface but should not be required for a reviewer to understand what Fork preserves.