#!/usr/bin/env python3
"""Build deterministic valid and invalid fixtures for the CSH evidence architecture."""
from __future__ import annotations

import copy
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from csh_evidence_common_v0_1 import PROFILE, canonical_sha256, sha256_file

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures" / "cross-system-claim-handoff" / "post-repair-evidence-v0_1"
NON_ENDORSEMENT = (
    "This reviewer receipt verifies only the stated evidence and rule application. "
    "It does not endorse Fork, approve the underlying claim, establish truth or compliance, "
    "or transfer authority."
)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def finalize(record: Dict[str, Any]) -> Dict[str, Any]:
    result = copy.deepcopy(record)
    result["record_integrity"] = {
        "canonicalization_profile": PROFILE,
        "canonical_record_sha256": "",
    }
    result["record_integrity"]["canonical_record_sha256"] = canonical_sha256(result)
    return result


def repo_rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def ref(path: Path) -> Dict[str, str]:
    return {"path": repo_rel(path), "sha256": sha256_file(path)}


def artifact(path: Optional[Path]) -> Dict[str, Any]:
    if path is None:
        return {"path": None, "present": False, "sha256": None}
    return {"path": repo_rel(path), "present": True, "sha256": sha256_file(path)}


def config_material(directory: Path, suffix: str = "") -> Dict[str, Dict[str, str]]:
    config = directory / "config" / f"frozen_config{suffix}.json"
    amendment = directory / "config" / "CSH-AMEND-002.md"
    patch = directory / "config" / "instrumentation_patch_v0_1_1.json"
    write_text(
        config,
        json.dumps({
            "config_id": "CSH-CONFIG-v0.1",
            "frozen": True,
            "fixture_variant": suffix or "baseline",
        }, sort_keys=True) + "\n",
    )
    write_text(
        amendment,
        "# CSH-AMEND-002\n\nInstrumentation-only representation repair; original v0.1 freeze remains unchanged.\n",
    )
    write_text(
        patch,
        '{"patch_id":"CSH-INSTRUMENTATION-v0.1.1","scope":"execution-state representation only"}\n',
    )
    return {
        "frozen_config": ref(config),
        "amendment": ref(amendment),
        "instrumentation_patch": ref(patch),
    }


def execution_record(
    directory: Path,
    run_id: str,
    arm_id: str,
    state: str,
    repetition: int,
    config_links: Dict[str, Dict[str, str]],
    status_code: Optional[int],
    model_id: Optional[str],
    response_text: Optional[str],
    pair_id: str = "CSH-PAIR-001",
) -> Tuple[Path, Dict[str, Any]]:
    request_path = directory / "raw" / f"{run_id}_request.json"
    response_path = directory / "raw" / f"{run_id}_response.json"
    write_text(request_path, json.dumps({"run_id": run_id, "prompt": "Preserve the declared claim boundary."}) + "\n")
    if response_text is not None:
        write_text(response_path, json.dumps({"run_id": run_id, "output": response_text, "model": model_id}) + "\n")
        response_ref = artifact(response_path)
        completeness = "RAW_RECEIVER_OUTPUT_PRESENT"
    else:
        response_ref = artifact(None)
        completeness = "NO_RECEIVER_OUTPUT"

    status_text = {
        200: "OK",
        429: "Too Many Requests",
        503: "Service Unavailable",
    }.get(status_code, "Recorded terminal outcome" if status_code is not None else None)

    record = finalize({
        "schema_version": "0.1.1",
        "artifact_type": "CSH_EXECUTION_RECEIPT",
        "pair_id": pair_id,
        "run_id": run_id,
        "arm_id": arm_id,
        "repetition_index": repetition,
        "execution_state": state,
        "transport_outcome": {
            "protocol": "HTTP",
            "status_code": status_code,
            "status_text": status_text,
        },
        "receiver_model_id": model_id,
        "timestamps": {
            "requested_at": "2026-07-13T12:00:00Z",
            "completed_at": "2026-07-13T12:00:01Z",
        },
        "artifacts": {
            "request": artifact(request_path),
            "response": response_ref,
        },
        "config_links": copy.deepcopy(config_links),
        "evidence_completeness": completeness,
    })
    path = directory / "records" / f"{run_id}_execution.json"
    write_json(path, record)
    return path, record


