from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEAM_DOC = ROOT / "docs" / "CONTROLLED_PILOT_SEAM_HARDENING_v0_1_1.md"
PACKAGE_INDEX = ROOT / "pilot_package" / "controlled_pilot_package_index_v0_1.json"
DRY_RUN_TEMPLATE = ROOT / "templates" / "pilot_approval_artifacts" / "dry_run_approval_artifact_v0_1.template.json"
LIVE_AUTH_TEMPLATE = ROOT / "templates" / "pilot_approval_artifacts" / "live_ingestion_authorization_external_reference_v0_1.template.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_seam_hardening_doc_exists_and_names_external_authorization_boundary() -> None:
    text = SEAM_DOC.read_text(encoding="utf-8")

    assert "CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_READY" in text
    assert "Fork does not issue the authorization" in text
    assert "Dry-run output hash binding" in text


def test_package_index_includes_seam_hardening_doc() -> None:
    package_index = load_json(PACKAGE_INDEX)
    component_ids = {component["component_id"] for component in package_index["package_components"]}

    assert "controlled_pilot_seam_hardening_doc" in component_ids


def test_dry_run_template_binds_to_exact_dry_run_outputs() -> None:
    template = load_json(DRY_RUN_TEMPLATE)
    binding = template["dry_run_output_binding"]

    assert binding["hash_algorithm"] == "SHA-256"
    assert binding["binding_scope"] == "EXACT_DRY_RUN_OUTPUTS"
    assert len(binding["validation_receipt_sha256"]) == 64
    assert len(binding["dry_run_summary_sha256"]) == 64
    assert binding["fork_does_not_certify_external_state_after_hashing"] is True


def test_live_ingestion_external_reference_template_keeps_authorization_external() -> None:
    template = load_json(LIVE_AUTH_TEMPLATE)
    boundary = template["boundary"]

    assert template["record_type"] == "LIVE_INGESTION_AUTHORIZATION_EXTERNAL_REFERENCE"
    assert boundary["fork_may_not_issue"] is True
    assert boundary["external_authorization_required"] is True
    assert boundary["institutional_authorization_ref"] is None
    assert boundary["fork_does_not_validate_authorization_sufficiency"] is True
    assert boundary["fork_readiness_is_not_live_ingestion_authorization"] is True


def test_retained_authority_acknowledgment_is_explicit() -> None:
    template = load_json(DRY_RUN_TEMPLATE)
    retained = template["institutional_retained_authority_acknowledgment"]

    assert retained["fork_is_not_decision_authority"] is True
    assert retained["institution_retains_clinical_authority"] is True
    assert retained["institution_retains_compliance_authority"] is True
    assert retained["institution_retains_legal_authority"] is True
    assert retained["institution_retains_operational_authority"] is True
    assert retained["institution_retains_utilization_management_authority"] is True
