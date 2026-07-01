# Fork Non-Claim Panel Specification v0.1

## Purpose

The Non-Claim Panel is Fork's signature reviewer-facing feature. It makes explicit what a sealed record does not establish.

This prevents preserved evidence from silently becoming broader authority.

## Required packet file

Every Fork packet MUST include:

`non_claims.json`

## Minimal structure

```json
{
  "version": "0.1.0",
  "not_established": [
    "This record does not certify legal sufficiency.",
    "This record does not establish vendor approval.",
    "This record does not certify model correctness.",
    "This record does not establish regulatory compliance.",
    "This record does not transfer upstream authority.",
    "This record does not prove underlying sources were true.",
    "This record preserves only the bounded evidence and reliance structure."
  ]
}
```

## Required rendered title

Every reviewer-facing artifact MUST render a section titled:

> Not Established by This Record

## Required appearances

The Non-Claim Panel MUST appear in:

- Evidence Card
- Review Packet
- Verification Receipt
- Replay / Recompute View, if present

## Verifier behavior

The verifier SHOULD:

- fail if `non_claims.json` is missing;
- warn or fail if `not_established` is empty;
- display non-claims by default;
- include a non-claim summary in the Verification Receipt.

## Boundary discipline

The Non-Claim Panel does not weaken the record. It preserves the boundary of the record.

Fork's doctrine is:

> Preservation without inheritance.

That doctrine becomes operational when every packet states what the record does not establish.

## Human-readable rendering

Reviewer-facing packets SHOULD include a human-readable Markdown rendering of the machine-readable `non-claims.json` file.

For examples and review packets, this rendering may appear as `NON_CLAIMS_PANEL.md`.

The Markdown rendering is not a replacement for the machine-readable non-claim record. It is the reviewer-facing surface that allows legal, compliance, audit, risk, governance, procurement, security, and executive reviewers to see which tempting downstream inferences are not established by the packet.

A conformant rendering should identify:

- the tempting inference;
- that the inference is not established;
- why the packet does not establish it;
- what external authority, review, approval, or evidence would be required before relying on it;
- the relevant boundary-map reference where applicable.

## Authority and policy context non-claim

The Non-Claim Panel SHOULD include a non-claim covering authority and policy context when the packet records an institutional review, acceptance, approval, memo, recommendation, or reliance event.

Required substance:

This record preserves the stated authority and policy context associated with the review, acceptance, or reliance event. It does not establish that the reviewer had sufficient institutional authority, that the policy was adequate, that the review was complete, or that the resulting decision satisfied legal, compliance, audit, procurement, security, risk, executive, or regulatory requirements.