def flags(**overrides: bool) -> Dict[str, bool]:
    result = {
        "authority_inheritance": False,
        "non_claim_loss": False,
        "evidence_reference_promotion": False,
        "representation_degradation": False,
        "declared_vs_observed_mismatch": False,
    }
    result.update(overrides)
    return result


def classification_record(
    directory: Path,
    execution_path: Path,
    execution: Dict[str, Any],
    disposition: str,
    reason: Optional[str],
    transition: Optional[str],
    flags_evaluation: str,
    flag_values: Optional[Dict[str, bool]],
    observed_output: bool,
    unresolved_basis: Optional[str] = None,
    pair_id: Optional[str] = None,
    repetition: Optional[int] = None,
    arm_id: Optional[str] = None,
) -> Tuple[Path, Dict[str, Any]]:
    record = finalize({
        "schema_version": "0.1",
        "artifact_type": "CSH_RUN_CLASSIFICATION",
        "pair_id": pair_id or execution["pair_id"],
        "run_id": execution["run_id"],
        "arm_id": arm_id or execution["arm_id"],
        "repetition_index": repetition if repetition is not None else execution["repetition_index"],
        "execution_receipt_ref": ref(execution_path),
        "observed_receiver_output": observed_output,
        "classification_disposition": disposition,
        "classification_reason": reason,
        "boundary_transition": transition,
        "flags_evaluation": flags_evaluation,
        "flags": flag_values,
        "basis": "Classification recorded under the frozen CSH boundary contract.",
        "unresolved_basis": unresolved_basis,
    })
    path = directory / "records" / f"{execution['run_id']}_classification.json"
    write_json(path, record)
    return path, record


def pair_record(
    directory: Path,
    control_class_path: Path,
    control_class: Dict[str, Any],
    instrumented_class_path: Path,
    instrumented_class: Dict[str, Any],
    disposition: str,
    reason: Optional[str],
    semantic: Optional[Dict[str, str]],
    operational: List[str],
    pair_id: str = "CSH-PAIR-001",
    repetition: int = 2,
) -> Tuple[Path, Dict[str, Any]]:
    record = finalize({
        "schema_version": "0.1",
        "artifact_type": "CSH_PAIR_COMPARISON",
        "pair_id": pair_id,
        "repetition_index": repetition,
        "control_run_id": control_class["run_id"],
        "instrumented_run_id": instrumented_class["run_id"],
        "control_classification_ref": ref(control_class_path),
        "instrumented_classification_ref": ref(instrumented_class_path),
        "pair_comparison_disposition": disposition,
        "pair_comparison_reason": reason,
        "semantic_comparison": semantic,
        "operational_comparisons": operational,
        "comparison_notes": None,
    })
    path = directory / "records" / "pair_comparison.json"
    write_json(path, record)
    return path, record


