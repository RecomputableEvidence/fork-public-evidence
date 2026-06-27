param(
    [string]$LogPath = "esal-tests\canonical\log1-basic-A-B-C.jsonl",
    [int]$Iterations = 50,
    [int]$Seed = 1701,
    [string]$ExpectedFingerprint = "6b38d8a5a586052c68cb767a6e44fe583c62e952bf1df54f3f4cf7763870a836"
)

$ErrorActionPreference = "Stop"

Write-Host "== ESAL v0.1 Permutation Invariance Test =="
Write-Host "Log:        $LogPath"
Write-Host "Iterations: $Iterations"
Write-Host "Seed:       $Seed"
Write-Host ""

if (!(Test-Path $LogPath)) {
    throw "Log path not found: $LogPath"
}

$repoRoot = (Get-Location).Path
$tempScript = Join-Path ([System.IO.Path]::GetTempPath()) ("test_esal_permutation_invariance_" + [System.Guid]::NewGuid().ToString("N") + ".py")

@"
import argparse
import copy
import json
import random
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Test ESAL v0.1 permutation invariance for a canonical JSONL log."
    )
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--log", required=True)
    parser.add_argument("--iterations", type=int, default=50)
    parser.add_argument("--seed", type=int, default=1701)
    parser.add_argument("--expected-fingerprint", default="")

    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    sys.path.insert(0, str(repo_root))

    from reference.esal.runner import load_jsonl, replay

    log_path = (repo_root / args.log).resolve()
    events = load_jsonl(log_path)

    if not events:
        print(f"ERROR: log contains no events: {log_path}")
        return 1

    baseline = replay(events)

    baseline_fingerprint = baseline["fingerprint"]
    baseline_canonical_hash = baseline["canonical_events_hash"]
    baseline_state = baseline["state_dict"]
    baseline_classification = baseline["classification"]

    print("Baseline:")
    print(f"  fingerprint:           {baseline_fingerprint}")
    print(f"  canonical_events_hash: {baseline_canonical_hash}")
    print(f"  classification:        {baseline_classification}")
    print("")

    if args.expected_fingerprint and baseline_fingerprint != args.expected_fingerprint:
        print("ERROR: baseline fingerprint does not match expected fingerprint")
        print(f"  expected: {args.expected_fingerprint}")
        print(f"  observed: {baseline_fingerprint}")
        return 1

    rng = random.Random(args.seed)

    for index in range(1, args.iterations + 1):
        permuted = copy.deepcopy(events)
        rng.shuffle(permuted)

        result = replay(permuted)

        if result["fingerprint"] != baseline_fingerprint:
            print(f"ERROR: fingerprint mismatch on permutation {index}")
            print(f"  expected: {baseline_fingerprint}")
            print(f"  observed: {result['fingerprint']}")
            return 1

        if result["canonical_events_hash"] != baseline_canonical_hash:
            print(f"ERROR: canonical event sequence hash mismatch on permutation {index}")
            print(f"  expected: {baseline_canonical_hash}")
            print(f"  observed: {result['canonical_events_hash']}")
            return 1

        if result["state_dict"] != baseline_state:
            print(f"ERROR: reduced state mismatch on permutation {index}")
            print("Expected state:")
            print(json.dumps(baseline_state, sort_keys=True, indent=2))
            print("Observed state:")
            print(json.dumps(result["state_dict"], sort_keys=True, indent=2))
            return 1

        if result["classification"] != baseline_classification:
            print(f"ERROR: classification mismatch on permutation {index}")
            print(f"  expected: {baseline_classification}")
            print(f"  observed: {result['classification']}")
            return 1

    print(f"PASS: {args.iterations} permutations preserved canonical hash, state, fingerprint, and classification.")
    print(f"Fingerprint: {baseline_fingerprint}")
    print(f"Canonical events hash: {baseline_canonical_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
"@ | Set-Content -Encoding UTF8 $tempScript

try {
    python $tempScript `
        --repo-root $repoRoot `
        --log $LogPath `
        --iterations $Iterations `
        --seed $Seed `
        --expected-fingerprint $ExpectedFingerprint

    if ($LASTEXITCODE -ne 0) {
        throw "Permutation invariance test failed with exit code $LASTEXITCODE"
    }
}
finally {
    if (Test-Path $tempScript) {
        Remove-Item $tempScript -Force
    }
}

Write-Host ""
Write-Host "ESAL permutation invariance test completed."
