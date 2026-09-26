import hashlib
import json
import subprocess
import sys
from copy import deepcopy
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


def scope_coordinate(
    claim: str = "BOUNDED_STACKED_CADENCE_SEMANTICS",
    *,
    surface: str = "TESTED_V0.1.5_SURFACE",
    dimension: str = "qualification_state",
    object_id: str = SUBJECT["object_id"],
) -> dict:
    return {
        "subject_object_id": object_id,
        "dimension": dimension,
        "surface": surface,
        "claim": claim,
    }


def make_surface(
    tmp_path: Path,
    source_text: str = "G01-G09 passed; v0.1.5 is now qualified.",
    *,
    asserted_state: str = QUALIFIED,
    assertion_scope: list[dict] | None = None,
):
    source = tmp_path / "ai_output.md"
    source.write_text(source_text, encoding="utf-8")
    source_sha = sha(source.read_bytes())

    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir()
    specs = [
        ("AUTH-001", "AUTHORIZATION_BASIS", "authorization.json", b'{"authorized":true}\n'),
        ("OCC-001", "OCCURRENCE_RECEIPT", "occurrence.json", b'{"occurred":true}\n'),
        ("EFF-001", "EFFECTIVITY_RECEIPT", "effectivity.json", b'{"effective":true}\n'),
        ("ADJ-001", "ADJUDICATION_DECISION", "decision.json", b'{"G01_G09":"PASS"}\n'),
        ("BASIS-001", "AUTHORITY_BASIS", "basis.json", b'{"authority":"gate"}\n'),
        ("STANDING-001", "STANDING_STATE_RECEIPT", "standing_receipt.json", b'{"standing":"qualified"}\n'),
    ]

    records = []
    bindings = {}
    for evidence_id, role, artifact, data in specs:
        path = evidence_dir / artifact
        path.write_bytes(data)
        digest = sha(data)
        records.append(
            {
                "evidence_id": evidence_id,
                "artifact": artifact,
                "path": f"evidence/{artifact}",
                "sha256": digest,
                "role": role,
                "subject_identity": SUBJECT,
                "status": "PRESENT",
            }
        )
        bindings[evidence_id] = {
            "evidence_id": evidence_id,
            "role": role,
            "artifact": artifact,
            "sha256": digest,
            "subject_identity": SUBJECT,
        }

    evidence_registry = tmp_path / "evidence.json"
    write_json(evidence_registry, {"registry_id": "TEST-EVIDENCE-001", "evidence": records})

    prohibited = {
        "coordinate": scope_coordinate("CAUSAL_EVIDENTIARY_CONSTITUTION_ESTABLISHED"),
        "promotion_class": "CANONICALITY_PROMOTION",
    }
    standing = tmp_path / "standing.json"
    write_json(
        standing,
        {
            "envelope_id": "TEST-STANDING-001",
            "subjects": [
                {
                    "subject_identity": SUBJECT,
                    "dimensions": {
                        "qualification_state": {
                            "current_state": QUALIFIED,
                            "verification_status": "VERIFIED",
                            "effective_from": "2026-09-19T00:00:00Z",
                            "effective_until": None,
                            "evidence_bindings": [bindings["STANDING-001"]],
                            "applies_to": [scope_coordinate()],
                            "explicit_non_effects": [prohibited],
                        }
                    },
                }
            ],
        },
    )

    transitions = tmp_path / "authorized_transitions.json"
    write_json(
        transitions,
        {
            "registry_id": "TEST-TRANSITIONS-001",
            "transitions": [
                {
                    "transition_id": "FORK-SC-v0.1.5-QUALIFICATION-TRANSITION-001",
                    "subject_identity": SUBJECT,
                    "transition_dimension": "qualification_state",
                    "transition_basis": {
                        "type": "AUTHORIZED_CONSTITUTIVE_ACT",
                        "authority_ref": "FINAL-QUALIFICATION-GATE-001",
                        "evidence_bindings": [bindings["BASIS-001"]],
                    },
                    "from_state": PENDING,
                    "to_state": QUALIFIED,
                    "authorization": {
                        "asserted_status": "AUTHORIZED",
                        "verification_status": "VERIFIED",
                        "authorized_at": "2026-09-19T00:00:00Z",
                        "evidence_bindings": [bindings["AUTH-001"]],
                    },
                    "occurrence": {
                        "asserted_status": "OCCURRED",
                        "verification_status": "VERIFIED",
                        "occurred_at": "2026-09-19T00:00:00Z",
                        "evidence_bindings": [bindings["OCC-001"]],
                    },
                    "effectivity": {
                        "asserted_status": "EFFECTIVE",
                        "verification_status": "VERIFIED",
                        "effective_from": "2026-09-19T00:00:00Z",
                        "effective_until": None,
                        "evidence_bindings": [bindings["EFF-001"]],
                    },
                    "evidence_bindings": [bindings["ADJ-001"]],
                    "scope": {
                        "applies_to": [scope_coordinate()],
                        "explicit_non_effects": [prohibited],
                    },
                }
            ],
        },
    )

    assertions = tmp_path / "assertions.json"
    write_json(
        assertions,
        {
            "source_sha256": source_sha,
            "normalization_provenance": {
                "normalizer_id": "TEST-NORMALIZER",
                "method": "manual frozen fixture mapping",
                "authority": "DESCRIPTIVE_MAPPING_ONLY",
                "coverage_status": "COMPLETE_CLAIMED",
            },
            "assertions": [
                {
                    "assertion_id": "A-001",
                    "exact_text": source_text,
                    "subject_identity": SUBJECT,
                    "transition_dimension": "qualification_state",
                    "asserted_state": asserted_state,
                    "temporal_anchor": {
                        "value": "2026-09-20T00:00:00Z",
                        "source_class": "REVIEWER_SUPPLIED",
                        "verification_status": "VERIFIED",
                    },
                    "scope": assertion_scope or [scope_coordinate()],
                }
            ],
        },
    )
    return source, standing, evidence_registry, transitions, assertions


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_checker(surface, *extra, assertions: bool = True):
    source, standing, evidence, transitions, assertion_path = surface
    cmd = [
        sys.executable,
        str(CHECKER),
        "--source",
        str(source),
        "--standing-envelope",
        str(standing),
        "--evidence-registry",
        str(evidence),
        "--transition-registry",
        str(transitions),
        "--json",
    ]
    if assertions:
        cmd.extend(["--assertions", str(assertion_path)])
    cmd.extend(extra)
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return proc, json.loads(proc.stdout) if proc.stdout else None


