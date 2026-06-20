#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CHECKER_ID = 'FORK_BOUNDARY_CROSSING_EVIDENCE_INSPECTABILITY_LAYER_CHECKER_v0_1'
VALIDATION_SCOPE = 'STRUCTURAL_HANDOFF_INSPECTABILITY_ONLY'

REQUIRED_DO_NOT_MAP_TO = {
    'APPROVAL', 'AUTHORIZATION', 'CERTIFICATION', 'COMPLIANCE', 'COMPATIBILITY_RECOGNITION',
    'ENDORSEMENT', 'EVIDE_COMPATIBILITY', 'GLM_COMPATIBILITY', 'INTEROPERABILITY_RECOGNITION',
    'LEGAL_SUFFICIENCY', 'PROVENANCE_RECOGNITION', 'RISK_ACCEPTANCE', 'RUNTIME_CONTROL',
    'SAFETY', 'SC_GOVERNANCE_VALIDATION', 'TRUTH', 'CAUSALITY_VALIDATION', 'ADMISSIBILITY_VALIDATION'
}

ALLOWED_REVIEW_STATES = {
    'UNDER_REVIEW', 'ISSUER_DECLARED', 'FORK_STRUCTURAL_TRACE',
    'FORK_STRUCTURAL_RECOMPUTATION_TRACE', 'UNREVIEWED'
}
ALLOWED_RECOMPUTATION_STATUS = {
    'RECOMPUTATION_NOT_AVAILABLE', 'RECOMPUTABLE_METHOD_DECLARED',
    'RECOMPUTATION_PERFORMED', 'RECOMPUTATION_FAILED'
}
FALSE_PUBLIC_CONSTRAINTS = {
    'public_attribution_allowed', 'endorsement_claim_allowed', 'compatibility_claim_allowed',
    'certification_claim_allowed', 'interoperability_claim_allowed'
}
FALSE_AUTHORITY_ASSERTIONS = {
    'claims_approval', 'claims_authorization', 'claims_certification', 'claims_compliance',
    'claims_compatibility', 'claims_endorsement', 'claims_interoperability', 'claims_legal_sufficiency',
    'claims_runtime_control', 'claims_safety', 'claims_truth', 'claims_upstream_governance_validation'
}
FALSE_AUTHORITY_BOUNDARY = {
    'authority_transfer', 'fork_validates_upstream_governance', 'fork_validates_causality',
    'fork_participates_in_runtime_control', 'fork_validates_truth', 'fork_validates_safety',
    'fork_validates_compliance', 'fork_validates_approval', 'fork_validates_authorization',
    'fork_validates_legal_sufficiency', 'fork_validates_admissibility'
}


def duplicate_rejecting_object_pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f'DUPLICATE_JSON_KEY:{key}')
        seen.add(key)
        obj[key] = value
    return obj


def load_json_strict(path: Path) -> tuple[Any | None, list[dict[str, str]]]:
    errors: list[dict[str, str]] = []
    raw = path.read_bytes()
    if raw.startswith(b'\xef\xbb\xbf'):
        errors.append({'code': 'UTF8_BOM_DETECTED', 'path': str(path), 'message': 'UTF-8 BOM is not allowed.'})
        return None, errors
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        errors.append({'code': 'INVALID_UTF8', 'path': str(path), 'message': str(exc)})
        return None, errors
    try:
        return json.loads(text, object_pairs_hook=duplicate_rejecting_object_pairs_hook), errors
    except ValueError as exc:
        msg = str(exc)
        if msg.startswith('DUPLICATE_JSON_KEY:'):
            errors.append({'code': 'DUPLICATE_JSON_KEY', 'path': msg.split(':', 1)[1], 'message': 'Duplicate JSON key detected.'})
        else:
            errors.append({'code': 'INVALID_JSON', 'path': str(path), 'message': msg})
        return None, errors


def err(errors: list[dict[str, str]], code: str, path: str, message: str) -> None:
    errors.append({'code': code, 'path': path, 'message': message})


def require_type(errors: list[dict[str, str]], obj: Any, typ: type, path: str) -> bool:
    if not isinstance(obj, typ):
        err(errors, 'INVALID_TYPE', path, f'Expected {typ.__name__}.')
        return False
    return True


def validate_false_block(errors: list[dict[str, str]], block: Any, required_keys: set[str], path: str, code: str) -> None:
    if not require_type(errors, block, dict, path):
        return
    missing = required_keys - set(block.keys())
    for key in sorted(missing):
        err(errors, 'MISSING_REQUIRED_FIELD', f'{path}.{key}', 'Required false boundary field is missing.')
    for key in sorted(required_keys & set(block.keys())):
        if block.get(key) is not False:
            err(errors, code, f'{path}.{key}', 'Authority, attribution, or validation flag must be false.')


