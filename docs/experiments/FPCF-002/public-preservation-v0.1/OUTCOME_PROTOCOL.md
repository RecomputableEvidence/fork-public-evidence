# FPCF-002 — Append-only resolution and comparison protocol v0.1

Status: proposed future adjudication process; no forecast results established here.

1. **Locate the original** by participant archive SHA-256, case ID, original source/predecision/final byte digests, and public bundle SHA-256. Do not edit the original or reinterpret it using later facts.
2. **Close the event window** according to that forecast's original criteria. Record both the event date and the publication/retrieval time of each source. Capture accessible original-source bytes and digest only if retrieved; otherwise declare citation-only.
3. **Apply original YES / NO / UNRESOLVED criteria** literally. If the rules are incoherent, the event predates publication, or no valid outcome can be determined, log `INVALID` or `UNRESOLVED`, not a favorable reinterpretation. `NO` means evidence satisfies the original specified negative condition, not merely absence of a positive source.
4. **Record dissent** with evidence, reviewer identity/independence and scope, whether causal uncertainty can change outcome, alternative interpretations and exact limitations. Do not turn public comments or social proof into authority.
5. **Score** resolvable binary forecasts with Brier score `(p_yes - observed_yes)^2` (0 best, 1 worst); report counts for missing / unresolved / invalid forecasts separately and analysis excluding them. Declared probabilities are not changed. Use proper scoring and confidence intervals where samples permit. Predefine comparison bases and do not present 6 arbitrary heterogeneous events as a causal proof.
6. **Compare the arms** only with source-date and event-selection limitations in view. The arms share a model family; A/B self-selected different questions; C had previous exposure. Future matching/randomization studies are distinct experiments.
7. **Publish one additive result per case** under a new event-specific identifier (and GitHub server timestamp), containing the original artifact pointer, rule references, source evidence, method of determination, disposition, calculations, and correction/dissent references. Existing public commits are never rewritten for outcome narratives.

**Minimum outcome fields:** `parent_commit`, `parent_bundle_sha256`, `arm`, `case_id`, `original_forecast_record_sha256`, `original_probability`, `original_yes_rule`, `original_no_rule`, `observed_event_date`, `source_publication_time`, `resolution_record_time`, `source_urls`, `source_byte_digests_if_available`, `method`, `reviewer_and_independence`, `disposition`, `reasoned_basis`, `challenge_or_dissent`, `invalid_or_unresolved_reason`, `brier_if_resolvable`, `nonclaims`.

No automatic resolution or publishing automation is configured by this document.