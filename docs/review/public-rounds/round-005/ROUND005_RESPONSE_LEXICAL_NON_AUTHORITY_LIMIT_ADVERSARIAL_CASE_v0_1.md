# Round 005 Response: Lexical Non-Authority Limit Adversarial Case v0.1

Status: Engineering response receipt.
Round: Public Review Round 005.
Response class: Adversarial case filing.

## 1. Finding addressed

Round 005 demonstrated that the Day-0 checkerâ€™s non-authority language check is lexical, not semantic or negation-aware.

A sentence can contain all required boundary terms while asserting authority.

This response preserves that finding as a reproducible adversarial case.

## 2. Added artifacts

- `docs/reconstruction/adversarial/LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT_ADVERSARIAL_CASE_v0_1.md`
- `docs/reconstruction/adversarial/fixtures/LRT_DAY0_ADV_002_lexical_non_authority_limit_v0_1.json`
- updated `tools/check_longitudinal_day0_adversarial_cases_v0_1.py`

## 3. Interpretation

A pass in this adversarial checker means:

- the adversarial sentence contains all required boundary terms;
- the Day-0 checkerâ€™s lexical boundary-term function accepts the sentence;
- the sentence nevertheless asserts institutional authority;
- therefore, keyword presence must not be overread as semantic non-authority verification.

It does not mean the clean Day-0 packet asserts authority.

## 4. Current limitation preserved

The Day-0 checkerâ€™s boundary-language check verifies term presence.

It does not verify semantic negation, legal meaning, institutional effect, authorization posture, or actual non-authority.

## 5. Future response options

Future work may add:

- explicit semantic-boundary review cases;
- deny-list detection for authority assertion language;
- structured non-claim fields instead of prose-only term checks;
- reviewer-facing warnings that lexical checks are not semantic verification.

## 6. Non-authority statement

This response records a lexical checker-scope limitation. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.