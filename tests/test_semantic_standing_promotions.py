import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_semantic_standing_promotions.py"
SUBJECT_SHA = "a" * 64
SUBJECT = {
    "object_id": "FORK-STACKED-CADENCE-BOUNDED-R&D-001",
    "version": "v0.1.5",
    "sha256": SUBJECT_SHA,
}
PENDING = "CANDIDATE_QUALIFICATION_PENDING"
QUALIFIED = "INDEPENDENT_QUALIFICATION_PASS__BOUNDED_STACKED_CADENCE"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def make_surface(tmp_path: Path, source_text: str, assertion: dict, *, corrupt_evidence: bool = False):
    source = tmp_path / "ai_output.md"
    source.write_text(source_text, encoding="utf-8")
    source_sha = sha(source.read_bytes())

    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir()
    decision = evidence_dir / "05_ADJUDICATION_DECISION.json"
    decision_bytes = b'{"G01_G09":"PASS"}\n'
    decision.write_bytes(decision_bytes)
    decision_sha = sha(decision_bytes)

    envelope = tmp_path / "standing.json"
    write_json(envelope, {
        "envelope_id": "TEST-STANDING-001",
        "subjects": [{
            "subject_identity": SUBJECT,
            "dimensions": {
                "qualification_state": {
                    "current_state": QUALIFIED,
                    "effective_from": "2026-09-19T00:00:00Z",
                    "effective_until": None,
                    "applies_to": ["TESTED_V0.1.5_SURFACE", "BOUNDED_STACKED_CADENCE_SEMANTICS"],
                    "explicit_non_effects": [
                        {"value": "CAUSAL_EVIDENTIARY_CONSTITUTION_ESTABLISHED", "promotion_class": "CANONICALITY_PROMOTION"},
                        {"value": "PRODUCTION_READY", "promotion_class": "MATURITY_PROMOTION"},
                    ],
                }
            },
        }],
    })

    evidence_registry = tmp_path / "evidence.json"
    write_json(evidence_registry, {
        "registry_id": "TEST-EVIDENCE-001",
        "evidence": [{
            "evidence_id": "ADJUDICATION-001",
            "artifact": "05_ADJUDICATION_DECISION.json",
            "path": "evidence/05_ADJUDICATION_DECISION.json",
            "sha256": decision_sha,
            "role": "ADJUDICATION_DECISION",
            "subject_identity": SUBJECT,
            "status": "PRESENT",
        }],
    })

    transitions = tmp_path / "authorized_transitions.json"
    write_json(transitions, {
        "registry_id": "TEST-TRANSITIONS-001",
        "transitions": [{
            "transition_id": "FORK-SC-v0.1.5-QUALIFICATION-TRANSITION-001",
            "subject_identity": SUBJECT,
            "transition_dimension": "qualification_state",
            "transition_basis": {
                "type": "AUTHORIZED_CONSTITUTIVE_ACT",
                "authority_ref": "FINAL-QUALIFICATION-GATE-001",
            },
            "from_state": PENDING,
            "to_state": QUALIFIED,
            "authorization": {"status": "AUTHORIZED", "authorized_at": "2026-09-19T00:00:00Z"},
            "occurrence": {"status": "OCCURRED", "occurred_at": "2026-09-19T00:00:00Z"},
            "effectivity": {"status": "EFFECTIVE", "effective_from": "2026-09-19T00:00:00Z", "effective_until": None},
            "evidence_bindings": [{
                "role": "ADJUDICATION_DECISION",
                "artifact": "05_ADJUDICATION_DECISION.json",
                "sha256": decision_sha,
            }],
            "scope": {
                "applies_to": ["TESTED_V0.1.5_SURFACE", "BOUNDED_STACKED_CADENCE_SEMANTICS"],
                "explicit_non_effects": [
                    "PRODUCTION_READY",
                    "UNIVERSAL_SEMANTIC_CORRECTNESS",
                    "CAUSAL_EVIDENTIARY_CONSTITUTION_ESTABLISHED",
                ],
            },
        }],
    })

    assertions = tmp_path / "assertions.json"
    write_json(assertions, {"source_sha256": source_sha, "assertions": [assertion]})

    if corrupt_evidence:
        decision.write_bytes(b"corrupted after registry binding\n")

    return source, envelope, evidence_registry, transitions, assertions


