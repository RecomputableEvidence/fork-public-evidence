from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEMO_DOC = ROOT / "docs" / "CONTROLLED_PILOT_STAKEHOLDER_ORIENTATION_MEMO_v0_1.md"
MEMO_TEMPLATE = ROOT / "templates" / "pilot_orientation" / "controlled_pilot_stakeholder_orientation_memo_v0_1.md"
PACKAGE_INDEX = ROOT / "pilot_package" / "controlled_pilot_package_index_v0_1.json"


def test_orientation_memo_exists_and_names_core_boundary() -> None:
    text = MEMO_DOC.read_text(encoding="utf-8")

    assert "Controlled-pilot readiness remains inside Fork." in text
    assert "Live-ingestion authorization remains exclusively with the institution." in text
    assert "Fork does not decide whether live ingestion may proceed." in text


def test_orientation_memo_preserves_structural_readiness_vocabulary() -> None:
    text = MEMO_DOC.read_text(encoding="utf-8")

    assert "CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_READY" in text
    assert "CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_INCOMPLETE" in text
    assert "is not live-ingestion authorization" in text


def test_orientation_memo_declares_external_reference_zero_valence() -> None:
    text = MEMO_DOC.read_text(encoding="utf-8")

    assert "LIVE_INGESTION_AUTHORIZATION_EXTERNAL_REFERENCE" in text
    assert "zero authorization valence" in text
    assert "Fork must not issue, populate, validate, or be treated as the system of record" in text


def test_orientation_template_contains_acknowledgment_language() -> None:
    text = MEMO_TEMPLATE.read_text(encoding="utf-8")

    assert "I understand that Fork controlled-pilot artifacts preserve structural evidence boundaries only." in text
    assert "I understand that CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_READY is not live-ingestion authorization." in text
    assert "I understand that Fork outputs may support institutional review but do not replace institutional approval." in text


def test_package_index_includes_orientation_memo_and_template_directory() -> None:
    package_index = json.loads(PACKAGE_INDEX.read_text(encoding="utf-8"))
    component_ids = {component["component_id"] for component in package_index["package_components"]}

    assert "controlled_pilot_stakeholder_orientation_memo_doc" in component_ids
    assert "controlled_pilot_stakeholder_orientation_template_directory" in component_ids
