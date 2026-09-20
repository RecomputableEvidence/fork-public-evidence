"""Pressure tests against commit 3284e82ca88f3d736a455398c72814882ec10e8b.

Each test targets a specific boundary of the checker that is either new in this
commit or exposed by the newly-documented occurrence-binding and CRLF rules.

Pressure vectors covered:

  P-26  Mixed CRLF+bare-CR in exact_text - lone CR is not normalised
  P-27  exact_text with lone \\r, LF source - no match expected
  P-28  CRLF source and CRLF exact_text   - both collapse → PASS
  P-29  SHA bound to CRLF bytes, source served as LF bytes - sha mismatch → code 4
  P-30  exact_text appears twice in source - occurrence-binding ambiguity open
  P-31  evidence_binding sha256 in uppercase - must normalise and match
  P-32  evidence path traversal ../ attempt - must reject (code 4)
  P-33  assertion scope superset of transition scope - G09 fails → WITHHOLD
  P-34  assertion scope is empty list - contract rejects (code 4)
  P-35  temporal anchor == effective_from boundary - must be inside (PASS)
  P-36  temporal anchor == effective_until boundary - must be inside (PASS)
  P-37  temporal anchor one second before effective_from - must be outside (WITHHOLD)
  P-38  two unverified superseding transitions - NO temporal promotion
  P-39  one verified + one unverified superseding transition - TEMPORAL_PROMOTION
  P-40  envelope dimension verification_status = UNKNOWN - INDETERMINATE
  P-41  assertion anchor before envelope effective_from - WITHHOLD_PROMOTION
  P-42  duplicate assertion_id - contract rejects (code 4)
  P-43  duplicate transition_id - contract rejects (code 4)
  P-44  EXTERNALLY_OBSERVED basis missing OBSERVATION_BASIS role - G11 fails
"""

import importlib.util
import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location(
    "_semantic_standing_helpers",
    ROOT / "tests" / "test_semantic_standing_promotions.py",
)
assert _SPEC is not None and _SPEC.loader is not None
_H = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_H)

make_surface = _H.make_surface
mutate_json = _H.mutate_json
run_checker = _H.run_checker
write_json = _H.write_json
sha = _H.sha
SUBJECT = _H.SUBJECT
QUALIFIED = _H.QUALIFIED
PENDING = _H.PENDING
scope_coordinate = _H.scope_coordinate


# ---------------------------------------------------------------------------
# P-26  Mixed CRLF + bare CR in exact_text – lone CR is NOT normalised
# ---------------------------------------------------------------------------

def test_p26_lone_cr_in_exact_text_does_not_match_lf_source(tmp_path):
    """exact_text containing \\r\\n followed by a lone \\r must not match an LF source
    because the lone \\r is not part of the CRLF normalisation rule."""
    surface = make_surface(tmp_path, "line1\nline2\nline3")
    source, _, _, _, assertions = surface
    # Source is pure LF.  exact_text has a lone \\r in it.
    mutate_json(
        assertions,
        lambda v: v["assertions"][0].__setitem__("exact_text", "line1\r\nline2\rline3"),
    )
    proc, result = run_checker(surface)
    assert proc.returncode == 3
    assert result["findings"][0]["disposition"] == "INDETERMINATE_NORMALIZATION_COVERAGE"


# ---------------------------------------------------------------------------
# P-27  exact_text with lone \\r only, LF source – no match
# ---------------------------------------------------------------------------

def test_p27_lone_cr_only_exact_text_does_not_match_lf_source(tmp_path):
    """A \\r-only line ending in exact_text is not equivalent to \\n."""
    surface = make_surface(tmp_path, "alpha\nbeta")
    source, _, _, _, assertions = surface
    mutate_json(
        assertions,
        lambda v: v["assertions"][0].__setitem__("exact_text", "alpha\rbeta"),
    )
    proc, result = run_checker(surface)
    assert proc.returncode == 3
    assert result["findings"][0]["disposition"] == "INDETERMINATE_NORMALIZATION_COVERAGE"


# ---------------------------------------------------------------------------
# P-28  CRLF source + CRLF exact_text – both normalise to LF → PASS
# ---------------------------------------------------------------------------

