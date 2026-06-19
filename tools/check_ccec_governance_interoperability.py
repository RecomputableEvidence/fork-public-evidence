#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import jsonschema
except Exception as exc:
    jsonschema = None
    JSONSCHEMA_IMPORT_ERROR = exc
else:
    JSONSCHEMA_IMPORT_ERROR = None

CHECKER_NAME = "check_ccec_governance_interoperability"
CHECKER_VERSION = "0.1.3"

PROHIBITED_MAPPINGS = [
    "APPROVAL_STATUS",
    "TRUTH_STATUS",
    "SAFETY_STATUS",
    "COMPLIANCE_STATUS",
    "LEGAL_SUFFICIENCY_STATUS",
    "INSTITUTIONAL_AUTHORIZATION_STATUS",
    "POLICY_SATISFACTION_STATUS",
    "RISK_ACCEPTANCE_STATUS",
    "AUTHORITY_TRANSFER",
    "CLAIM_EXPANSION_BY_MAPPING",
    "AUTOMATED_CONTROL_DECISION",
    "CONTROL_STATUS",
    "CONTROL_EFFECTIVENESS_STATUS",
    "CONTROL_SATISFIED",
    "AUTOMATED_CONTROL_SATISFIED",
    "ASSURANCE_LEVEL",
    "CONFIDENCE_LEVEL",
    "RESIDUAL_RISK_STATUS",
    "ISSUE_CLOSED_STATUS",
    "SIGN_OFF_STATUS",
    "GO_LIVE_AUTHORIZATION",
    "DEPLOYMENT_APPROVED",
    "EVIDENCE_SUFFICIENCY",
    "AUDIT_SUFFICIENCY",
    "REASONABLE_RELIANCE",
    "STANDARD_OF_CARE",
    "DELEGATED_AUTHORITY",
    "PERPETUAL_RELIANCE",
    "SOLE_EVIDENCE",
    "EXCEPTION_GRANTED",
    "WAIVER_APPROVED",
    "INHERENT_RISK_REDUCED",
    "RESIDUAL_RISK_ACCEPTED",
    "COMPENSATING_CONTROL_ACTIVE",
    "AUDIT_FINDING_CLOSED",
    "REMEDIATION_COMPLETE",
    "OPERATIONAL_READINESS",
    "DEPLOYMENT_ALLOWED",
    "CONTRACTUAL_RELIANCE_ALLOWED",
    "BOOLEAN_COERCION",
    "NUMERIC_SCORE_COERCION",
    "WEIGHTED_RISK_REDUCTION",
    "WORKFLOW_PHASE_UNLOCK",
    "NEGATIVE_GATE_CONDITION",
    "NECESSARY_CONDITION_GATE",
    "COVERAGE_PERCENTAGE_POSTURE",
    "TRAFFIC_LIGHT_RENDERING",
    "CHECKMARK_RENDERING",
    "TERMINAL_WORKFLOW_STATE",
    "DISPOSITION_MAPPING",
    "QUANTITATIVE_RISK_SCORING",
    "DATA_QUALITY_PROXY",
    "DOCUMENTATION_COMPLETENESS_PROXY",
    "METADATA_HEALTH_PROXY",
    "SLA_TIMER_COERCION",
    "SLA_MET_STATUS",
    "SLA_PAUSED_STATUS",
    "SLA_STOPPED_STATUS",
    "REVIEW_TIER_FAST_TRACK",
    "LOWER_FRICTION_QUEUE_ROUTING",
    "ROUTING_TIER_REDUCTION",
    "TRIAGE_COMPLETE_STATUS",
    "ARCHIVAL_CLOSURE",
    "PROMOTION_STATUS",
    "GOVERNANCE_READINESS_SCORE",
    "GOVERNANCE_HEALTH_INDEX",
    "REQUIRED_COVERAGE_BASELINE",
    "HOST_NATIVE_SCORING_INPUT",
    "HOST_DESIGN_SYSTEM_ASSURANCE_SIGNAL",
    "HUMAN_PROSE_GREEN_SIGNAL",
    "OUTPUT_OK_BOOLEAN",
    "CI_CD_BLOCKING_GATE",
]