def mutate_json(path: Path, fn) -> None:
    value = read_json(path)
    fn(value)
    write_json(path, value)


def test_01_verified_transition_is_supported(tmp_path):
    proc, result = run_checker(make_surface(tmp_path))
    assert proc.returncode == 0
    assert result["overall_action"] == "PASS"
    assert result["source_assurance"] == "SUPPLIED_ASSERTIONS_ONLY"
    assert result["findings"][0]["disposition"] == "SUPPORTED_WITHIN_DECLARED_TRANSITION"


def test_02_explicit_non_effect_is_withheld(tmp_path):
    text = "Stacked Cadence validates Fork's causal-evidentiary constitution."
    surface = make_surface(
        tmp_path,
        text,
        assertion_scope=[scope_coordinate("CAUSAL_EVIDENTIARY_CONSTITUTION_ESTABLISHED")],
    )
    proc, result = run_checker(surface)
    assert proc.returncode == 2
    finding = result["findings"][0]
    assert finding["action"] == "WITHHOLD"
    assert finding["promotion_class"] == "CANONICALITY_PROMOTION"


def test_03_verified_supersession_detects_temporal_promotion(tmp_path):
    text = "The final qualification gate package will determine if G01-G09 pass."
    proc, result = run_checker(make_surface(tmp_path, text, asserted_state=PENDING))
    assert proc.returncode == 2
    assert result["findings"][0]["promotion_class"] == "TEMPORAL_PROMOTION"


def test_04_no_normalized_assertions_is_indeterminate(tmp_path):
    proc, result = run_checker(make_surface(tmp_path), assertions=False)
    assert proc.returncode == 3
    assert result["overall_action"] == "INDETERMINATE"