def test_p28_crlf_source_and_crlf_exact_text_both_normalise(tmp_path):
    """When both the source file and exact_text carry CRLF, both normalise to LF
    for the containment check and the result should be PASS."""
    lf_text = "G01-G09 passed; v0.1.5 is now qualified."
    surface = make_surface(tmp_path, lf_text)
    source, _, _, _, assertions = surface

    # Overwrite source with CRLF bytes and rebind the SHA.
    crlf_bytes = (lf_text + "\r\n").encode("utf-8")
    source.write_bytes(crlf_bytes)
    mutate_json(
        assertions,
        lambda v: (
            v.__setitem__("source_sha256", sha(crlf_bytes)),
            v["assertions"][0].__setitem__("exact_text", lf_text + "\r\n"),
        ),
    )

    proc, result = run_checker(surface)
    assert proc.returncode == 0
    assert result["overall_action"] == "PASS"
    assert result["findings"][0]["disposition"] == "SUPPORTED_WITHIN_DECLARED_TRANSITION"


# ---------------------------------------------------------------------------
# P-29  SHA bound to CRLF bytes, actual source file has LF bytes – SHA mismatch → code 4
# ---------------------------------------------------------------------------

def test_p29_sha_mismatch_crlf_sidecar_lf_source_is_rejected(tmp_path):
    """If the sidecar SHA was computed from CRLF bytes but the source file
    is LF-only (bytes written directly), the SHA binding check must fail
    before any evaluation.

    The source is written with write_bytes so the on-disk bytes are
    guaranteed LF-only regardless of platform line-ending translation.
    The sidecar SHA is then set to the CRLF equivalent, creating a
    genuine mismatch that the checker must reject."""
    lf_text = "G01-G09 passed; v0.1.5 is now qualified.\n"
    surface = make_surface(tmp_path, lf_text)
    source, _, _, _, assertions = surface

    # Force the source file to pure LF bytes, bypassing platform translation.
    lf_bytes = lf_text.encode("utf-8")
    source.write_bytes(lf_bytes)

    # Set the sidecar SHA to the CRLF version — now it genuinely mismatches.
    crlf_bytes = lf_text.replace("\n", "\r\n").encode("utf-8")
    assert lf_bytes != crlf_bytes, "precondition: LF and CRLF bytes must differ"
    mutate_json(assertions, lambda v: v.__setitem__("source_sha256", sha(crlf_bytes)))

    proc, result = run_checker(surface)
    assert proc.returncode == 4   # CheckerError raised before evaluation
    assert result is None
    assert "SHA-256" in proc.stderr


# ---------------------------------------------------------------------------
# P-30  exact_text appears twice in the source – occurrence-binding ambiguity open
# ---------------------------------------------------------------------------

def test_p30_duplicate_occurrence_in_source_does_not_promote(tmp_path):
    """The checker must not treat text that appears multiple times in the source
    as automatically evidence-backed.  The outcome should still reflect the
    transition/envelope evaluation, not fabricate a second binding.
    We expect the checker to continue evaluating normally (PASS if transition
    is verified) but the occurrence ambiguity remains open per WORK_ORDER item 7."""
    repeated = "G01-G09 passed; v0.1.5 is now qualified."
    source_text = repeated + "\n" + repeated  # text appears twice
    surface = make_surface(tmp_path, source_text, asserted_state=QUALIFIED)
    # exact_text = source_text (both occurrences present) — still a valid PASS
    # because transition verification is independent of occurrence count.
    proc, result = run_checker(surface)
    assert proc.returncode == 0, f"unexpected stderr: {proc.stderr}"
    assert result["overall_action"] == "PASS"
    # Confirm no fabricated second finding was emitted.
    assert len(result["findings"]) == 1


# ---------------------------------------------------------------------------
# P-31  evidence_binding sha256 in uppercase – must normalise and match
# ---------------------------------------------------------------------------

