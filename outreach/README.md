# Outreach Templates

## Purpose

This directory contains public-safe outreach templates for Fork.

These templates support selective outreach after the public review surface, buyer conversion layer, and enterprise PoV packet have been established.

## Boundary

Do not commit populated outreach trackers.

Do not commit:

- target names;
- private relationship notes;
- warm-introduction sources;
- prospect research;
- reply details;
- private contact information;
- commercial negotiation notes;
- non-public buyer context.

Use `outreach/templates/` for public-safe structures only.

Use `outreach/private/` for local working files. That directory is ignored by `.gitignore`.

## Public-safe files

- `outreach/templates/OUTREACH_TARGET_MAP_TEMPLATE_v0_1.md`
- `outreach/templates/OUTREACH_PATH_ASSIGNMENT_TRACKER_TEMPLATE_v0_1.csv`

## Private working file

The patch creates:

- `outreach/private/OUTREACH_TARGET_MAP_PRIVATE_v0_1.md`

This file is ignored and should remain local unless intentionally moved into a private workspace.
