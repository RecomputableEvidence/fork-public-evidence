import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


def compute_localization_posture(record: Dict[str, Any]) -> Tuple[str, List[str], List[str]]:
    """
    Returns (localization_status, localization_findings, localization_limitations_additions).

    Strictly non-interpretive:
    - Does NOT infer whether an establishment *should* exist.
    - ONLY checks whether one is explicitly declared via an `establishment_ref` field.
    """
    localization_findings: List[str] = []
    localization_limitations: List[str] = []

    claims = record.get("claims", []) or []

    has_establishment_ref = any(
        isinstance(claim, dict) and "establishment_ref" in claim
        for claim in claims
    )

    if has_establishment_ref:
        localization_status = "LOCALIZABLE_OR_RECONSTRUCTABLE_ESTABLISHMENT"
    else:
        localization_status = "NO_LOCALIZABLE_ESTABLISHMENT"
        localization_findings.append("NO_ESTABLISHMENT_EVENT_REF")
        localization_limitations.append("no_localized_establishment_for_transferred_property")

    return localization_status, localization_findings, localization_limitations


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: check_boundary_delta_record.py <path-to-bdr-json>", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])

    # Use utf-8-sig so we tolerate an optional BOM if present
    with input_path.open("r", encoding="utf-8-sig") as f:
        record: Dict[str, Any] = json.load(f)

    findings: List[str] = []
    limitations: List[str] = []

    # Placeholder structural outcome; real BDR logic would compute this.
    # For now we use INSPECTABLE so we do not accidentally collapse existing flows.
    outcome = "INSPECTABLE"

    localization_status, loc_findings, loc_limitations = compute_localization_posture(record)

    findings.extend(loc_findings)
    limitations.extend(loc_limitations)

    receipt: Dict[str, Any] = {
        "input_path": str(input_path),
        "outcome": outcome,
        "findings": findings,
        "limitations": limitations,
        "localization_status": localization_status,
        "localization_findings": loc_findings,
    }

    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