DO_NOT_MAP_TO = [
    "APPROVAL",
    "APPROVED",
    "TRUTH",
    "TRUE",
    "VERIFIED",
    "SAFETY",
    "SAFE",
    "COMPLIANCE",
    "COMPLIANT",
    "CERTIFIED",
    "LEGAL",
    "LEGAL_SUFFICIENCY",
    "AUTHORITY",
    "AUTHORIZED",
    "INSTITUTIONAL_AUTHORIZATION",
    "POLICY",
    "POLICY_SATISFACTION",
    "RISK",
    "RISK_ACCEPTANCE",
    "VALID",
    "VALIDATED",
    "AUTHORITY_TRANSFER",
    "CLAIM_EXPANSION_BY_MAPPING",
    "AUTOMATED_CONTROL_DECISION",
    "CONTROL_STATUS",
    "CONTROL_EFFECTIVENESS_STATUS",
    "CONTROL_SATISFIED",
    "AUTOMATED_CONTROL_SATISFIED",
    "ASSURANCE_LEVEL",
    "CONFIDENCE_LEVEL",
    "RESIDUAL_RISK_STATUS",
    "ISSUE_CLOSED_STATUS",
    "SIGN_OFF_STATUS",
    "GO_LIVE_AUTHORIZATION",
    "DEPLOYMENT_APPROVED",
    "EVIDENCE_SUFFICIENCY",
    "AUDIT_SUFFICIENCY",
    "REASONABLE_RELIANCE",
    "STANDARD_OF_CARE",
    "DELEGATED_AUTHORITY",
    "PERPETUAL_RELIANCE",
    "SOLE_EVIDENCE",
    "EXCEPTION_GRANTED",
    "WAIVER_APPROVED",
    "INHERENT_RISK_REDUCED",
    "RESIDUAL_RISK_ACCEPTED",
    "COMPENSATING_CONTROL_ACTIVE",
    "AUDIT_FINDING_CLOSED",
    "REMEDIATION_COMPLETE",
    "OPERATIONAL_READINESS",
    "DEPLOYMENT_ALLOWED",
    "CONTRACTUAL_RELIANCE_ALLOWED",
    "BOOLEAN_COERCION",
    "NUMERIC_SCORE_COERCION",
    "WEIGHTED_RISK_REDUCTION",
    "WORKFLOW_PHASE_UNLOCK",
    "NEGATIVE_GATE_CONDITION",
    "NECESSARY_CONDITION_GATE",
    "COVERAGE_PERCENTAGE_POSTURE",
    "TRAFFIC_LIGHT_RENDERING",
    "CHECKMARK_RENDERING",
    "TERMINAL_WORKFLOW_STATE",
    "DISPOSITION_MAPPING",
    "QUANTITATIVE_RISK_SCORING",
    "DATA_QUALITY_PROXY",
    "DOCUMENTATION_COMPLETENESS_PROXY",
    "METADATA_HEALTH_PROXY",
    "SLA_TIMER_COERCION",
    "SLA_MET",
    "SLA_PAUSED",
    "SLA_STOPPED",
    "REVIEW_TIER_FAST_TRACK",
    "LOWER_FRICTION_QUEUE_ROUTING",
    "ROUTING_TIER_REDUCTION",
    "TRIAGE_COMPLETE",
    "ARCHIVAL_CLOSURE",
    "PROMOTION_STATUS",
    "GOVERNANCE_READINESS_SCORE",
    "GOVERNANCE_HEALTH_INDEX",
    "REQUIRED_COVERAGE_BASELINE",
    "HOST_NATIVE_SCORING_INPUT",
    "HOST_DESIGN_SYSTEM_ASSURANCE_SIGNAL",
    "HUMAN_PROSE_GREEN_SIGNAL",
    "OUTPUT_OK_BOOLEAN",
    "CI_CD_BLOCKING_GATE",
]

LIMITATIONS = {
    "safe_to_automate": False,
    "automation_interpretation_required": True,
    "bounded_reference_only": True,
    "synthetic_structural_checker_only": True,
    "does_not_validate_approval": True,
    "does_not_validate_truth": True,
    "does_not_validate_safety": True,
    "does_not_validate_compliance": True,
    "does_not_validate_legal_sufficiency": True,
    "does_not_validate_institutional_authorization": True,
    "does_not_validate_policy_satisfaction": True,
    "does_not_validate_risk_acceptance": True,
    "does_not_validate_control_satisfaction": True,
    "does_not_validate_issue_closure": True,
    "does_not_validate_deployment_authorization": True,
    "does_not_validate_evidence_sufficiency": True,
    "does_not_validate_reasonable_reliance": True,
    "does_not_validate_aggregation_posture": True,
    "does_not_validate_quantitative_risk_reduction": True,
    "does_not_validate_visual_assurance": True,
    "does_not_validate_workflow_transition": True,
    "does_not_validate_runtime_configuration_compliance": True,
    "does_not_validate_external_system_governance_adequacy": True,
    "does_not_transfer_authority": True,
    "not_runtime_control": True,
    "not_policy_engine": True,
    "not_compliance_oracle": True,
    "does_not_validate_host_platform_native_scoring_behavior": True,
    "does_not_validate_human_free_text_interpretation": True,
    "does_not_validate_executive_narrative_framing": True,
    "does_not_validate_sla_configuration_compliance": True,
    "does_not_validate_review_queue_routing_adequacy": True,
    "does_not_validate_data_quality": True,
    "does_not_validate_metadata_health": True,
    "does_not_validate_documentation_completeness": True,
}

