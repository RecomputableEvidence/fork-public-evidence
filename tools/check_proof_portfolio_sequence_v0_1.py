#!/usr/bin/env python3
"""Validate the bounded Fork proof-portfolio development sequence candidate."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = Path("docs/proof-atlas/development/PROOF_PORTFOLIO_REGISTRY_v0_1.json")
CONTRACT_PATH = Path("docs/proof-atlas/development/PROOF_PORTFOLIO_PROMOTION_CONTRACT_v0_1.json")
SCHEMA_PATH = Path("schemas/fork_proof_portfolio_sequence_v0_1.schema.json")
BASE = "cda8c68fd6a930c327b04bcbe72088c4fabd72fd"
PASS = "PROOF_PORTFOLIO_SEQUENCE_CANDIDATE_CONFORMS_NOT_ADMITTED"
FAIL = "PROOF_PORTFOLIO_SEQUENCE_CANDIDATE_INVALID"
PROOF_IDS = [f"PROOF-{number:03d}" for number in range(1, 7)]
PR_HEADS = {
    65: "479de5f929cb37377ccba5ef93f7a4f7b93e1120",
    84: "46fcd2c2580abd86ffbe215e6c387fee2bcb1b39",
    86: "f72ca3fad82bee068527fe63eaf1c8eba87dd698",
    100: "cdb757a97c2e554cf3df822e4764ac51122ca8eb",
    104: "2c58b95bd5d075f4e56c07939ec9c93dd374c07f",
    105: "b5c9d12109055a258b5ef33dac48f4f504b0a212",
}
COMMERCIAL_STAGES = [
    "PUBLIC_PROOF",
    "BUYER_SPECIFIC_DEMONSTRATION",
    "BOUNDED_PROOF_OF_VALUE",
    "LIMITED_PRODUCTION",
    "ENTERPRISE_EVIDENCE_SERVICE",
]
EFFECTS = {
    "evidence_standing": "NONE",
    "review_standing": "NONE",
    "admission_standing": "NONE",
    "authority_state": "NONE",
    "execution_state": "NONE",
    "provider_calls": 0,
    "pair_001_calls": 0,
    "repository_settings": "NONE",
    "main": "NONE",
}
PROOF_RE = re.compile(r"^PROOF-[0-9]{3}$")


class DuplicateKeyError(ValueError):
    pass


def unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite JSON number")
    if isinstance(value, dict):
        for child in value.values():
            finite(child)
    elif isinstance(value, list):
        for child in value:
            finite(child)


def absolute(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def load(path: Path) -> Any:
    with absolute(path).open("r", encoding="utf-8") as handle:
        value = json.load(
            handle,
            object_pairs_hook=unique_keys,
            parse_constant=reject_constant,
        )
    finite(value)
    return value


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def evaluate(
    registry_path: Path = REGISTRY_PATH,
    contract_path: Path = CONTRACT_PATH,
    *,
    check_git: bool = True,
) -> dict[str, Any]:
    findings: list[dict[str, str]] = []

    def add(code: str, detail: str, path: str) -> None:
        findings.append({"code": code, "detail": detail, "path": path})

    try:
        registry = load(registry_path)
        contract = load(contract_path)
        schema = load(SCHEMA_PATH)
    except Exception as exc:
        return {
            "checker": Path(__file__).name,
            "status": FAIL,
            "findings": [{"code": "PORTFOLIO_INPUT_INVALID", "detail": str(exc), "path": "$input"}],
        }

    if not isinstance(registry, dict) or not isinstance(contract, dict) or not isinstance(schema, dict):
        add("PORTFOLIO_ROOT_INVALID", "registry, contract, and schema roots must be objects", "$input")
        registry = registry if isinstance(registry, dict) else {}
        contract = contract if isinstance(contract, dict) else {}

    if registry.get("sequence_id") != "FORK-PROOF-PORTFOLIO-SEQUENCE-v0.1":
        add("SEQUENCE_ID_MISMATCH", "unexpected sequence identifier", "$.sequence_id")
    if registry.get("promotion_contract_path") != CONTRACT_PATH.as_posix():
        add("PROMOTION_CONTRACT_ROUTE_MISMATCH", "non-canonical contract path", "$.promotion_contract_path")
    if registry.get("descriptive_schema_path") != SCHEMA_PATH.as_posix():
        add("SCHEMA_ROUTE_MISMATCH", "non-canonical schema path", "$.descriptive_schema_path")
    construction = registry.get("construction_base", {})
    if not isinstance(construction, dict) or construction.get("commit_sha") != BASE:
        add("CONSTRUCTION_BASE_MISMATCH", "registry is not bound to the admitted route checkpoint", "$.construction_base")
    if construction.get("branch") != "preservation/clean-continuance-v0.1":
        add("CONSTRUCTION_BRANCH_MISMATCH", "registry must use the governed preservation branch", "$.construction_base.branch")

    if contract.get("contract_id") != "FORK-PROOF-PORTFOLIO-PROMOTION-CONTRACT-v0.1":
        add("CONTRACT_ID_MISMATCH", "unexpected contract identifier", "$contract.contract_id")
    gates_required = contract.get("finished_proof_required_gates")
    if not isinstance(gates_required, list) or not gates_required or len(gates_required) != len(set(gates_required)):
        add("REQUIRED_GATES_INVALID", "finished-proof gates must be a unique non-empty list", "$contract.finished_proof_required_gates")
        gates_required = []

    disallowed = contract.get("disallowed_promotions")
    pairs = {
        (item.get("from"), item.get("to"))
        for item in disallowed
        if isinstance(item, dict)
    } if isinstance(disallowed, list) else set()
    for pair in {
        ("CI_SUCCESS", "ADMITTED"),
        ("EXTERIOR_REVIEW", "AUTHORITY_OR_ENDORSEMENT"),
        ("MARKET_RELEVANCE", "TECHNICAL_OR_EVIDENTIARY_STANDING"),
        ("CORRECTION", "PREDECESSOR_FAILURE_ERASED"),
        ("PREREGISTRATION_COMPLETE", "EXECUTION_AUTHORIZED"),
    }:
        if pair not in pairs:
            add("REQUIRED_DISALLOWED_PROMOTION_MISSING", f"missing {pair[0]} -> {pair[1]}", "$contract.disallowed_promotions")

    ladder = registry.get("commercialization_ladder")
    stages = [
        item.get("stage") if isinstance(item, dict) else None
        for item in ladder
    ] if isinstance(ladder, list) else []
    if stages != COMMERCIAL_STAGES:
        add("COMMERCIAL_LADDER_ORDER_MISMATCH", f"found {stages!r}", "$.commercialization_ladder")

    purposes = registry.get("source_pr_purpose_registry")
    by_pr: dict[int, dict[str, Any]] = {}
    if not isinstance(purposes, list):
        add("PR_PURPOSE_REGISTRY_INVALID", "purpose registry must be an array", "$.source_pr_purpose_registry")
        purposes = []
    for index, item in enumerate(purposes):
        path = f"$.source_pr_purpose_registry[{index}]"
        if not isinstance(item, dict) or not isinstance(item.get("pr_number"), int):
            add("PR_PURPOSE_INVALID", "purpose entry requires an integer PR number", path)
            continue
        number = item["pr_number"]
        if number in by_pr:
            add("PR_PURPOSE_DUPLICATE", f"duplicate PR #{number}", path)
            continue
        by_pr[number] = item
        if item.get("exact_head") != PR_HEADS.get(number):
            add("PR_EXACT_HEAD_MISMATCH", f"PR #{number} head mismatch", f"{path}.exact_head")
        if not isinstance(item.get("primary_role"), str) or not item["primary_role"]:
            add("PR_PRIMARY_ROLE_MISSING", "one primary role is required", f"{path}.primary_role")
        served = item.get("serves_proof_ids")
        if not isinstance(served, list) or not served or len(served) != len(set(served)):
            add("PR_SERVED_PROOFS_INVALID", "served proofs must be a unique non-empty list", f"{path}.serves_proof_ids")
        if item.get("exact_head_ci") != "SUCCESS":
            add("CAPTURED_EXACT_HEAD_CI_NOT_SUCCESS", "captured PR head must record CI success", f"{path}.exact_head_ci")
        expected_effect = "ROUTING_ONLY" if number == 104 else "NONE"
        if item.get("admission_effect") != expected_effect:
            add("SOURCE_PR_ADMISSION_OVERCLAIM", f"PR #{number} expected {expected_effect}", f"{path}.admission_effect")
    if set(by_pr) != set(PR_HEADS):
        add("PR_PURPOSE_SET_MISMATCH", f"found {sorted(by_pr)!r}", "$.source_pr_purpose_registry")

    proofs = registry.get("proof_sequence")
    proof_by_id: dict[str, dict[str, Any]] = {}
    seen_ids: list[str] = []
    seen_numbers: list[int] = []
    if not isinstance(proofs, list):
        add("PROOF_SEQUENCE_INVALID", "proof sequence must be an array", "$.proof_sequence")
        proofs = []
    for index, proof in enumerate(proofs):
        path = f"$.proof_sequence[{index}]"
        if not isinstance(proof, dict):
            add("PROOF_ENTRY_INVALID", "proof entry must be an object", path)
            continue
        proof_id = proof.get("proof_id")
        number = proof.get("sequence")
        if not isinstance(proof_id, str) or PROOF_RE.fullmatch(proof_id) is None:
            add("PROOF_ID_INVALID", "proof identifier must match PROOF-NNN", f"{path}.proof_id")
            continue
        if proof_id in proof_by_id:
            add("PROOF_ID_DUPLICATE", f"duplicate {proof_id}", f"{path}.proof_id")
        proof_by_id[proof_id] = proof
        seen_ids.append(proof_id)
        if isinstance(number, int):
            seen_numbers.append(number)
        else:
            add("PROOF_SEQUENCE_NUMBER_INVALID", "sequence must be an integer", f"{path}.sequence")

        dependencies = proof.get("depends_on")
        if not isinstance(dependencies, list) or len(dependencies) != len(set(dependencies)):
            add("PROOF_DEPENDENCIES_INVALID", "dependencies must be a unique list", f"{path}.depends_on")
            dependencies = []
        for dependency in dependencies:
            if dependency not in seen_ids[:-1]:
                add("PROOF_DEPENDENCY_NOT_EARLIER", f"{dependency!r} is not earlier", f"{path}.depends_on")

        source_prs = proof.get("source_prs")
        if not isinstance(source_prs, list) or len(source_prs) != len(set(source_prs)):
            add("PROOF_SOURCE_PRS_INVALID", "source PRs must be a unique list", f"{path}.source_prs")
            source_prs = []
        for pr_number in source_prs:
            purpose = by_pr.get(pr_number)
            if purpose is None:
                add("PROOF_SOURCE_PR_UNREGISTERED", f"PR #{pr_number} is unregistered", f"{path}.source_prs")
            elif proof_id not in purpose.get("serves_proof_ids", []):
                add("PROOF_SOURCE_PR_PURPOSE_MISMATCH", f"PR #{pr_number} does not serve {proof_id}", f"{path}.source_prs")
        if not source_prs and not isinstance(proof.get("source_identifier"), str):
            add("PROOF_SOURCE_IDENTIFIER_MISSING", "non-PR source requires source_identifier", path)

        for field in ("target_title", "current_form", "institutional_problem", "bounded_claim", "next_required_action"):
            if not isinstance(proof.get(field), str) or not proof[field]:
                add("PROOF_REQUIRED_TEXT_MISSING", f"{field} is required", f"{path}.{field}")

        scientific = proof.get("scientific_grade")
        if not isinstance(scientific, dict):
            add("SCIENTIFIC_GRADE_INVALID", "scientific_grade must be an object", f"{path}.scientific_grade")
        else:
            for field in ("research_question", "falsification_condition", "recomputation_path"):
                if not isinstance(scientific.get(field), str) or not scientific[field]:
                    add("SCIENTIFIC_FIELD_MISSING", f"{field} is required", f"{path}.scientific_grade.{field}")
            if scientific.get("adverse_case_required") is not True:
                add("ADVERSE_CASE_REQUIREMENT_REMOVED", "adverse case requirement must remain true", f"{path}.scientific_grade.adverse_case_required")

        commercial = proof.get("commercial_track")
        if not isinstance(commercial, dict):
            add("COMMERCIAL_TRACK_INVALID", "commercial_track must be an object", f"{path}.commercial_track")
            commercial = {}
        for field in ("capability", "offer_state", "value_hypothesis"):
            if not isinstance(commercial.get(field), str) or not commercial[field]:
                add("COMMERCIAL_FIELD_MISSING", f"{field} is required", f"{path}.commercial_track.{field}")

        gates = proof.get("gates")
        if not isinstance(gates, dict):
            add("PROOF_GATES_INVALID", "gates must be an object", f"{path}.gates")
            gates = {}
        if set(gates) != set(gates_required):
            add("PROOF_GATE_SET_MISMATCH", "gate set does not match promotion contract", f"{path}.gates")
        if any(not isinstance(value, bool) for value in gates.values()):
            add("PROOF_GATE_NOT_BOOLEAN", "all gate values must be boolean", f"{path}.gates")

        finished = proof.get("promotion_state") == "FINISHED_PROOF_SURFACE_ADMITTED"
        if finished and (not gates_required or not all(gates.get(name) is True for name in gates_required)):
            add("FINISHED_PROOF_GATE_INCOMPLETE", "finished proof requires every gate", f"{path}.promotion_state")
        if not finished and commercial.get("offer_state") == "ACTIVE_PRODUCTION_CAPABILITY":
            add("COMMERCIAL_READINESS_OVERCLAIM", "unfinished proof cannot claim active production capability", f"{path}.commercial_track.offer_state")
        if commercial.get("offer_state") == "ACTIVE_PRODUCTION_CAPABILITY" and gates.get("institutional_validation") is not True:
            add("ACTIVE_OFFER_WITHOUT_INSTITUTIONAL_VALIDATION", "active offer requires institutional validation", f"{path}.commercial_track.offer_state")
        if proof.get("execution_authorized") is not False:
            add("EXECUTION_AUTHORITY_OVERCLAIM", "portfolio cannot authorize execution", f"{path}.execution_authorized")
        if proof.get("provider_calls") != 0:
            add("PROVIDER_CALL_EFFECT_NONZERO", "provider calls must remain zero", f"{path}.provider_calls")
        non_claims = proof.get("non_claims")
        if not isinstance(non_claims, list) or not non_claims:
            add("PROOF_NON_CLAIMS_INVALID", "proof requires explicit non-claims", f"{path}.non_claims")

    if seen_ids != PROOF_IDS:
        add("PROOF_SEQUENCE_ID_ORDER_MISMATCH", f"found {seen_ids!r}", "$.proof_sequence")
    if seen_numbers != list(range(1, 7)):
        add("PROOF_SEQUENCE_NUMBER_ORDER_MISMATCH", f"found {seen_numbers!r}", "$.proof_sequence")
    for pr_number, purpose in by_pr.items():
        for proof_id in purpose.get("serves_proof_ids", []):
            if proof_id not in proof_by_id:
                add("PR_PURPOSE_UNKNOWN_PROOF", f"PR #{pr_number} references {proof_id}", "$.source_pr_purpose_registry")

    if registry.get("effects") != EFFECTS:
        add("PORTFOLIO_EFFECT_WIDENED", "registry non-effects changed", "$.effects")
    contract_effects = {key: value for key, value in EFFECTS.items() if key not in {"repository_settings", "main"}}
    if contract.get("effects") != contract_effects:
        add("CONTRACT_EFFECT_WIDENED", "contract non-effects changed", "$contract.effects")
    if registry.get("standing") != "PROOF_PORTFOLIO_DEVELOPMENT_SEQUENCE_CANDIDATE_NOT_ADMITTED":
        add("REGISTRY_STANDING_OVERCLAIM", "registry must remain a candidate", "$.standing")
    if contract.get("standing") != "PROMOTION_CONTRACT_CANDIDATE_NOT_ADMITTED":
        add("CONTRACT_STANDING_OVERCLAIM", "contract must remain a candidate", "$contract.standing")

    if check_git:
        resolved = git("rev-parse", f"{BASE}^{{commit}}")
        ancestor = git("merge-base", "--is-ancestor", BASE, "HEAD")
        if resolved.returncode != 0 or resolved.stdout.strip() != BASE:
            add("CONSTRUCTION_BASE_UNAVAILABLE", resolved.stderr.strip(), "$git")
        if ancestor.returncode != 0:
            add("CANDIDATE_NOT_DESCENDED_FROM_CONSTRUCTION_BASE", "HEAD is not descended from construction base", "$git")

    findings.sort(key=lambda item: (item["code"], item["path"], item["detail"]))
    return {
        "checker": Path(__file__).name,
        "status": PASS if not findings else FAIL,
        "construction_base": BASE,
        "proof_count": len(proofs),
        "registered_pr_count": len(by_pr),
        "provider_calls": registry.get("effects", {}).get("provider_calls")
        if isinstance(registry.get("effects"), dict)
        else None,
        "findings": findings,
        "non_claims": [
            "Portfolio conformance is not proof completion or admission.",
            "A declared PR purpose creates no source standing.",
            "Scientific relevance, institutional utility, and commercial relevance remain separate dimensions.",
            "No checker result authorizes execution, provider calls, production use, or institutional reliance.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--contract", type=Path, default=CONTRACT_PATH)
    parser.add_argument("--no-git", action="store_true")
    args = parser.parse_args()
    result = evaluate(args.registry, args.contract, check_git=not args.no_git)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not result["findings"] else 1


if __name__ == "__main__":
    sys.exit(main())
