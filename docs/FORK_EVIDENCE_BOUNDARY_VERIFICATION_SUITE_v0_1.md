# Fork Evidence Boundary Verification Suite v0.1



**Artifact ID:** FORK-EVIDENCE-BOUNDARY-VERIFICATION-SUITE-v0.1-001  

**Status:** Documentation  

**Scope:** Reviewer-facing description of the top-level Fork evidence-boundary verification command  

**Primary command:** `tools/Test-ForkEvidenceBoundary.ps1`



---



## 1. Purpose



The Fork Evidence Boundary Verification Suite provides a single top-level command for running the current executable evidence-boundary checks in this repository.



The suite is intentionally narrow.



It does not merge the semantics of the underlying checkers. It orchestrates them and records their results in one machine-readable report.



Current command:



```powershell

.\tools\Test-ForkEvidenceBoundary.ps1

```



Current combined report:



```text

reports/FORK_EVIDENCE_BOUNDARY_REPORT.json

```



---



## 2. Current Verification Surface



The suite currently runs two bounded checks:



| Suite | Script | Expected result | Report |

|---|---|---|---|

| ESAL v0.1 conformance | `tools/Test-EsalConformance.ps1` | `CONFORMANCE_PASS` | `reports/ESAL_v0_1_CONFORMANCE_REPORT.json` |

| BDR / ESAL handoff validation | `tools/Test-BdrEsalHandoff.ps1` | `HANDOFF_VALIDATOR_PASS` | `reports/BDR_ESAL_HANDOFF_VALIDATION_REPORT.json` |

| Fork evidence-boundary orchestration | `tools/Test-ForkEvidenceBoundary.ps1` | `FORK_EVIDENCE_BOUNDARY_PASS` | `reports/FORK_EVIDENCE_BOUNDARY_REPORT.json` |



---



## 3. What the Top-Level Suite Does



`tools/Test-ForkEvidenceBoundary.ps1` performs the following actions:



1. Confirms required repository files are present.

2. Runs the ESAL v0.1 conformance harness.

3. Confirms the ESAL conformance harness emits `CONFORMANCE_PASS`.

4. Confirms the ESAL conformance report records `CONFORMANCE_PASS`.

5. Runs the BDR / ESAL handoff validator.

6. Confirms the handoff validator emits `HANDOFF_VALIDATOR_PASS`.

7. Confirms the handoff validator report records `HANDOFF_VALIDATOR_PASS`.

8. Writes a combined evidence-boundary report.



The top-level suite passes only when all non-skipped child suites pass.



---



## 4. What `FORK_EVIDENCE_BOUNDARY_PASS` Means



`FORK_EVIDENCE_BOUNDARY_PASS` means:



```text

The current ESAL conformance harness passed.

The current BDR / ESAL handoff validator passed.

The top-level orchestration script observed both pass states.

The combined report was written.

```



More specifically:



- ESAL v0.1 reference-oracle conformance matched the expected fixture surface.

- The valid BDR / ESAL handoff example was accepted.

- The invalid authority-inheritance handoff example was rejected.

- The top-level suite preserved the distinction between ESAL conformance and BDR / ESAL handoff validation.



---



## 5. What `FORK_EVIDENCE_BOUNDARY_PASS` Does Not Mean



`FORK_EVIDENCE_BOUNDARY_PASS` does not establish:



- production completeness;

- legal sufficiency;

- compliance sufficiency;

- authorization correctness;

- policy approval;

- endorsement;

- safety;

- truth;

- external governance validity;

- independent implementation convergence;

- BDR truth;

- BDR legal or compliance sufficiency;

- ESAL validation of the underlying BDR transition;

- or that ESAL has become a policy-enforcement engine.



The suite verifies bounded executable evidence behavior only.



---



## 6. Layer Boundaries



The suite preserves the following layer separation:



```text

ESAL conformance

  = reference-oracle expected-output checking



BDR / ESAL handoff validation

  = accepts a bounded handoff and rejects an authority-inheritance attempt



Fork evidence-boundary suite

  = orchestrates both checks without collapsing their semantics

```



The top-level suite must not be interpreted as creating a new authority layer above ESAL or BDR.



---



## 7. Relationship to ESAL



ESAL remains an event-state replay and fingerprint oracle.