def validate_bundle(data: Any) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if not require_type(errors, data, dict, '$'):
        return errors

    if data.get('layer_version') != '0.1':
        err(errors, 'INVALID_LAYER_VERSION', '$.layer_version', 'Expected layer_version 0.1.')
    if data.get('validation_scope') != VALIDATION_SCOPE:
        err(errors, 'INVALID_VALIDATION_SCOPE', '$.validation_scope', f'Expected {VALIDATION_SCOPE}.')

    validate_false_block(
        errors,
        data.get('public_attribution_constraints'),
        FALSE_PUBLIC_CONSTRAINTS,
        '$.public_attribution_constraints',
        'PUBLIC_ATTRIBUTION_LEAK_DETECTED',
    )

    artifacts = data.get('upstream_artifacts')
    if not require_type(errors, artifacts, list, '$.upstream_artifacts'):
        artifacts = []
    if not artifacts:
        err(errors, 'MISSING_UPSTREAM_ARTIFACT', '$.upstream_artifacts', 'At least one upstream artifact is required.')

    artifact_ids: set[str] = set()
    for idx, artifact in enumerate(artifacts):
        path = f'$.upstream_artifacts[{idx}]'
        if not require_type(errors, artifact, dict, path):
            continue
        artifact_id = artifact.get('artifact_id')
        if not isinstance(artifact_id, str) or not artifact_id:
            err(errors, 'MISSING_REQUIRED_FIELD', f'{path}.artifact_id', 'artifact_id is required.')
        elif artifact_id in artifact_ids:
            err(errors, 'DUPLICATE_ARTIFACT_ID', f'{path}.artifact_id', 'artifact_id must be unique.')
        else:
            artifact_ids.add(artifact_id)
        if artifact.get('review_state') not in ALLOWED_REVIEW_STATES:
            err(errors, 'INVALID_REVIEW_STATE', f'{path}.review_state', 'Invalid review_state.')
        for field in ('claims', 'non_claims'):
            value = artifact.get(field)
            if not isinstance(value, list) or not value or not all(isinstance(x, str) and x for x in value):
                err(errors, 'MISSING_REQUIRED_FIELD', f'{path}.{field}', f'{field} must be a non-empty string array.')
        validate_false_block(
            errors,
            artifact.get('authority_assertions'),
            FALSE_AUTHORITY_ASSERTIONS,
            f'{path}.authority_assertions',
            'AUTHORITY_BORROWING_ATTEMPTED',
        )

    records = data.get('fork_normalized_handoff_records')
    if not require_type(errors, records, list, '$.fork_normalized_handoff_records'):
        records = []
    if not records:
        err(errors, 'MISSING_NORMALIZED_HANDOFF_RECORD', '$.fork_normalized_handoff_records', 'At least one normalized handoff record is required.')

    for idx, record in enumerate(records):
        path = f'$.fork_normalized_handoff_records[{idx}]'
        if not require_type(errors, record, dict, path):
            continue
        source_ids = record.get('source_artifact_ids')
        if not isinstance(source_ids, list) or not source_ids:
            err(errors, 'MISSING_SOURCE_ARTIFACT_ID', f'{path}.source_artifact_ids', 'source_artifact_ids must be non-empty.')
        else:
            for source_id in source_ids:
                if source_id not in artifact_ids:
                    err(errors, 'UNKNOWN_SOURCE_ARTIFACT_ID', f'{path}.source_artifact_ids', f'Unknown source artifact id: {source_id}')
        validate_false_block(
            errors,
            record.get('authority_boundary'),
            FALSE_AUTHORITY_BOUNDARY,
            f'{path}.authority_boundary',
            'AUTHORITY_BORROWING_ATTEMPTED',
        )
        if record.get('claims_preserved') is not True:
            err(errors, 'CLAIM_PRESERVATION_FAILURE', f'{path}.claims_preserved', 'claims_preserved must be true.')
        if record.get('non_claims_preserved') is not True:
            err(errors, 'NON_CLAIM_DROPPED', f'{path}.non_claims_preserved', 'non_claims_preserved must be true.')
        dropped = record.get('dropped_non_claims')
        if dropped != []:
            err(errors, 'NON_CLAIM_DROPPED', f'{path}.dropped_non_claims', 'dropped_non_claims must be empty.')
        recomputation = record.get('recomputation')
        if not require_type(errors, recomputation, dict, f'{path}.recomputation'):
            continue
        status = recomputation.get('status')
        if status not in ALLOWED_RECOMPUTATION_STATUS:
            err(errors, 'INVALID_RECOMPUTATION_STATUS', f'{path}.recomputation.status', 'Invalid recomputation status.')
        if recomputation.get('does_not_validate_truth') is not True:
            err(errors, 'RECOMPUTATION_OVERCLAIM', f'{path}.recomputation.does_not_validate_truth', 'Recomputation must not be mapped to truth validation.')
        if status == 'RECOMPUTATION_PERFORMED':
            if recomputation.get('digest_subject_available') is not True:
                err(errors, 'RECOMPUTATION_SUBJECT_MISSING', f'{path}.recomputation.digest_subject_available', 'Performed recomputation requires digest subject availability.')
            if recomputation.get('matches_declared_digest') is not True:
                err(errors, 'RECOMPUTATION_DIGEST_MISMATCH', f'{path}.recomputation.matches_declared_digest', 'Performed recomputation must match the declared digest for a structural pass.')

    result = data.get('handoff_result')
    if require_type(errors, result, dict, '$.handoff_result'):
        if result.get('fork_inherited_upstream_authority') is not False:
            err(errors, 'AUTHORITY_BORROWING_ATTEMPTED', '$.handoff_result.fork_inherited_upstream_authority', 'Fork cannot inherit upstream authority.')
        if result.get('non_claims_dropped') is not False:
            err(errors, 'NON_CLAIM_DROPPED', '$.handoff_result.non_claims_dropped', 'Result cannot drop non-claims.')
        if result.get('claim_expansion_detected') is not False:
            err(errors, 'CLAIM_EXPANSION_DETECTED', '$.handoff_result.claim_expansion_detected', 'Claim expansion detected.')
        if result.get('public_endorsement_leak_detected') is not False:
            err(errors, 'PUBLIC_ATTRIBUTION_LEAK_DETECTED', '$.handoff_result.public_endorsement_leak_detected', 'Public endorsement leak detected.')
        if result.get('interpretation_required') is not True:
            err(errors, 'INTERPRETATION_REQUIRED_MISSING', '$.handoff_result.interpretation_required', 'interpretation_required must be true.')

    do_not_map_to = data.get('do_not_map_to')
    if not isinstance(do_not_map_to, list):
        err(errors, 'MISSING_DO_NOT_MAP_TO', '$.do_not_map_to', 'do_not_map_to must be an array.')
    else:
        present = {x for x in do_not_map_to if isinstance(x, str)}
        missing = REQUIRED_DO_NOT_MAP_TO - present
        for token in sorted(missing):
            err(errors, 'MISSING_DO_NOT_MAP_TO_TOKEN', '$.do_not_map_to', f'Missing token: {token}')

    return errors


