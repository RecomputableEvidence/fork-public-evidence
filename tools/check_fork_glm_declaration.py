#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

CHECKER_NAME = "check_fork_glm_declaration"
CHECKER_VERSION = "0.1"
SCOPE = "FORK_GLM_DECLARATION_BOUNDARY_GUARD_ONLY"

PASS_RESULT = "STRUCTURAL_PASS"
FAIL_RESULT = "STRUCTURAL_FAIL"
INPUT_ERROR_RESULT = "INPUT_ERROR"

REQUIRED_FORBIDDEN_INTERPRETATIONS = {
    "approval",
    "authorization",
    "execution_authorization",
    "execution_permission",
    "runtime_approval",
    "runtime_control",
    "truth_certification",
    "correctness_certification",
    "safety_certification",
    "compliance_certification",
    "legal_sufficiency",
    "admissibility_certification",
    "authority_validation",
    "authority_transfer",
    "interoperability_certification",
    "evide_compatibility_certification",
    "glm_certification",
    "semantic_inheritance",
    "claim_inheritance",
    "non_claim_erasure",
    "unresolved_pointer_resolution",
    "downstream_expansion_authorization",
}

REQUIRED_FALSE_CAPABILITIES = [
    "machine_readable_status.execution_capability",
    "machine_readable_status.runtime_control",
    "machine_readable_status.approval_capability",
    "machine_readable_status.authorization_capability",
    "machine_readable_status.truth_determination_capability",
    "machine_readable_status.safety_certification_capability",
    "machine_readable_status.compliance_certification_capability",
    "machine_readable_status.legal_sufficiency_capability",
    "machine_readable_status.admissibility_capability",
    "machine_readable_status.interoperability_certification_capability",
]

REQUIRED_OUT_OF_BAND_POSTURE = {
    "operational_scope.out_of_band_posture.read_only": True,
    "operational_scope.out_of_band_posture.fail_open": True,
    "operational_scope.out_of_band_posture.runtime_control": False,
    "operational_scope.out_of_band_posture.decision_authority": False,
    "operational_scope.out_of_band_posture.policy_engine": False,
    "operational_scope.out_of_band_posture.approval_engine": False,
    "operational_scope.out_of_band_posture.compliance_engine": False,
    "operational_scope.out_of_band_posture.legal_adjudication_engine": False,
}

REQUIRED_NON_CLAIM_PHRASES = {
    "truth": ["does not determine truth", "truth_certification"],
    "factual_correctness": ["does not determine factual correctness", "correctness_certification"],
    "legal_sufficiency": ["does not determine legal sufficiency", "legal_sufficiency"],
    "regulatory_compliance": ["does not determine regulatory compliance", "compliance_certification"],
    "safety": ["does not certify safety", "safety_certification"],
    "approval": ["does not approve decisions", "approval"],
    "authorization": ["does not authorize execution", "authorization"],
    "admissibility": ["does not resolve admissibility", "admissibility_certification"],
    "authority_transfer": ["does not validate authority", "authority_transfer"],
    "runtime_control": ["does not control runtime behavior", "runtime_control"],
    "evide_compatibility": ["does not claim compatibility with evide", "evide_compatibility_certification"],
    "interoperability_certification": ["does not certify interoperability", "interoperability_certification"],
}

ALLOWED_TIMING_POSITIONS = {"pre-bind", "at-bind", "post-bind", "cross-cutting"}
PROHIBITED_TIMING_POSITIONS = {"post-closure"}

NEGATION_MARKERS = [
    "does not",
    "do not",
    "must not",
    "should not",
    "without",
    "forbidden",
    "cannot",
    "can not",
    "is not",
    "are not",
    "not ",
    "no ",
    "non-",
    "non_",
]

