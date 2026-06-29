# Receipts Boundary

## Status

This directory contains cryptographic and integrity-oriented receipts for public Fork artifacts.

In this repository, "receipt" means an evidence-preservation or integrity record, such as a checksum, digest, manifest reference, seal reference, or detached verification artifact.

## What these receipts may support

Receipts may support bounded review of:

- artifact identity;
- byte-level integrity;
- manifest membership;
- checksum recomputation;
- declared package or disclosure relationships;
- preservation of verification status where explicitly stated.

## What these receipts do not establish

Receipts in this directory are not:

- payment receipts;
- purchase confirmations;
- customer transaction records;
- deployment confirmations;
- procurement records;
- customer acceptance records;
- production-operation records;
- legal-admissibility determinations;
- compliance certifications;
- audit opinions;
- security certifications;
- non-repudiation guarantees unless separately established;
- public signer-identity proof unless separately established.

## Interpretation rule

A receipt establishes only the bounded integrity or preservation condition declared by that receipt.

It must not be interpreted as proof that the underlying source event was true, complete, lawful, compliant, approved, independently witnessed, customer-deployed, or production-ready.
