# scripts/build_ahi_viewer_data_v0_1.py
# Builds the static data bundle for docs/viewer/ahi-viewer-v0_1.
# Does not stage, commit, push, tag, or modify source artifacts.

import json
from pathlib import Path


ROOT = Path.cwd()
REGISTRY = ROOT / "examples/simulations/governance-proof-surface/scenario_registry.json"
OUT = ROOT / "docs/viewer/ahi-viewer-v0_1/data/scenarios_bundle.json"

def read_text(path: Path):
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8", errors="replace")

def read_json(path: Path):
    if not path.exists() or path.suffix.lower() != ".json":
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def arr(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]

def add_unique(target, value):
    if value is None:
        return
    for item in arr(value):
        if item is None:
            continue
        if isinstance(item, dict):
            item = item.get("statement") or item.get("description") or item.get("claim") or json.dumps(item, ensure_ascii=False)
        s = str(item).strip()
        if s and s not in target:
            target.append(s)

def artifact_type(path_string: str):
    name = Path(path_string).name
    checks = [
        ("boundary_delta_record", "BDR"),
        ("claim_boundary_contract", "CBC"),
        ("claim_consumption_event", "CCE"),
        ("system_mapping_receipt", "SMR"),
        ("unsupported_inheritance_event", "UIE"),
        ("suppressed_limitations_event", "SLE"),
        ("distributed_authority_failure_event", "DAFE"),
        ("authority_policy_context", "APC"),
        ("policy_reference_context", "PRC"),
        ("original_non_claims_panel", "ONCP"),
        ("non_claims_panel", "NCP"),
        ("downstream_memo_excerpt", "DME"),
    ]
    for needle, label in checks:
        if needle in name:
            return label
    if name.endswith(".json"):
        return "JSON"
    if name.endswith(".md"):
        return "MD"
    return "ARTIFACT"

def short_preview(text, limit=3500):
    if text is None:
        return None
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n[truncated for viewer bundle]"

def collect_from_bdr(obj, supports, nonsupports, unresolved, classifications):
    if not isinstance(obj, dict):
        return
    upstream = obj.get("upstream_state") or {}

    for claim in arr(upstream.get("recorded_claims")):
        if isinstance(claim, dict):
            statement = claim.get("statement")
            scope = claim.get("scope")
            if statement and scope:
                add_unique(supports, f"{statement} Scope: {scope}")
            else:
                add_unique(supports, statement)

    add_unique(nonsupports, upstream.get("recorded_non_claims"))

    for item in arr(upstream.get("unresolved_state")):
        if isinstance(item, dict):
            add_unique(unresolved, item.get("description"))
        else:
            add_unique(unresolved, item)

    add_unique(unresolved, obj.get("required_revalidation"))
    add_unique(unresolved, obj.get("required_revalidation_for"))

    classifications["delta_classification"] = obj.get("delta_classification")
    classifications["inspectability_result"] = obj.get("inspectability_result")
    classifications["fork_role"] = obj.get("fork_role")
    classifications["fork_non_authority_statement"] = obj.get("fork_non_authority_statement")

def collect_from_cbc(obj, supports, nonsupports, unresolved):
    if not isinstance(obj, dict):
        return

    for claim in arr(obj.get("claims_allowed_to_cross")):
        if isinstance(claim, dict):
            statement = claim.get("statement")
            scope = claim.get("scope")
            if statement and scope:
                add_unique(supports, f"{statement} Scope: {scope}")
            else:
                add_unique(supports, statement)

    for nc in arr(obj.get("material_non_claims_required_to_cross")):
        if isinstance(nc, dict):
            add_unique(nonsupports, nc.get("statement"))
        else:
            add_unique(nonsupports, nc)

    add_unique(nonsupports, obj.get("claims_not_allowed_to_be_inferred"))
    add_unique(unresolved, obj.get("revalidation_required_for"))

def collect_from_cce(obj, unresolved, classifications):
    if not isinstance(obj, dict):
        return
    classifications["claim_consumption_classification"] = obj.get("classification")
    add_unique(unresolved, obj.get("required_next_action"))

