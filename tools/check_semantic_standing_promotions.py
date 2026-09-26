#!/usr/bin/env python3
"""Bounded semantic-standing promotion checker candidate.

FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001

This tool does NOT perform general semantic interpretation of arbitrary prose.
A separate normalized-assertion sidecar supplies the semantic claim vector. The
checker mechanically evaluates that vector against declared standing,
transition, and evidence records while preserving the original source bytes.

Core boundaries:
  PROMOTION_DETECTED != SOURCE_REWRITTEN
  CHECKER_FINDING != FINAL_SEMANTIC_ADJUDICATION
  AUTHORIZED_TO_TRANSITION != TRANSITION_OCCURRED != TRANSITION_IS_EFFECTIVE
  REGISTRY_ENTRY != PROOF_OF_TRANSITION
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

PROMOTION_CLASSES = {
    "ESTABLISHMENT_PROMOTION",
    "CANONICALITY_PROMOTION",
    "VALIDATION_PROMOTION",
    "GENERALIZATION_PROMOTION",
    "AUTHORITY_PROMOTION",
    "CROSS_OBJECT_PROMOTION",
    "TEMPORAL_PROMOTION",
    "MATURITY_PROMOTION",
    "CONSEQUENCE_PROMOTION",
}

PASS = "PASS"
WITHHOLD = "WITHHOLD"
INDETERMINATE = "INDETERMINATE"
SUPPORTED_TRANSITION = "SUPPORTED_WITHIN_DECLARED_TRANSITION"
SUPPORTED_ENVELOPE = "SUPPORTED_WITHIN_DECLARED_ENVELOPE"


class CheckerError(RuntimeError):
    pass


@dataclass(frozen=True)
class SubjectIdentity:
    object_id: str
    version: str
    sha256: str

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "SubjectIdentity":
        return cls(
            object_id=str(value["object_id"]),
            version=str(value["version"]),
            sha256=str(value["sha256"]).lower(),
        )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise CheckerError(f"expected JSON object: {path}")
    return value


def parse_time(value: str | None) -> datetime | None:
    if value is None:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise CheckerError(f"timestamp must include timezone: {value}")
    return parsed.astimezone(timezone.utc)


def same_subject(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return SubjectIdentity.from_mapping(left) == SubjectIdentity.from_mapping(right)


def scope_is_covered(asserted_scope: Iterable[str], allowed_scope: Iterable[str]) -> bool:
    return set(asserted_scope).issubset(set(allowed_scope))


def temporal_in_window(anchor: str, start: str, end: str | None) -> bool:
    t_anchor = parse_time(anchor)
    t_start = parse_time(start)
    t_end = parse_time(end)
    if t_anchor is None or t_start is None:
        return False
    if t_anchor < t_start:
        return False
    return t_end is None or t_anchor <= t_end


def safe_resolve(base: Path, relative_path: str) -> Path:
    root = base.resolve()
    candidate = (base / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise CheckerError(f"evidence path escapes registry directory: {relative_path}") from exc
    return candidate


def verify_evidence_bindings(
    transition: dict[str, Any],
    evidence_registry: dict[str, Any],
    evidence_registry_path: Path,
) -> tuple[bool, list[dict[str, Any]]]:
    records = evidence_registry.get("evidence", [])
    results: list[dict[str, Any]] = []
    all_ok = True

    for binding in transition.get("evidence_bindings", []):
        artifact = binding["artifact"]
        expected = str(binding["sha256"]).lower()
        candidates = [
            item for item in records
            if item.get("artifact") == artifact
            and str(item.get("sha256", "")).lower() == expected
        ]
        if len(candidates) != 1:
            all_ok = False
            results.append({
                "artifact": artifact,
                "expected_sha256": expected,
                "status": "REGISTRY_BINDING_NOT_UNIQUE",
                "matches": len(candidates),
            })
            continue

        record = candidates[0]
        path = safe_resolve(evidence_registry_path.parent, str(record["path"]))
        if not path.is_file():
            all_ok = False
            results.append({
                "artifact": artifact,
                "expected_sha256": expected,
                "status": "EVIDENCE_UNAVAILABLE",
                "path": str(path),
            })
            continue

        actual = sha256_file(path)
        ok = actual == expected
        all_ok = all_ok and ok
        results.append({
            "artifact": artifact,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "status": "VERIFIED" if ok else "HASH_MISMATCH",
        })

    return all_ok, results


def basis_verified(transition: dict[str, Any]) -> tuple[bool, str]:
    basis = transition.get("transition_basis", {})
    basis_type = basis.get("type")
    if basis_type == "MECHANICALLY_DERIVED":
        required = {"rule_id", "authority_ref", "premise_set_ref"}
        missing = sorted(required - set(basis))
        if missing:
            return False, f"missing mechanically-derived basis fields: {', '.join(missing)}"
    elif basis_type in {
        "AUTHORIZED_CONSTITUTIVE_ACT",
        "ADJUDICATED",
        "EXTERNALLY_OBSERVED",
        "CONTRACTUALLY_MATURED",
    }:
        if basis_type in {"AUTHORIZED_CONSTITUTIVE_ACT", "ADJUDICATED"} and not basis.get("authority_ref"):
            return False, "authority_ref required for authorized/adjudicated transition"
    else:
        return False, f"unsupported transition basis: {basis_type}"
    return True, "verified"


def envelope_subject(
    envelope: dict[str, Any], subject: dict[str, Any]
) -> dict[str, Any] | None:
    matches = [item for item in envelope.get("subjects", []) if same_subject(item["subject_identity"], subject)]
    if len(matches) == 1:
        return matches[0]
    return None


def exact_transitions(
    registry: dict[str, Any], assertion: dict[str, Any]
) -> list[dict[str, Any]]:
    return [
        transition
        for transition in registry.get("transitions", [])
        if same_subject(transition["subject_identity"], assertion["subject_identity"])
        and transition.get("transition_dimension") == assertion.get("transition_dimension")
        and transition.get("to_state") == assertion.get("asserted_state")
    ]


def superseding_transitions(
    registry: dict[str, Any], assertion: dict[str, Any]
) -> list[dict[str, Any]]:
    """Transitions that make an asserted predecessor/pending state historical."""
    return [
        transition
        for transition in registry.get("transitions", [])
        if same_subject(transition["subject_identity"], assertion["subject_identity"])
        and transition.get("transition_dimension") == assertion.get("transition_dimension")
        and transition.get("from_state") == assertion.get("asserted_state")
        and transition.get("occurrence", {}).get("status") == "OCCURRED"
        and transition.get("effectivity", {}).get("status") == "EFFECTIVE"
        and temporal_in_window(
            assertion["temporal_anchor"],
            transition["effectivity"]["effective_from"],
            transition["effectivity"].get("effective_until"),
        )
    ]


def promotion_class(assertion: dict[str, Any], fallback: str = "ESTABLISHMENT_PROMOTION") -> str:
    hint = assertion.get("promotion_class_hint")
    if hint in PROMOTION_CLASSES:
        return hint
    return fallback


def evaluate_assertion(
    assertion: dict[str, Any],
    envelope: dict[str, Any],
    evidence_registry: dict[str, Any],
    transition_registry: dict[str, Any],
    evidence_registry_path: Path,
    evidence_failure: str,
) -> dict[str, Any]:
    gates: list[dict[str, Any]] = []

    subject_record = envelope_subject(envelope, assertion["subject_identity"])
    if subject_record is None:
        return {
            "assertion_id": assertion["assertion_id"],
            "disposition": WITHHOLD,
            "promotion_class": promotion_class(assertion, "CROSS_OBJECT_PROMOTION"),
            "reason": "subject identity not present uniquely in standing envelope",
            "gates": gates,
        }

    # A claim that a predecessor/pending state is operative after an effective
    # successor transition is a temporal-state error even though the predecessor
    # remains historically true.
    superseding = superseding_transitions(transition_registry, assertion)
    if superseding:
        return {
            "assertion_id": assertion["assertion_id"],
            "disposition": WITHHOLD,
            "promotion_class": "TEMPORAL_PROMOTION",
            "reason": "asserted predecessor state is historical at the assertion temporal anchor",
            "matched_transition_ids": [t["transition_id"] for t in superseding],
            "gates": gates,
        }

    transitions = exact_transitions(transition_registry, assertion)
    if len(transitions) > 1:
        return {
            "assertion_id": assertion["assertion_id"],
            "disposition": INDETERMINATE,
            "reason": "multiple exact transition records matched",
            "matched_transition_ids": [t["transition_id"] for t in transitions],
            "gates": gates,
        }

    if len(transitions) == 1:
        transition = transitions[0]
        gates.append({"gate": "G01_EXACT_SUBJECT", "pass": True})
        gates.append({"gate": "G02_EXACT_DIMENSION", "pass": True})
        gates.append({"gate": "G03_STATE_ALIGNMENT", "pass": True})

        authorized = transition.get("authorization", {}).get("status") == "AUTHORIZED"
        occurred = transition.get("occurrence", {}).get("status") == "OCCURRED"
        effective = transition.get("effectivity", {}).get("status") == "EFFECTIVE"
        temporal = effective and temporal_in_window(
            assertion["temporal_anchor"],
            transition["effectivity"]["effective_from"],
            transition["effectivity"].get("effective_until"),
        )
        gates.extend([
            {"gate": "G04_AUTHORIZATION", "pass": authorized},
            {"gate": "G05_OCCURRENCE", "pass": occurred},
            {"gate": "G06_EFFECTIVITY", "pass": effective},
            {"gate": "G07_TEMPORAL_ALIGNMENT", "pass": temporal},
        ])

        evidence_ok, evidence_results = verify_evidence_bindings(
            transition, evidence_registry, evidence_registry_path
        )
        gates.append({"gate": "G08_EVIDENCE_BINDINGS", "pass": evidence_ok, "details": evidence_results})

        scope_ok = scope_is_covered(assertion.get("scope", []), transition.get("scope", {}).get("applies_to", []))
        gates.append({"gate": "G09_SCOPE", "pass": scope_ok})

        explicit_non_effects = set(transition.get("scope", {}).get("explicit_non_effects", []))
        asserted_tokens = set(assertion.get("scope", [])) | {str(assertion.get("asserted_state", ""))}
        non_effect_ok = explicit_non_effects.isdisjoint(asserted_tokens)
        gates.append({"gate": "G10_EXPLICIT_NON_EFFECTS", "pass": non_effect_ok})

        basis_ok, basis_reason = basis_verified(transition)
        gates.append({"gate": "G11_BASIS", "pass": basis_ok, "details": basis_reason})

        if not evidence_ok:
            return {
                "assertion_id": assertion["assertion_id"],
                "disposition": WITHHOLD if evidence_failure == "withhold" else INDETERMINATE,
                "reason": "transition evidence could not be mechanically verified",
                "matched_transition_id": transition["transition_id"],
                "gates": gates,
            }

        if not non_effect_ok:
            return {
                "assertion_id": assertion["assertion_id"],
                "disposition": WITHHOLD,
                "promotion_class": promotion_class(assertion),
                "reason": "assertion intersects an explicit non-effect",
                "matched_transition_id": transition["transition_id"],
                "gates": gates,
            }

        if all(gate["pass"] for gate in gates):
            return {
                "assertion_id": assertion["assertion_id"],
                "disposition": PASS,
                "support": SUPPORTED_TRANSITION,
                "matched_transition_id": transition["transition_id"],
                "gates": gates,
            }

        return {
            "assertion_id": assertion["assertion_id"],
            "disposition": WITHHOLD,
            "promotion_class": promotion_class(assertion),
            "reason": "declared transition exists but one or more mechanical gates were not satisfied",
            "matched_transition_id": transition["transition_id"],
            "gates": gates,
        }

    # No exact transition. A current-state assertion can still be supported by
    # the standing envelope without manufacturing a transition event.
    dimension = subject_record.get("dimensions", {}).get(assertion["transition_dimension"])
    if dimension:
        current = dimension.get("current_state") == assertion.get("asserted_state")
        temporal = temporal_in_window(
            assertion["temporal_anchor"],
            dimension["effective_from"],
            dimension.get("effective_until"),
        )
        scope_ok = scope_is_covered(assertion.get("scope", []), dimension.get("applies_to", []))
        prohibited = {item["value"] for item in dimension.get("explicit_non_effects", [])}
        asserted_tokens = set(assertion.get("scope", [])) | {str(assertion.get("asserted_state", ""))}
        non_effect_ok = prohibited.isdisjoint(asserted_tokens)
        if current and temporal and scope_ok and non_effect_ok:
            return {
                "assertion_id": assertion["assertion_id"],
                "disposition": PASS,
                "support": SUPPORTED_ENVELOPE,
                "gates": [],
            }

    return {
        "assertion_id": assertion["assertion_id"],
        "disposition": WITHHOLD,
        "promotion_class": promotion_class(assertion),
        "reason": "no evidence-backed transition or standing-envelope state supports the assertion",
        "gates": [],
    }


def preserve_output_cluster(
    output_dir: Path,
    source_path: Path,
    source_bytes: bytes,
    findings: dict[str, Any],
    receipt: dict[str, Any],
) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise CheckerError(f"output directory must be absent or empty: {output_dir}")

    source_dir = output_dir / "source"
    analysis_dir = output_dir / "analysis"
    disposition_dir = output_dir / "disposition"
    source_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)
    disposition_dir.mkdir(parents=True, exist_ok=True)

    preserved_source = source_dir / f"original_ai_output{source_path.suffix or '.txt'}"
    preserved_source.write_bytes(source_bytes)
    if preserved_source.read_bytes() != source_bytes:
        raise CheckerError("source preservation byte comparison failed")

    (analysis_dir / "promotion_findings.json").write_text(
        json.dumps(findings, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (analysis_dir / "promotion_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (disposition_dir / "reviewer_decision.json").write_text(
        json.dumps({
            "status": "PENDING_AUTHORIZED_DISPOSITION",
            "checker_did_not_adjudicate": True,
            "source_sha256": receipt["source_sha256"],
        }, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--standing-envelope", required=True, type=Path)
    parser.add_argument("--evidence-registry", required=True, type=Path)
    parser.add_argument("--transition-registry", required=True, type=Path)
    parser.add_argument(
        "--assertions",
        type=Path,
        help="Normalized assertion sidecar. If omitted, semantic extraction is not guessed and disposition is INDETERMINATE.",
    )
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--evidence-failure", choices=("indeterminate", "withhold"), default="indeterminate")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        source_bytes = args.source.read_bytes()
        source_sha = sha256_bytes(source_bytes)
        envelope = load_json(args.standing_envelope)
        evidence = load_json(args.evidence_registry)
        transitions = load_json(args.transition_registry)

        if args.assertions is None:
            result = {
                "checker": "FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001",
                "candidate_status": "NOT_EMPIRICALLY_QUALIFIED",
                "overall_disposition": INDETERMINATE,
                "reason": "normalized assertion extraction not supplied; checker will not infer semantics from arbitrary prose",
                "source_sha256": source_sha,
                "findings": [],
            }
        else:
            assertion_doc = load_json(args.assertions)
            if assertion_doc.get("source_sha256", "").lower() != source_sha:
                raise CheckerError("normalized assertion sidecar does not bind to source SHA-256")

            source_text = source_bytes.decode("utf-8")
            findings: list[dict[str, Any]] = []
            for assertion in assertion_doc.get("assertions", []):
                exact_text = assertion.get("exact_text", "")
                if not exact_text or exact_text not in source_text:
                    findings.append({
                        "assertion_id": assertion.get("assertion_id", "UNIDENTIFIED"),
                        "disposition": INDETERMINATE,
                        "reason": "normalized assertion exact_text not found in preserved source",
                    })
                    continue
                findings.append(evaluate_assertion(
                    assertion,
                    envelope,
                    evidence,
                    transitions,
                    args.evidence_registry,
                    args.evidence_failure,
                ))

            dispositions = {item["disposition"] for item in findings}
            if WITHHOLD in dispositions:
                overall = WITHHOLD
            elif INDETERMINATE in dispositions:
                overall = INDETERMINATE
            else:
                overall = PASS

            result = {
                "checker": "FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001",
                "candidate_status": "NOT_EMPIRICALLY_QUALIFIED",
                "source_sha256": source_sha,
                "overall_disposition": overall,
                "findings": findings,
                "boundaries": [
                    "PROMOTION_DETECTED != SOURCE_REWRITTEN",
                    "CHECKER_FINDING != FINAL_SEMANTIC_ADJUDICATION",
                    "REGISTRY_ENTRY != PROOF_OF_TRANSITION",
                ],
            }

        receipt = {
            "checker": "FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001",
            "executed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "source_path": str(args.source),
            "source_sha256": source_sha,
            "standing_envelope_sha256": sha256_file(args.standing_envelope),
            "evidence_registry_sha256": sha256_file(args.evidence_registry),
            "transition_registry_sha256": sha256_file(args.transition_registry),
            "assertions_sha256": sha256_file(args.assertions) if args.assertions else None,
            "source_modified": False,
            "semantic_adjudication_authority": "NONE",
        }

        if args.output_dir:
            preserve_output_cluster(args.output_dir, args.source, source_bytes, result, receipt)

        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print(f"{result['overall_disposition']}: semantic-standing promotion checker candidate")
            for finding in result.get("findings", []):
                print(f"- {finding.get('assertion_id')}: {finding.get('disposition')} {finding.get('promotion_class', '')}".rstrip())

        return 0 if result["overall_disposition"] == PASS else 2 if result["overall_disposition"] == WITHHOLD else 3
    except (OSError, ValueError, KeyError, json.JSONDecodeError, CheckerError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