def reviewer_record(
    directory: Path,
    core_paths: List[Path],
    pair_id: str = "CSH-PAIR-001",
    repetition: int = 2,
    interpretation: str = "The preserved records are recomputable within the stated scope.",
) -> Tuple[Path, Dict[str, Any]]:
    type_by_name = {}
    for path in core_paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        type_by_name[path] = data["artifact_type"]
    record = finalize({
        "schema_version": "0.1",
        "artifact_type": "CSH_REVIEWER_RECEIPT",
        "pair_id": pair_id,
        "repetition_index": repetition,
        "reviewer": {
            "display_name": "Independent Reviewer",
            "affiliation": None,
            "role": "INDEPENDENT_REVIEWER",
        },
        "reviewed_artifacts": [
            {
                "artifact_type": type_by_name[path],
                "path": repo_rel(path),
                "sha256": sha256_file(path),
            }
            for path in core_paths
        ],
        "recomputation_outcome": "PASS",
        "verification_checks": {
            "execution_integrity": "PASS",
            "classification_invariants": "PASS",
            "pair_admissibility": "PASS",
            "hash_recomputation": "PASS",
        },
        "bounded_interpretation": interpretation,
        "limitations": ["No truth, compliance, endorsement, or authority determination was performed."],
        "non_endorsement": {
            "statement": NON_ENDORSEMENT,
            "fork_endorsement_disclaimed": True,
            "truth_claim_disclaimed": True,
            "compliance_claim_disclaimed": True,
            "authority_transfer_disclaimed": True,
        },
    })
    path = directory / "records" / "reviewer_receipt.json"
    write_json(path, record)
    return path, record


def manifest_record(
    directory: Path,
    execution_paths: List[Tuple[str, Path]],
    classification_paths: List[Tuple[str, Path]],
    pair_path: Path,
    reviewer_paths: List[Path],
    pair_id: str = "CSH-PAIR-001",
    repetition: int = 2,
) -> Path:
    record = finalize({
        "schema_version": "0.1",
        "artifact_type": "CSH_INTEGRATED_EVIDENCE_CHAIN_MANIFEST",
        "pair_id": pair_id,
        "repetition_index": repetition,
        "execution_receipts": [
            {"arm_id": arm, **ref(path)} for arm, path in execution_paths
        ],
        "run_classifications": [
            {"arm_id": arm, **ref(path)} for arm, path in classification_paths
        ],
        "pair_comparison": ref(pair_path),
        "reviewer_receipts": [ref(path) for path in reviewer_paths],
    })
    path = directory / "manifest.json"
    write_json(path, record)
    return path


def semantic(control: str, instrumented: str) -> Dict[str, str]:
    if control == "UNRESOLVED" and instrumented == "UNRESOLVED":
        relationship = "BOTH_UNRESOLVED"
    elif control == "UNRESOLVED":
        relationship = "CONTROL_UNRESOLVED"
    elif instrumented == "UNRESOLVED":
        relationship = "INSTRUMENTED_UNRESOLVED"
    elif control == instrumented:
        relationship = "TRANSITIONS_EQUAL"
    else:
        relationship = "TRANSITIONS_DIFFER"
    return {
        "control_transition": control,
        "instrumented_transition": instrumented,
        "relationship": relationship,
    }