def collect_from_event(obj, label, classifications):
    if not isinstance(obj, dict):
        return
    classifications[label] = {
        "category": obj.get("category"),
        "secondary_categories": obj.get("secondary_categories"),
        "inferred_claim": obj.get("inferred_claim"),
        "record_support": obj.get("record_support"),
        "why_unsupported": obj.get("why_unsupported"),
        "fork_result": obj.get("fork_result"),
        "fork_non_authority_statement": obj.get("fork_non_authority_statement"),
    }

def build():
    print(f"Reading scenario registry: {REGISTRY.relative_to(ROOT)}")
    registry = read_json(REGISTRY)
    if not registry:
        raise SystemExit(f"Missing or invalid registry: {REGISTRY}")

    scenario_records = []

    for scenario in registry.get("scenarios", []):
        scenario_id = scenario.get("scenario_id")
        print(f"Bundling {scenario_id}")

        narrative_path = ROOT / scenario.get("file", "")
        narrative = short_preview(read_text(narrative_path))

        artifact_records = []
        supports = []
        nonsupports = []
        unresolved = []
        classifications = {}

        for artifact_path_string in arr(scenario.get("artifact_files")):
            artifact_path = ROOT / artifact_path_string
            atype = artifact_type(artifact_path_string)
            fmt = "json" if artifact_path_string.endswith(".json") else "markdown" if artifact_path_string.endswith(".md") else "text"
            exists = artifact_path.exists()

            artifact_records.append({
                "artifact_type": atype,
                "path": artifact_path_string,
                "format": fmt,
                "exists": exists
            })

            obj = read_json(artifact_path)
            if atype == "BDR":
                collect_from_bdr(obj, supports, nonsupports, unresolved, classifications)
            elif atype == "CBC":
                collect_from_cbc(obj, supports, nonsupports, unresolved)
            elif atype == "CCE":
                collect_from_cce(obj, unresolved, classifications)
            elif atype in ("UIE", "SLE", "DAFE"):
                collect_from_event(obj, atype, classifications)

        main_checker = scenario.get("main_checker") or {}
        included = bool(main_checker.get("narrative_file_required") or main_checker.get("artifact_files_required"))

        scenario_records.append({
            "scenario_number": scenario.get("scenario_number"),
            "scenario_id": scenario_id,
            "title": scenario.get("title"),
            "purpose": scenario.get("purpose"),
            "file": scenario.get("file"),
            "verification_posture": scenario.get("verification_posture"),
            "posture_description": scenario.get("posture_description"),
            "primary_category": scenario.get("primary_category"),
            "secondary_categories": scenario.get("secondary_categories") or [],
            "viewer_treatment": scenario.get("viewer_treatment"),
            "narrative_markdown": narrative,
            "artifacts": artifact_records,
            "selected_fields": {
                "supports_summary": supports,
                "non_support_summary": nonsupports,
                "requires_separate_evidence_summary": unresolved,
                "classifications": classifications
            },
            "checker_coverage": {
                "included_in_checker": included,
                "json_validated": bool(main_checker.get("json_validation")),
                "semantic_assertions_present": bool(main_checker.get("semantic_classification_assertions")),
                "dedicated_checker_invoked": bool(main_checker.get("dedicated_checker_invoked")),
                "overclaim_scan_covered": bool(main_checker.get("overclaim_scan_covered"))
            }
        })

    bundle = {
        "artifact_type": "AHI_VIEWER_SCENARIOS_BUNDLE",
        "artifact_version": "0.1",
        "generated": True,
        "generation_mode": "deterministic",
        "source_registry": str(REGISTRY.relative_to(ROOT)).replace("\\", "/"),
        "source_checker": "scripts/run_ahi_sim_v0_1_checks.ps1",
        "non_authority_statement": "Fork Boundary Explorer is a read-only evidence viewer for accountable handoff records. It does not approve, certify, score, authorize, or judge correctness. It shows what the record supports, what it explicitly does not support, and what remains unresolved.",
        "posture_enum": ["BASELINE", "STRUCTURAL", "SEMANTICALLY_VERIFIED", "SCAFFOLD"],
        "posture_note": "Posture enum is the primary maturity layer. Failure-mode terms are categories or boundary effects, not verification posture.",
        "scenarios": scenario_records
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n")

    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print("")
    print("Done.")
    print(f"Scenario count: {len(scenario_records)}")

if __name__ == "__main__":
    build()
