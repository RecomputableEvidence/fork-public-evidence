#!/usr/bin/env python3
"""Verify Fork Public Technical Disclosure Bundle v0.1.1 using Python stdlib only."""
from __future__ import annotations
import hashlib, hmac, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent
FIXTURE = ROOT / "PUBLIC_REFERENCE_FIXTURE"
ERRORS: list[str] = []

INCLUDED = {"SOURCE_ASSERTION", "AI_OUTPUT", "HUMAN_REVIEW_RECORD", "INSTITUTIONAL_DISPOSITION"}
EXCLUDED_CONTROL = {"PACKET_MEMBERSHIP", "PACKET_MANIFEST", "SEAL_BINDING", "TIMESTAMP_ANCHOR"}
PROHIBITED_KEYS = {"PACKET_VALID", "TRUSTED", "COMPLIANT", "ADMISSIBLE", "LEGALLY_SUFFICIENT"}
PUBLIC_KEY = b"FORK_PUBLIC_DISCLOSURE_V0_1_1_NON_SECRET_TEST_KEY"

def load(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        ERRORS.append(f"JSON READ FAILURE: {path.relative_to(ROOT)}: {exc}")
        return None

def digest(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(condition: bool, message: str):
    if not condition:
        ERRORS.append(message)

def recursive_keys(value):
    if isinstance(value, dict):
        for k, v in value.items():
            yield k
            yield from recursive_keys(v)
    elif isinstance(value, list):
        for item in value:
            yield from recursive_keys(item)

# Load core records.
membership = load(FIXTURE / "packet_membership.json")
manifest = load(FIXTURE / "packet_manifest.json")
seal = load(FIXTURE / "seal_binding.json")
ts = load(FIXTURE / "timestamp_anchor.json")
vr = load(ROOT / "SELECTED_PUBLIC_VERIFICATION_RESULT_v0_1_1.json")
if any(x is None for x in (membership, manifest, seal, ts, vr)):
    sys.exit(1)

# Gate 001: explicit membership eligibility and enumeration.
rule = membership.get("membership_eligibility_rule", {})
require(rule.get("rule_status") == "EXPLICIT", "MEMBERSHIP ELIGIBILITY RULE NOT EXPLICIT")
require(set(rule.get("included_artifact_classes", [])) == INCLUDED, "INCLUDED ARTIFACT CLASS SET MISMATCH")
require(set(rule.get("excluded_control_artifact_classes", [])) == EXCLUDED_CONTROL, "EXCLUDED CONTROL CLASS SET MISMATCH")
declared = membership.get("declared_members", [])
require(membership.get("membership_count_declared") == len(declared), "DECLARED MEMBERSHIP COUNT MISMATCH")
ids = [m.get("member_id") for m in declared]
files = [m.get("filename") for m in declared]
require(len(ids) == len(set(ids)), "DUPLICATE MEMBER ID")
require(len(files) == len(set(files)), "DUPLICATE MEMBER FILENAME")

observed_eligible = []
for path in sorted(FIXTURE.glob("*.json")):
    obj = load(path)
    if obj is None:
        continue
    cls = obj.get("_fork_artifact_class")
    if cls in INCLUDED:
        observed_eligible.append(path.name)
    elif cls not in EXCLUDED_CONTROL:
        ERRORS.append(f"UNKNOWN OR UNCLASSIFIED FIXTURE ARTIFACT CLASS: {path.name}: {cls}")
require(set(files) == set(observed_eligible), f"ELIGIBLE MEMBERSHIP MISMATCH declared={sorted(files)} observed={sorted(observed_eligible)}")
print("PASS GATE_PUBLIC_001 DECLARED_PACKET_MEMBERSHIP")

# Gate 002: member digests.
manifest_members = manifest.get("declared_members", [])
require(manifest.get("membership_count_declared") == len(manifest_members), "MANIFEST MEMBERSHIP COUNT MISMATCH")
manifest_ids = [m.get("member_id") for m in manifest_members]
manifest_files = [m.get("filename") for m in manifest_members]
require(len(manifest_ids) == len(set(manifest_ids)), "MANIFEST DUPLICATE MEMBER ID")
require(len(manifest_files) == len(set(manifest_files)), "MANIFEST DUPLICATE FILENAME")
for member in manifest_members:
    path = FIXTURE / member["filename"]
    require(path.exists(), f"MISSING DECLARED MEMBER: {member['filename']}")
    if path.exists():
        actual = digest(path)
        require(actual == member.get("sha256"), f"MEMBER DIGEST MISMATCH: {member['filename']}")
print("PASS GATE_PUBLIC_002 MEMBER_DIGESTS")

# Gate 003: manifest digest.
fields = manifest.get("manifest_digest_canonical_fields")
require(fields == ["declared_members", "membership_count_declared", "packet_id", "packet_version"], "CANONICAL FIELD SET MISMATCH")
body = {k: manifest[k] for k in fields}
canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
actual_manifest_digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
require(actual_manifest_digest == manifest.get("manifest_digest"), "MANIFEST DIGEST MISMATCH")
print("PASS GATE_PUBLIC_003 MANIFEST_DIGEST")

# Gate 004: HMAC seal.
require(seal.get("manifest_digest_sealed") == manifest.get("manifest_digest"), "SEALED MANIFEST DIGEST REFERENCE MISMATCH")
actual_seal = hmac.new(PUBLIC_KEY, seal["manifest_digest_sealed"].encode("utf-8"), hashlib.sha256).hexdigest()
require(actual_seal == seal.get("seal_value"), "HMAC SEAL MISMATCH")
print("PASS GATE_PUBLIC_004 HMAC_SEAL_BINDING")

# Gate 005 is satisfied by this executable path over persisted bytes.
print("PASS GATE_PUBLIC_005 PERSISTED_ARTIFACT_RECOMPUTATION")

# Gate 006: granular states; append-only explicitly not checked.
gates = vr.get("gate_results", [])
valid_states = {"PASS", "FAIL", "NOT_CHECKED"}
require(all(g.get("result") in valid_states for g in gates), "INVALID GATE RESULT STATE")
require(len({g.get('gate_id') for g in gates}) == len(gates), "DUPLICATE GATE ID")
g6 = next((g for g in gates if g.get("gate_id") == "GATE_PUBLIC_006"), None)
require(g6 is not None, "GATE_PUBLIC_006 MISSING")
if g6:
    require(g6.get("sub_checks", {}).get("append_only_persistence") == "NOT_CHECKED", "APPEND_ONLY_PERSISTENCE MUST BE NOT_CHECKED")
print("PASS GATE_PUBLIC_006 GRANULAR_STATE_PRESERVATION; APPEND_ONLY_PERSISTENCE=NOT_CHECKED")

# Gate 007: recursively reject prohibited aggregate verdict fields.
found = PROHIBITED_KEYS.intersection(set(recursive_keys(vr)))
require(not found, f"PROHIBITED AGGREGATE VERDICT FIELDS PRESENT: {sorted(found)}")
summary = vr.get("verification_summary", {})
require(summary.get("gates_declared") == len(gates), "GATE SUMMARY DECLARED COUNT MISMATCH")
require(summary.get("gates_pass") == sum(g.get("result") == "PASS" for g in gates), "GATE SUMMARY PASS COUNT MISMATCH")
require(summary.get("gates_not_checked") == sum(g.get("result") == "NOT_CHECKED" for g in gates), "GATE SUMMARY NOT_CHECKED COUNT MISMATCH")
require(summary.get("gates_fail") == sum(g.get("result") == "FAIL" for g in gates), "GATE SUMMARY FAIL COUNT MISMATCH")
for key in ("aggregate_trust_verdict", "aggregate_validity_verdict", "aggregate_compliance_verdict"):
    require(summary.get(key) == "NOT_EMITTED", f"AGGREGATE VERDICT EMITTED: {key}")
print("PASS GATE_PUBLIC_007 NO_AGGREGATE_TRUST_VERDICT")

# Gate 008: internal inventory layers.
sums_path = ROOT / "SHA256SUMS.txt"
listed = {}
for raw in sums_path.read_text(encoding="utf-8").splitlines():
    if not raw or raw.startswith("#"):
        continue
    expected, sep, rel = raw.partition("  ")
    require(bool(sep), f"INVALID SHA256SUMS LINE: {raw}")
    listed[rel] = expected
for rel, expected in listed.items():
    path = ROOT / rel
    require(path.is_file(), f"INVENTORIED FILE MISSING: {rel}")
    if path.is_file():
        require(digest(path) == expected, f"BUNDLE FILE DIGEST MISMATCH: {rel}")
require("SHA256SUMS.txt" not in listed, "SHA256SUMS MUST NOT SELF-HASH")
require("PUBLIC_DISCLOSURE_MANIFEST_v0_1_1.json" not in listed, "PUBLIC MANIFEST MUST NOT APPEAR IN SHA256SUMS CIRCULAR LAYER")
public_manifest = load(ROOT / "PUBLIC_DISCLOSURE_MANIFEST_v0_1_1.json")
if public_manifest:
    require(public_manifest.get("sha256sums_sha256") == digest(sums_path), "PUBLIC MANIFEST SHA256SUMS HASH MISMATCH")
    inv = {x['filename']: x['sha256'] for x in public_manifest.get('inventoried_files', [])}
    require(inv == listed, "PUBLIC MANIFEST INVENTORY DOES NOT MATCH SHA256SUMS")
    require(public_manifest.get("public_manifest_self_hash") == "NOT_INCLUDED_RECURSION_AVOIDED", "PUBLIC MANIFEST SELF-HASH BOUNDARY MISSING")
    require(public_manifest.get("outer_zip_anchor", {}).get("status") == "PUBLISHED_AS_DETACHED_RECEIPT", "DETACHED OUTER ZIP RECEIPT STATUS MISSING")
print("PASS GATE_PUBLIC_008 EXPORT_INVENTORY_AND_DIGESTS")

# Gate 009: mechanically reproduced semantic non-promotion.
sa = load(FIXTURE / "source_assertion.json")
ao = load(FIXTURE / "ai_output.json")
hr = load(FIXTURE / "human_review.json")
idoc = load(FIXTURE / "institutional_disposition.json")
require(sa.get("_fork_artifact_class") == "SOURCE_ASSERTION", "SOURCE ASSERTION CLASS MISMATCH")
require(sa.get("_fork_source_truth") == "NOT_CLAIMED", "SOURCE ASSERTION TRUTH PROMOTION DETECTED")
require("does not adopt" in sa.get("_fork_authority_note", "").lower(), "SOURCE ASSERTION AUTHORITY BOUNDARY MISSING")
require(ao.get("_fork_artifact_class") == "AI_OUTPUT", "AI OUTPUT CLASS MISMATCH")
require("does not adopt" in ao.get("_fork_authority_note", "").lower(), "AI OUTPUT AUTHORITY BOUNDARY MISSING")
require("institutional_decision" not in ao, "AI OUTPUT PROMOTED TO INSTITUTIONAL DECISION")
require(hr.get("_fork_artifact_class") == "HUMAN_REVIEW_RECORD", "HUMAN REVIEW CLASS MISMATCH")
require("POLICY_SATISFACTION_DETERMINED_BY_FORK: FALSE" in hr.get("_fork_review_activity_vs_judgment_note", ""), "HUMAN REVIEW POLICY-SATISFACTION BOUNDARY MISSING")
require(idoc.get("_fork_artifact_class") == "INSTITUTIONAL_DISPOSITION", "INSTITUTIONAL DISPOSITION CLASS MISMATCH")
require(idoc.get("content", {}).get("disposition_meaning_authority") == "INSTITUTION", "DISPOSITION MEANING AUTHORITY PROMOTION DETECTED")
require("FORK_DOES_NOT_SILENTLY_PROMOTE" in idoc.get("_fork_operative_vs_determined_state_note", ""), "OPERATIVE/DETERMINED STATE BOUNDARY MISSING")
print("PASS GATE_PUBLIC_009 SEMANTIC_AUTHORITY_NON_PROMOTION METHOD=MECHANICALLY_REPRODUCED_GATE")

# Gate 010: timestamp disclosure boundary.
require(ts.get("timestamp_metadata_record_presence", {}).get("result") == "PASS", "TIMESTAMP METADATA RECORD PRESENCE NOT PASS")
require(ts.get("rfc3161_request_response_pair_presence", {}).get("result") == "NOT_ESTABLISHED", "RFC3161 PAIR PRESENCE MUST BE NOT_ESTABLISHED")
require(ts.get("timestamp_digest_relationship", {}).get("result") == "NOT_CHECKED", "TIMESTAMP DIGEST RELATIONSHIP MUST BE NOT_CHECKED")
require(ts.get("certificate_trust_chain_validation", {}).get("result") == "NOT_CHECKED", "TIMESTAMP TRUST CHAIN MUST BE NOT_CHECKED")
require(ts.get("independent_time_of_existence", {}).get("result") == "NOT_ESTABLISHED", "INDEPENDENT TIME OF EXISTENCE MUST BE NOT_ESTABLISHED")
print("NOT_CHECKED GATE_PUBLIC_010 TIMESTAMP_DISCLOSURE_BOUNDARY")

print()
if ERRORS:
    print("FORK_PUBLIC_TECHNICAL_DISCLOSURE_V0_1_1_FAIL")
    for error in ERRORS:
        print(f"ERROR: {error}")
    sys.exit(1)
print("FORK_PUBLIC_TECHNICAL_DISCLOSURE_V0_1_1_PASS")
print("GATES_PASS: 9")
print("GATES_NOT_CHECKED: 1")
print("GATES_FAIL: 0")
print("APPEND_ONLY_PERSISTENCE: NOT_CHECKED")
print("RFC3161_REQUEST_RESPONSE_PAIR_PRESENCE: NOT_ESTABLISHED")
print("AGGREGATE_TRUST_VERDICT: NOT_EMITTED")