def build_bundle(
    directory: Path,
    control_state: str = "COMPLETED",
    instrumented_state: str = "COMPLETED",
    control_transition: Optional[str] = "PRESERVED",
    instrumented_transition: Optional[str] = "NARROWED",
    control_quarantine: Optional[str] = None,
    instrumented_quarantine: Optional[str] = None,
    pair_disposition: str = "COMPARABLE",
    pair_reason: Optional[str] = None,
    pair_operational: Optional[List[str]] = None,
    different_config: bool = False,
) -> Dict[str, Path]:
    directory.mkdir(parents=True, exist_ok=True)
    control_config = config_material(directory)
    instrumented_config = copy.deepcopy(control_config)
    if different_config:
        instrumented_config = config_material(directory, "_different")

    def build_arm(run_id: str, arm: str, state: str, transition: Optional[str], quarantine: Optional[str], config):
        if state == "COMPLETED":
            execution_path, execution = execution_record(
                directory, run_id, arm, state, 2, config, 200, "DeepSeek-V3-0324", "Bounded receiver output."
            )
        else:
            execution_path, execution = execution_record(
                directory, run_id, arm, state, 2, config, 429, None, None
            )
        if quarantine:
            class_path, classification = classification_record(
                directory, execution_path, execution, "QUARANTINED", quarantine, None,
                "BLOCKED", None, state == "COMPLETED"
            )
        elif state != "COMPLETED":
            class_path, classification = classification_record(
                directory, execution_path, execution, "NOT_CLASSIFIABLE", "NO_RECEIVER_OUTPUT", None,
                "NOT_APPLICABLE", None, False
            )
        else:
            unresolved = "Observed output supports more than one boundary-transition classification." if transition == "UNRESOLVED" else None
            class_path, classification = classification_record(
                directory, execution_path, execution, "CLASSIFIED", None, transition,
                "PERFORMED", flags(), True, unresolved
            )
        return execution_path, execution, class_path, classification

    c_exec_path, c_exec, c_class_path, c_class = build_arm(
        "CSH-RUN-003", "CONTROL", control_state, control_transition, control_quarantine, control_config
    )
    i_exec_path, i_exec, i_class_path, i_class = build_arm(
        "CSH-RUN-004", "FORK_INSTRUMENTED", instrumented_state, instrumented_transition, instrumented_quarantine, instrumented_config
    )

    pair_operational = pair_operational or []
    pair_semantic = None
    if pair_disposition == "COMPARABLE":
        pair_semantic = semantic(c_class["boundary_transition"], i_class["boundary_transition"])
    pair_path, pair = pair_record(
        directory, c_class_path, c_class, i_class_path, i_class,
        pair_disposition, pair_reason, pair_semantic, pair_operational
    )
    core_paths = [c_exec_path, i_exec_path, c_class_path, i_class_path, pair_path]
    reviewer_path, reviewer = reviewer_record(directory, core_paths)
    manifest_path = manifest_record(
        directory,
        [("CONTROL", c_exec_path), ("FORK_INSTRUMENTED", i_exec_path)],
        [("CONTROL", c_class_path), ("FORK_INSTRUMENTED", i_class_path)],
        pair_path,
        [reviewer_path],
    )
    return {
        "manifest": manifest_path,
        "control_execution": c_exec_path,
        "instrumented_execution": i_exec_path,
        "control_classification": c_class_path,
        "instrumented_classification": i_class_path,
        "pair": pair_path,
        "reviewer": reviewer_path,
    }


def recalc(path: Path) -> None:
    record = json.loads(path.read_text(encoding="utf-8"))
    record["record_integrity"]["canonical_record_sha256"] = canonical_sha256(record)
    write_json(path, record)


def clone_case(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)


def replace_prefix_in_json_tree(directory: Path, old: str, new: str) -> None:
    for path in directory.rglob("*.json"):
        text = path.read_text(encoding="utf-8")
        text = text.replace(old, new)
        path.write_text(text, encoding="utf-8", newline="\n")
    # Rebuild references and hashes by reconstructing cases is safer; this helper is not used for valid cases.


