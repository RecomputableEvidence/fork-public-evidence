# Fork Public Disclosure v0.1.1 — Local Recomputation

This bundle can be checked with Python 3.8+ standard library only.

## 0. Verify the detached outer-ZIP receipt before extraction

The detached file `FORK_PUBLIC_TECHNICAL_DISCLOSURE_BUNDLE_v0_1_1.zip.sha256` is published beside the ZIP, not inside it.

Linux/macOS:

```bash
sha256sum --check FORK_PUBLIC_TECHNICAL_DISCLOSURE_BUNDLE_v0_1_1.zip.sha256
```

Windows PowerShell:

```powershell
$expected = (Get-Content .\FORK_PUBLIC_TECHNICAL_DISCLOSURE_BUNDLE_v0_1_1.zip.sha256).Split()[0].ToLower()
$actual = (Get-FileHash .\FORK_PUBLIC_TECHNICAL_DISCLOSURE_BUNDLE_v0_1_1.zip -Algorithm SHA256).Hash.ToLower()
if ($actual -ne $expected) { throw "OUTER_ZIP_SHA256_MISMATCH" }
"OUTER_ZIP_SHA256_PASS"
```

## 1. Extract and run the included verifier

Linux/macOS:

```bash
unzip FORK_PUBLIC_TECHNICAL_DISCLOSURE_BUNDLE_v0_1_1.zip
cd FORK_PUBLIC_DISCLOSURE_v0_1_1
python3 verify_public_disclosure.py
```

Windows PowerShell:

```powershell
Expand-Archive .\FORK_PUBLIC_TECHNICAL_DISCLOSURE_BUNDLE_v0_1_1.zip -DestinationPath .ork_public_v0_1_1 -Force
Set-Location .ork_public_v0_1_1\FORK_PUBLIC_DISCLOSURE_v0_1_1
python .erify_public_disclosure.py
if ($LASTEXITCODE -ne 0) { throw "PUBLIC_DISCLOSURE_VERIFICATION_FAILURE" }
```

Expected terminal conclusion:

```text
FORK_PUBLIC_TECHNICAL_DISCLOSURE_V0_1_1_PASS
GATES_PASS: 9
GATES_NOT_CHECKED: 1
GATES_FAIL: 0
APPEND_ONLY_PERSISTENCE: NOT_CHECKED
RFC3161_REQUEST_RESPONSE_PAIR_PRESENCE: NOT_ESTABLISHED
AGGREGATE_TRUST_VERDICT: NOT_EMITTED
```

## What the verifier checks

- explicit workflow-member eligibility and control-plane exclusion;
- declared-member count and unique member identifiers/filenames;
- no undeclared eligible workflow artifact;
- each member SHA-256 digest;
- canonical manifest digest;
- public test-key HMAC binding;
- granular gate-state counts;
- append-only persistence remains NOT_CHECKED;
- recursive absence of prohibited aggregate verdict fields;
- layered file inventory and recursion-avoidance boundary;
- mechanically reproduced semantic authority non-promotion;
- timestamp metadata presence and unestablished RFC 3161 pair.

## Inventory boundary

`SHA256SUMS.txt` intentionally excludes:

- itself, to avoid self-hash recursion;
- `PUBLIC_DISCLOSURE_MANIFEST_v0_1_1.json`, to avoid a circular manifest/SHA256SUMS dependency.

The public disclosure manifest records the digest of `SHA256SUMS.txt`. The detached outer-ZIP receipt anchors the entire ZIP, including the public disclosure manifest.

## Time semantics

Workflow event timestamps inside the fixture are fixed synthetic times. They are not the disclosure build time. This release records the actual verification and public-disclosure build time as `2026-06-11T18:49:54Z`.

## What successful recomputation establishes

It establishes byte identity and declared structural relationships for the published synthetic fixture under the declared method.

## What it does not establish

It does not establish source truth, workflow completeness, append-only persistence, RFC 3161 validation, independent time of existence, signer identity, non-repudiation, legal admissibility, compliance, third-party independence, live institutional deployment, or production readiness.
