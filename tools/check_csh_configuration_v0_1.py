#!/usr/bin/env python3
"""Validate the complete, still-unfrozen CSH v0.1 experiment configuration."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

BASE = Path("docs/experiments/cross-system-claim-handoff-v0.1")
PROMPTS = BASE / "prompts"
HANDOFF = BASE / "handoff"
CORPUS = BASE / "corpus"
REGISTRY = BASE / "SYSTEM_REGISTRY_v0_1.json"
MANIFEST = BASE / "EXPERIMENT_MANIFEST_v0_1.json"
FREEZE = BASE / "CORPUS_FREEZE_v0_1.json"
RUN_ORDER = PROMPTS / "RUN_ORDER_v0_1.json"
PAIR_MANIFEST = PROMPTS / "PAIR_MANIFEST_v0_1.json"
SHARED_INSTRUCTION_PATH = PROMPTS / "SHARED_RECEIVER_INSTRUCTION_v0_1.txt"
PROMPT_SCHEMA = Path("schemas/cross_system_claim_handoff_prompt_packet_v0_1.schema.json")
RUN_ORDER_SCHEMA = Path("schemas/cross_system_claim_handoff_run_order_v0_1.schema.json")
HANDOFF_SCHEMA = Path("schemas/cross_system_claim_handoff_state_artifact_v0_1.schema.json")
REGISTRY_SCHEMA = Path("schemas/cross_system_claim_handoff_system_registry_v0_1.schema.json")
SCENARIO_SCHEMA = Path("schemas/cross_system_claim_handoff_scenario_v0_1.schema.json")
SCENARIO_IDS = (
    "SIM_A_BOUNDARY_PRESERVED",
    "SIM_B_BOUNDARY_NARROWED",
    "SIM_C_NON_CLAIM_DROPPED",
    "SIM_D_EXPANSION_WITHOUT_AUTHORITY",
    "SIM_F_POINTER_UNRESOLVED",
    "SIM_H_CASCADING_INHERITANCE",
)
RECEIVER_IDS = ("llm_receiver_a", "llm_receiver_b", "deterministic_receiver")
CONDITIONS = ("control_h0", "instrumented_h1")
RUN_ORDER_SALT = "CSH_V0_1_PAIR_BLOCK_ORDER_SHA256_2026_07_11"
WORKFLOW_TASK = "Prepare a downstream transfer record for another system using only the supplied packet."
SHARED_INSTRUCTION = """You are a downstream receiver in a controlled claim-handoff study.
Use only the supplied user-message packet. Do not use tools, retrieval, memory, prior conversation, or outside knowledge.
Prepare a downstream transfer record for another system.
Return exactly one JSON object with these keys:
{
  "summary": "string",
  "assertions": [
    {
      "text": "string",
      "relationship_to_source": "PRESERVED|NARROWED|EXPANDED|UNRESOLVED|MIXED"
    }
  ],
  "caveats": ["string"],
  "unresolved_items": ["string"],
  "authority_basis": ["string"],
  "evidence_basis": ["string"],
  "local_revalidation": ["string"]
}
Do not include markdown or text outside the JSON object.
"""


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "README.md").exists():
            return candidate
    raise RuntimeError("Repository root not found")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def schema_errors(instance: Any, schema: Any) -> list[str]:
    return [
        f"{'/'.join(str(p) for p in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(instance),
            key=lambda error: list(error.absolute_path),
        )
    ]


def scenario_path(scenario_id: str) -> Path:
    return CORPUS / f"{scenario_id}.json"


def handoff_path(scenario_id: str) -> Path:
    return HANDOFF / f"HANDOFF_{scenario_id}_v0_1.json"


def prompt_path(scenario_id: str, condition: str) -> Path:
    return PROMPTS / f"PROMPT_PACKET_{scenario_id}_{condition}_v0_1.json"


def expected_run_units() -> list[dict[str, Any]]:
    entrypoints = {
        "llm_receiver_a": "tools/csh_receiver_a_llama_v0_1.py",
        "llm_receiver_b": "tools/csh_receiver_b_deepseek_v0_1.py",
        "deterministic_receiver": "tools/csh_receiver_deterministic_v0_1.py",
    }
    pair_keys = []
    for scenario_id in SCENARIO_IDS:
        for receiver_id in RECEIVER_IDS:
            for replicate_id in (1, 2, 3):
                key = f"{scenario_id}|{receiver_id}|r{replicate_id}"
                pair_keys.append((scenario_id, receiver_id, replicate_id, key))
    pair_keys.sort(key=lambda item: hashlib.sha256(f"{RUN_ORDER_SALT}|{item[3]}".encode()).hexdigest())
    units = []
    ordinal = 1
    instruction = (PROMPTS / "SHARED_RECEIVER_INSTRUCTION_v0_1.txt").as_posix()
    for block_index, (scenario_id, receiver_id, replicate_id, key) in enumerate(pair_keys, start=1):
        order = CONDITIONS if block_index % 2 == 1 else tuple(reversed(CONDITIONS))
        for condition in order:
            present = condition == "instrumented_h1"
            units.append(
                {
                    "ordinal": ordinal,
                    "planned_run_id": f"CSH-RUN-{ordinal:03d}",
                    "pair_block_ordinal": block_index,
                    "pairing_key": key,
                    "scenario_id": scenario_id,
                    "condition": condition,
                    "receiver_class_id": receiver_id,
                    "replicate_id": replicate_id,
                    "system_instruction_path": instruction,
                    "prompt_path": prompt_path(scenario_id, condition).as_posix(),
                    "source_artifact_path": scenario_path(scenario_id).as_posix(),
                    "handoff_artifact_path": handoff_path(scenario_id).as_posix() if present else None,
                    "handoff_artifact_present": present,
                    "receiver_entrypoint": entrypoints[receiver_id],
                }
            )
            ordinal += 1
    return units


def expected_registry(root: Path, registry_status: str = "draft_unfrozen") -> dict[str, Any]:
    a_adapter = Path("tools/csh_receiver_a_llama_v0_1.py")
    b_adapter = Path("tools/csh_receiver_b_deepseek_v0_1.py")
    c_adapter = Path("tools/csh_receiver_deterministic_v0_1.py")
    a_config = BASE / "receivers/RECEIVER_A_GITHUB_MODELS_LLAMA_SCOUT_v0_1.json"
    b_config = BASE / "receivers/RECEIVER_B_GITHUB_MODELS_DEEPSEEK_V3_0324_v0_1.json"
    common = {
        "endpoint": "https://models.github.ai/inference/chat/completions",
        "temperature": 0,
        "top_p": 1,
        "max_tokens": 2048,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "stream": False,
        "tools": "omitted",
        "retrieval": "disabled",
        "memory": "disabled",
        "conversation_history": "none",
        "seed": "omitted",
        "authentication_environment_variable": "GITHUB_TOKEN",
        "required_permission": "models: read",
        "secret_persisted": False,
    }
    a_parameters = dict(common)
    a_parameters.update({
        "expected_returned_model": "Llama-4-Scout-17B-16E-Instruct",
        "adapter_path": a_adapter.as_posix(),
        "adapter_sha256": sha256(root / a_adapter),
        "configuration_path": a_config.as_posix(),
        "configuration_sha256": sha256(root / a_config),
    })
    b_parameters = dict(common)
    b_parameters.update({
        "expected_returned_model": "DeepSeek-V3-0324",
        "adapter_path": b_adapter.as_posix(),
        "adapter_sha256": sha256(root / b_adapter),
        "configuration_path": b_config.as_posix(),
        "configuration_sha256": sha256(root / b_config),
    })
    c_hash = sha256(root / c_adapter)
    return {
        "experiment_id": "cross_system_claim_handoff_v0_1",
        "schema_version": "v0.1",
        "registry_status": registry_status,
        "receiver_classes": [
            {
                "receiver_class_id": "llm_receiver_a",
                "receiver_type": "llm",
                "provider": "Meta via GitHub Models",
                "model_or_system": "meta/Llama-4-Scout-17B-16E-Instruct",
                "version": "requested model ID meta/Llama-4-Scout-17B-16E-Instruct; expected returned model Llama-4-Scout-17B-16E-Instruct",
                "parameters": a_parameters,
                "access_path": "GitHub Models REST inference through tools/csh_receiver_a_llama_v0_1.py",
            },
            {
                "receiver_class_id": "llm_receiver_b",
                "receiver_type": "llm",
                "provider": "DeepSeek via GitHub Models",
                "model_or_system": "deepseek/DeepSeek-V3-0324",
                "version": "requested model ID deepseek/DeepSeek-V3-0324; expected returned model DeepSeek-V3-0324",
                "parameters": b_parameters,
                "access_path": "GitHub Models REST inference through tools/csh_receiver_b_deepseek_v0_1.py",
            },
            {
                "receiver_class_id": "deterministic_receiver",
                "receiver_type": "deterministic",
                "provider": "local",
                "model_or_system": c_adapter.as_posix(),
                "version": f"v0.1 source_sha256={c_hash}",
                "parameters": {
                    "network_calls": False,
                    "model_calls": False,
                    "randomness": False,
                    "clock_input": False,
                    "environment_input": False,
                    "ordered_rules": True,
                    "canonical_utf8_lf_json": True,
                    "byte_identical_for_identical_inputs_and_source": True,
                    "python_requirement": ">=3.11",
                    "source_sha256": c_hash,
                },
                "access_path": "local_execution through tools/csh_receiver_deterministic_v0_1.py",
            },
        ],
        "freeze_requirements": [
            "verify tools/check_csh_configuration_v0_1.py passes",
            "compute the system registry digest during PrepareFreeze",
            "bind scenario, prompt, handoff, schema, checker, and fixed run-order artifacts",
            "bind the subject commit and verify the signed freeze tag before baseline execution",
        ],
    }


def evaluate(root: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    schema_paths = [PROMPT_SCHEMA, RUN_ORDER_SCHEMA, HANDOFF_SCHEMA, REGISTRY_SCHEMA, SCENARIO_SCHEMA]
    schemas: dict[Path, Any] = {}
    for path in schema_paths:
        try:
            schema = load(root / path)
            Draft202012Validator.check_schema(schema)
            schemas[path] = schema
            record(f"schema:{path.name}", True, "valid")
        except Exception as exc:
            record(f"schema:{path.name}", False, str(exc))

    try:
        instruction = (root / SHARED_INSTRUCTION_PATH).read_text(encoding="utf-8")
        record("shared_instruction_exact", instruction == SHARED_INSTRUCTION, "exact frozen candidate text")
    except Exception as exc:
        record("shared_instruction_exact", False, str(exc))

    scenarios: dict[str, Any] = {}
    scenario_errors = []
    for scenario_id in SCENARIO_IDS:
        path = root / scenario_path(scenario_id)
        try:
            item = load(path)
            scenarios[scenario_id] = item
            errors = schema_errors(item, schemas[SCENARIO_SCHEMA])
            if errors:
                scenario_errors.extend(f"{scenario_id}: {error}" for error in errors)
        except Exception as exc:
            scenario_errors.append(f"{scenario_id}: {exc}")
    record("scenario_set", not scenario_errors and set(scenarios) == set(SCENARIO_IDS), "; ".join(scenario_errors) or "six valid scenarios")

    handoffs: dict[str, Any] = {}
    handoff_errors = []
    observed_handoff_paths = sorted((root / HANDOFF).glob("HANDOFF_SIM_*_v0_1.json"))
    if len(observed_handoff_paths) != 6:
        handoff_errors.append(f"expected 6 handoffs; found {len(observed_handoff_paths)}")
    for scenario_id, scenario in scenarios.items():
        path = root / handoff_path(scenario_id)
        try:
            item = load(path)
            handoffs[scenario_id] = item
            handoff_errors.extend(f"{scenario_id}: {e}" for e in schema_errors(item, schemas[HANDOFF_SCHEMA]))
            if item.get("scenario_id") != scenario_id:
                handoff_errors.append(f"{scenario_id}: scenario mismatch")
            emitted = [{"claim_id": x.get("claim_id"), "text": x.get("text")} for x in item.get("emitted_claims", [])]
            if emitted != scenario["source_claims"]:
                handoff_errors.append(f"{scenario_id}: emitted claims differ from source claims")
            if item.get("non_claims") != scenario["source_non_claims"]:
                handoff_errors.append(f"{scenario_id}: non-claims differ from source")
            if item.get("unresolved_state") != scenario["unresolved_references"]:
                handoff_errors.append(f"{scenario_id}: unresolved state differs from source")
            if item.get("permitted_narrowing") != scenario["permitted_transformations"]:
                handoff_errors.append(f"{scenario_id}: permitted narrowing differs from source")
            missing_prohibited = sorted(set(scenario["prohibited_outcomes"]) - set(item.get("prohibited_inferences", [])))
            if missing_prohibited:
                handoff_errors.append(f"{scenario_id}: missing prohibited outcomes {missing_prohibited}")
            expected_evidence = [scenario_path(scenario_id).as_posix()]
            if item.get("evidence_references") != expected_evidence:
                handoff_errors.append(f"{scenario_id}: evidence reference mismatch")
            if item.get("authority_references") != []:
                handoff_errors.append(f"{scenario_id}: authority references must remain explicitly empty")
        except Exception as exc:
            handoff_errors.append(f"{scenario_id}: {exc}")
    record("handoff_artifacts", not handoff_errors, "; ".join(handoff_errors) or "six schema-valid handoff artifacts")

    prompt_errors = []
    observed_prompt_paths = sorted((root / PROMPTS).glob("PROMPT_PACKET_SIM_*_v0_1.json"))
    if len(observed_prompt_paths) != 12:
        prompt_errors.append(f"expected 12 prompt packets; found {len(observed_prompt_paths)}")
    for scenario_id, scenario in scenarios.items():
        control = instrumented = None
        for condition in CONDITIONS:
            path = root / prompt_path(scenario_id, condition)
            try:
                item = load(path)
                prompt_errors.extend(f"{path.name}: {e}" for e in schema_errors(item, schemas[PROMPT_SCHEMA]))
                if item.get("scenario_id") != scenario_id:
                    prompt_errors.append(f"{path.name}: scenario mismatch")
                if item.get("source_artifact") != scenario:
                    prompt_errors.append(f"{path.name}: source artifact mismatch")
                if item.get("workflow_task") != WORKFLOW_TASK:
                    prompt_errors.append(f"{path.name}: workflow task mismatch")
                if condition == "control_h0":
                    control = item
                    if item.get("handoff_state_artifact") is not None:
                        prompt_errors.append(f"{path.name}: control contains a handoff artifact")
                else:
                    instrumented = item
                    if item.get("handoff_state_artifact") != handoffs.get(scenario_id):
                        prompt_errors.append(f"{path.name}: treatment handoff mismatch")
            except Exception as exc:
                prompt_errors.append(f"{path.name}: {exc}")
        if control is not None and instrumented is not None:
            c = dict(control)
            i = dict(instrumented)
            c.pop("handoff_state_artifact", None)
            i.pop("handoff_state_artifact", None)
            if c != i:
                prompt_errors.append(f"{scenario_id}: paired packets differ outside handoff_state_artifact")
    record("paired_prompt_packets", not prompt_errors, "; ".join(prompt_errors) or "12 packets; pairwise difference limited to handoff field")

    try:
        pair_manifest = load(root / PAIR_MANIFEST)
        pair_errors = []
        if pair_manifest.get("pair_count") != 6:
            pair_errors.append("pair_count is not 6")
        if pair_manifest.get("shared_instruction_path") != SHARED_INSTRUCTION_PATH.as_posix():
            pair_errors.append("shared instruction path mismatch")
        if pair_manifest.get("shared_instruction_sha256") != sha256(root / SHARED_INSTRUCTION_PATH):
            pair_errors.append("shared instruction hash mismatch")
        entries = pair_manifest.get("pairs", [])
        if [x.get("scenario_id") for x in entries] != list(SCENARIO_IDS):
            pair_errors.append("scenario order mismatch")
        for entry in entries:
            for key in ("source_artifact", "handoff_artifact", "control_prompt", "instrumented_prompt"):
                info = entry.get(key, {})
                path = root / info.get("path", "")
                if not path.is_file() or info.get("sha256") != sha256(path):
                    pair_errors.append(f"{entry.get('scenario_id')}: {key} digest mismatch")
            if entry.get("difference_contract") != "handoff_state_artifact_only":
                pair_errors.append(f"{entry.get('scenario_id')}: difference contract mismatch")
        record("pair_manifest", not pair_errors, "; ".join(pair_errors) or "all pair digests and contracts verified")
    except Exception as exc:
        record("pair_manifest", False, str(exc))

    try:
        registry = load(root / REGISTRY)
        registry_errors = schema_errors(registry, schemas[REGISTRY_SCHEMA])
        if "UNASSIGNED" in json.dumps(registry):
            registry_errors.append("registry contains UNASSIGNED")
        if registry != expected_registry(root, registry.get("registry_status", "")):
            registry_errors.append("registry differs from the exact receiver configuration")
        record("system_registry", not registry_errors, "; ".join(registry_errors) or "exact assigned registry")
    except Exception as exc:
        record("system_registry", False, str(exc))

    try:
        run_order = load(root / RUN_ORDER)
        order_errors = schema_errors(run_order, schemas[RUN_ORDER_SCHEMA])
        if run_order.get("units") != expected_run_units():
            order_errors.append("unit order differs from fixed salted pair-block algorithm")
        units = run_order.get("units", [])
        if len({u.get("planned_run_id") for u in units}) != 108:
            order_errors.append("planned run IDs are not unique")
        first_conditions = [units[i]["condition"] for i in range(0, len(units), 2)] if len(units) == 108 else []
        if first_conditions.count("control_h0") != 27 or first_conditions.count("instrumented_h1") != 27:
            order_errors.append("pair-block first-condition counterbalance is not 27/27")
        record("fixed_run_order", not order_errors, "; ".join(order_errors) or "108 units in 54 adjacent counterbalanced pair blocks")
    except Exception as exc:
        record("fixed_run_order", False, str(exc))

    try:
        manifest = load(root / MANIFEST)
        required_schemas = {
            PROMPT_SCHEMA.as_posix(),
            RUN_ORDER_SCHEMA.as_posix(),
            HANDOFF_SCHEMA.as_posix(),
        }
        required_checkers = {"tools/check_csh_configuration_v0_1.py"}
        errors = []
        if not required_schemas.issubset(set(manifest.get("schemas", []))):
            errors.append("manifest does not list all Step 5 schemas")
        if not required_checkers.issubset(set(manifest.get("checkers", []))):
            errors.append("manifest does not list configuration checker")
        if manifest.get("baseline_run_status") != "not_started":
            errors.append("baseline status is not not_started")
        if manifest.get("freeze_status") not in {"draft_unfrozen", "frozen"}:
            errors.append("manifest freeze status is invalid")
        if manifest.get("freeze_status") == "draft_unfrozen" and manifest.get("status") != "preregistered_not_executed":
            errors.append("draft manifest status mismatch")
        if manifest.get("freeze_status") == "frozen" and manifest.get("status") != "frozen_not_executed":
            errors.append("frozen manifest status mismatch")
        record("manifest_configuration_binding", not errors, "; ".join(errors) or "Step 5 schemas/checker listed; execution state consistent")
    except Exception as exc:
        record("manifest_configuration_binding", False, str(exc))

    try:
        freeze = load(root / FREEZE)
        errors = []
        status = freeze.get("freeze_status")
        if status == "draft_unfrozen":
            if freeze.get("baseline_execution_permitted") is not False:
                errors.append("draft baseline execution is not blocked")
            if not freeze.get("blocking_unresolved_items"):
                errors.append("draft blocking unresolved items are empty")
        elif status == "frozen":
            if freeze.get("baseline_execution_permitted") is not True:
                errors.append("frozen baseline execution is not permitted")
            if freeze.get("blocking_unresolved_items") != []:
                errors.append("frozen blocking unresolved items are not empty")
        else:
            errors.append("unknown freeze status")
        registry_status = load(root / REGISTRY).get("registry_status")
        if registry_status != status:
            errors.append("registry and freeze status differ")
        record("execution_gate_consistency", not errors, "; ".join(errors) or f"configuration and execution gate consistent for {status}")
    except Exception as exc:
        record("unfrozen_execution_gate", False, str(exc))

    integration_errors = []
    required_text = {
        "scripts/seal_csh_experiment_v0_1.ps1": [
            "cross_system_claim_handoff_prompt_packet_v0_1.schema.json",
            "cross_system_claim_handoff_run_order_v0_1.schema.json",
            "check_csh_configuration_v0_1.py",
            "Expected exactly twelve paired prompt packets",
            "Expected exactly six handoff-state artifacts",
        ],
        ".github/workflows/cross-system-claim-handoff-v0-1.yml": [
            "Validate complete CSH configuration",
            "Run CSH configuration tests",
            "tools/check_csh_configuration_v0_1.py",
            "tests/test_csh_configuration_v0_1.py",
        ],
        "scripts/verify_fork_proof_surface_v0_1.ps1": [
            "Cross-System Claim Handoff configuration",
            "tests/test_csh_configuration_v0_1.py",
        ],
        "tools/validate_json_schema_bundle_v0_1.py": [
            "cross_system_claim_handoff_prompt_packet_v0_1.schema.json",
            "cross_system_claim_handoff_run_order_v0_1.schema.json",
            "HANDOFF_SIM_*_v0_1.json",
        ],
    }
    for relative, needles in required_text.items():
        try:
            text = (root / relative).read_text(encoding="utf-8")
            for needle in needles:
                if needle not in text:
                    integration_errors.append(f"{relative}: missing {needle}")
        except Exception as exc:
            integration_errors.append(f"{relative}: {exc}")
    record("integration_bindings", not integration_errors, "; ".join(integration_errors) or "freeze, workflow, verifier, and schema bundle bindings present")

    failed = [item for item in checks if not item["passed"]]
    return {
        "checker": Path(__file__).name,
        "total": len(checks),
        "passed": len(checks) - len(failed),
        "failed": len(failed),
        "checks": checks,
        "interpretation": {
            "proves": [
                "the complete Step 5 receiver, prompt, handoff, registry, and fixed run-order configuration is structurally present",
                "paired prompt packets differ only by the explicit handoff-state artifact field",
                "the execution gate is consistent with the current draft or frozen state",
            ],
            "does_not_prove": [
                "that any baseline unit executed",
                "that hosted receivers will remain available",
                "that the CSH hypothesis is true",
                "truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, production readiness, or institutional authority",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    result = evaluate(repo_root(args.root))
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for item in result["checks"]:
            print(f"[{'PASS' if item['passed'] else 'FAIL'}] {item['name']}: {item['detail']}")
        print("CSH_CONFIGURATION_PASS" if result["failed"] == 0 else "CSH_CONFIGURATION_FAIL")
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