def build_output(path: Path, ok: bool, errors: list[dict[str, str]]) -> dict[str, Any]:
    return {
        'checker': CHECKER_ID,
        'checked_path': str(path),
        'validation_scope': VALIDATION_SCOPE,
        'ok': ok,
        'result_kind': 'BOUNDARY_CROSSING_EVIDENCE_INSPECTABLE' if ok else 'BOUNDARY_CROSSING_EVIDENCE_NOT_INSPECTABLE',
        'errors': errors,
        'limitations': {
            'structural_handoff_inspectability_only': True,
            'does_not_validate_truth': True,
            'does_not_validate_safety': True,
            'does_not_validate_compliance': True,
            'does_not_validate_approval': True,
            'does_not_validate_authorization': True,
            'does_not_validate_legal_sufficiency': True,
            'does_not_validate_admissibility': True,
            'does_not_validate_causality': True,
            'does_not_validate_upstream_governance': True,
            'does_not_claim_glm_compatibility': True,
            'does_not_claim_evide_compatibility': True,
            'does_not_claim_sc_validation': True,
            'does_not_claim_interoperability_recognition': True,
            'does_not_claim_endorsement': True,
            'interpretation_required': True,
            'do_not_map_to': sorted(REQUIRED_DO_NOT_MAP_TO),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description='Check Fork Boundary-Crossing Evidence Inspectability Layer bundle v0.1.')
    parser.add_argument('path', type=Path)
    parser.add_argument('--compact', action='store_true')
    args = parser.parse_args()

    data, load_errors = load_json_strict(args.path)
    errors = load_errors
    if data is not None:
        errors.extend(validate_bundle(data))
    ok = not errors
    output = build_output(args.path, ok, errors)
    if args.compact:
        print(json.dumps(output, sort_keys=True, separators=(',', ':')))
    else:
        print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
