from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LEXICON_DOC = ROOT / "docs" / "CONTROLLED_PILOT_ORIENTATION_LEXICON_HARDENING_v0_1_1.md"
MEMO_DOC = ROOT / "docs" / "CONTROLLED_PILOT_STAKEHOLDER_ORIENTATION_MEMO_v0_1.md"
MEMO_TEMPLATE = ROOT / "templates" / "pilot_orientation" / "controlled_pilot_stakeholder_orientation_memo_v0_1.md"
PACKAGE_INDEX = ROOT / "pilot_package" / "controlled_pilot_package_index_v0_1.json"
APPROVAL_SCHEMA = ROOT / "schemas" / "pilot_approval_artifacts_v0_1.schema.json"
DRY_RUN_TEMPLATE = ROOT / "templates" / "pilot_approval_artifacts" / "dry_run_approval_artifact_v0_1.template.json"
ORIENTATION_TEMPLATE = ROOT / "templates" / "pilot_approval_artifacts" / "written_orientation_artifact_v0_1.template.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_lexicon_hardening_doc_exists_and_names_changes() -> None:
    text = LEXICON_DOC.read_text(encoding="utf-8")

    assert "Replace \"zero authorization valence\"" in text
    assert "Define structural readiness" in text
    assert "Rename ambiguous APPROVED statuses" in text


def test_memo_defines_structural_readiness_as_fork_internal_validation_only() -> None:
    text = MEMO_DOC.read_text(encoding="utf-8")

    assert "Structural readiness refers only to Fork's schema, hash, receipt, template, package-index, and checker validation." in text
    assert "It does not mean workflow readiness, clinical readiness, operational readiness, compliance readiness, production readiness, or live-ingestion authorization." in text


def test_memo_replaces_zero_valence_with_plain_authorization_language() -> None:
    text = MEMO_DOC.read_text(encoding="utf-8")

    assert "zero authorization valence" not in text
    assert "confers zero authorization by its mere existence" in text
    assert "no legal, operational, clinical, compliance, or live-ingestion authorization effect by itself" in text


def test_template_uses_structural_evidence_not_support_language() -> None:
    text = MEMO_TEMPLATE.read_text(encoding="utf-8")

    assert "Fork outputs may support institutional review" not in text
    assert "Fork outputs may serve as structural evidence during institutional review" in text
    assert "do not constitute or replace institutional approval" in text


def test_dry_run_artifact_uses_review_status_not_generic_approved() -> None:
    obj = load_json(DRY_RUN_TEMPLATE)

    assert "approval_status" not in obj
    assert obj["dry_run_review_status"] == "DRY_RUN_REVIEWED"


def test_orientation_artifact_uses_acknowledgment_status_not_generic_approved() -> None:
    obj = load_json(ORIENTATION_TEMPLATE)

    assert "approval_status" not in obj
    assert obj["orientation_acknowledgment_status"] == "ORIENTATION_ACKNOWLEDGED"


def test_schema_requires_new_status_fields() -> None:
    schema = load_json(APPROVAL_SCHEMA)
    defs = schema["$defs"]

    dry_run = defs["dry_run_approval_artifact"]
    orientation = defs["written_orientation_artifact"]

    assert "approval_status" not in dry_run["required"]
    assert "dry_run_review_status" in dry_run["required"]
    assert dry_run["properties"]["dry_run_review_status"]["const"] == "DRY_RUN_REVIEWED"

    assert "approval_status" not in orientation["required"]
    assert "orientation_acknowledgment_status" in orientation["required"]
    assert orientation["properties"]["orientation_acknowledgment_status"]["const"] == "ORIENTATION_ACKNOWLEDGED"


def test_package_index_includes_lexicon_hardening_doc() -> None:
    package_index = load_json(PACKAGE_INDEX)
    component_ids = {component["component_id"] for component in package_index["package_components"]}

    assert "controlled_pilot_orientation_lexicon_hardening_doc" in component_ids
