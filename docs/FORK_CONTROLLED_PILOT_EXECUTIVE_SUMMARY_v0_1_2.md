# Fork Controlled Pilot Executive Summary v0.1.2

## Purpose

Fork is being proposed as an out-of-band evidence-boundary sidecar for an existing workflow.

Fork is closer to an evidentiary flight recorder than a co-pilot: it records how claims, limits, evidence references, and reliance moved, but it does not fly the plane.

The pilot is designed to observe existing workflow artifacts without changing the institution's decision process, production systems, reviewer authority, appeal process, or operational controls.

## What Fork does

Fork preserves bounded evidence packets showing what workflow artifact was observed, what evidence references were used, what claim boundary was declared, what required non-claims were preserved, what human, vendor, rules-assisted, or AI-assisted review occurred, whether downstream artifacts attempted to expand the record beyond its declared boundary, and whether the preserved packet structurally verifies later.

## What Fork does not do

Fork does not decide outcomes or certify source truth, medical correctness, legal admissibility, regulatory compliance, lawfulness, completeness, clinical appropriateness, institutional approval, runtime authorization, reviewer judgment, or utilization-management sufficiency.

Fork/RGV `PASS`, `FAIL`, and `INDETERMINATE` are structural postures only.

## Recommended first pilot workflow

The recommended first pilot candidate is prior authorization denial + internal appeals review.

This workflow already produces durable artifacts, operates under defined criteria, involves bounded human or vendor-assisted review, creates records that matter to legal/compliance/audit/risk teams, and has downstream overclaim risk that is structurally possible without requiring the institution to concede process defectiveness.

## Required pilot gates

Three named pilot artifacts must be completed before live ingestion is authorized:

1. Redaction Scope Artifact
2. Pilot Canonicalization Record
3. Dry-Run Approval Artifact

A Written Orientation Artifact should also acknowledge that Fork/RGV posture terms are structural only.

## Executive framing

Fork preserves the boundary of what workflow evidence is allowed to mean.

The pilot is not asking the institution to change how it decides. It is asking whether existing workflow artifacts can be preserved in a way that makes downstream overclaiming visible, reviewable, and structurally bounded.
