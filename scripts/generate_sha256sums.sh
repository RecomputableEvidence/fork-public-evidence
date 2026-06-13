#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
export REPO_ROOT

PKT_DIR="${1:-.}"
PKT_DIR="$(cd "$PKT_DIR" && pwd)"
cd "$PKT_DIR"

if [ ! -f manifest.json ]; then
  echo "ERROR: manifest.json not found in $PKT_DIR" >&2
  exit 2
fi

python3 - <<'PY' > .manifest_digest.tmp
import json, hashlib, sys
m = json.load(open('manifest.json', encoding='utf-8'))
for forbidden in ['manifest_digest', 'signatures', 'gate_receipts']:
    if forbidden in m:
        print(f'ERROR: manifest.json contains forbidden field: {forbidden}', file=sys.stderr)
        sys.exit(2)
canonical = json.dumps(m, sort_keys=True, separators=(',', ':')).encode('utf-8')
print(hashlib.sha256(canonical).hexdigest())
PY

MANIFEST_DIGEST="$(cat .manifest_digest.tmp)"
printf 'sha256:%s  manifest.json
' "$MANIFEST_DIGEST" > SHA256SUMS

python3 - <<'PY' >> SHA256SUMS
import json, hashlib, sys, os
m = json.load(open('manifest.json', encoding='utf-8'))
lines = []
for a in m.get('artifacts', []):
    path = a['path']
    if not os.path.exists(path):
        print(f'ERROR: artifact missing: {path}', file=sys.stderr)
        sys.exit(2)
    digest = hashlib.sha256(open(path, 'rb').read()).hexdigest()
    lines.append((path, digest))
for path, digest in sorted(lines):
    print(f'sha256:{digest}  {path}')
PY

rm -f .manifest_digest.tmp
echo "Wrote SHA256SUMS in $PKT_DIR"