def test_p31_uppercase_sha256_in_evidence_binding_is_accepted(tmp_path):
    """Evidence binding sha256 stored in uppercase should still match because
    the checker normalises both sides to lowercase before comparison."""
    surface = make_surface(tmp_path)
    mutate_json(
        surface[3],
        lambda v: v["transitions"][0]["evidence_bindings"][0].__setitem__(
            "sha256",
            v["transitions"][0]["evidence_bindings"][0]["sha256"].upper(),
        ),
    )
    proc, result = run_checker(surface)
    assert proc.returncode == 0
    assert result["findings"][0]["disposition"] == "SUPPORTED_WITHIN_DECLARED_TRANSITION"


# ---------------------------------------------------------------------------
# P-32  Evidence path traversal ../ attempt – must reject (code 4)
# ---------------------------------------------------------------------------

def test_p32_evidence_path_traversal_is_rejected(tmp_path):
    """An evidence record whose path escapes the registry directory via ../
    must be rejected with a CheckerError."""
    surface = make_surface(tmp_path)
    def mutate(v):
        for item in v["evidence"]:
            if item["evidence_id"] == "ADJ-001":
                item["path"] = "../outside.json"
    mutate_json(surface[2], mutate)
    proc, result = run_checker(surface)
    assert proc.returncode == 4
    assert result is None
    assert "escapes" in proc.stderr


# ---------------------------------------------------------------------------
# P-33  Assertion scope superset of transition scope – G09 fails → WITHHOLD
# ---------------------------------------------------------------------------

def test_p33_assertion_scope_superset_of_transition_scope_is_withheld(tmp_path):
    """If the assertion claims a scope coordinate not covered by the transition's
    applies_to list, G09 must fail and the result must be WITHHOLD."""
    surface = make_surface(tmp_path)
    extra_coord = scope_coordinate("EXTRA_CLAIM_NOT_IN_TRANSITION")
    mutate_json(
        surface[4],
        lambda v: v["assertions"][0].__setitem__(
            "scope",
            [scope_coordinate(), extra_coord],
        ),
    )
    proc, result = run_checker(surface)
    assert proc.returncode == 2
    finding = result["findings"][0]
    assert finding["action"] == "WITHHOLD"


# ---------------------------------------------------------------------------
# P-34  Assertion scope is empty list – contract validation rejects (code 4)
# ---------------------------------------------------------------------------

def test_p34_empty_assertion_scope_is_rejected_by_contract(tmp_path):
    """The assertions schema requires scope to be a non-empty array.
    Supplying an empty list must be caught by validate_assertion_doc."""
    surface = make_surface(tmp_path)
    mutate_json(surface[4], lambda v: v["assertions"][0].__setitem__("scope", []))
    proc, result = run_checker(surface)
    assert proc.returncode == 4
    assert result is None
    assert "scope" in proc.stderr.lower() or "non-empty" in proc.stderr


# ---------------------------------------------------------------------------
# P-35  Temporal anchor == effective_from – inclusive lower bound → PASS
# ---------------------------------------------------------------------------

def test_p35_temporal_anchor_equal_to_effective_from_is_inside_window(tmp_path):
    """The lower bound of the effectivity window is inclusive.
    An anchor exactly equal to effective_from must yield PASS."""
    surface = make_surface(tmp_path)
    # Both transition effective_from and assertion anchor are 2026-09-19T00:00:00Z.
    # Make them match exactly.
    mutate_json(
        surface[4],
        lambda v: v["assertions"][0]["temporal_anchor"].__setitem__(
            "value", "2026-09-19T00:00:00Z"
        ),
    )
    proc, result = run_checker(surface)
    assert proc.returncode == 0
    assert result["findings"][0]["disposition"] == "SUPPORTED_WITHIN_DECLARED_TRANSITION"


# ---------------------------------------------------------------------------
# P-36  Temporal anchor == effective_until – inclusive upper bound → PASS
# ---------------------------------------------------------------------------

def test_p36_temporal_anchor_equal_to_effective_until_is_inside_window(tmp_path):
    """The upper bound of the effectivity window is inclusive.
    An anchor exactly equal to effective_until must yield PASS."""
    surface = make_surface(tmp_path)
    end = "2026-12-31T23:59:59Z"
    # Set effective_until on the transition effectivity.
    mutate_json(
        surface[3],
        lambda v: v["transitions"][0]["effectivity"].__setitem__("effective_until", end),
    )
    # Set the assertion anchor to that exact boundary.
    mutate_json(
        surface[4],
        lambda v: v["assertions"][0]["temporal_anchor"].__setitem__("value", end),
    )
    proc, result = run_checker(surface)
    assert proc.returncode == 0
    assert result["findings"][0]["disposition"] == "SUPPORTED_WITHIN_DECLARED_TRANSITION"


