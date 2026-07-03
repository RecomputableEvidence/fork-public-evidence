# AHI Local Verification Guide v0.3

## Purpose

This guide lets a reviewer verify the current AHI proof surface locally.

It assumes the reviewer is in the repository root.

```powershell
cd C:\N\fork-public-evidence
```

## Step 1 — Confirm clean checkout

```powershell
git status -sb
```

## Step 2 — Run main AHI proof-surface checks

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1
```

Expected ending:

```text
PASS: ahi-sim-v0.1.x simulation proof-surface checks completed.
```

## Step 3 — Run Viewer v0.1 determinism

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
```

Expected ending:

```text
Scenario count: 9
PASS: viewer builder is deterministic from a clean working tree
PASS: AHI viewer v0.1 hardening checks completed
```

## Step 4 — Run Viewer v0.2 determinism

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism
```

Expected ending:

```text
PASS: viewer v0.2 comparison builder is deterministic from a clean working tree
PASS: AHI viewer v0.2 comparison mode checks completed
```

## Step 5 — Confirm repository remained clean

```powershell
git diff --check
git status -sb
```

## What this establishes

These checks establish that the AHI proof surface is structurally present, bounded, parseable, internally aligned, non-authority preserving, and deterministically rebuildable.

## What this does not establish

These checks do not establish legal sufficiency, regulatory compliance, admissibility, approval, authorization, safety, correctness, negligence, excuse, external acceptance, or execution eligibility.
