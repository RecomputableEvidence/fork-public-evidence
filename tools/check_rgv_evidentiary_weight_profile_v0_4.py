#!/usr/bin/env python3
"""
RGV v0.4 evidentiary-weight profile checker.

This checker validates the profile contract only. It does not assert legal
sufficiency, admissibility, self-authentication, business-records status,
truth, compliance, safety, signer identity, non-repudiation, or timestamp
authority.

The v0.4 profile is non-breaking against RGV v0.3. It binds the dependency
order for evidentiary-weight hardening:
canonicalization -> seal/integrity -> timestamp anchor -> provenance tier -> receipt envelope.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

DIGEST_RE = re.compile(r"^sha256:[a-f0-9]{64}$")

TIER_STRENGTH = {
    "UNRESOLVED": 0,
    "GENERATED": 1,
    "INTERPRETIVE": 2,
    "ATTRIBUTED": 3,
    "DOCUMENTED": 4,
}

VALID_SEAL_SCOPES = {
    "BUNDLE_ONLY",
    "RESULT_ONLY",
    "BUNDLE_AND_RESULT_INDEPENDENT",
    "COMPOUND_BUNDLE_RESULT",
}


def err(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def require(obj: dict[str, Any], key: str, errors: list[dict[str, str]], where: str) -> bool:
    if key not in obj:
        errors.append(err("MISSING_REQUIRED_FIELD", f"{where}.{key} is required"))
        return False
    return True


def check_digest(value: Any, field: str, errors: list[dict[str, str]]) -> None:
    if not isinstance(value, str) or not DIGEST_RE.match(value):
        errors.append(err("INVALID_DIGEST", f"{field} must match sha256:<64 lowercase hex chars>"))


def check_profile(profile: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    if profile.get("record_type") != "RGV_EVIDENTIARY_WEIGHT_PROFILE":
        errors.append(err("INVALID_RECORD_TYPE", "record_type must be RGV_EVIDENTIARY_WEIGHT_PROFILE"))

    if profile.get("profile_version") != "0.4":
        errors.append(err("INVALID_PROFILE_VERSION", "profile_version must be 0.4"))

    required_top = [
        "profile_scope",
        "canonicalization_profile",
        "verifier_binding",
        "seal_binding",
        "timestamp_anchor_ref",
        "provenance_binding",
        "profile_non_claims",
    ]

    for key in required_top:
        require(profile, key, errors, "profile")

    canonicalization = profile.get("canonicalization_profile", {})
    if isinstance(canonicalization, dict):
        if canonicalization.get("canonicalization_profile_id") != "RFC8785_JCS":
            errors.append(err("CANONICALIZATION_NOT_CONST_JCS", "canonicalization_profile_id must be RFC8785_JCS"))
        if canonicalization.get("canonicalization_profile_type") != "CONST":
            errors.append(err("CANONICALIZATION_NOT_CONST", "canonicalization_profile_type must be CONST"))
    else:
        errors.append(err("INVALID_CANONICALIZATION_OBJECT", "canonicalization_profile must be an object"))

    verifier = profile.get("verifier_binding", {})
    if isinstance(verifier, dict):
        if verifier.get("verifier_name") != "RGV":
            errors.append(err("INVALID_VERIFIER_NAME", "verifier_name must be RGV"))
        if verifier.get("verifier_version") != "RGV_v0_3":
            errors.append(err("INVALID_VERIFIER_VERSION", "verifier_version must be RGV_v0_3"))
        if verifier.get("verifier_version_in_sealed_scope") is not True:
            errors.append(err("VERIFIER_VERSION_NOT_IN_SEALED_SCOPE", "sealed scope must include the verifier version identifier"))
    else:
        errors.append(err("INVALID_VERIFIER_BINDING", "verifier_binding must be an object"))

    seal = profile.get("seal_binding", {})
    if isinstance(seal, dict):
        scope = seal.get("seal_scope")
        if scope not in VALID_SEAL_SCOPES:
            errors.append(err("INVALID_SEAL_SCOPE", "seal_scope must be a recognized v0.4 seal scope"))

        if seal.get("seal_algorithm") != "SHA256":
            errors.append(err("INVALID_OR_MISSING_SEAL_ALGORITHM", "seal_algorithm must be SHA256"))

        if seal.get("declared_method") != "SHA256_OVER_RFC8785_JCS_CANONICAL_JSON":
            errors.append(err("INVALID_DECLARED_METHOD", "declared_method must bind SHA256 over RFC8785_JCS canonical JSON"))

        if scope == "BUNDLE_ONLY":
            require(seal, "bundle_digest", errors, "seal_binding")
            if "bundle_digest" in seal:
                check_digest(seal["bundle_digest"], "seal_binding.bundle_digest", errors)
        elif scope == "RESULT_ONLY":
            require(seal, "result_digest", errors, "seal_binding")
            if "result_digest" in seal:
                check_digest(seal["result_digest"], "seal_binding.result_digest", errors)
        elif scope == "BUNDLE_AND_RESULT_INDEPENDENT":
            require(seal, "bundle_digest", errors, "seal_binding")
            require(seal, "result_digest", errors, "seal_binding")
            if "bundle_digest" in seal:
                check_digest(seal["bundle_digest"], "seal_binding.bundle_digest", errors)
            if "result_digest" in seal:
                check_digest(seal["result_digest"], "seal_binding.result_digest", errors)
        elif scope == "COMPOUND_BUNDLE_RESULT":
            require(seal, "compound_digest", errors, "seal_binding")
            require(seal, "compound_digest_ordering", errors, "seal_binding")
            if "compound_digest" in seal:
                check_digest(seal["compound_digest"], "seal_binding.compound_digest", errors)
            if seal.get("compound_digest_ordering") != "BUNDLE_CANONICAL_JSON_THEN_RESULT_CANONICAL_JSON":
                errors.append(err("INVALID_COMPOUND_DIGEST_ORDERING", "compound digest ordering must be explicit"))

        for state_field in ["signer_identity", "non_repudiation"]:
            if require(seal, state_field, errors, "seal_binding"):
                state_obj = seal.get(state_field)
                if not isinstance(state_obj, dict) or state_obj.get("state") not in {"ESTABLISHED", "NOT_ESTABLISHED", "NOT_CHECKED"}:
                    errors.append(err("INVALID_ESTABLISHMENT_STATE", f"seal_binding.{state_field}.state must be ESTABLISHED, NOT_ESTABLISHED, or NOT_CHECKED"))
    else:
        errors.append(err("INVALID_SEAL_BINDING", "seal_binding must be an object"))

    provenance = profile.get("provenance_binding", {})
    if isinstance(provenance, dict):
        cbc_items = provenance.get("cbc_provenance", [])
        if not isinstance(cbc_items, list) or not cbc_items:
            errors.append(err("MISSING_CBC_PROVENANCE", "provenance_binding.cbc_provenance must be a non-empty list"))
        else:
            tiers = []
            for item in cbc_items:
                if not isinstance(item, dict):
                    errors.append(err("INVALID_CBC_PROVENANCE_ITEM", "Each cbc_provenance item must be an object"))
                    continue
                tier = item.get("declared_provenance_tier")
                if tier not in TIER_STRENGTH:
                    errors.append(err("INVALID_PROVENANCE_TIER", "declared_provenance_tier must be a known v0.4 tier"))
                else:
                    tiers.append(tier)

            if tiers:
                computed_min = min(tiers, key=lambda tier: TIER_STRENGTH[tier])
                declared_min = provenance.get("minimum_provenance_tier")
                if declared_min != computed_min:
                    errors.append(
                        err(
                            "PROVENANCE_ROLLUP_LAUNDERING",
                            f"minimum_provenance_tier must equal weakest CBC tier {computed_min}, not {declared_min}",
                        )
                    )

        if provenance.get("minimum_rollup_rule") != "BUNDLE_PROVENANCE_CANNOT_EXCEED_LOWEST_CONFIDENCE_CBC_NODE":
            errors.append(err("INVALID_MINIMUM_ROLLUP_RULE", "minimum_rollup_rule must prevent provenance laundering"))
    else:
        errors.append(err("INVALID_PROVENANCE_BINDING", "provenance_binding must be an object"))

    non_claims = profile.get("profile_non_claims", [])
    if not isinstance(non_claims, list) or len(non_claims) < 5:
        errors.append(err("INSUFFICIENT_PROFILE_NON_CLAIMS", "profile_non_claims must contain at least five non-claims"))

    required_non_claim_ids = {
        "RGV_V0_4_PROFILE_NON_CLAIM_LEGAL_SUFFICIENCY",
        "RGV_V0_4_PROFILE_NON_CLAIM_FRE_902",
        "RGV_V0_4_PROFILE_NON_CLAIM_FRE_803_6",
        "RGV_V0_4_PROFILE_NON_CLAIM_SIGNATURE",
        "RGV_V0_4_PROFILE_NON_CLAIM_CANONICALIZATION_IMPLEMENTATION",
    }

    present_ids = {
        item.get("non_claim_id")
        for item in non_claims
        if isinstance(item, dict)
    }

    missing = sorted(required_non_claim_ids - present_ids)
    for non_claim_id in missing:
        errors.append(err("MISSING_REQUIRED_NON_CLAIM", f"Missing required non-claim {non_claim_id}"))

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(json.dumps({"result": "ERROR", "errors": [err("USAGE", "Usage: check_rgv_evidentiary_weight_profile_v0_4.py <profile.json>")]}, indent=2))
        return 2

    path = Path(argv[1])
    try:
        profile = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        print(json.dumps({"result": "FAIL", "errors": [err("JSON_PARSE_ERROR", str(exc))]}, indent=2))
        return 1

    if not isinstance(profile, dict):
        print(json.dumps({"result": "FAIL", "errors": [err("PROFILE_NOT_OBJECT", "Profile must be a JSON object")]}, indent=2))
        return 1

    errors = check_profile(profile)
    result = "PASS" if not errors else "FAIL"

    output = {
        "checker": "check_rgv_evidentiary_weight_profile_v0_4",
        "result": result,
        "checked_profile": str(path),
        "errors": errors,
        "checker_non_claims": [
            "This checker does not assert legal sufficiency, admissibility, self-authentication, business-records status, truth, compliance, safety, or runtime authority.",
            "This checker validates v0.4 evidentiary-weight profile declarations and deterministic consistency rules only.",
            "DECLARED canonicalization profile does not by itself prove independent RFC8785/JCS implementation conformance."
        ]
    }

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