# ---------------------------------------------------------------------------
# P-37  Temporal anchor one second before effective_from – outside window → WITHHOLD
# ---------------------------------------------------------------------------

def test_p37_temporal_anchor_one_second_before_effective_from_is_outside_window(tmp_path):
    """An anchor one second before the transition effective_from must not pass
    the temporal alignment gate."""
    surface = make_surface(tmp_path)
    # effective_from is 2026-09-19T00:00:00Z; set anchor to one second before.
    mutate_json(
        surface[4],
        lambda v: v["assertions"][0]["temporal_anchor"].__setitem__(
            "value", "2026-09-18T23:59:59Z"
        ),
    )
    proc, result = run_checker(surface)
    # No transition passes G07; no envelope temporal match either (anchor < effective_from).
    assert proc.returncode == 2
    assert result["findings"][0]["action"] == "WITHHOLD"


# ---------------------------------------------------------------------------
# P-38  Two unverified superseding transitions – NO temporal promotion
# ---------------------------------------------------------------------------

def test_p38_two_unverified_superseding_transitions_do_not_produce_temporal_promotion(tmp_path):
    """Two superseding transitions that both fail evidentiary verification must
    not cause TEMPORAL_PROMOTION.  Only a fully-verified superseding transition
    triggers that classification."""
    text = "The final qualification gate package will determine if G01-G09 pass."
    surface = make_surface(tmp_path, text, asserted_state=PENDING)

    def mutate(v):
        # First unverified superseder already exists from make_surface
        v["transitions"][0]["authorization"]["verification_status"] = "UNVERIFIED"
        # Add a second unverified superseder.
        second = deepcopy(v["transitions"][0])
        second["transition_id"] = "SUPERSEDER-002"
        v["transitions"].append(second)

    mutate_json(surface[3], mutate)
    proc, result = run_checker(surface)
    finding = result["findings"][0]
    # Must NOT be TEMPORAL_PROMOTION (no verified superseder).
    assert finding.get("promotion_class") != "TEMPORAL_PROMOTION"


# ---------------------------------------------------------------------------
# P-39  One verified + one unverified superseding transition – TEMPORAL_PROMOTION
# ---------------------------------------------------------------------------

def test_p39_one_verified_superseding_transition_yields_temporal_promotion(tmp_path):
    """A mix of one verified and one unverified superseding transition:
    the verified one is sufficient to trigger TEMPORAL_PROMOTION."""
    text = "The final qualification gate package will determine if G01-G09 pass."
    surface = make_surface(tmp_path, text, asserted_state=PENDING)

    def mutate(v):
        # Keep the first transition fully verified (it will supersede PENDING).
        # Add a second, unverified superseder alongside it.
        second = deepcopy(v["transitions"][0])
        second["transition_id"] = "SUPERSEDER-003-UNVERIFIED"
        second["authorization"]["verification_status"] = "UNVERIFIED"
        v["transitions"].append(second)

    mutate_json(surface[3], mutate)
    proc, result = run_checker(surface)
    assert proc.returncode == 2
    assert result["findings"][0]["promotion_class"] == "TEMPORAL_PROMOTION"


# ---------------------------------------------------------------------------
# P-40  Envelope dimension verification_status = UNKNOWN – INDETERMINATE
# ---------------------------------------------------------------------------

def test_p40_envelope_dimension_unknown_verification_is_indeterminate(tmp_path):
    """If the standing envelope dimension carries verification_status UNKNOWN,
    the checker must not accept it as verified support."""
    surface = make_surface(tmp_path)
    # Remove all transitions so only the envelope path is available.
    mutate_json(surface[3], lambda v: v.__setitem__("transitions", []))
    # Set envelope verification_status to UNKNOWN.
    mutate_json(
        surface[1],
        lambda v: v["subjects"][0]["dimensions"]["qualification_state"].__setitem__(
            "verification_status", "UNKNOWN"
        ),
    )
    proc, result = run_checker(surface)
    assert proc.returncode == 3
    assert result["findings"][0]["disposition"] == "INDETERMINATE_UNRESOLVED_EVIDENCE"


