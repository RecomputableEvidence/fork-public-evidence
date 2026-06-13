import json
import sys
from pathlib import Path

VALID_RECOMPUTABILITY_CLASSES = {
    "STRONG_RECOMPUTATION",
    "BOUNDED_RECOMPUTATION",
    "REFERENTIAL_RECOMPUTATION",
    "NON_RECOMPUTABLE",
}

VALID_RECOMPUTATION_SURFACES = {
    "EXPORT_SURFACE",
    "PACKET_LEVEL",
    "FOREIGN_VERIFIER",
}

REQUIRED_FIELDS = [
    "contract_version",
    "artifact_id",
    "gate_id",
    "declared_recomputability_class",
    "required_recomputability_class",
    "recomputation_surface",
    "claim_boundary",
]


def fail(code: str, message: str) -> int:
    print(f"{code}: {message}")
    return 1


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception as exc:
        raise ValueError(f"Unable to load JSON: {exc}") from exc


def check_required_fields(payload: dict) -> None:
    for field in REQUIRED_FIELDS:
        if field not in payload:
            raise ValueError(f"Missing required field: {field}")

    if payload["contract_version"] != "recomputability_class_v0_1":
        raise ValueError("contract_version must be recomputability_class_v0_1")

    declared = payload["declared_recomputability_class"]
    required = payload["required_recomputability_class"]
    surface = payload["recomputation_surface"]

    if declared not in VALID_RECOMPUTABILITY_CLASSES:
        raise ValueError(f"Invalid declared_recomputability_class: {declared}")

    if required not in VALID_RECOMPUTABILITY_CLASSES:
        raise ValueError(f"Invalid required_recomputability_class: {required}")

    if surface not in VALID_RECOMPUTATION_SURFACES:
        raise ValueError(f"Invalid recomputation_surface: {surface}")


def check_recomputability_class(payload: dict) -> int:
    declared = payload["declared_recomputability_class"]
    required = payload["required_recomputability_class"]

    if declared == "NON_RECOMPUTABLE" and required == "STRONG_RECOMPUTATION":
        return fail(
            "RECOMPUTABILITY_ESCALATION_DEFECT",
            "NON_RECOMPUTABLE artifacts must not satisfy gates that require STRONG_RECOMPUTATION.",
        )

    print("RECOMPUTABILITY_CLASS_PASS")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        return fail("USAGE_ERROR", "Usage: python tools/check_recomputability_class.py <payload.json>")

    path = Path(argv[1])

    try:
        payload = load_json(path)
        if not isinstance(payload, dict):
            raise ValueError("Payload must be a JSON object.")
        check_required_fields(payload)
    except ValueError as exc:
        return fail("RECOMPUTABILITY_SCHEMA_DEFECT", str(exc))

    return check_recomputability_class(payload)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
