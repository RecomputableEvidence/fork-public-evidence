# Security and Data-Handling Questions

## Purpose

This document lists initial security and data-handling questions for Fork pilot discovery.

## Data classification

1. What data classifications may appear in the candidate workflow?
2. Does the workflow involve regulated, confidential, privileged, personal, financial, health, employment, security, or procurement data?
3. Are any artifacts prohibited from being copied?
4. Are any artifacts allowed to be hashed but not stored?
5. Are any artifacts allowed only as external pointers?

## Access model

1. What read-only access model is acceptable?
2. Can exports be provided manually?
3. Can file drops be used?
4. Can API pulls be considered later?
5. Are service accounts allowed?
6. Are production credentials prohibited during discovery?

## Retention

1. How long may discovery artifacts be retained?
2. Which artifacts must not leave client systems?
3. Which artifacts must be redacted?
4. Which artifacts may be represented only by hash?
5. Which artifacts must be destroyed after review?

## Security review

1. Who owns security review?
2. Who owns vendor-risk review?
3. Who approves data-handling assumptions?
4. Who approves access to source-system exports?
5. Who owns incident response if preservation reveals a gap?

## Boundary rule

Fork discovery should not request broader access than needed to determine pilot suitability.

Read-only and out-of-band posture must be preserved.