# ---------------------------------------------------------------------------
# P-41  Assertion temporal anchor before envelope effective_from – WITHHOLD_PROMOTION
# ---------------------------------------------------------------------------

def test_p41_anchor_before_envelope_effective_from_is_withheld(tmp_path):
    """When no transition matches and the assertion's temporal anchor is before
    the envelope effective_from, the envelope temporal check must fail and the
    result must be WITHHOLD_PROMOTION (not a PASS via envelope)."""
    surface = make_surface(tmp_path)
    mutate_json(surface[3], lambda v: v.__setitem__("transitions", []))
    # Anchor one year before the envelope effective_from (2026-09-19).
    mutate_json(
        surface[4],
        lambda v: v["assertions"][0]["temporal_anchor"].__setitem__(
            "value", "2025-01-01T00:00:00Z"
        ),
    )
    proc, result = run_checker(surface)
    assert proc.returncode == 2
    assert result["findings"][0]["action"] == "WITHHOLD"


# ---------------------------------------------------------------------------
# P-42  Duplicate assertion_id – contract rejects (code 4)
# ---------------------------------------------------------------------------

def test_p42_duplicate_assertion_id_is_rejected(tmp_path):
    """Two assertions sharing the same assertion_id must be rejected by
    validate_assertion_doc before any evaluation."""
    surface = make_surface(tmp_path)

    def mutate(v):
        second = deepcopy(v["assertions"][0])
        second["exact_text"] = v["assertions"][0]["exact_text"]
        v["assertions"].append(second)

    mutate_json(surface[4], mutate)
    proc, result = run_checker(surface)
    assert proc.returncode == 4
    assert result is None
    assert "duplicate" in proc.stderr.lower()


# ---------------------------------------------------------------------------
# P-43  Duplicate transition_id – contract rejects (code 4)
# ---------------------------------------------------------------------------

def test_p43_duplicate_transition_id_is_rejected(tmp_path):
    """Two transitions sharing the same transition_id must be rejected by
    validate_transition_registry before any evaluation."""
    surface = make_surface(tmp_path)

    def mutate(v):
        second = deepcopy(v["transitions"][0])
        v["transitions"].append(second)

    mutate_json(surface[3], mutate)
    proc, result = run_checker(surface)
    assert proc.returncode == 4
    assert result is None
    assert "duplicate" in proc.stderr.lower()


# ---------------------------------------------------------------------------
# P-44  EXTERNALLY_OBSERVED basis missing OBSERVATION_BASIS role – G11 fails
# ---------------------------------------------------------------------------

def test_p44_externally_observed_basis_missing_observation_role_fails_g11(tmp_path):
    """An EXTERNALLY_OBSERVED transition basis must supply an evidence binding
    with role OBSERVATION_BASIS.  Supplying a different role must fail G11."""
    surface = make_surface(tmp_path)

    def mutate_transition(v):
        basis = v["transitions"][0]["transition_basis"]
        basis["type"] = "EXTERNALLY_OBSERVED"
        # Remove MECHANICALLY_DERIVED-only fields if present.
        for key in ("authority_ref", "rule_id", "premise_set_ref"):
            basis.pop(key, None)
        # Keep the existing binding but with a non-OBSERVATION_BASIS role.
        for binding in basis["evidence_bindings"]:
            binding["role"] = "AUTHORITY_BASIS"  # wrong for EXTERNALLY_OBSERVED

    def mutate_evidence(v):
        for item in v["evidence"]:
            if item["evidence_id"] == "BASIS-001":
                item["role"] = "AUTHORITY_BASIS"

    mutate_json(surface[3], mutate_transition)
    mutate_json(surface[2], mutate_evidence)

    proc, result = run_checker(surface)
    assert proc.returncode == 3
    gates = result["findings"][0].get("gates", [])
    g11 = next((g for g in gates if g["gate"] == "G11_BASIS_VERIFIED"), None)
    assert g11 is not None, "G11 gate not reported in finding"
    assert g11["pass"] is False