NON_CLAIMS = {
    "does_not_create_approval_status": True,
    "does_not_create_compliance_status": True,
    "does_not_create_safety_status": True,
    "does_not_create_truth_status": True,
    "does_not_create_legal_sufficiency_status": True,
    "does_not_transfer_authority": True,
    "does_not_close_unresolved_gaps": True,
    "does_not_accept_risk": True,
    "does_not_create_control_satisfaction": True,
    "does_not_create_workflow_transition": True,
    "does_not_create_aggregate_posture": True,
    "does_not_create_sla_satisfaction": True,
    "does_not_create_review_tier_eligibility": True,
    "does_not_create_data_quality_status": True,
    "does_not_create_metadata_health_status": True,
    "does_not_create_documentation_completeness_status": True,
    "does_not_create_host_native_scoring_input": True,
    "does_not_create_human_prose_approval": True,
}

VALIDATES = [
    "json_parseability",
    "ccec_governance_interoperability_schema_conformance",
    "permitted_mapping_consistency",
    "prohibited_mapping_completeness",
    "expanded_do_not_map_to_completeness",
    "runtime_use_constraints",
    "rendering_constraints",
    "aggregation_constraints",
    "behavioral_use_constraints",
    "visual_semantics_constraints",
    "aggregate_metric_constraints",
    "workflow_transition_constraints",
    "forbidden_oracle_target_field_absence",
    "anti_coercion_target_detection",
    "terminal_state_mapping_detection",
    "quantitative_scoring_prohibition",
    "visual_assurance_signal_prohibition",
    "authority_inheritance_prohibition",
    "unresolved_gap_preservation",
    "checker_output_contract_conformance",
    "output_actionability_constraints",
    "proxy_laundering_constraints",
    "host_conformance_constraints",
    "proxy_laundering_detection",
    "sla_timer_coercion_detection",
    "review_tier_routing_detection",
    "host_native_scoring_attachment_detection",
    "output_ok_boolean_absence",
]

DOES_NOT_VALIDATE = [
    "truth_of_source_ccec",
    "correctness_of_external_governance_decision",
    "compliance_of_external_system",
    "safety_of_external_system",
    "legal_sufficiency_of_external_decision",
    "institutional_authority_of_external_owner",
    "policy_satisfaction",
    "risk_acceptance",
    "control_satisfaction",
    "issue_closure",
    "deployment_authorization",
    "evidence_sufficiency",
    "reasonable_reliance",
    "aggregation_posture",
    "external_runtime_behavior",
    "external_dashboard_behavior",
    "external_workflow_configuration_compliance",
    "third_party_governance_adequacy",
    "quantitative_risk_reduction",
    "visual_assurance",
    "workflow_transition",
    "host_platform_native_scoring_behavior",
    "human_free_text_interpretation",
    "executive_narrative_framing",
    "sla_configuration_compliance",
    "review_queue_routing_adequacy",
    "data_quality_actuality",
    "metadata_health_actuality",
    "documentation_completeness_actuality",
]

FORBIDDEN_FIELD_NAMES = {
    "approval_status",
    "approved",
    "truth_status",
    "is_true",
    "safety_status",
    "is_safe",
    "compliance_status",
    "is_compliant",
    "legal_sufficiency_status",
    "legally_sufficient",
    "authorization_status",
    "authorized",
    "risk_acceptance_status",
    "risk_accepted",
    "authority_transfer",
    "control_status",
    "control_effectiveness_status",
    "control_satisfied",
    "issue_closed_status",
    "deployment_approved",
    "go_live_authorization",
    "evidence_sufficiency",
    "audit_sufficiency",
    "reasonable_reliance",
    "status_code",
    "ok_flag",
    "pass_flag",
    "go_flag",
    "trust_level",
    "confidence_score",
}

