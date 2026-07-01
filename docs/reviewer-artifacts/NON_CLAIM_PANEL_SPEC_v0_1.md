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
