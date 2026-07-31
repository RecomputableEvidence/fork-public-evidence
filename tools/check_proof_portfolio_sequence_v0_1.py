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

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = Path(
    "docs/proof-atlas/development/PROOF_PORTFOLIO_REGISTRY_v0_1.json"
)
CONTRACT_PATH = Path(
    "docs/proof-atlas/development/PROOF_PORTFOLIO_PROMOTION_CONTRACT_v0_1.json"
)
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
PR_ROLES = {
    65: "CORRECTION_AND_NEGATIVE_EVIDENCE",
    84: "RESEARCH_PROTOCOL_AND_CANDIDATE_CASE",
    86: "SECOND_ORDER_META_ASSESSMENT",
    100: "DETERMINISTIC_INTEROPERABILITY_EXPERIMENT",
    104: "PUBLIC_ROUTING",
    105: "EXTERIOR_RECOMPUTATION_AND_TEMPORAL_SUCCESSION",
}
PR_SERVES = {
    65: ["PROOF-002"],
    84: ["PROOF-005"],
    86: ["PROOF-005"],
    100: ["PROOF-004"],
    104: ["PROOF-001"],
    105: ["PROOF-003"],
}
RECOMPUTATION_PATHS = {
    "PROOF-001": "tools/run_proof_001_review_does_not_silently_travel_v0_1.py",
    "PROOF-002": "tools/check_longitudinal_reconstruction_day0_packet_v0_1_1.py",
    "PROOF-003": "tools/check_shayne_pr63_pr64_attachment_successor_v0_1.py",
    "PROOF-004": "tools/check_ghch_candidate_v0_1.py",
    "PROOF-005": "tools/check_fork_cad_candidate_v0_1.py",
    "PROOF-006": "INTERIOR_ONLY_UNTIL_SEPARATELY_PUBLISHED",
}
SOURCE_IDENTIFIERS = {
    "PROOF-001": (
        "docs/proof-atlas/PROOF-001-review-does-not-silently-travel-v0.1/"
        "PROOF-MANIFEST.json"
    ),
    "PROOF-006": "CROSS_SYSTEM_HANDOFF_SEQUENCE_PREREGISTRATION_v0_1",
}
PROMOTION_STATES = {
    "PROOF-001": "PROOF_CANDIDATE_NOT_FINISHED",
    "PROOF-002": "SOURCE_NOT_READY_FOR_PROOF_PACKAGING",
    "PROOF-003": "SOURCE_NOT_READY_FOR_PROOF_PACKAGING",
    "PROOF-004": "SOURCE_NOT_READY_FOR_PROOF_PACKAGING",
    "PROOF-005": "SOURCE_NOT_READY_FOR_PROOF_PACKAGING",
    "PROOF-006": "PREREGISTRATION_REPAIR_AND_EXECUTION_AUTHORIZATION_REQUIRED",
}
COMMERCIAL_STAGES = [
    "PUBLIC_PROOF",
    "BUYER_SPECIFIC_DEMONSTRATION",
    "BOUNDED_PROOF_OF_VALUE",
    "LIMITED_PRODUCTION",
    "ENTERPRISE_EVIDENCE_SERVICE",
]
REQUIRED_DIMENSIONS = [
    "institutional_problem",
    "bounded_claim",
    "scientific_grade.research_question",
    "scientific_grade.falsification_condition",
    "scientific_grade.recomputation_path",
    "commercial_track.capability",
    "commercial_track.buyer_roles",
    "commercial_track.service_path",
    "commercial_track.offer_state",
    "commercial_track.value_hypothesis",
    "non_claims",
    "next_required_action",
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
SELF_ADMISSION_RULE = (
    "This development registry may not declare FINISHED_PROOF_SURFACE_ADMITTED. "
    "A later successor must bind a separate proof-packaging admission artifact "
    "and be reviewed under a separately authorized admission decision."
)
ACTIVE_OFFER_RULE = (
    "This development registry may not declare ACTIVE_PRODUCTION_CAPABILITY "
    "because it contains no separately bound operational authorization or "
    "privacy, security, retention, rollback, and incident-control record."
)


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


def json_path(error: Any) -> str:
    parts = [str(part) for part in error.absolute_path]
    return "$" if not parts else "$." + ".".join(parts)


def make_result(
    findings: list[dict[str, str]],
    registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    registry = registry or {}
    proofs = registry.get("proof_sequence", [])
    purposes = registry.get("source_pr_purpose_registry", [])
    effects = registry.get("effects", {})
    return {
        "checker": Path(__file__).name,
        "status": PASS if not findings else FAIL,
        "construction_base": BASE,
        "proof_count": len(proofs) if isinstance(proofs, list) else 0,
        "registered_pr_count": len(purposes) if isinstance(purposes, list) else 0,
        "provider_calls": effects.get("provider_calls")
        if isinstance(effects, dict)
        else None,
        "findings": sorted(
            findings,
            key=lambda item: (item["code"], item["path"], item["detail"]),
        ),
        "non_claims": [
            "Portfolio conformance is not proof completion or admission.",
            "A declared PR purpose creates no source standing.",
            (
                "Scientific relevance, institutional utility, and commercial "
                "relevance remain separate dimensions."
            ),
            (
                "No checker result authorizes execution, provider calls, "
                "production use, or institutional reliance."
            ),
        ],
    }


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
        return make_result(
            [{"code": "PORTFOLIO_INPUT_INVALID", "detail": str(exc), "path": "$input"}]
        )

    if not isinstance(registry, dict):
        add("PORTFOLIO_ROOT_INVALID", "registry root must be an object", "$input")
        return make_result(findings)
    if not isinstance(contract, dict):
        add("CONTRACT_ROOT_INVALID", "contract root must be an object", "$contract")
        return make_result(findings, registry)
    if not isinstance(schema, dict):
        add("SCHEMA_ROOT_INVALID", "schema root must be an object", "$schema")
        return make_result(findings, registry)

    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        schema_errors = sorted(
            validator.iter_errors(registry),
            key=lambda error: (list(error.absolute_path), error.message),
        )
    except SchemaError as exc:
        add("PORTFOLIO_SCHEMA_INVALID", str(exc), "$schema")
        return make_result(findings, registry)

    for error in schema_errors:
        add("REGISTRY_SCHEMA_INVALID", error.message, json_path(error))
    if schema_errors:
        return make_result(findings, registry)

    if registry.get("sequence_id") != "FORK-PROOF-PORTFOLIO-SEQUENCE-v0.1":
        add("SEQUENCE_ID_MISMATCH", "unexpected sequence identifier", "$.sequence_id")
    if registry.get("promotion_contract_path") != CONTRACT_PATH.as_posix():
        add(
            "PROMOTION_CONTRACT_ROUTE_MISMATCH",
            "non-canonical contract path",
            "$.promotion_contract_path",
        )
    if registry.get("descriptive_schema_path") != SCHEMA_PATH.as_posix():
        add(
            "SCHEMA_ROUTE_MISMATCH",
            "non-canonical schema path",
            "$.descriptive_schema_path",
        )

    construction = registry.get("construction_base", {})
    if construction.get("commit_sha") != BASE:
        add(
            "CONSTRUCTION_BASE_MISMATCH",
            "registry is not bound to the admitted route checkpoint",
            "$.construction_base",
        )
    if construction.get("branch") != "preservation/clean-continuance-v0.1":
        add(
            "CONSTRUCTION_BRANCH_MISMATCH",
            "registry must use the governed preservation branch",
            "$.construction_base.branch",
        )

    if (
        contract.get("contract_id")
        != "FORK-PROOF-PORTFOLIO-PROMOTION-CONTRACT-v0.1"
    ):
        add(
            "CONTRACT_ID_MISMATCH",
            "unexpected contract identifier",
            "$contract.contract_id",
        )

    gates_required = contract.get("finished_proof_required_gates")
    if (
        not isinstance(gates_required, list)
        or not gates_required
        or any(not isinstance(item, str) or not item for item in gates_required)
        or len(gates_required) != len(set(gates_required))
    ):
        add(
            "REQUIRED_GATES_INVALID",
            "finished-proof gates must be unique non-empty strings",
            "$contract.finished_proof_required_gates",
        )
        gates_required = []

    role_enum = contract.get("source_role_enum")
    if (
        not isinstance(role_enum, list)
        or any(not isinstance(item, str) or not item for item in role_enum)
        or len(role_enum) != len(set(role_enum))
    ):
        add(
            "SOURCE_ROLE_ENUM_INVALID",
            "source roles must be unique non-empty strings",
            "$contract.source_role_enum",
        )
        role_enum = []

    promotion_enum = contract.get("promotion_state_enum")
    if (
        not isinstance(promotion_enum, list)
        or any(not isinstance(item, str) or not item for item in promotion_enum)
        or len(promotion_enum) != len(set(promotion_enum))
    ):
        add(
            "PROMOTION_STATE_ENUM_INVALID",
            "promotion states must be unique non-empty strings",
            "$contract.promotion_state_enum",
        )
        promotion_enum = []

    if contract.get("required_proof_dimensions") != REQUIRED_DIMENSIONS:
        add(
            "REQUIRED_PROOF_DIMENSIONS_MISMATCH",
            "required proof dimensions changed",
            "$contract.required_proof_dimensions",
        )
    if contract.get("self_admission_rule") != SELF_ADMISSION_RULE:
        add(
            "SELF_ADMISSION_RULE_MISSING",
            "candidate self-admission prohibition changed",
            "$contract.self_admission_rule",
        )
    if contract.get("active_offer_rule") != ACTIVE_OFFER_RULE:
        add(
            "ACTIVE_OFFER_RULE_MISSING",
            "candidate active-offer prohibition changed",
            "$contract.active_offer_rule",
        )

    disallowed = contract.get("disallowed_promotions")
    pairs = (
        {
            (item.get("from"), item.get("to"))
            for item in disallowed
            if isinstance(item, dict)
        }
        if isinstance(disallowed, list)
        else set()
    )
    for pair in {
        ("CI_SUCCESS", "ADMITTED"),
        ("EXTERIOR_REVIEW", "AUTHORITY_OR_ENDORSEMENT"),
        ("MARKET_RELEVANCE", "TECHNICAL_OR_EVIDENTIARY_STANDING"),
        ("CORRECTION", "PREDECESSOR_FAILURE_ERASED"),
        ("PREREGISTRATION_COMPLETE", "EXECUTION_AUTHORIZED"),
    }:
        if pair not in pairs:
            add(
                "REQUIRED_DISALLOWED_PROMOTION_MISSING",
                f"missing {pair[0]} -> {pair[1]}",
                "$contract.disallowed_promotions",
            )

    ladder = registry.get("commercialization_ladder", [])
    stages = [item.get("stage") for item in ladder]
    if stages != COMMERCIAL_STAGES:
        add(
            "COMMERCIAL_LADDER_ORDER_MISMATCH",
            f"found {stages!r}",
            "$.commercialization_ladder",
        )

    purposes = registry.get("source_pr_purpose_registry", [])
    by_pr: dict[int, dict[str, Any]] = {}
    for index, item in enumerate(purposes):
        path = f"$.source_pr_purpose_registry[{index}]"
        number = item["pr_number"]
        if number in by_pr:
            add("PR_PURPOSE_DUPLICATE", f"duplicate PR #{number}", path)
            continue
        by_pr[number] = item
        if item.get("exact_head") != PR_HEADS.get(number):
            add(
                "PR_EXACT_HEAD_MISMATCH",
                f"PR #{number} head mismatch",
                f"{path}.exact_head",
            )
        if item.get("primary_role") not in role_enum:
            add(
                "PR_PRIMARY_ROLE_NOT_IN_CONTRACT",
                f"PR #{number} role is not permitted",
                f"{path}.primary_role",
            )
        if item.get("primary_role") != PR_ROLES.get(number):
            add(
                "PR_PRIMARY_ROLE_MISMATCH",
                f"PR #{number} purpose changed",
                f"{path}.primary_role",
            )
        if item.get("serves_proof_ids") != PR_SERVES.get(number):
            add(
                "PR_SERVED_PROOFS_MISMATCH",
                f"PR #{number} proof assignment changed",
                f"{path}.serves_proof_ids",
            )
        if item.get("exact_head_ci") != "SUCCESS":
            add(
                "CAPTURED_EXACT_HEAD_CI_NOT_SUCCESS",
                "captured PR head must record CI success",
                f"{path}.exact_head_ci",
            )
        expected_effect = "ROUTING_ONLY" if number == 104 else "NONE"
        if item.get("admission_effect") != expected_effect:
            add(
                "SOURCE_PR_ADMISSION_OVERCLAIM",
                f"PR #{number} expected {expected_effect}",
                f"{path}.admission_effect",
            )
    if set(by_pr) != set(PR_HEADS):
        add(
            "PR_PURPOSE_SET_MISMATCH",
            f"found {sorted(by_pr)!r}",
            "$.source_pr_purpose_registry",
        )

    proofs = registry.get("proof_sequence", [])
    proof_by_id: dict[str, dict[str, Any]] = {}
    seen_ids: list[str] = []
    seen_numbers: list[int] = []
    for index, proof in enumerate(proofs):
        path = f"$.proof_sequence[{index}]"
        proof_id = proof["proof_id"]
        number = proof["sequence"]
        if PROOF_RE.fullmatch(proof_id) is None:
            add(
                "PROOF_ID_INVALID",
                "proof identifier must match PROOF-NNN",
                f"{path}.proof_id",
            )
            continue
        if proof_id in proof_by_id:
            add("PROOF_ID_DUPLICATE", f"duplicate {proof_id}", f"{path}.proof_id")
        proof_by_id[proof_id] = proof
        seen_ids.append(proof_id)
        seen_numbers.append(number)

        dependencies = proof["depends_on"]
        for dependency in dependencies:
            if dependency not in seen_ids[:-1]:
                add(
                    "PROOF_DEPENDENCY_NOT_EARLIER",
                    f"{dependency!r} is not earlier",
                    f"{path}.depends_on",
                )

        source_prs = proof["source_prs"]
        for pr_number in source_prs:
            purpose = by_pr.get(pr_number)
            if purpose is None:
                add(
                    "PROOF_SOURCE_PR_UNREGISTERED",
                    f"PR #{pr_number} is unregistered",
                    f"{path}.source_prs",
                )
                continue
            if purpose.get("primary_role") == "PUBLIC_ROUTING":
                add(
                    "ROUTING_PR_USED_AS_EVIDENCE_SOURCE",
                    f"PR #{pr_number} is routing-only",
                    f"{path}.source_prs",
                )
            if proof_id not in purpose.get("serves_proof_ids", []):
                add(
                    "PROOF_SOURCE_PR_PURPOSE_MISMATCH",
                    f"PR #{pr_number} does not serve {proof_id}",
                    f"{path}.source_prs",
                )

        expected_identifier = SOURCE_IDENTIFIERS.get(proof_id)
        actual_identifier = proof.get("source_identifier")
        if expected_identifier is not None and actual_identifier != expected_identifier:
            add(
                "PROOF_SOURCE_IDENTIFIER_MISMATCH",
                f"{proof_id} source identifier changed",
                f"{path}.source_identifier",
            )
        if expected_identifier is None and actual_identifier is not None:
            add(
                "UNEXPECTED_PROOF_SOURCE_IDENTIFIER",
                f"{proof_id} must use registered source PRs",
                f"{path}.source_identifier",
            )
        if not source_prs and expected_identifier is None:
            add(
                "PROOF_SOURCE_IDENTIFIER_MISSING",
                "non-PR source requires source_identifier",
                path,
            )

        scientific = proof["scientific_grade"]
        if (
            scientific.get("recomputation_path")
            != RECOMPUTATION_PATHS.get(proof_id)
        ):
            add(
                "PROOF_RECOMPUTATION_PATH_MISMATCH",
                f"{proof_id} recomputation route changed or is nonexistent",
                f"{path}.scientific_grade.recomputation_path",
            )
        if scientific.get("adverse_case_required") is not True:
            add(
                "ADVERSE_CASE_REQUIREMENT_REMOVED",
                "adverse case requirement must remain true",
                f"{path}.scientific_grade.adverse_case_required",
            )

        gates = proof["gates"]
        if set(gates) != set(gates_required):
            add(
                "PROOF_GATE_SET_MISMATCH",
                "gate set does not match promotion contract",
                f"{path}.gates",
            )
        if any(not isinstance(value, bool) for value in gates.values()):
            add(
                "PROOF_GATE_NOT_BOOLEAN",
                "all gate values must be boolean",
                f"{path}.gates",
            )

        promotion_state = proof["promotion_state"]
        if promotion_state not in promotion_enum:
            add(
                "PROMOTION_STATE_NOT_IN_CONTRACT",
                f"{promotion_state!r} is not permitted",
                f"{path}.promotion_state",
            )
        if promotion_state != PROMOTION_STATES.get(proof_id):
            add(
                "PROOF_PROMOTION_STATE_MISMATCH",
                f"{proof_id} captured promotion state changed",
                f"{path}.promotion_state",
            )

        finished = promotion_state == "FINISHED_PROOF_SURFACE_ADMITTED"
        if finished and not all(gates.get(name) is True for name in gates_required):
            add(
                "FINISHED_PROOF_GATE_INCOMPLETE",
                "finished proof requires every gate",
                f"{path}.promotion_state",
            )
        if finished:
            add(
                "FINISHED_PROOF_SELF_ADMISSION_PROHIBITED",
                "this candidate cannot perform proof admission",
                f"{path}.promotion_state",
            )
        if gates_required and all(gates.get(name) is True for name in gates_required):
            add(
                "ALL_GATES_TRUE_WITHOUT_SEPARATE_ADMISSION_ARTIFACT",
                "gate booleans cannot perform a separate admission act",
                f"{path}.gates",
            )

        offer_state = proof["commercial_track"]["offer_state"]
        if offer_state == "ACTIVE_PRODUCTION_CAPABILITY":
            add(
                "ACTIVE_PRODUCTION_OFFER_OUT_OF_SCOPE",
                "this registry has no bound operational authorization",
                f"{path}.commercial_track.offer_state",
            )
        if (
            promotion_state == "SOURCE_NOT_READY_FOR_PROOF_PACKAGING"
            and all(
                gates.get(name) is True
                for name in (
                    "exact_source_binding",
                    "exact_head_ci",
                    "exterior_recomputation_or_declared_not_required",
                    "source_disposition_adjudicated",
                    "source_admission_or_explicit_bounded_basis",
                )
            )
        ):
            add(
                "SOURCE_READINESS_STATE_STALE",
                "source-not-ready state conflicts with completed source gates",
                f"{path}.promotion_state",
            )

        if proof["execution_authorized"] is not False:
            add(
                "EXECUTION_AUTHORITY_OVERCLAIM",
                "portfolio cannot authorize execution",
                f"{path}.execution_authorized",
            )
        if proof["provider_calls"] != 0:
            add(
                "PROVIDER_CALL_EFFECT_NONZERO",
                "provider calls must remain zero",
                f"{path}.provider_calls",
            )

    if seen_ids != PROOF_IDS:
        add(
            "PROOF_SEQUENCE_ID_ORDER_MISMATCH",
            f"found {seen_ids!r}",
            "$.proof_sequence",
        )
    if seen_numbers != list(range(1, 7)):
        add(
            "PROOF_SEQUENCE_NUMBER_ORDER_MISMATCH",
            f"found {seen_numbers!r}",
            "$.proof_sequence",
        )

    for pr_number, purpose in by_pr.items():
        if purpose.get("primary_role") == "PUBLIC_ROUTING":
            continue
        for proof_id in purpose.get("serves_proof_ids", []):
            proof = proof_by_id.get(proof_id, {})
            if pr_number not in proof.get("source_prs", []):
                add(
                    "PR_PURPOSE_NOT_BOUND_FROM_PROOF",
                    f"PR #{pr_number} is not listed by {proof_id}",
                    "$.source_pr_purpose_registry",
                )

    if registry.get("effects") != EFFECTS:
        add("PORTFOLIO_EFFECT_WIDENED", "registry non-effects changed", "$.effects")
    contract_effects = {
        key: value
        for key, value in EFFECTS.items()
        if key not in {"repository_settings", "main"}
    }
    if contract.get("effects") != contract_effects:
        add(
            "CONTRACT_EFFECT_WIDENED",
            "contract non-effects changed",
            "$contract.effects",
        )
    if (
        registry.get("standing")
        != "PROOF_PORTFOLIO_DEVELOPMENT_SEQUENCE_CANDIDATE_NOT_ADMITTED"
    ):
        add(
            "REGISTRY_STANDING_OVERCLAIM",
            "registry must remain a candidate",
            "$.standing",
        )
    if contract.get("standing") != "PROMOTION_CONTRACT_CANDIDATE_NOT_ADMITTED":
        add(
            "CONTRACT_STANDING_OVERCLAIM",
            "contract must remain a candidate",
            "$contract.standing",
        )

    proof_001_source = SOURCE_IDENTIFIERS["PROOF-001"]
    if not (ROOT / proof_001_source).is_file():
        add(
            "PROOF_001_SOURCE_MANIFEST_MISSING",
            "bound Proof 001 source manifest is absent",
            "$.proof_sequence[0].source_identifier",
        )
    proof_001_wrapper = RECOMPUTATION_PATHS["PROOF-001"]
    if not (ROOT / proof_001_wrapper).is_file():
        add(
            "PROOF_001_WRAPPER_MISSING",
            "bound Proof 001 wrapper is absent",
            "$.proof_sequence[0].scientific_grade.recomputation_path",
        )

    if check_git:
        resolved = git("rev-parse", f"{BASE}^{{commit}}")
        ancestor = git("merge-base", "--is-ancestor", BASE, "HEAD")
        if resolved.returncode != 0 or resolved.stdout.strip() != BASE:
            add(
                "CONSTRUCTION_BASE_UNAVAILABLE",
                resolved.stderr.strip(),
                "$git",
            )
        if ancestor.returncode != 0:
            add(
                "CANDIDATE_NOT_DESCENDED_FROM_CONSTRUCTION_BASE",
                "HEAD is not descended from construction base",
                "$git",
            )

    return make_result(findings, registry)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--contract", type=Path, default=CONTRACT_PATH)
    parser.add_argument("--no-git", action="store_true")
    args = parser.parse_args()
    result = evaluate(
        args.registry,
        args.contract,
        check_git=not args.no_git,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not result["findings"] else 1


if __name__ == "__main__":
    sys.exit(main())