def test_05_output_cluster_preserves_source_bytes(tmp_path):
    surface = make_surface(tmp_path, "G01-G09 passed; v0.1.5 is now qualified.\n")
    out = tmp_path / "out"
    proc, result = run_checker(surface, "--output-dir", str(out))
    assert proc.returncode == 0
    assert (out / "source" / "original_ai_output.md").read_bytes() == surface[0].read_bytes()
    decision = read_json(out / "disposition" / "reviewer_decision.json")
    assert decision["status"] == "PENDING_AUTHORIZED_DISPOSITION"
    assert decision["checker_did_not_adjudicate"] is True


def test_06_corrupt_transition_evidence_is_indeterminate(tmp_path):
    surface = make_surface(tmp_path)
    (tmp_path / "evidence" / "decision.json").write_bytes(b"corrupted\n")
    proc, result = run_checker(surface)
    assert proc.returncode == 3
    assert result["findings"][0]["disposition"] == "INDETERMINATE_UNRESOLVED_EVIDENCE"


def test_07_standing_envelope_requires_verified_evidence(tmp_path):
    surface = make_surface(tmp_path)
    mutate_json(surface[3], lambda value: value.__setitem__("transitions", []))
    def mutate(value):
        for item in value["evidence"]:
            if item["evidence_id"] == "STANDING-001":
                item["status"] = "SUPERSEDED"
    mutate_json(surface[2], mutate)
    proc, result = run_checker(surface)
    assert proc.returncode == 3
    assert result["findings"][0]["disposition"] == "INDETERMINATE_UNRESOLVED_EVIDENCE"


def test_08_verified_standing_envelope_can_index_current_state(tmp_path):
    surface = make_surface(tmp_path)
    mutate_json(surface[3], lambda value: value.__setitem__("transitions", []))
    proc, result = run_checker(surface)
    assert proc.returncode == 0
    assert result["findings"][0]["disposition"] == "SUPPORTED_WITHIN_VERIFIED_ENVELOPE"


def test_09_asserted_authorization_without_verification_is_not_accepted(tmp_path):
    surface = make_surface(tmp_path)
    mutate_json(
        surface[3],
        lambda value: value["transitions"][0]["authorization"].__setitem__("verification_status", "UNVERIFIED"),
    )
    proc, result = run_checker(surface)
    assert proc.returncode == 3
    assert result["findings"][0]["disposition"] == "INDETERMINATE_UNRESOLVED_EVIDENCE"


def test_10_asserted_occurrence_without_verification_is_not_accepted(tmp_path):
    surface = make_surface(tmp_path)
    mutate_json(
        surface[3],
        lambda value: value["transitions"][0]["occurrence"].__setitem__("verification_status", "UNVERIFIED"),
    )
    proc, _ = run_checker(surface)
    assert proc.returncode == 3


def test_11_asserted_effectivity_without_verification_is_not_accepted(tmp_path):
    surface = make_surface(tmp_path)
    mutate_json(
        surface[3],
        lambda value: value["transitions"][0]["effectivity"].__setitem__("verification_status", "UNVERIFIED"),
    )
    proc, _ = run_checker(surface)
    assert proc.returncode == 3


def test_12_wrong_subject_evidence_cannot_satisfy_binding(tmp_path):
    surface = make_surface(tmp_path)
    def mutate(value):
        for item in value["evidence"]:
            if item["evidence_id"] == "AUTH-001":
                item["subject_identity"] = {**SUBJECT, "version": "v0.1.4"}
    mutate_json(surface[2], mutate)
    proc, _ = run_checker(surface)
    assert proc.returncode == 3


def test_13_wrong_role_evidence_cannot_satisfy_binding(tmp_path):
    surface = make_surface(tmp_path)
    def mutate(value):
        for item in value["evidence"]:
            if item["evidence_id"] == "AUTH-001":
                item["role"] = "UNRELATED_ROLE"
    mutate_json(surface[2], mutate)
    proc, _ = run_checker(surface)
    assert proc.returncode == 3


def test_14_superseded_evidence_cannot_satisfy_binding(tmp_path):
    surface = make_surface(tmp_path)
    def mutate(value):
        for item in value["evidence"]:
            if item["evidence_id"] == "AUTH-001":
                item["status"] = "SUPERSEDED"
    mutate_json(surface[2], mutate)
    proc, _ = run_checker(surface)
    assert proc.returncode == 3