FORBIDDEN_TARGET_FRAGMENTS = [
    "approval",
    "approved",
    "approver",
    "signoff",
    "sign_off",
    "sign-off",
    "authorized_by",
    "authorization_status",
    "authority_transfer",
    "compliance_status",
    "compliance_state",
    "compliance_level",
    "compliance_evidence",
    "compliant",
    "control_status",
    "control_effectiveness",
    "control_satisfied",
    "control_passed",
    "control_effective",
    "control_maturity",
    "automated_control_satisfied",
    "risk_acceptance",
    "risk_accepted",
    "risk_state",
    "risk_level",
    "risk_score",
    "residual_risk",
    "inherent_risk",
    "risk_tolerance",
    "legal_sufficiency",
    "policy_satisfaction",
    "policy_gate",
    "evidence_sufficiency",
    "evidence_sufficient",
    "evidence_accepted",
    "audit_sufficiency",
    "audit_sufficient",
    "audit_accepted",
    "audit_passed",
    "audit_status",
    "audit_finding",
    "finding_status",
    "reasonable_reliance",
    "standard_of_care",
    "issue_closed",
    "issue_resolved",
    "issue_status",
    "ticket_resolution",
    "remediation_complete",
    "exception_granted",
    "waiver_approved",
    "compensating_control",
    "go_live",
    "go_no_go",
    "go_decision",
    "deploy_allowed",
    "deployment_allowed",
    "deployment_approved",
    "deployment_authorized",
    "deploy_status",
    "production_ready",
    "production_authorized",
    "operational_readiness",
    "phase_gate",
    "tollgate",
    "milestone_clearance",
    "review_outcome",
    "review_complete",
    "attestation_state",
    "record_state",
    "maturity_level",
    "model_approval",
    "validation_status",
    "drift_status",
    "gate_status",
    "resolution",
    "disposition",
    "terminal_state",
    "ready_for_deploy",
    "ready_for_go_live",
    "status_code",
    "ok_flag",
    "pass_flag",
    "go_flag",
    "authz",
    "assurance_level",
    "assurance_score",
    "trust_level",
    "confidence_level",
    "confidence_score",
    "documentation_coverage",
    "evidence_hygiene_score",
    "reliance_completeness_index",
    "boundary_preservation_rate",
    "coverage_percentage",
    "coverage_percent",
    "compliance_coverage",
    "green_badge",
    "pass_badge",
    "checkmark",
    "traffic_light",
    "negative_gate",
    "default_allow",
    "no_ccec",
    "unless_no_ccec",
    "data_quality",
    "metadata_health",
    "documentation_completeness",
    "sla_met",
    "sla_paused",
    "sla_stopped",
    "sla_timer",
    "fast_track",
    "routing_tier",
    "review_tier",
    "lower_friction",
    "standard_review_queue",
    "triage_complete",
    "archived",
    "promoted",
    "governance_readiness",
    "governance_health",
    "required_coverage",
    "native_scoring",
    "evidence_attachment_count",
    "host_design_system",
    "verified_secure",
    "secure_shield",
    "human_prose",
    "green_signal",
    "metadata_quality",
]

RUNTIME_USE_EXPECTED = {
    "may_be_used_as_sufficient_condition_for_approval": False,
    "may_be_used_as_sufficient_condition_for_compliance_status": False,
    "may_be_used_as_sufficient_condition_for_control_satisfaction": False,
    "may_be_used_as_sufficient_condition_for_issue_closure": False,
    "may_be_used_as_sufficient_condition_for_deployment_authorization": False,
    "may_be_used_as_sufficient_condition_for_risk_acceptance": False,
    "may_be_used_as_sufficient_condition_for_authority_transfer": False,
    "may_be_used_in_composite_gate_rules": False,
    "external_status_change_requires_separate_local_decision_record": True,
}

RENDERING_EXPECTED = {
    "ccec_derived_fields_require_co_rendered_limitations": True,
    "ccec_derived_fields_require_co_rendered_non_claims": True,
    "ccec_derived_fields_require_co_rendered_unresolved_gaps": True,
    "ccec_derived_fields_require_co_rendered_authority_boundary": True,
    "single_badge_summary_prohibited": True,
    "green_badge_without_limitations_prohibited": True,
}

AGGREGATION_EXPECTED = {
    "aggregation_may_claim_only_boundary_record_coverage": True,
    "aggregation_must_not_claim_control_effectiveness": True,
    "aggregation_must_not_claim_compliance": True,
    "aggregation_must_not_claim_safety": True,
    "aggregation_must_not_claim_risk_acceptance": True,
    "aggregation_requires_non_claim_and_gap_disclosure": True,
}

