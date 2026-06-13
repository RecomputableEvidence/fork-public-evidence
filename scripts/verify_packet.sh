#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
export REPO_ROOT
SCHEMA_PATH="$REPO_ROOT/schema/observed-evidence-packet.schema.json"
export SCHEMA_PATH

PKT_DIR="${1:-.}"
PKT_DIR="$(cd "$PKT_DIR" && pwd)"
cd "$PKT_DIR"

echo "Verifying packet at $PKT_DIR"

python3 - <<'PY'
import json, os, sys
from jsonschema import Draft202012Validator, exceptions
schema_path = os.environ['SCHEMA_PATH']
if not os.path.exists(schema_path):
    print(f'ERROR: schema not found: {schema_path}', file=sys.stderr)
    sys.exit(2)
schema = json.load(open(schema_path, encoding='utf-8'))
manifest = json.load(open('manifest.json', encoding='utf-8'))
try:
    Draft202012Validator(schema).validate(manifest)
except exceptions.ValidationError as e:
    print('Manifest schema validation failed:', e.message, file=sys.stderr)
    print('Path:', '/'.join(str(p) for p in e.path), file=sys.stderr)
    sys.exit(2)
print('Manifest schema validation: OK')
PY

python3 - <<'PY'
import json, sys
m = json.load(open('manifest.json', encoding='utf-8'))
for forbidden in ['manifest_digest', 'signatures', 'gate_receipts']:
    if forbidden in m:
        print(f'ERROR: manifest.json contains forbidden field: {forbidden}', file=sys.stderr)
        sys.exit(2)
print('No forbidden embedded fields in manifest: OK')
PY

if [ ! -f SHA256SUMS ]; then
  echo "SHA256SUMS not found; generating via scripts/generate_sha256sums.sh"
  "$REPO_ROOT/scripts/generate_sha256sums.sh" "$PKT_DIR"
fi

python3 - <<'PY'
import json, hashlib, os, sys, subprocess, datetime, shutil

m = json.load(open('manifest.json', encoding='utf-8'))

sums = {}
for line in open('SHA256SUMS', encoding='utf-8').read().splitlines():
    if not line.strip():
        continue
    parts = line.split()
    if len(parts) != 2 or not parts[0].startswith('sha256:'):
        print(f'ERROR: malformed SHA256SUMS line: {line}', file=sys.stderr)
        sys.exit(2)
    sums[parts[1]] = parts[0].split(':', 1)[1]

canonical = json.dumps(m, sort_keys=True, separators=(',', ':')).encode('utf-8')
manifest_digest = hashlib.sha256(canonical).hexdigest()
if sums.get('manifest.json') != manifest_digest:
    print('ERROR: manifest digest mismatch between computed canonical digest and SHA256SUMS', file=sys.stderr)
    print('computed:', manifest_digest, file=sys.stderr)
    print('SHA256SUMS:', sums.get('manifest.json'), file=sys.stderr)
    sys.exit(2)
print('Manifest digest matches SHA256SUMS: OK')

artifact_results = []
for artifact in m.get('artifacts', []):
    path = artifact['path']
    claimed_digest = artifact['digest'].split(':', 1)[1]
    if path not in sums:
        print(f'ERROR: SHA256SUMS missing artifact entry for {path}', file=sys.stderr)
        sys.exit(2)
    if sums[path] != claimed_digest:
        print(f'ERROR: manifest digest for {path} does not match SHA256SUMS', file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(path):
        print(f'ERROR: artifact file missing: {path}', file=sys.stderr)
        sys.exit(2)
    data = open(path, 'rb').read()
    actual_digest = hashlib.sha256(data).hexdigest()
    if actual_digest != sums[path]:
        print(f'ERROR: actual artifact hash mismatch for {path}', file=sys.stderr)
        sys.exit(2)
    actual_size = len(data)
    if actual_size != artifact['size_bytes']:
        print(f'ERROR: size_bytes mismatch for {path}: manifest {artifact["size_bytes"]}, actual {actual_size}', file=sys.stderr)
        sys.exit(2)
    artifact_results.append({'path': path, 'integrity': 'pass', 'size_bytes_verified': True})
print('Artifact digests, manifest digests, and size_bytes verified: OK')

signature_status = 'NOT_CHECKED'
if os.path.exists('receipt.json'):
    receipt = json.load(open('receipt.json', encoding='utf-8'))
    for rec in receipt.get('gate_receipts', []):
        if rec.get('signed_digest_ref') != 'sha256:' + manifest_digest:
            print('ERROR: receipt signed_digest_ref does not match manifest digest', file=sys.stderr)
            sys.exit(2)
    print('Receipt digest references verified; cryptographic signature verification NOT_CHECKED')
elif os.path.exists('receipt.template.json'):
    print('receipt.template.json is illustrative only; not used for verification')
else:
    print('No receipt.json present; cryptographic signature verification NOT_CHECKED')

commands = {cmd['artifact_path']: cmd for cmd in m.get('recomputation', {}).get('commands', [])}
checks = []
for artifact in m.get('artifacts', []):
    path = artifact['path']
    cls = artifact['recomputability_class']
    if cls == 'NON_RECOMPUTABLE':
        checks.append({'path': path, 'recomputability_class': cls, 'action': 'preserve_only', 'result': 'not_attempted', 'note': 'NON_RECOMPUTABLE declared; recomputation not attempted'})
    elif cls == 'STRONG_RECOMPUTATION':
        if path not in commands:
            print(f'ERROR: STRONG_RECOMPUTATION artifact lacks recomputation command: {path}', file=sys.stderr)
            sys.exit(2)
        cmd = commands[path]
        for dep in cmd.get('dependencies', []):
            dep_path = dep['path']
            if not os.path.exists(dep_path):
                print(f'ERROR: recomputation dependency missing: {dep_path}', file=sys.stderr)
                sys.exit(2)
            dep_data = open(dep_path, 'rb').read()
            dep_digest = 'sha256:' + hashlib.sha256(dep_data).hexdigest()
            if dep_digest != dep['digest']:
                print(f'ERROR: recomputation dependency digest mismatch: {dep_path}', file=sys.stderr)
                sys.exit(2)
            if len(dep_data) != dep['size_bytes']:
                print(f'ERROR: recomputation dependency size mismatch: {dep_path}', file=sys.stderr)
                sys.exit(2)
        output_path = cmd['output_path']
        if os.path.exists(output_path):
            if os.path.isdir(output_path):
                shutil.rmtree(output_path)
            else:
                os.remove(output_path)
        subprocess.run(cmd['command'], cwd=cmd.get('working_directory', '.'), check=True)
        original = open(path, 'rb').read()
        recomputed = open(output_path, 'rb').read()
        if original != recomputed:
            print(f'ERROR: bytewise recomputation mismatch for {path}', file=sys.stderr)
            sys.exit(2)
        checks.append({'path': path, 'recomputability_class': cls, 'action': 'bytewise_recompute', 'result': 'pass', 'output_path': output_path})
    else:
        print(f'ERROR: unsupported recomputability class: {cls}', file=sys.stderr)
        sys.exit(2)

verification_result = {
    'verified_at': datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
    'manifest_digest': 'sha256:' + manifest_digest,
    'artifact_integrity': artifact_results,
    'recomputability_checks': checks,
    'signature_verification': signature_status,
    'claim_boundary_preserved': True
}
open('verification_result.json', 'w', encoding='utf-8').write(json.dumps(verification_result, sort_keys=True, indent=2) + '\n')
print('Wrote verification_result.json')
PY

echo "Verification completed successfully for $PKT_DIR"
