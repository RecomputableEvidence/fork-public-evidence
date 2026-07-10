#!/usr/bin/env python3
"""
Fork Longitudinal Day-0 Schema Scope Checker v0.1.

This checker verifies the documentation distinction between schema presence and
schema enforcement for the Day-0 packet.

It confirms the current v0.1 scope:

- schema artifact is present;
- public verifier requires the schema path;
- Day-0 packet manifest is present and parseable;
- Day-0 checker source does not import jsonschema or call known JSON Schema
  validator APIs;
- documentation explicitly says schema presence is not schema enforcement.

This checker does not enforce the Day-0 schema. It does not validate truth,
compliance, legal sufficiency, safety, authorization, approval, certification,
endorsement, validation, schema conformance, production readiness, procurement
approval, or institutional authority.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any, Dict, List


SCHEMA_PATH = pathlib.Path("schemas/longitudinal_reconstruction_day0_packet_manifest_v0_1.schema.json")
MANIFEST_PATH = pathlib.Path("docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/packet_manifest.json")
DAY0_CHECKER_PATH = pathlib.Path("tools/check_longitudinal_reconstruction_day0_packet_v0_1.py")
PUBLIC_VERIFIER_PATH = pathlib.Path("scripts/verify_public_review_package_v0_1.ps1")
SCOPE_DOC_PATH = pathlib.Path("docs/reconstruction/LONGITUDINAL_DAY0_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md")
RESPONSE_RECEIPT_PATH = pathlib.Path("docs/review/public-rounds/round-005/ROUND005_RESPONSE_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md")

NON_AUTHORITY_TERMS = [
    "does not",
    "truth",
    "compliance",
    "legal",
    "safety",
    "authorization",
    "approval",
    "certification",
    "endorsement",
    "validation",
    "production readiness",
    "authority",
]

FORBIDDEN_SCHEMA_ENFORCEMENT_TOKENS = [
    "import jsonschema",
    "from jsonschema",
    "jsonschema.",
    "Draft202012Validator",
    "Draft7Validator",
    "validate(instance",
    "validate(",
]


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: pathlib.Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def result(name: str, passed: bool, detail: str, data: Any = None) -> Dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "detail": detail,
        "data": data,
    }


def has_non_authority_terms(text: str) -> List[str]:
    lower = text.lower()
    return [term for term in NON_AUTHORITY_TERMS if term not in lower]


def contains_schema_scope_distinction(text: str) -> bool:
    lower = text.lower()

    has_presence = (
        "schema presence" in lower
        or "schema artifact: present" in lower
        or "schema file is present" in lower
        or "schema artifact is present" in lower
    )

    has_enforcement = (
        "schema enforcement" in lower
        or "schema-enforcement" in lower
        or "mechanical json schema validation" in lower
    )

    has_not_enforced = (
        "does not mechanically enforce" in lower
        or "not mechanically enforced" in lower
        or "mechanical json schema validation: not implemented" in lower
        or "mechanical json schema validation is not implemented" in lower
        or "not implemented in v0.1" in lower
    )

    return has_presence and has_enforcement and has_not_enforced


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    checks: List[Dict[str, Any]] = []

    paths = [
        ("path:schema", SCHEMA_PATH),
        ("path:manifest", MANIFEST_PATH),
        ("path:day0-checker", DAY0_CHECKER_PATH),
        ("path:public-verifier", PUBLIC_VERIFIER_PATH),
        ("path:schema-scope-doc", SCOPE_DOC_PATH),
        ("path:round005-response", RESPONSE_RECEIPT_PATH),
    ]

    for name, path in paths:
        checks.append(result(name, path.is_file(), "present" if path.is_file() else "missing", str(path).replace("\\", "/")))

    schema_data = None
    try:
        schema_data = load_json(SCHEMA_PATH)
        checks.append(result("schema:parse", isinstance(schema_data, dict), "schema parses as JSON object"))
    except Exception as exc:
        checks.append(result("schema:parse", False, str(exc)))

    manifest_data = None
    try:
        manifest_data = load_json(MANIFEST_PATH)
        checks.append(result("manifest:parse", isinstance(manifest_data, dict), "manifest parses as JSON object"))
    except Exception as exc:
        checks.append(result("manifest:parse", False, str(exc)))

    if isinstance(manifest_data, dict):
        schema_like_fields = [key for key in manifest_data.keys() if "schema" in str(key).lower()]
        checks.append(result(
            "manifest:schema-field-present",
            bool(schema_like_fields),
            "manifest contains at least one schema-related field" if schema_like_fields else "manifest has no schema-related field",
            schema_like_fields,
        ))
    else:
        checks.append(result("manifest:schema-field-present", False, "manifest unavailable"))

    try:
        verifier_text = read_text(PUBLIC_VERIFIER_PATH)
        checks.append(result(
            "public-verifier:requires-schema-path",
            str(SCHEMA_PATH).replace("\\", "/") in verifier_text.replace("\\", "/"),
            "public verifier includes schema path",
        ))
        checks.append(result(
            "public-verifier:requires-scope-doc",
            str(SCOPE_DOC_PATH).replace("\\", "/") in verifier_text.replace("\\", "/"),
            "public verifier includes schema-scope doc path",
        ))
        checks.append(result(
            "public-verifier:requires-response-receipt",
            str(RESPONSE_RECEIPT_PATH).replace("\\", "/") in verifier_text.replace("\\", "/"),
            "public verifier includes Round 005 schema response receipt path",
        ))
    except Exception as exc:
        checks.append(result("public-verifier:read", False, str(exc)))

    try:
        day0_checker_text = read_text(DAY0_CHECKER_PATH)
        token_hits = [token for token in FORBIDDEN_SCHEMA_ENFORCEMENT_TOKENS if token in day0_checker_text]
        checks.append(result(
            "day0-checker:no-jsonschema-enforcement-tokens",
            len(token_hits) == 0,
            "no known JSON Schema enforcement token found" if not token_hits else "JSON Schema enforcement token found",
            token_hits,
        ))
        exact_schema_filename = SCHEMA_PATH.name
        checks.append(result(
            "day0-checker:does-not-load-schema-file-by-name",
            exact_schema_filename not in day0_checker_text,
            "Day-0 checker does not reference schema filename directly" if exact_schema_filename not in day0_checker_text else "Day-0 checker references schema filename",
        ))
    except Exception as exc:
        checks.append(result("day0-checker:read", False, str(exc)))

    try:
        scope_doc_text = read_text(SCOPE_DOC_PATH)
        missing_terms = has_non_authority_terms(scope_doc_text)
        checks.append(result(
            "scope-doc:schema-presence-vs-enforcement-language",
            contains_schema_scope_distinction(scope_doc_text),
            "scope distinction language present",
        ))
        checks.append(result(
            "scope-doc:non-authority-terms",
            len(missing_terms) == 0,
            "non-authority terms present" if not missing_terms else "missing non-authority terms",
            missing_terms,
        ))
    except Exception as exc:
        checks.append(result("scope-doc:read", False, str(exc)))

    try:
        response_text = read_text(RESPONSE_RECEIPT_PATH)
        missing_terms = has_non_authority_terms(response_text)
        checks.append(result(
            "round005-response:schema-presence-vs-enforcement-language",
            contains_schema_scope_distinction(response_text),
            "scope distinction language present",
        ))
        checks.append(result(
            "round005-response:non-authority-terms",
            len(missing_terms) == 0,
            "non-authority terms present" if not missing_terms else "missing non-authority terms",
            missing_terms,
        ))
    except Exception as exc:
        checks.append(result("round005-response:read", False, str(exc)))

    failed = sum(1 for item in checks if not item["passed"])

    summary = {
        "checker": "check_longitudinal_day0_schema_scope_v0_1.py",
        "total": len(checks),
        "passed": len(checks) - failed,
        "failed": failed,
        "results": checks,
        "interpretation": (
            "A pass confirms the v0.1 schema-scope distinction is documented: schema presence and public path coverage exist, "
            "but mechanical JSON Schema enforcement is not implemented in the Day-0 checker."
        ),
        "non_authority_statement": (
            "This checker clarifies schema-scope behavior only; it does not validate truth, compliance, legal sufficiency, "
            "safety, authorization, approval, certification, endorsement, validation, schema conformance, "
            "production readiness, procurement approval, or institutional authority."
        ),
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"Longitudinal Day-0 schema-scope checks: {summary['passed']}/{summary['total']} passed")
        for item in checks:
            status = "PASS" if item["passed"] else "FAIL"
            print(f"{status} {item['name']}: {item['detail']}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))