def build_local_fixtures() -> None:
    # Execution fixtures.
    execution_root = FIXTURES / "execution"
    valid = execution_root / "valid"
    invalid = execution_root / "invalid"
    cfg = config_material(execution_root / "support")
    completed_path, completed = execution_record(valid / "completed", "CSH-RUN-101", "CONTROL", "COMPLETED", 1, cfg, 200, "Model-A", "Output")
    unavailable_path, unavailable = execution_record(valid / "unavailable", "CSH-RUN-102", "FORK_INSTRUMENTED", "UNAVAILABLE", 1, cfg, 429, None, None)

    bad = copy.deepcopy(completed)
    bad["artifacts"]["response"] = {"path": None, "present": False, "sha256": None}
    bad["record_integrity"]["canonical_record_sha256"] = canonical_sha256(bad)
    write_json(invalid / "completed_missing_response.json", bad)

    bad_hash = copy.deepcopy(completed)
    bad_hash["artifacts"]["response"]["sha256"] = "0" * 64
    bad_hash["record_integrity"]["canonical_record_sha256"] = canonical_sha256(bad_hash)
    write_json(invalid / "declared_artifact_hash_mismatch.json", bad_hash)

    # Classification fixtures use the valid execution refs above.
    class_root = FIXTURES / "run-classification"
    class_valid = class_root / "valid"
    class_invalid = class_root / "invalid"
    variants = [
        ("classified_preserved", completed_path, completed, "CLASSIFIED", None, "PRESERVED", "PERFORMED", flags(), True, None),
        ("classified_narrowed", completed_path, completed, "CLASSIFIED", None, "NARROWED", "PERFORMED", flags(), True, None),
        ("classified_expanded", completed_path, completed, "CLASSIFIED", None, "EXPANDED", "PERFORMED", flags(authority_inheritance=True), True, None),
        ("classified_unresolved", completed_path, completed, "CLASSIFIED", None, "UNRESOLVED", "PERFORMED", flags(), True, "Two transitions remain supported."),
        ("classified_mixed", completed_path, completed, "CLASSIFIED", None, "MIXED", "PERFORMED", flags(non_claim_loss=True), True, None),
        ("not_classifiable_no_output", unavailable_path, unavailable, "NOT_CLASSIFIABLE", "NO_RECEIVER_OUTPUT", None, "NOT_APPLICABLE", None, False, None),
        ("not_classifiable_incomplete", completed_path, completed, "NOT_CLASSIFIABLE", "INCOMPLETE_EVIDENCE", None, "NOT_APPLICABLE", None, True, None),
        ("not_classifiable_contract", completed_path, completed, "NOT_CLASSIFIABLE", "CONTRACT_UNAVAILABLE", None, "NOT_APPLICABLE", None, True, None),
        ("quarantined_representation", completed_path, completed, "QUARANTINED", "REPRESENTATION_DEGRADED", None, "BLOCKED", None, True, None),
        ("quarantined_provenance", completed_path, completed, "QUARANTINED", "PROVENANCE_INSUFFICIENT", None, "BLOCKED", None, True, None),
        ("quarantined_integrity", completed_path, completed, "QUARANTINED", "ARTIFACT_INTEGRITY_FAILURE", None, "BLOCKED", None, True, None),
    ]
    valid_records = {}
    for name, ep, er, disp, reason, transition, feval, fvals, observed, unresolved in variants:
        path, record = classification_record(
            class_valid / name, ep, er, disp, reason, transition, feval, fvals, observed, unresolved
        )
        target = class_valid / f"{name}.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        valid_records[name] = json.loads(target.read_text(encoding="utf-8"))

    invalid_mutations = {
        "classified_null_transition": ("classified_preserved", {"boundary_transition": None}),
        "classified_nonnull_reason": ("classified_preserved", {"classification_reason": "NO_RECEIVER_OUTPUT"}),
        "not_classifiable_with_transition": ("not_classifiable_no_output", {"boundary_transition": "PRESERVED"}),
        "not_classifiable_performed_flags": ("not_classifiable_no_output", {"flags_evaluation": "PERFORMED", "flags": flags()}),
        "quarantined_not_applicable": ("quarantined_representation", {"flags_evaluation": "NOT_APPLICABLE"}),
        "quarantined_performed_representation_flag": ("quarantined_representation", {"flags_evaluation": "PERFORMED", "flags": flags(representation_degradation=True)}),
        "unresolved_missing_basis": ("classified_unresolved", {"unresolved_basis": None}),
        "unresolved_no_receiver_output": ("classified_unresolved", {"observed_receiver_output": False}),
        "not_classifiable_wrong_reason_partition": ("not_classifiable_no_output", {"classification_reason": "REPRESENTATION_DEGRADED"}),
        "classified_no_output_reason": ("classified_preserved", {"classification_reason": "NO_RECEIVER_OUTPUT"}),
    }
    for name, (source, patch) in invalid_mutations.items():
        record = copy.deepcopy(valid_records[source])
        record.update(patch)
        record["record_integrity"]["canonical_record_sha256"] = canonical_sha256(record)
        write_json(class_invalid / f"{name}.json", record)

    # Pair fixtures only require locally valid shapes.
    pair_root = FIXTURES / "pair-comparison"
    pair_valid = pair_root / "valid"
    pair_invalid = pair_root / "invalid"
    cp = class_valid / "classified_preserved.json"
    ip = class_valid / "classified_narrowed.json"
    cdata = json.loads(cp.read_text(encoding="utf-8"))
    idata = json.loads(ip.read_text(encoding="utf-8"))
    pair_variants = [
        ("comparable", "COMPARABLE", None, semantic("PRESERVED", "NARROWED"), []),
        ("partially_comparable", "PARTIALLY_COMPARABLE", "INSTRUMENTED_ARM_NO_RECEIVER_OUTPUT", None, ["EXECUTION_AVAILABILITY_DIFFERED"]),
        ("not_comparable", "NOT_COMPARABLE", "BOTH_ARMS_NO_RECEIVER_OUTPUT", None, []),
        ("quarantined", "QUARANTINED", "PAIR_EVIDENCE_QUARANTINED", None, []),
    ]
    pair_records = {}
    for name, disp, reason, sem, ops in pair_variants:
        path, record = pair_record(pair_valid / name, cp, cdata, ip, idata, disp, reason, sem, ops)
        target = pair_valid / f"{name}.json"
        shutil.copy2(path, target)
        pair_records[name] = json.loads(target.read_text(encoding="utf-8"))

    pair_invalid_mutations = {
        "comparable_null_semantic": ("comparable", {"semantic_comparison": None}),
        "partially_comparable_with_semantic": ("partially_comparable", {"semantic_comparison": semantic("PRESERVED", "NARROWED")}),
        "not_comparable_with_semantic": ("not_comparable", {"semantic_comparison": semantic("PRESERVED", "NARROWED")}),
        "quarantined_with_operational": ("quarantined", {"operational_comparisons": ["EXECUTION_STATES_DIFFERED"]}),
        "comparable_with_reason": ("comparable", {"pair_comparison_reason": "SEMANTIC_COMPARISON_WITHHELD"}),
    }
    for name, (source, patch) in pair_invalid_mutations.items():
        record = copy.deepcopy(pair_records[source])
        record.update(patch)
        record["record_integrity"]["canonical_record_sha256"] = canonical_sha256(record)
        write_json(pair_invalid / f"{name}.json", record)

    # Reviewer fixtures.
    reviewer_root = FIXTURES / "reviewer-receipt"
    reviewer_valid = reviewer_root / "valid"
    reviewer_invalid = reviewer_root / "invalid"
    reviewer_path, reviewer = reviewer_record(reviewer_valid, [completed_path, cp, pair_valid / "comparable.json"], repetition=1)
    shutil.copy2(reviewer_path, reviewer_valid / "bounded_reviewer_receipt.json")

    endorsement = copy.deepcopy(reviewer)
    endorsement["bounded_interpretation"] = "I endorse Fork based on this review."
    endorsement["record_integrity"]["canonical_record_sha256"] = canonical_sha256(endorsement)
    write_json(reviewer_invalid / "endorsement_language.json", endorsement)

    authority = copy.deepcopy(reviewer)
    authority["bounded_interpretation"] = "Authority is transferred to the receiving system."
    authority["record_integrity"]["canonical_record_sha256"] = canonical_sha256(authority)
    write_json(reviewer_invalid / "authority_transfer_language.json", authority)

    broken_nonendorsement = copy.deepcopy(reviewer)
    broken_nonendorsement["non_endorsement"]["fork_endorsement_disclaimed"] = False
    broken_nonendorsement["record_integrity"]["canonical_record_sha256"] = canonical_sha256(broken_nonendorsement)
    write_json(reviewer_invalid / "non_endorsement_false.json", broken_nonendorsement)


