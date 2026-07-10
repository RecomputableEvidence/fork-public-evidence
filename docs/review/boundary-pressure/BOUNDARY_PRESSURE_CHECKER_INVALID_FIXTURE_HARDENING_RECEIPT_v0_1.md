# Boundary Pressure Checker Invalid-Fixture Hardening Receipt v0.1

Status: Hardening receipt.
Scope: Boundary-pressure checker invalid-fixture semantics.
Classification: Engineering response to Public Review Round 004 adversarial observation.

## 1. Background

Public Review Round 004 produced an execution/recomputation/adversarial observation against the boundary-pressure checker.

The finding was narrow:

- the shipped fixtures were honestly authored;
- the public verifier was runnable;
- the default boundary-pressure suite passed;
- however, invalid fixture branches could classify negative fixtures by placement or self-declaration rather than fully content-gating the invalid condition.

## 2. Hardening Change

The checker now separates:

- `evaluation_ok`: whether the checker recognized and evaluated the fixture semantics;
- `actual_valid`: whether the fixture is boundary-valid;
- `passed`: whether the fixture result matches the expected suite role.

Invalid fixtures now pass the default suite only when the invalid condition is actually detected.

Malformed, mislabeled, content-free, valid-shaped-negative, or unknown-family fixtures must not silently pass.

## 3. Adversarial Regression Fixtures

The hardening adds adversarial fixtures under:

- `docs/review/boundary-pressure/fixtures/adversarial/`

The adversarial regression suite tests that the checker refuses to silently accept:

- retrieval limitation content filed as invalid without explicit upgrade signal;
- near-empty recomputation receipt overread fixtures;
- invalid recomputation receipt overread fixtures without overread flags;
- unknown fixture families that would otherwise rely on placement or self-declaration.

## 4. Commands

Default boundary-pressure suite:

- `python tools/check_boundary_pressure_review_cases_v0_1.py --json`

Default plus adversarial regression suite:

- `python tools/check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial`

Public verifier:

- `powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1`

## 5. Boundary Statement

This hardening does not validate Fork, certify Fork, approve Fork, establish legal sufficiency, establish compliance sufficiency, establish safety, establish production readiness, or transfer authority.

It narrows the checker claim by ensuring invalid fixture pass status depends on detected boundary-pressure content rather than placement or self-declaration alone.