BEHAVIORAL_USE_EXPECTED = {
    "ccec_presence_absence_gate_prohibited": True,
    "ccec_as_necessary_condition_prohibited": True,
    "ccec_as_sufficient_condition_prohibited": True,
    "ccec_as_negative_gate_condition_prohibited": True,
    "ccec_as_workflow_phase_unlock_prohibited": True,
    "boolean_coercion_prohibited": True,
    "numeric_score_coercion_prohibited": True,
    "weighted_risk_reduction_prohibited": True,
    "compensating_control_use_prohibited": True,
    "coverage_percentage_posture_prohibited": True,
    "result_ok_actionability_prohibited": True,
    "external_runtime_enforcement_required": True,
}

VISUAL_SEMANTICS_EXPECTED = {
    "traffic_light_rendering_prohibited": True,
    "checkmark_icon_rendering_prohibited": True,
    "pass_fail_iconography_prohibited": True,
    "same_viewport_limitations_required": True,
    "click_to_expand_limitations_insufficient": True,
    "tooltip_status_language_prohibited": True,
    "neutral_documentation_label_required": True,
    "host_design_system_assurance_signal_prohibited": True,
    "tab_or_pagination_limitation_disclosure_insufficient": True,
    "scroll_only_limitation_disclosure_insufficient": True,
}

AGGREGATE_METRIC_EXPECTED = {
    "raw_event_count_aggregates_allowed": True,
    "ratio_aggregates_over_ccec_content_prohibited": True,
    "percentage_aggregates_over_ccec_content_prohibited": True,
    "trendline_aggregates_over_ccec_content_prohibited": True,
    "weighted_scores_from_ccec_fields_prohibited": True,
    "coverage_percentage_as_compliance_proxy_prohibited": True,
    "aggregate_metric_names_must_not_imply_posture": True,
}

WORKFLOW_TRANSITION_EXPECTED = {
    "terminal_status_mapping_prohibited": True,
    "stage_state_disposition_terminal_mapping_prohibited": True,
    "ccec_triggered_ticket_resolution_prohibited": True,
    "ccec_triggered_deployment_transition_prohibited": True,
    "ccec_triggered_audit_finding_closure_prohibited": True,
    "ccec_triggered_policy_exception_or_waiver_prohibited": True,
}

OUTPUT_ACTIONABILITY_EXPECTED = {
    "top_level_ok_boolean_prohibited": True,
    "structural_pass_non_actionable": True,
    "exit_zero_not_approval_signal": True,
    "ci_cd_blocking_gate_use_prohibited": True,
    "checker_may_run_only_as_audit_or_non_actionable_validation": True,
    "ci_job_name_must_disclose_structural_only_scope": True,
    "result_kind_must_not_be_extracted_without_limitations": True
}

PROXY_LAUNDERING_EXPECTED = {
    "data_quality_proxy_mapping_prohibited": True,
    "metadata_health_proxy_mapping_prohibited": True,
    "documentation_completeness_proxy_mapping_prohibited": True,
    "sla_timer_coercion_prohibited": True,
    "sla_met_or_paused_status_prohibited": True,
    "review_tier_fast_track_prohibited": True,
    "lower_friction_queue_routing_prohibited": True,
    "triage_completion_proxy_prohibited": True,
    "required_coverage_baseline_posture_prohibited": True,
    "host_design_system_assurance_signal_prohibited": True
}

HOST_CONFORMANCE_EXPECTED = {
    "host_native_scoring_must_not_use_ccec_attachment_count": True,
    "ccec_attachment_to_scored_object_requires_disabled_score_contribution": True,
    "human_checklist_item_must_not_use_ccec_as_gate": True,
    "human_free_text_summary_must_not_launder_ccec_into_approval": True,
    "ccec_presence_must_not_control_approval_ui_availability": True,
    "integration_conformance_review_required": True,
    "external_behavior_outside_checker_scope_acknowledged": True,
    "opaque_host_scoring_declared_residual_risk": True,
    "human_prose_summary_declared_residual_risk": True
}

def repo_root() -> Path:
    invoked = Path(sys.argv[0]).resolve()
    if invoked.parent.name == "tools":
        return invoked.parents[1]
    return Path.cwd()

def profile_schema_path() -> Path:
    return repo_root() / "schemas" / "ccec_governance_interoperability_profile_v0_1.schema.json"

