#!/usr/bin/env python3
"""Check actual packet bytes against preserved bindings, never just declared hashes."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

from build_csh_s001_packets_v0_1 import SCENARIOS, EXP

BINDING = Path('docs/experiments/cross-system-claim-handoff-successor-001-v0.1/PACKET_BINDING_v0_1.json')
MANIFEST = 'PACKET_MATERIALIZATION_MANIFEST_v0_1.json'


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON member')
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def safe_file(base, relative):
    path = base / relative
    for part in (path, *path.parents):
        if part == base.parent:
            break
        if part.is_symlink():
            raise ValueError(f'symlink forbidden: {relative}')
    if not path.resolve().is_relative_to(base.resolve()) or not path.is_file():
        raise ValueError(f'missing or unsafe file: {relative}')
    return path


def index(records):
    if not isinstance(records, list):
        raise ValueError('records must be an array')
    result = {}
    for row in records:
        if not isinstance(row, dict) or not isinstance(row.get('scenario_id'), str):
            raise ValueError('invalid scenario record')
        sid = row['scenario_id']
        if sid in result:
            raise ValueError('duplicate scenario')
        result[sid] = row
    if set(result) != set(SCENARIOS):
        raise ValueError('scenario population mismatch')
    return result


def evaluate(root, candidate):
    root, candidate = Path(root), Path(candidate)
    checks = []
    def record(name, passed, **details):
        checks.append({'name': name, 'passed': passed, **details})
    try:
        binding = load(root / BINDING)
        manifest = load(safe_file(candidate, MANIFEST))
        expected, observed = index(binding['records']), index(manifest['records'])
        if manifest.get('scenario_count') != len(SCENARIOS) or manifest.get('experiment_id') != EXP:
            raise ValueError('manifest identity/count mismatch')
        record('scenario_population', True)
        population = {MANIFEST}
        for sid in SCENARIOS:
            paths = {
                'projection': f'projections/HANDOFF_{sid}_s001_v0_1.json',
                'control_packet': f'packets/PROMPT_PACKET_{sid}_control_h0_s001_v0_1.json',
                'instrumented_packet': f'packets/PROMPT_PACKET_{sid}_instrumented_h1_s001_v0_1.json',
            }
            for role, relative in paths.items():
                population.add(relative)
                entry = observed[sid][role]
                if not isinstance(entry, dict) or entry.get('path') != relative:
                    raise ValueError(f'{sid}:{role}: unexpected path')
                data = safe_file(candidate, relative).read_bytes()
                actual = hashlib.sha256(data).hexdigest()
                wanted = expected[sid][role + '_sha256']
                record(f'{sid}:{role}', actual == wanted == entry.get('sha256'),
                       path=relative, actual_sha256=actual, expected_sha256=wanted,
                       declared_sha256=entry.get('sha256'))
        present = set()
        for path in candidate.rglob('*'):
            if path.is_symlink():
                raise ValueError('symlink in candidate population')
            if path.is_file():
                present.add(path.relative_to(candidate).as_posix())
        record('exact_file_population', present == population,
               missing=sorted(population-present), extra=sorted(present-population))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        record('input_structure', False, error=str(exc))
    failed = sum(not row['passed'] for row in checks)
    return {'checker': Path(__file__).name, 'checks': checks, 'failed': failed,
            'passed': len(checks)-failed, 'status': 'FAIL' if failed else 'PASS',
            'boundary': 'Local byte identity only; not delivered bytes, provider access, or experiment outcome.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('materialized_dir', type=Path)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    result = evaluate(args.root, args.materialized_dir)
    print(json.dumps(result, indent=2))
    return int(result['failed'] != 0)


if __name__ == '__main__':
    raise SystemExit(main())