def test_15_basis_reference_requires_bound_basis_evidence(tmp_path):
    surface = make_surface(tmp_path)
    def mutate_transition(value):
        value["transitions"][0]["transition_basis"]["evidence_bindings"][0]["role"] = "UNRELATED_ROLE"
    def mutate_evidence(value):
        for item in value["evidence"]:
            if item["evidence_id"] == "BASIS-001":
                item["role"] = "UNRELATED_ROLE"
    mutate_json(surface[3], mutate_transition)
    mutate_json(surface[2], mutate_evidence)
    proc, result = run_checker(surface)
    assert proc.returncode == 3
    gates = result["findings"][0]["gates"]
    assert next(g for g in gates if g["gate"] == "G11_BASIS_VERIFIED")["pass"] is False


def test_16_unverified_superseding_transition_cannot_create_temporal_promotion(tmp_path):
    text = "The final qualification gate package will determine if G01-G09 pass."
    surface = make_surface(tmp_path, text, asserted_state=PENDING)
    mutate_json(
        surface[3],
        lambda value: value["transitions"][0]["authorization"].__setitem__("verification_status", "UNVERIFIED"),
    )
    proc, result = run_checker(surface)
    assert proc.returncode == 2
    assert result["findings"][0].get("promotion_class") != "TEMPORAL_PROMOTION"


def test_17_conflicting_verified_transitions_are_indeterminate(tmp_path):
    surface = make_surface(tmp_path)
    def mutate(value):
        second = deepcopy(value["transitions"][0])
        second["transition_id"] = "FORK-SC-v0.1.5-QUALIFICATION-TRANSITION-002"
        value["transitions"].append(second)
    mutate_json(surface[3], mutate)
    proc, result = run_checker(surface)
    assert proc.returncode == 3
    assert result["findings"][0]["disposition"] == "INDETERMINATE_CONFLICTING_TRANSITIONS"


def test_18_inferred_temporal_anchor_is_indeterminate(tmp_path):
    surface = make_surface(tmp_path)
    mutate_json(
        surface[4],
        lambda value: value["assertions"][0]["temporal_anchor"].__setitem__("source_class", "INFERRED"),
    )
    proc, result = run_checker(surface)
    assert proc.returncode == 3
    assert result["findings"][0]["disposition"] == "INDETERMINATE_TEMPORAL_ANCHOR"


def test_19_schema_contract_extra_property_is_rejected(tmp_path):
    surface = make_surface(tmp_path)
    mutate_json(surface[4], lambda value: value.__setitem__("undeclared_field", True))
    proc, result = run_checker(surface)
    assert proc.returncode == 4
    assert result is None
    assert "unsupported keys" in proc.stderr


def test_20_version_leakage_is_subject_mismatch(tmp_path):
    surface = make_surface(tmp_path)
    mutate_json(
        surface[4],
        lambda value: value["assertions"][0].__setitem__("subject_identity", {**SUBJECT, "version": "v0.1.4"}),
    )
    proc, result = run_checker(surface)
    assert proc.returncode == 2
    finding = result["findings"][0]
    assert finding["disposition"] == "WITHHOLD_SUBJECT_MISMATCH"
    assert finding["promotion_class"] == "CROSS_OBJECT_PROMOTION"


def test_21_dimension_leakage_is_dimension_mismatch(tmp_path):
    surface = make_surface(tmp_path)
    mutate_json(
        surface[4],
        lambda value: value["assertions"][0].__setitem__("transition_dimension", "production_state"),
    )
    proc, result = run_checker(surface)
    assert proc.returncode == 2
    assert result["findings"][0]["disposition"] == "WITHHOLD_DIMENSION_MISMATCH"


def test_22_normalization_is_descriptive_and_source_assurance_is_bounded(tmp_path):
    proc, result = run_checker(make_surface(tmp_path))
    assert proc.returncode == 0
    assert result["normalization_provenance"]["authority"] == "DESCRIPTIVE_MAPPING_ONLY"
    assert result["source_assurance"] == "SUPPLIED_ASSERTIONS_ONLY"
