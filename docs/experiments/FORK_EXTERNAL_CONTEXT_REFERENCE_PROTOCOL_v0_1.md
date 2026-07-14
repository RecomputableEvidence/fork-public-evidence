# Fork External Context Reference Protocol v0.1

The following values remain externally owned: `risk_tier_ref`, `impact_assessment_id`, `aims_process_phase`, and `required_provenance_profile_id`.

Fork may validate syntax, ownership declarations, version presence, reference resolution, and whether a declared provenance profile was mechanically satisfied. Fork may not assign risk, determine legal category, conduct or approve impact assessment, infer AIMS phase, choose the applicable profile, or declare compliance, legitimacy, safety, fairness, approval, or governance sufficiency.

Missing context is represented as `NOT_SUPPLIED`, `UNAVAILABLE`, `UNRESOLVED_BY_CHANNEL`, `NOT_APPLICABLE`, or `WITHHELD`. It is never replaced by an inferred value.