POSITIVE_AUTHORITY_PATTERNS = [
    (
        "POSITIVE_APPROVAL_OR_AUTHORIZATION_CLAIM",
        re.compile(
            r"\bfork\b.{0,120}\b(approves?|authorizes?|permits?|allows|clears|greenlights)\b"
            r".{0,120}\b(decisions?|execution|runtime|action|actions|deployment|production)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "POSITIVE_TRUTH_OR_CORRECTNESS_CLAIM",
        re.compile(
            r"\bfork\b.{0,120}\b(certifies?|validates?|determines?|proves?)\b"
            r".{0,120}\b(truth|true|correctness|correct|factual)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "POSITIVE_SAFETY_OR_COMPLIANCE_CLAIM",
        re.compile(
            r"\bfork\b.{0,120}\b(certifies?|validates?|determines?|proves?)\b"
            r".{0,120}\b(safety|safe|compliance|compliant|regulatory)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "POSITIVE_LEGAL_OR_ADMISSIBILITY_CLAIM",
        re.compile(
            r"\bfork\b.{0,120}\b(certifies?|validates?|determines?|resolves?|proves?)\b"
            r".{0,120}\b(legal sufficiency|legally sufficient|admissibility|admissible)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "POSITIVE_RUNTIME_CONTROL_CLAIM",
        re.compile(
            r"\bfork\b.{0,120}\b(controls?|blocks?|permits?|enforces?|executes?)\b"
            r".{0,120}\b(runtime|execution|production|deployment|actions?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "POSITIVE_AUTHORITY_TRANSFER_CLAIM",
        re.compile(
            r"\bfork\b.{0,120}\b(transfers?|confers?|grants?|validates?|establishes?)\b"
            r".{0,120}\b(authority|authorization|permission|standing)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "POSITIVE_EVIDE_COMPATIBILITY_CLAIM",
        re.compile(
            r"\bevide\b.{0,120}\b(compatible|compatibility|certified|certification|interoperable|interoperability|composable|composability)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "POSITIVE_GLM_CERTIFICATION_CLAIM",
        re.compile(
            r"\bglm\b.{0,120}\b(certifies?|certified|certification|approves?|approval|validates?|validated|validation)\b",
            re.IGNORECASE,
        ),
    ),
]

LIMITATIONS = {
    "scope": SCOPE,
    "structural_only": True,
    "does_not_validate": [
        "full GLM compliance",
        "EVIDE compatibility",
        "interoperability",
        "truth",
        "factual correctness",
        "safety",
        "regulatory compliance",
        "legal sufficiency",
        "approval",
        "authorization",
        "admissibility",
        "runtime control",
        "institutional acceptance",
        "production readiness",
    ],
    "interpretation_required": True,
    "human_review_required_for_publication": True,
}


def issue(code: str, path: str, message: str, observed: Any = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"code": code, "path": path, "message": message}
    if observed is not None:
        payload["observed"] = observed
    return payload


def normalize_token(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def normalize_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value).strip().lower())


def get_path(obj: Any, dotted_path: str) -> tuple[bool, Any]:
    cursor = obj
    for part in dotted_path.split("."):
        if isinstance(cursor, dict) and part in cursor:
            cursor = cursor[part]
        else:
            return False, None
    return True, cursor


def iter_strings(obj: Any, path: str = "$"):
    if isinstance(obj, dict):
        for key in sorted(obj.keys()):
            yield from iter_strings(obj[key], f"{path}.{key}")
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            yield from iter_strings(item, f"{path}[{index}]")
    elif isinstance(obj, str):
        yield path, obj


def is_negated_near(text: str, start: int, end: int) -> bool:
    window = text[max(0, start - 140):min(len(text), end + 60)].lower()
    return any(marker in window for marker in NEGATION_MARKERS)


def require_exact(manifest: dict[str, Any], path: str, expected: Any, errors: list[dict[str, Any]], code: str) -> None:
    exists, observed = get_path(manifest, path)
    if not exists:
        errors.append(issue(code, path, f"Required field is missing; expected {expected!r}."))
    elif observed != expected:
        errors.append(issue(code, path, f"Expected {expected!r}.", observed))


def check_layer_identity(manifest: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    require_exact(manifest, "schema_version", "1.3", errors, "SCHEMA_VERSION_MISMATCH")
    require_exact(manifest, "manifest_kind", "layer", errors, "MANIFEST_KIND_MISMATCH")
    require_exact(manifest, "layer.layer_type", "cross_cutting", errors, "LAYER_TYPE_MUST_BE_CROSS_CUTTING")
    require_exact(manifest, "layer.status", "experimental", errors, "LAYER_STATUS_MUST_BE_EXPERIMENTAL")

    exists, observed = get_path(manifest, "layer.vendor_layer_name")
    if not exists or normalize_token(observed) != "fork":
        errors.append(issue(
            "LAYER_NAME_MUST_BE_FORK",
            "layer.vendor_layer_name",
            "This checker is only for Fork GLM declarations.",
            observed if exists else None,
        ))


def check_timing_axis(manifest: dict[str, Any], errors: list[dict[str, Any]], warnings: list[dict[str, Any]]) -> None:
    exists, position = get_path(manifest, "timing_axis.position")
    if not exists:
        errors.append(issue("MISSING_TIMING_AXIS_POSITION", "timing_axis.position", "timing_axis.position is required."))
    elif normalize_token(position) != "cross_cutting":
        errors.append(issue(
            "TIMING_AXIS_MUST_BE_CROSS_CUTTING",
            "timing_axis.position",
            "Fork GLM declaration must use cross-cutting timing posture.",
            position,
        ))

    exists, surfaces = get_path(manifest, "timing_axis.surfaces")
    if not exists:
        errors.append(issue("MISSING_TIMING_SURFACES", "timing_axis.surfaces", "cross_cutting layer must declare surfaces."))
        return

    if not isinstance(surfaces, list) or not surfaces:
        errors.append(issue("INVALID_TIMING_SURFACES", "timing_axis.surfaces", "timing_axis.surfaces must be a non-empty list.", surfaces))
        return

    for index, surface in enumerate(surfaces):
        base = f"timing_axis.surfaces[{index}]"
        if not isinstance(surface, dict):
            errors.append(issue("INVALID_TIMING_SURFACE", base, "Each timing surface must be an object.", surface))
            continue

        timing_position = surface.get("timing_position")
        if timing_position in PROHIBITED_TIMING_POSITIONS:
            errors.append(issue(
                "PROHIBITED_TIMING_POSITION_VALUE",
                f"{base}.timing_position",
                "Use post-bind plus timing_qualifier instead of post-closure as the controlled timing value.",
                timing_position,
            ))
        elif timing_position not in ALLOWED_TIMING_POSITIONS:
            errors.append(issue(
                "UNKNOWN_TIMING_POSITION_VALUE",
                f"{base}.timing_position",
                "timing_position must be one of: pre-bind, at-bind, post-bind, cross-cutting.",
                timing_position,
            ))

        if "does_not" not in surface:
            warnings.append(issue(
                "TIMING_SURFACE_WITHOUT_DOES_NOT",
                f"{base}.does_not",
                "Recommended: each timing surface should explicitly state what it does not do.",
            ))


def check_authoritative_claim(manifest: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    path = "claims_boundary.authoritative_layer_claim"
    exists, observed = get_path(manifest, path)

    if not exists:
        errors.append(issue("MISSING_AUTHORITATIVE_LAYER_CLAIM", path, "Fork GLM declaration requires a bounded authoritative_layer_claim."))
        return

    if not isinstance(observed, str) or not observed.strip():
        errors.append(issue("INVALID_AUTHORITATIVE_LAYER_CLAIM", path, "authoritative_layer_claim must be a non-empty string.", observed))
        return

    claim = normalize_text(observed)
    required_terms = [
        "without deciding",
        "truth",
        "safety",
        "compliance",
        "approval",
        "legal sufficiency",
        "admissibility",
        "authority",
    ]
    missing = [term for term in required_terms if term not in claim]

    if missing:
        errors.append(issue(
            "AUTHORITATIVE_CLAIM_NOT_BOUNDED_ENOUGH",
            path,
            "authoritative_layer_claim must visibly exclude truth/safety/compliance/approval/legal/admissibility/authority readings.",
            missing,
        ))


def check_forbidden_interpretations(manifest: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    path = "claims_boundary.forbidden_interpretations"
    exists, observed = get_path(manifest, path)

    if not exists:
        errors.append(issue("MISSING_FORBIDDEN_INTERPRETATIONS", path, "claims_boundary.forbidden_interpretations is required."))
        return

    if not isinstance(observed, list) or not all(isinstance(item, str) for item in observed):
        errors.append(issue("INVALID_FORBIDDEN_INTERPRETATIONS", path, "forbidden_interpretations must be a list of strings.", observed))
        return

    normalized = {normalize_token(item) for item in observed}
    missing = sorted(REQUIRED_FORBIDDEN_INTERPRETATIONS - normalized)

    if missing:
        errors.append(issue(
            "MISSING_REQUIRED_FORBIDDEN_INTERPRETATION",
            path,
            "Fork declaration is missing required forbidden interpretation tokens.",
            missing,
        ))


def check_non_claim_themes(manifest: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    fields = []

    for path in [
        "claims_boundary.explicit_non_claims",
        "claims_boundary.consumer_boundary_constraint",
        "claims_boundary.forbidden_interpretations",
        "operational_scope.does_not",
        "layer.declaration_note",
        "machine_readable_status.declaration_status_note",
    ]:
        exists, observed = get_path(manifest, path)
        if exists:
            fields.extend(observed if isinstance(observed, list) else [observed])

    combined = normalize_text(" ".join(str(item) for item in fields))
    missing = []

    for theme, phrases in REQUIRED_NON_CLAIM_PHRASES.items():
        if not any(normalize_text(phrase) in combined for phrase in phrases):
            missing.append(theme)

    if missing:
        errors.append(issue(
            "MISSING_REQUIRED_NON_CLAIM_THEME",
            "claims_boundary.explicit_non_claims",
            "Fork declaration does not explicitly preserve all required non-authority themes.",
            missing,
        ))


def check_false_capabilities(manifest: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    for path in REQUIRED_FALSE_CAPABILITIES:
        exists, observed = get_path(manifest, path)

        if not exists:
            errors.append(issue("MISSING_FALSE_CAPABILITY_FIELD", path, "Required machine-readable non-capability field is missing."))
        elif observed is not False:
            errors.append(issue("CAPABILITY_MUST_BE_FALSE", path, "Fork GLM declaration must not expose this capability.", observed))


def check_out_of_band_posture(manifest: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    for path, expected in REQUIRED_OUT_OF_BAND_POSTURE.items():
        exists, observed = get_path(manifest, path)

        if not exists:
            errors.append(issue("MISSING_OUT_OF_BAND_POSTURE_FIELD", path, f"Required out-of-band posture field is missing; expected {expected!r}."))
        elif observed is not expected:
            errors.append(issue("OUT_OF_BAND_POSTURE_MISMATCH", path, f"Expected {expected!r}.", observed))


def check_composition(manifest: dict[str, Any], errors: list[dict[str, Any]], warnings: list[dict[str, Any]]) -> None:
    path = "composition.composable_with_manifests"
    exists, observed = get_path(manifest, path)

    if not exists:
        errors.append(issue("MISSING_COMPOSABLE_WITH_MANIFESTS", path, "v0.1 requires an explicit empty composable_with_manifests list."))
    elif observed != []:
        errors.append(issue(
            "EXTERNAL_MANIFEST_COMPOSITION_NOT_ALLOWED_IN_V0_1",
            path,
            "Fork GLM v0.1 must not claim verified composability with any specific external manifest.",
            observed,
        ))

    note_exists, note = get_path(manifest, "composition.composition_note")
    if not note_exists or not isinstance(note, str) or "does not claim" not in note.lower():
        warnings.append(issue(
            "COMPOSITION_NOTE_SHOULD_EXPLICITLY_DENY_VERIFIED_COMPOSABILITY",
            "composition.composition_note",
            "Recommended: composition_note should explicitly say v0.1 does not claim verified composability or reciprocal compatibility.",
            note if note_exists else None,
        ))


def check_positive_authority_language(manifest: dict[str, Any], errors: list[dict[str, Any]]) -> None:
    for path, value in iter_strings(manifest):
        if "forbidden_interpretations" in path:
            continue

        text = value.strip()
        if not text:
            continue

        for code, pattern in POSITIVE_AUTHORITY_PATTERNS:
            for match in pattern.finditer(text):
                if not is_negated_near(text, match.start(), match.end()):
                    errors.append(issue(
                        code,
                        path,
                        "Potential positive authority/certification/control claim found without nearby negation.",
                        {
                            "matched_text": match.group(0),
                            "full_value": value,
                        },
                    ))


def check_digest_and_publication(manifest: dict[str, Any], warnings: list[dict[str, Any]]) -> None:
    exists, digest_type = get_path(manifest, "manifest_digest.type")
    if not exists or normalize_token(digest_type) != "sha256":
        warnings.append(issue(
            "MANIFEST_DIGEST_SHA256_RECOMMENDED",
            "manifest_digest.type",
            "Recommended: manifest_digest.type should be sha256.",
            digest_type if exists else None,
        ))

    exists, digest_value = get_path(manifest, "manifest_digest.value")
    if not exists or not isinstance(digest_value, str) or not digest_value.strip():
        warnings.append(issue(
            "MANIFEST_DIGEST_VALUE_MISSING_OR_EMPTY",
            "manifest_digest.value",
            "Recommended: include a non-empty manifest_digest.value placeholder before public digest computation.",
            digest_value if exists else None,
        ))

    exists, publication_note = get_path(manifest, "public_anchors.publication_note")
    if not exists:
        warnings.append(issue(
            "MISSING_PUBLICATION_NOTE",
            "public_anchors.publication_note",
            "Recommended: state repo-first experimental publication and defer /.well-known publication until review.",
        ))
    elif isinstance(publication_note, str):
        note = publication_note.lower()
        if "/.well-known/governance-layer-manifest.json" in note and "only after" not in note:
            warnings.append(issue(
                "WELL_KNOWN_PUBLICATION_NEEDS_REVIEW_GATE",
                "public_anchors.publication_note",
                "Recommended: /.well-known publication should be gated by local Fork checks and GLM validator review.",
                publication_note,
            ))


def build_result(manifest: dict[str, Any], input_path: str) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    check_layer_identity(manifest, errors)
    check_timing_axis(manifest, errors, warnings)
    check_authoritative_claim(manifest, errors)
    check_forbidden_interpretations(manifest, errors)
    check_non_claim_themes(manifest, errors)
    check_false_capabilities(manifest, errors)
    check_out_of_band_posture(manifest, errors)
    check_composition(manifest, errors, warnings)
    check_positive_authority_language(manifest, errors)
    check_digest_and_publication(manifest, warnings)

    def observed_value(path: str) -> Any:
        return get_path(manifest, path)[1]

    composable_exists, composable = get_path(manifest, "composition.composable_with_manifests")

    return {
        "checker": {
            "name": CHECKER_NAME,
            "version": CHECKER_VERSION,
            "scope": SCOPE,
        },
        "input": {
            "path": input_path,
        },
        "result": PASS_RESULT if not errors else FAIL_RESULT,
        "observed": {
            "schema_version": observed_value("schema_version"),
            "manifest_kind": observed_value("manifest_kind"),
            "layer_type": observed_value("layer.layer_type"),
            "layer_status": observed_value("layer.status"),
            "execution_capability": observed_value("machine_readable_status.execution_capability"),
            "runtime_control": observed_value("machine_readable_status.runtime_control"),
            "composable_with_manifests_count": len(composable) if composable_exists and isinstance(composable, list) else None,
        },
        "findings": {
            "errors": errors,
            "warnings": warnings,
        },
        "limitations": LIMITATIONS,
    }


def input_error(input_path: str, code: str, message: str, observed: Any = None) -> dict[str, Any]:
    return {
        "checker": {
            "name": CHECKER_NAME,
            "version": CHECKER_VERSION,
            "scope": SCOPE,
        },
        "input": {
            "path": input_path,
        },
        "result": INPUT_ERROR_RESULT,
        "findings": {
            "errors": [issue(code, "$", message, observed)],
            "warnings": [],
        },
        "limitations": LIMITATIONS,
    }


def load_json(path: Path) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    if not path.exists():
        return None, input_error(str(path), "INPUT_FILE_NOT_FOUND", "Input manifest file was not found.", str(path))

    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, input_error(
            str(path),
            "INVALID_JSON",
            "Input file is not valid JSON.",
            {
                "line": exc.lineno,
                "column": exc.colno,
                "message": exc.msg,
            },
        )

    if not isinstance(loaded, dict):
        return None, input_error(
            str(path),
            "ROOT_MUST_BE_OBJECT",
            "Input manifest root must be a JSON object.",
            type(loaded).__name__,
        )

    return loaded, None


def write_result(result: dict[str, Any], output_path: str | None) -> None:
    text = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"

    if output_path is None:
        sys.stdout.write(text)
        return

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fork-local GLM declaration non-authority guard checker.")
    parser.add_argument("manifest", help="Path to Fork GLM declaration JSON.")
    parser.add_argument("--output", "-o", default=None, help="Optional path for JSON check output.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    manifest, error_result = load_json(Path(args.manifest))
    if error_result is not None:
        write_result(error_result, args.output)
        return 2

    assert manifest is not None
    result = build_result(manifest, args.manifest)
    write_result(result, args.output)

    return 0 if result["result"] == PASS_RESULT else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))