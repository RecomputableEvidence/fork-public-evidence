#!/usr/bin/env python3
"""Validate Fork Proof Portfolio Sequence v0.2 without promoting proof standing."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path("docs/proof-atlas/development/v0.2/PROOF_PORTFOLIO_REGISTRY_v0_2.json")
CONTRACT = Path("docs/proof-atlas/development/v0.2/PROOF_PORTFOLIO_PROMOTION_CONTRACT_v0_2.json")
SCHEMA = Path("schemas/fork_proof_portfolio_sequence_v0_2.schema.json")
BASE = "8f17d3de2d22e9dcb1f49c3813926d6166bc1bb8"
PASS = "PROOF_PORTFOLIO_SEQUENCE_V0_2_CANDIDATE_CONFORMS_NOT_ADMITTED"
FAIL = "PROOF_PORTFOLIO_SEQUENCE_V0_2_CANDIDATE_INVALID"
PROOF_IDS = [f"PROOF-{n:03d}" for n in range(1, 7)]
SAFE_EXECUTION_STATES = {
    "NO_NEW_EXECUTION_AUTHORIZED",
    "LIVE_ADAPTERS_NOT_AUTHORIZED",
    "LIVE_EXECUTION_AND_PROVIDER_CALLS_CLOSED",
}


class DuplicateKeyError(ValueError):
    pass


def _unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def _finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite JSON number")
    if isinstance(value, dict):
        for child in value.values():
            _finite(child)
    elif isinstance(value, list):
        for child in value:
            _finite(child)


def load(path: Path) -> Any:
    target = path if path.is_absolute() else ROOT / path
    with target.open("r", encoding="utf-8") as handle:
        value = json.load(handle, object_pairs_hook=_unique, parse_constant=_reject_constant)
    _finite(value)
    return value


def evaluate(registry_path: Path = REGISTRY) -> dict[str, Any]:
    findings: list[dict[str, str]] = []

    def add(code: str, path: str, detail: str) -> None:
        findings.append({"code": code, "path": path, "detail": detail})

    try:
        registry = load(registry_path)
        contract = load(CONTRACT)
        schema = load(SCHEMA)
    except Exception as exc:
        add("INPUT_INVALID", "$input", str(exc))
        return _result(findings)

    if not isinstance(registry, dict) or not isinstance(contract, dict) or not isinstance(schema, dict):
        add("ROOT_INVALID", "$", "registry, contract, and schema roots must be objects")
        return _result(findings)

    errors = sorted(Draft202012Validator(schema).iter_errors(registry), key=lambda e: (list(e.absolute_path), e.message))
    for error in errors:
        path = "$" + "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.absolute_path)
        add("REGISTRY_SCHEMA_INVALID", path, error.message)
    if errors:
        return _result(findings, registry)

    if registry["construction_base"]["commit_sha"] != BASE:
        add("BASE_MISMATCH", "$.construction_base.commit_sha", "v0.2 must bind the post-PR118 governed basis")

    proofs = registry["proof_sequence"]
    ids = [item["proof_id"] for item in proofs]
    if ids != PROOF_IDS:
        add("PROOF_ORDER_MISMATCH", "$.proof_sequence", f"expected {PROOF_IDS!r}, found {ids!r}")

    if contract.get("proof_order") != PROOF_IDS:
        add("CONTRACT_ORDER_MISMATCH", "$contract.proof_order", "contract proof order changed")

    required_pairs = {
        ("CI_SUCCESS", "ADMISSION"),
        ("EXTERIOR_REVIEW", "AUTHORITY_OR_ENDORSEMENT"),
        ("SOURCE_EVIDENCE_ADMITTED", "PROOF_PACKAGING_ADMITTED"),
        ("SOURCE_PR_MERGED", "PROOF_STANDING"),
        ("PREREGISTRATION_COMPLETE", "EXECUTION_AUTHORIZED"),
    }
    observed_pairs = {
        (item.get("from"), item.get("to"))
        for item in contract.get("disallowed_promotions", [])
        if isinstance(item, dict)
    }
    missing = required_pairs - observed_pairs
    if missing:
        add("PROMOTION_GUARD_MISSING", "$contract.disallowed_promotions", repr(sorted(missing)))

    by_id = {item["proof_id"]: item for item in proofs}
    expected_states = {
        "PROOF-002": "CORRECTED_HEAD_EXTERIOR_RECOMPUTATION_PENDING",
        "PROOF-003": "ADMITTED_EXTERIOR_EVIDENCE_SUCCESSOR",
        "PROOF-004": "DETERMINISTIC_SIMULATION_CANDIDATE_EXTERIOR_RECOMPUTATION_PENDING",
        "PROOF-005": "CORRECTION_SOURCE_GROUNDING_AND_EXTERIOR_REVIEW_PENDING",
        "PROOF-006": "PREREGISTERED_OR_OFFLINE_ONLY",
    }
    for proof_id, expected in expected_states.items():
        actual = by_id.get(proof_id, {}).get("source_evidence_state")
        if actual != expected:
            add("SOURCE_STATE_PROMOTION_OR_DRIFT", f"$.proof_sequence[{proof_id}]", f"expected {expected}, found {actual}")

    p3 = by_id.get("PROOF-003", {})
    admission = p3.get("source_admission", {})
    if admission.get("pull_request") != 118 or admission.get("merge_commit") != BASE:
        add("PROOF003_ADMISSION_BINDING_INVALID", "$.proof_sequence[PROOF-003].source_admission", "must bind PR #118 merge at the v0.2 basis")
    if p3.get("proof_packaging_state") != "NOT_ADMITTED":
        add("SOURCE_TO_PROOF_PROMOTION", "$.proof_sequence[PROOF-003].proof_packaging_state", "admitted source evidence may not admit proof packaging")

    for proof in proofs:
        packaging = proof.get("proof_packaging_state", "")
        if packaging == "ADMITTED" or packaging.startswith("ADMITTED_"):
            add("PROOF_SELF_ADMISSION", f"$.proof_sequence[{proof['proof_id']}].proof_packaging_state", packaging)
        execution = proof.get("execution_state", "")
        if execution not in SAFE_EXECUTION_STATES:
            add("EXECUTION_STATE_INVALID_OR_PROMOTED", f"$.proof_sequence[{proof['proof_id']}].execution_state", execution)

    model = registry["model_state"]
    required_model = contract.get("required_global_state", {})
    if model.get("standing") != required_model.get("candidate_model_standing"):
        add("MODEL_STANDING_PROMOTION", "$.model_state.standing", str(model.get("standing")))
    if model.get("corpus_cases_admitted") != 0 or model.get("empirical_validation") != "NOT_ESTABLISHED" or model.get("independent_validation") != "NOT_ESTABLISHED":
        add("EMPIRICAL_STANDING_PROMOTION", "$.model_state", "corpus/empirical/independent standing exceeds current governed basis")

    effects = registry["effects"]
    if effects.get("execution_authorized") is not False or effects.get("provider_calls_authorized") != 0 or effects.get("pair_001_calls_authorized") != 0:
        add("EXECUTION_EFFECT_NONZERO", "$.effects", "execution and provider/Pair-001 calls must remain closed")
    if effects.get("proof_admission_delta") != "NONE" or effects.get("model_standing_delta") != "NONE" or effects.get("authority_delta") != "NONE":
        add("UNAUTHORIZED_STANDING_DELTA", "$.effects", "proof/model/authority delta must remain NONE")

    return _result(findings, registry)


def _result(findings: list[dict[str, str]], registry: dict[str, Any] | None = None) -> dict[str, Any]:
    registry = registry or {}
    proofs = registry.get("proof_sequence", [])
    return {
        "checker": Path(__file__).name,
        "status": PASS if not findings else FAIL,
        "construction_base": BASE,
        "proof_count": len(proofs) if isinstance(proofs, list) else 0,
        "findings": sorted(findings, key=lambda item: (item["code"], item["path"], item["detail"])),
        "interpretation": {
            "proves": ["the v0.2 proof-portfolio successor satisfies its declared structural and promotion-boundary checks"],
            "does_not_prove": ["proof completion", "empirical validation", "truth", "compliance", "safety", "authorization", "endorsement", "production readiness", "institutional authority"]
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = evaluate(args.registry)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
        for finding in result["findings"]:
            print(f"{finding['code']}: {finding['path']}: {finding['detail']}")
    return 0 if result["status"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