def output_schema_path() -> Path:
    return repo_root() / "schemas" / "ccec_governance_interoperability_checker_output_v0_1.schema.json"

def finding(code: str, message: str, path: str | None = None) -> dict[str, str]:
    item = {"code": code, "message": message}
    if path:
        item["path"] = path
    return item

def load_json_file(path: Path) -> tuple[Any | None, list[dict[str, str]]]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, [finding("INPUT_FILE_NOT_FOUND", f"Input file not found: {path}", "$")]
    except OSError as exc:
        return None, [finding("INPUT_FILE_READ_ERROR", f"Could not read input file: {exc}", "$")]

    try:
        return json.loads(text), []
    except json.JSONDecodeError as exc:
        return None, [finding("INPUT_JSON_PARSE_ERROR", f"Input is not valid JSON: {exc.msg}", f"line {exc.lineno}, column {exc.colno}")]

def load_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def json_path(error: Any) -> str:
    parts = list(error.absolute_path)
    if not parts:
        return "$"

    rendered = "$"
    for part in parts:
        if isinstance(part, int):
            rendered += f"[{part}]"
        else:
            rendered += f".{part}"
    return rendered

def validate_schema(instance: Any, schema: dict[str, Any]) -> list[dict[str, str]]:
    if jsonschema is None:
        return [finding("JSONSCHEMA_IMPORT_ERROR", f"jsonschema could not be imported: {JSONSCHEMA_IMPORT_ERROR}", "$")]

    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.absolute_path))
    return [finding("SCHEMA_VALIDATION_ERROR", error.message, json_path(error)) for error in errors]

