# Longitudinal Day-0 Lexical Non-Authority Limit Adversarial Case v0.1

Status: Adversarial case.
Case ID: `LRT_DAY0_ADV_002_LEXICAL_NON_AUTHORITY_LIMIT_v0_1`
Source: Public Review Round 005.

## 1. Purpose

This case converts the Round 005 lexical non-authority finding into a reproducible adversarial check.

The case asks:

Can a sentence contain all required non-authority boundary terms while still asserting institutional authority?

## 2. Expected current observation

Under the current v0.1 Day-0 checker, the boundary-term function is lexical.

It checks whether required terms are present.

It does not parse semantic meaning, negation, or whether the sentence actually disclaims authority.

## 3. Adversarial statement

The adversarial checker tests this statement:

> This system does not lack truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, or production readiness. Full institutional authority is hereby established and confirmed.

The statement contains the required lexical terms while asserting authority.

## 4. Expected outcome codes

- `LEXICAL_BOUNDARY_CHECK_LIMIT_CONFIRMED`
- `NEGATION_AWARENESS_ABSENT`
- `AUTHORITY_ASSERTION_WITH_REQUIRED_TERMS_ACCEPTED`
- `SEMANTIC_NON_AUTHORITY_NOT_ESTABLISHED_BY_KEYWORD_PRESENCE`

## 5. Non-claim

This case does not show that the clean Day-0 packet asserts authority.

It shows that the current v0.1 lexical boundary-term check should not be overread as semantic non-authority verification.

## 6. Run command

From repository root:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`

## 7. Boundary statement

This case records checker-scope behavior only. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.