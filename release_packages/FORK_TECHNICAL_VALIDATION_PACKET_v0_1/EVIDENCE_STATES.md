# Evidence States

## Purpose

This document provides a public orientation to evidence-state language used in Fork materials.

These states are not legal conclusions.

These states are not compliance conclusions.

These states do not prove decision correctness.

## Core states

### PASS

The checked artifact or package satisfies the declared verification boundary.

### FAIL

The checked artifact or package does not satisfy the declared verification boundary.

### NOT_CHECKED

The condition was not checked.

A NOT_CHECKED state must not be interpreted as PASS.

## Audit-facing qualifiers

### PARTIAL

Some expected or relevant evidence is present, but the boundary is incomplete or only partially represented.

### STALE_CONTEXT

The preserved record may still verify, but some referenced context may have changed, expired, or become stale.

### OUT_OF_SCOPE

The claim or question exceeds the declared evidence boundary.

### SOURCE_UNAVAILABLE

A source, artifact, or reference needed for fuller review is unavailable.

## Boundary rule

No evidence state should be interpreted beyond its declared verification boundary.

PASS does not mean correct.

FAIL does not mean wrongdoing.

NOT_CHECKED does not mean safe.

PARTIAL does not mean invalid.

STALE_CONTEXT does not mean false.

OUT_OF_SCOPE does not mean noncompliant.

SOURCE_UNAVAILABLE does not mean concealed.

Each state identifies what can and cannot be responsibly inferred from the preserved record.