def run_checker(surface, *extra):
    source, envelope, evidence, transitions, assertions = surface
    cmd = [
        sys.executable,
        str(CHECKER),
        "--source", str(source),
        "--standing-envelope", str(envelope),
        "--evidence-registry", str(evidence),
        "--transition-registry", str(transitions),
        "--assertions", str(assertions),
        "--json",
        *extra,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return proc, json.loads(proc.stdout) if proc.stdout else None


def base_assertion(text: str, state: str, scope: list[str], hint: str | None = None):
    value = {
        "assertion_id": "A-001",
        "exact_text": text,
        "subject_identity": SUBJECT,
        "transition_dimension": "qualification_state",
        "asserted_state": state,
        "temporal_anchor": "2026-09-20T00:00:00Z",
        "scope": scope,
    }
    if hint:
        value["promotion_class_hint"] = hint
    return value


def test_01_accurate_current_standing_passes(tmp_path):
    text = "G01-G09 passed; v0.1.5 is now qualified."
    assertion = base_assertion(text, QUALIFIED, ["TESTED_V0.1.5_SURFACE"])
    proc, result = run_checker(make_surface(tmp_path, text, assertion))
    assert proc.returncode == 0
    assert result["overall_disposition"] == "PASS"
    assert result["findings"][0]["support"] == "SUPPORTED_WITHIN_DECLARED_TRANSITION"


def test_02_explicit_non_effect_is_withheld(tmp_path):
    text = "Stacked Cadence validates Fork's causal-evidentiary constitution."
    assertion = base_assertion(
        text,
        QUALIFIED,
        ["TESTED_V0.1.5_SURFACE", "CAUSAL_EVIDENTIARY_CONSTITUTION_ESTABLISHED"],
        "CROSS_OBJECT_PROMOTION",
    )
    proc, result = run_checker(make_surface(tmp_path, text, assertion))
    assert proc.returncode == 2
    assert result["overall_disposition"] == "WITHHOLD"
    assert result["findings"][0]["promotion_class"] == "CROSS_OBJECT_PROMOTION"


def test_03_historical_pending_state_is_temporal_promotion(tmp_path):
    text = "The final qualification gate package will determine if G01-G09 pass."
    assertion = base_assertion(text, PENDING, ["TESTED_V0.1.5_SURFACE"], "TEMPORAL_PROMOTION")
    proc, result = run_checker(make_surface(tmp_path, text, assertion))
    assert proc.returncode == 2
    assert result["findings"][0]["promotion_class"] == "TEMPORAL_PROMOTION"


def test_04_no_normalized_assertions_is_indeterminate(tmp_path):
    text = "Unparsed semantic text."
    assertion = base_assertion(text, QUALIFIED, ["TESTED_V0.1.5_SURFACE"])
    source, envelope, evidence, transitions, _ = make_surface(tmp_path, text, assertion)
    cmd = [
        sys.executable,
        str(CHECKER),
        "--source", str(source),
        "--standing-envelope", str(envelope),
        "--evidence-registry", str(evidence),
        "--transition-registry", str(transitions),
        "--json",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    result = json.loads(proc.stdout)
    assert proc.returncode == 3
    assert result["overall_disposition"] == "INDETERMINATE"


def test_05_output_cluster_preserves_source_bytes(tmp_path):
    text = "G01-G09 passed; v0.1.5 is now qualified.\n"
    assertion = base_assertion(text.strip(), QUALIFIED, ["TESTED_V0.1.5_SURFACE"])
    surface = make_surface(tmp_path, text, assertion)
    out = tmp_path / "out"
    proc, result = run_checker(surface, "--output-dir", str(out))
    assert proc.returncode == 0
    assert result["overall_disposition"] == "PASS"
    assert (out / "source" / "original_ai_output.md").read_bytes() == surface[0].read_bytes()
    disposition = json.loads((out / "disposition" / "reviewer_decision.json").read_text(encoding="utf-8"))
    assert disposition["status"] == "PENDING_AUTHORIZED_DISPOSITION"
    assert disposition["checker_did_not_adjudicate"] is True


def test_06_hash_mismatch_is_indeterminate_by_default(tmp_path):
    text = "G01-G09 passed; v0.1.5 is now qualified."
    assertion = base_assertion(text, QUALIFIED, ["TESTED_V0.1.5_SURFACE"])
    proc, result = run_checker(make_surface(tmp_path, text, assertion, corrupt_evidence=True))
    assert proc.returncode == 3
    assert result["overall_disposition"] == "INDETERMINATE"
    assert result["findings"][0]["reason"] == "transition evidence could not be mechanically verified"