The evidence-boundary suite does not change ESAL semantics, fixtures, classifications, fingerprints, or reference-oracle behavior.



The suite only runs the ESAL conformance harness and records whether it passed.



Relevant ESAL files include:



```text

tools/Test-EsalConformance.ps1

reports/ESAL_v0_1_EXPECTED_OUTPUTS.md

reports/ESAL_v0_1_CONFORMANCE_REPORT.json

```



---



## 8. Relationship to BDR / ESAL Handoff



The BDR / ESAL handoff validator checks a narrow contract surface:



```text

A valid BDR-derived ESAL event may be consumed for replay, state reduction, classification, and fingerprinting.

An invalid handoff that attempts authority inheritance must be rejected.

```



The validator does not establish that the underlying BDR is true, sufficient, compliant, approved, authorized, or externally valid.



Relevant handoff files include:



```text

docs/BDR_ESAL_HANDOFF_CONTRACT_v0_1.md

examples/bdr_esal_handoff/valid_vendor_risk_handoff_event.json

examples/bdr_esal_handoff/invalid_authority_inheritance_handoff_event.json

tools/Test-BdrEsalHandoff.ps1

reports/BDR_ESAL_HANDOFF_VALIDATION_REPORT.json

```



---



## 9. Report Structure



The combined report is written to:



```text

reports/FORK_EVIDENCE_BOUNDARY_REPORT.json

```



The report includes:



- artifact identifier;

- generation timestamp;

- git branch;

- git commit;

- overall result;

- suite-level results;

- child-suite report expectations;

- child-suite output excerpts;

- explicit non-claims;

- and issues, if any.



Expected overall result:



```text

FORK_EVIDENCE_BOUNDARY_PASS

```



Failure result:



```text

FORK_EVIDENCE_BOUNDARY_FAIL

```



---



## 10. Reviewer Reproduction



From the repository root:



```powershell

.\tools\Test-ForkEvidenceBoundary.ps1

```



Expected console output includes:



```text

== Fork Evidence Boundary Verification Suite ==



Running suite: ESAL v0.1 conformance

Running suite: BDR / ESAL handoff



== Fork Evidence Boundary Result ==

FORK_EVIDENCE_BOUNDARY_PASS



ESAL v0.1 conformance: PASS

BDR / ESAL handoff: PASS

Report written: reports\FORK_EVIDENCE_BOUNDARY_REPORT.json

```



To inspect the report:



```powershell

Get-Content reports\FORK_EVIDENCE_BOUNDARY_REPORT.json -Raw | ConvertFrom-Json

```



---



## 11. Failure Interpretation



A failure means at least one bounded executable check did not produce its expected result.



A failure does not automatically mean that Fork, BDR, ESAL, or any external governance claim is invalid.



A failure should be interpreted according to the failing layer:



| Failed layer | Meaning |

|---|---|

| ESAL conformance | The ESAL reference-oracle expected-output surface did not reproduce as expected. |

| BDR / ESAL handoff | The handoff validator did not accept the valid example, did not reject the invalid example, or could not detect the expected authority-inheritance attempt. |

| Top-level suite | The orchestrator could not run, observe, parse, or record the expected child-suite result. |



---



## 12. Maintenance Rule



New checks may be added to the top-level suite only if their scope is explicitly bounded.



A new child suite must declare:



1. the command being run;

2. the expected pass token;

3. the expected report path;

4. the exact claim supported by a pass;

5. the explicit non-claims preserved by the check.



No child suite should be added if it silently expands Fork from evidence-boundary verification into approval, certification, compliance determination, safety determination, truth determination, or policy enforcement.



---



## 13. Current Claim Boundary



The current top-level claim is:



> Fork has a top-level evidence-boundary verification suite that runs ESAL v0.1 conformance and BDR / ESAL handoff validation, producing a machine-readable report while preserving the boundary between replay conformance and handoff validation.



This claim is structural and evidentiary only.



It is not a claim of production readiness, legal sufficiency, compliance sufficiency, authorization correctness, safety, truth, approval, endorsement, external governance validity, or independent implementation convergence.



---



## 14. Current Status



As of this document version, the expected successful result is:



```text

FORK_EVIDENCE_BOUNDARY_PASS

```



The suite should be treated as a reproducible evidence-boundary verification command for the current repository surface.