def walk_forbidden_fields(value: Any, path: str = "$") -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in FORBIDDEN_FIELD_NAMES:
                errors.append(
                    finding(
                        "CCEC_INTEROP_FORBIDDEN_ORACLE_FIELD",
                        f"Forbidden oracle-like field name '{key}' is not allowed in an interoperability profile.",
                        child_path,
                    )
                )
            errors.extend(walk_forbidden_fields(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(walk_forbidden_fields(child, f"{path}[{index}]"))

    return errors

def check_expected_object(profile: dict[str, Any], field: str, expected: dict[str, bool], code: str, errors: list[dict[str, str]]) -> None:
    value = profile.get(field)
    if not isinstance(value, dict):
        errors.append(finding(code, f"{field} must be present as an object.", f"$.{field}"))
        return

    for key, expected_value in expected.items():
        if value.get(key) is not expected_value:
            errors.append(
                finding(
                    code,
                    f"{field}.{key} must be {expected_value}.",
                    f"$.{field}.{key}",
                )
            )

def target_field_errors(rule: dict[str, Any], index: int) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    target = str(rule.get("external_target_field", "")).lower()
    transform = str(rule.get("transformation", "")).lower()

    for fragment in FORBIDDEN_TARGET_FRAGMENTS:
        if fragment in target:
            errors.append(
                finding(
                    "CCEC_INTEROP_ORACLE_TARGET_FIELD",
                    f"external_target_field '{rule.get('external_target_field')}' would map a bounded CCEC reference into a prohibited oracle-like, behavioral, workflow, scoring, or visual target.",
                    f"$.mapping_rules[{index}].external_target_field",
                )
            )
            break

    for fragment in ["boolean", "numeric", "score", "weight", "weighted", "coerce", "status_code", "risk_reduction"]:
        if fragment in transform:
            errors.append(
                finding(
                    "CCEC_INTEROP_COERCIVE_TRANSFORMATION_PROHIBITED",
                    f"transformation '{rule.get('transformation')}' implies coercion, scoring, or status transformation.",
                    f"$.mapping_rules[{index}].transformation",
                )
            )
            break

    if rule.get("creates_external_status") is True:
        errors.append(
            finding(
                "CCEC_INTEROP_EXTERNAL_STATUS_CREATION_PROHIBITED",
                "mapping_rules items must not create external status.",
                f"$.mapping_rules[{index}].creates_external_status",
            )
        )

    return errors

def contract_errors(profile: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    permitted = set(profile.get("permitted_mappings", []))
    prohibited = set(profile.get("prohibited_mappings", []))

    missing_prohibited = [item for item in PROHIBITED_MAPPINGS if item not in prohibited]
    if missing_prohibited:
        errors.append(
            finding(
                "CCEC_INTEROP_PROHIBITED_MAPPINGS_INCOMPLETE",
                "prohibited_mappings is missing: " + ", ".join(missing_prohibited),
                "$.prohibited_mappings",
            )
        )

    accord_limitations = profile.get("accord_limitations")
    if isinstance(accord_limitations, dict):
        mapped = set(accord_limitations.get("do_not_map_to", []))
        missing = [item for item in DO_NOT_MAP_TO if item not in mapped]
        if missing:
            errors.append(
                finding(
                    "CCEC_INTEROP_DO_NOT_MAP_TO_INCOMPLETE",
                    "accord_limitations.do_not_map_to is missing: " + ", ".join(missing),
                    "$.accord_limitations.do_not_map_to",
                )
            )

        expected_limitations = {
            "safe_to_automate": False,
            "automation_interpretation_required": True,
            "bounded_reference_only": True,
            "does_not_validate_approval": True,
            "does_not_validate_truth": True,
            "does_not_validate_safety": True,
            "does_not_validate_compliance": True,
            "does_not_validate_legal_sufficiency": True,
            "does_not_validate_institutional_authorization": True,
            "does_not_validate_policy_satisfaction": True,
            "does_not_validate_risk_acceptance": True,
            "does_not_validate_control_satisfaction": True,
            "does_not_validate_issue_closure": True,
            "does_not_validate_deployment_authorization": True,
            "does_not_validate_evidence_sufficiency": True,
            "does_not_validate_reasonable_reliance": True,
            "does_not_validate_aggregation_posture": True,
            "does_not_validate_quantitative_risk_reduction": True,
            "does_not_validate_visual_assurance": True,
            "does_not_validate_workflow_transition": True,
            "does_not_validate_runtime_configuration_compliance": True,
            "does_not_validate_external_system_governance_adequacy": True,
            "does_not_transfer_authority": True,
            "not_runtime_control": True,
            "not_policy_engine": True,
            "not_compliance_oracle": True,
        }
        for key, expected in expected_limitations.items():
            if accord_limitations.get(key) is not expected:
                errors.append(
                    finding(
                        "CCEC_INTEROP_LIMITATION_VALUE_INVALID",
                        f"accord_limitations.{key} must be {expected}.",
                        f"$.accord_limitations.{key}",
                    )
                )

    check_expected_object(profile, "runtime_use_constraints", RUNTIME_USE_EXPECTED, "CCEC_INTEROP_RUNTIME_USE_CONSTRAINT_VIOLATION", errors)
    check_expected_object(profile, "rendering_constraints", RENDERING_EXPECTED, "CCEC_INTEROP_RENDERING_CONSTRAINT_VIOLATION", errors)
    check_expected_object(profile, "aggregation_constraints", AGGREGATION_EXPECTED, "CCEC_INTEROP_AGGREGATION_CONSTRAINT_VIOLATION", errors)
    check_expected_object(profile, "behavioral_use_constraints", BEHAVIORAL_USE_EXPECTED, "CCEC_INTEROP_BEHAVIORAL_USE_CONSTRAINT_VIOLATION", errors)
    check_expected_object(profile, "visual_semantics_constraints", VISUAL_SEMANTICS_EXPECTED, "CCEC_INTEROP_VISUAL_SEMANTICS_CONSTRAINT_VIOLATION", errors)
    check_expected_object(profile, "aggregate_metric_constraints", AGGREGATE_METRIC_EXPECTED, "CCEC_INTEROP_AGGREGATE_METRIC_CONSTRAINT_VIOLATION", errors)
    check_expected_object(profile, "workflow_transition_constraints", WORKFLOW_TRANSITION_EXPECTED, "CCEC_INTEROP_WORKFLOW_TRANSITION_CONSTRAINT_VIOLATION", errors)
    check_expected_object(profile, "output_actionability_constraints", OUTPUT_ACTIONABILITY_EXPECTED, "CCEC_INTEROP_OUTPUT_ACTIONABILITY_CONSTRAINT_VIOLATION", errors)
    check_expected_object(profile, "proxy_laundering_constraints", PROXY_LAUNDERING_EXPECTED, "CCEC_INTEROP_PROXY_LAUNDERING_CONSTRAINT_VIOLATION", errors)
    check_expected_object(profile, "host_conformance_constraints", HOST_CONFORMANCE_EXPECTED, "CCEC_INTEROP_HOST_CONFORMANCE_CONSTRAINT_VIOLATION", errors)

    for index, rule in enumerate(profile.get("mapping_rules", [])):
        if not isinstance(rule, dict):
            continue

        mapping_kind = rule.get("mapping_kind")
        if mapping_kind not in permitted:
            errors.append(
                finding(
                    "CCEC_INTEROP_MAPPING_KIND_NOT_PERMITTED",
                    f"mapping rule uses {mapping_kind}, but that kind is not listed in permitted_mappings.",
                    f"$.mapping_rules[{index}].mapping_kind",
                )
            )

        errors.extend(target_field_errors(rule, index))

    local_authority = profile.get("local_authority_boundary")
    if isinstance(local_authority, dict):
        if local_authority.get("external_status_change_basis") == "INHERITED_FROM_CCEC":
            errors.append(
                finding(
                    "CCEC_INTEROP_AUTHORITY_INHERITANCE_PROHIBITED",
                    "external_status_change_basis must not be INHERITED_FROM_CCEC.",
                    "$.local_authority_boundary.external_status_change_basis",
                )
            )

    gap_handling = profile.get("unresolved_gaps_handling")
    if isinstance(gap_handling, dict):
        if gap_handling.get("may_close_gaps_by_mapping") is not False:
            errors.append(
                finding(
                    "CCEC_INTEROP_GAPS_MUST_NOT_CLOSE_BY_MAPPING",
                    "Unresolved gaps may not be closed by interoperability mapping.",
                    "$.unresolved_gaps_handling.may_close_gaps_by_mapping",
                )
            )

    errors.extend(walk_forbidden_fields(profile))
    return errors

def make_output(input_path: Path, result_kind: str, errors: list[dict[str, str]], warnings: list[dict[str, str]] | None = None) -> dict[str, Any]:
    return {
        "checker": {"name": CHECKER_NAME, "version": CHECKER_VERSION},
        "input": {"path": str(input_path)},
        "result": {
            "result_kind": result_kind,
            "actionability": "NON_ACTIONABLE_STRUCTURAL_CONFORMANCE_ONLY",
            "safe_to_automate": False,
            "automation_interpretation_required": True,
        },
        "errors": errors,
        "warnings": warnings or [],
        "scope": {
            "checker_scope": "structural_ccec_governance_interoperability_validation_only",
            "validates": VALIDATES,
            "does_not_validate": DOES_NOT_VALIDATE,
        },
        "limitations": LIMITATIONS,
        "do_not_map_to": DO_NOT_MAP_TO,
        "non_claims": NON_CLAIMS,
    }

def output_contract_errors(output: dict[str, Any]) -> list[dict[str, str]]:
    try:
        schema = load_schema(output_schema_path())
    except Exception as exc:
        return [finding("OUTPUT_SCHEMA_LOAD_ERROR", f"Could not load output schema: {exc}", "$")]
    return validate_schema(output, schema)

def emit(output: dict[str, Any]) -> int:
    output_errors = output_contract_errors(output)
    if output_errors:
        emergency_output = make_output(
            Path(output.get("input", {}).get("path", "")),
            "OUTPUT_CONTRACT_VIOLATION",
            [
                finding("CCEC_INTEROP_OUTPUT_CONTRACT_VIOLATION", "Checker output failed its own output contract.", "$"),
                *output_errors,
            ],
        )
        print(json.dumps(emergency_output, indent=2, sort_keys=True))
        return 2

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if output["result"]["result_kind"] == "STRUCTURAL_PASS" else 1

def check(path: Path) -> dict[str, Any]:
    profile, input_errors = load_json_file(path)
    if input_errors:
        return make_output(path, "INPUT_ERROR", input_errors)

    schema = load_schema(profile_schema_path())
    schema_errors = validate_schema(profile, schema)
    if schema_errors:
        return make_output(path, "SCHEMA_VALIDATION_FAILED", schema_errors)

    if not isinstance(profile, dict):
        return make_output(path, "SCHEMA_VALIDATION_FAILED", [finding("CCEC_INTEROP_ROOT_NOT_OBJECT", "Input root must be a JSON object.", "$")])

    extra_errors = contract_errors(profile)
    if extra_errors:
        return make_output(path, "CONTRACT_VALIDATION_FAILED", extra_errors)

    return make_output(path, "STRUCTURAL_PASS", [])

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a CCEC Governance Interoperability Profile v0.1.2 behavioral-layer hardened structural contract.")
    parser.add_argument("path", type=Path, help="Path to the CCEC governance interoperability profile JSON file.")
    args = parser.parse_args(argv)

    try:
        output = check(args.path)
    except Exception as exc:
        output = make_output(args.path, "INPUT_ERROR", [finding("CHECKER_UNHANDLED_ERROR", str(exc), "$")])

    return emit(output)

raise SystemExit(main())