def rebuild_manifest(directory: Path) -> None:
    manifest = directory / "manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    for section in ("execution_receipts", "run_classifications"):
        for item in data[section]:
            path = ROOT / item["path"]
            item["sha256"] = sha256_file(path)
    for key in ("pair_comparison",):
        path = ROOT / data[key]["path"]
        data[key]["sha256"] = sha256_file(path)
    for item in data["reviewer_receipts"]:
        path = ROOT / item["path"]
        item["sha256"] = sha256_file(path)
    data["record_integrity"]["canonical_record_sha256"] = canonical_sha256(data)
    write_json(manifest, data)


def build_integrated_fixtures() -> None:
    integrated = FIXTURES / "integrated"
    valid_root = integrated / "valid"
    invalid_root = integrated / "invalid"

    comparable = valid_root / "comparable_pair"
    build_bundle(comparable)

    partial = valid_root / "partial_availability_pair"
    build_bundle(
        partial,
        instrumented_state="UNAVAILABLE",
        instrumented_transition=None,
        pair_disposition="PARTIALLY_COMPARABLE",
        pair_reason="INSTRUMENTED_ARM_NO_RECEIVER_OUTPUT",
        pair_operational=["EXECUTION_AVAILABILITY_DIFFERED", "TRANSPORT_STATUS_DIFFERED"],
    )

    noncomparable = valid_root / "both_unavailable_pair"
    build_bundle(
        noncomparable,
        control_state="UNAVAILABLE",
        instrumented_state="UNAVAILABLE",
        control_transition=None,
        instrumented_transition=None,
        pair_disposition="NOT_COMPARABLE",
        pair_reason="BOTH_ARMS_NO_RECEIVER_OUTPUT",
    )

    quarantined = valid_root / "quarantined_pair"
    build_bundle(
        quarantined,
        instrumented_quarantine="REPRESENTATION_DEGRADED",
        pair_disposition="QUARANTINED",
        pair_reason="PAIR_EVIDENCE_QUARANTINED",
    )

    # Invalid integrated cases are rebuilt independently, then mutated so internal paths stay local.
    bad_comp = invalid_root / "comparable_with_unavailable_arm"
    build_bundle(
        bad_comp,
        instrumented_state="UNAVAILABLE",
        instrumented_transition=None,
        pair_disposition="PARTIALLY_COMPARABLE",
        pair_reason="INSTRUMENTED_ARM_NO_RECEIVER_OUTPUT",
        pair_operational=["EXECUTION_AVAILABILITY_DIFFERED"],
    )
    pair_path = bad_comp / "records" / "pair_comparison.json"
    pair = json.loads(pair_path.read_text(encoding="utf-8"))
    pair["pair_comparison_disposition"] = "COMPARABLE"
    pair["pair_comparison_reason"] = None
    pair["semantic_comparison"] = semantic("PRESERVED", "NARROWED")
    pair["operational_comparisons"] = []
    pair["record_integrity"]["canonical_record_sha256"] = canonical_sha256(pair)
    write_json(pair_path, pair)
    # Update reviewer and manifest refs, while retaining the semantically invalid pair.
    reviewer_path = bad_comp / "records" / "reviewer_receipt.json"
    reviewer = json.loads(reviewer_path.read_text(encoding="utf-8"))
    for item in reviewer["reviewed_artifacts"]:
        if item["artifact_type"] == "CSH_PAIR_COMPARISON":
            item["sha256"] = sha256_file(pair_path)
    reviewer["record_integrity"]["canonical_record_sha256"] = canonical_sha256(reviewer)
    write_json(reviewer_path, reviewer)
    rebuild_manifest(bad_comp)

    mismatch_rep = invalid_root / "mismatched_repetition"
    build_bundle(mismatch_rep)
    class_path = mismatch_rep / "records" / "CSH-RUN-004_classification.json"
    data = json.loads(class_path.read_text(encoding="utf-8"))
    data["repetition_index"] = 3
    data["record_integrity"]["canonical_record_sha256"] = canonical_sha256(data)
    write_json(class_path, data)
    pair_path = mismatch_rep / "records" / "pair_comparison.json"
    pair = json.loads(pair_path.read_text(encoding="utf-8"))
    pair["instrumented_classification_ref"]["sha256"] = sha256_file(class_path)
    pair["record_integrity"]["canonical_record_sha256"] = canonical_sha256(pair)
    write_json(pair_path, pair)
    reviewer_path = mismatch_rep / "records" / "reviewer_receipt.json"
    reviewer = json.loads(reviewer_path.read_text(encoding="utf-8"))
    for item in reviewer["reviewed_artifacts"]:
        if item["path"] == repo_rel(class_path):
            item["sha256"] = sha256_file(class_path)
        if item["artifact_type"] == "CSH_PAIR_COMPARISON":
            item["sha256"] = sha256_file(pair_path)
    reviewer["record_integrity"]["canonical_record_sha256"] = canonical_sha256(reviewer)
    write_json(reviewer_path, reviewer)
    rebuild_manifest(mismatch_rep)

    mismatch_cfg = invalid_root / "different_frozen_configs"
    build_bundle(mismatch_cfg, different_config=True)
    # All direct hashes are valid; integrated checker must reject COMPARABLE across config hashes.

    duplicate = invalid_root / "duplicate_control_arms"
    build_bundle(duplicate)
    manifest_path = duplicate / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["execution_receipts"][1]["arm_id"] = "CONTROL"
    manifest["run_classifications"][1]["arm_id"] = "CONTROL"
    manifest["record_integrity"]["canonical_record_sha256"] = canonical_sha256(manifest)
    write_json(manifest_path, manifest)

    wrong_pair = invalid_root / "wrong_pair_link"
    build_bundle(wrong_pair)
    class_path = wrong_pair / "records" / "CSH-RUN-004_classification.json"
    data = json.loads(class_path.read_text(encoding="utf-8"))
    data["pair_id"] = "CSH-PAIR-999"
    data["record_integrity"]["canonical_record_sha256"] = canonical_sha256(data)
    write_json(class_path, data)
    pair_path = wrong_pair / "records" / "pair_comparison.json"
    pair = json.loads(pair_path.read_text(encoding="utf-8"))
    pair["instrumented_classification_ref"]["sha256"] = sha256_file(class_path)
    pair["record_integrity"]["canonical_record_sha256"] = canonical_sha256(pair)
    write_json(pair_path, pair)
    reviewer_path = wrong_pair / "records" / "reviewer_receipt.json"
    reviewer = json.loads(reviewer_path.read_text(encoding="utf-8"))
    for item in reviewer["reviewed_artifacts"]:
        if item["path"] == repo_rel(class_path):
            item["sha256"] = sha256_file(class_path)
        if item["artifact_type"] == "CSH_PAIR_COMPARISON":
            item["sha256"] = sha256_file(pair_path)
    reviewer["record_integrity"]["canonical_record_sha256"] = canonical_sha256(reviewer)
    write_json(reviewer_path, reviewer)
    rebuild_manifest(wrong_pair)

    hash_mismatch = invalid_root / "raw_artifact_hash_mismatch"
    build_bundle(hash_mismatch)
    raw_response = hash_mismatch / "raw" / "CSH-RUN-003_response.json"
    write_text(raw_response, '{"tampered":true}\n')
    # Receipt and manifest remain unchanged, so direct raw-artifact verification fails.


def main() -> int:
    if FIXTURES.exists():
        shutil.rmtree(FIXTURES)
    FIXTURES.mkdir(parents=True, exist_ok=True)
    build_local_fixtures()
    build_integrated_fixtures()
    print(f"Built fixtures under {FIXTURES.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())