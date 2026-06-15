# Claim Boundary Placement Layer v0.1

Status: Doctrine / Architecture Layer
Version: v0.1
Parent architecture: AI Governance Mapping System v0.1

## 1. Purpose

The Claim Boundary Placement Layer defines the architectural discipline required before AI-governance systems exchange artifacts.

It answers the placement question:

```text
Before these systems connect,
where does each system sit,
what does each prove,
what does each refuse to claim,
what may be handed off,
and what claims must stop at the boundary?
```

## 2. Core thesis

AI governance cannot be made safe merely by connecting systems.

It requires claim-boundary placement before handoff.

Otherwise interoperability becomes silent claim inheritance.

## 3. What the placement layer is

The Claim Boundary Placement Layer is:

* architectural scaffolding,
* a placement discipline,
* a claim-boundary discipline,
* a system-of-systems composition layer,
* a way to define lanes before artifact movement,
* a method for preventing claim leakage across governance subsystems.

It does not produce evidence itself.

It defines where evidence-producing, evidence-consuming, authority-bearing, and review-bearing systems sit in relation to one another.

## 4. What the placement layer is not

The Claim Boundary Placement Layer is not:

* a product module,
* a runtime control plane,
* a compliance engine,
* a legal authority,
* an audit function,
* a governance standard,
* a replacement for Fork,
* a replacement for adjacent systems.

It is an architectural doctrine that makes safe composition possible.

## 5. Placement problem

Adjacent AI-governance systems often appear compatible because their artifacts can technically move between systems.

The danger is that artifact movement can be mistaken for claim transfer.

Examples:

* A runtime receipt may be mistaken for output correctness.
* A permissioning verdict may be mistaken for later decision correctness.
* A preserved record may be mistaken for legal admissibility.
* A verified packet may be mistaken for compliance satisfaction.
* A historical determination may be mistaken for present-state validity.
* A reconstructable path may be mistaken for determination trustworthiness.

The placement layer prevents those collapses by requiring claim boundaries before handoff.

## 6. Placement questions

For each system, the placement layer asks:

1. What is this system's function?
2. Where does it sit in the governance pipeline?
3. What does it prove?
4. What does it refuse to claim?
5. What artifacts does it emit?
6. What artifacts does it consume?
7. What authority does it have?
8. What authority does it lack?
9. What verification model does it use?
10. What dependencies does it rely on?
11. What unknowns remain?
12. What failures can it surface?
13. What may safely pass downstream?
14. What claims must not transfer?
15. What must be re-verified before any downstream claim is reattached?

## 7. Generic placement lanes

The placement layer can describe systems across governance lanes such as:

| Lane                             | Primary question                                    | Common claim risk                                            |
| -------------------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| Runtime anchoring                | What did the AI produce at runtime?                 | Runtime record becomes output correctness.                   |
| Pre-execution governance         | Should the action be permitted before execution?    | Permissioning becomes later correctness.                     |
| Execution control                | Should execution continue under current conditions? | Continuation logic becomes institutional authority.          |
| Inference telemetry              | What signals existed before output commitment?      | Telemetry becomes truth or reliability.                      |
| Continuation validity            | Did supportability remain intact?                   | Valid continuation becomes final justification.              |
| Admissibility-before-bind        | Can a consequence-bearing path bind?                | Admissibility becomes evidentiary reconstruction.            |
| Authorization-context continuity | Did the authorization basis remain continuous?      | Preserved authority becomes present validity.                |
| Evidence preservation            | What was observed, sealed, and verified?            | Integrity becomes correctness, compliance, or admissibility. |
| Compliance review                | Does the record satisfy a compliance regime?        | Compliance finding becomes universal governance truth.       |
| Audit review                     | Is the record sufficient for audit review?          | Audit sufficiency becomes legal or operational correctness.  |
| Legal interpretation             | What is the legal consequence?                      | Legal conclusion becomes technical verification.             |
| Risk acceptance                  | Who accepts residual risk?                          | Risk acceptance becomes evidence integrity.                  |
| Remediation                      | What corrective action occurred?                    | Remediation becomes proof of original correctness.           |
| Reporting                        | What was disclosed?                                 | Reporting completeness becomes source completeness.          |

## 8. Fork placement

Fork sits in the evidence preservation / evidentiary reconstruction lane.

Fork's native question is:

```text
Can the preserved evidence boundary be independently checked later against what was captured, hashed, referenced, unavailable, not checked, and explicitly not claimed?
```

Fork's native question is not:

```text
Was the AI output correct?
Was the decision correct?
Was the action legally admissible?
Was the workflow compliant?
Was the audit sufficient?
Was the institution authorized?
Should the action have occurred?
```

## 9. Handoff rule

Handoffs move artifacts.

Boundaries control claim inheritance.

A handoff may include:

* hash,
* receipt,
* trace ID,
* manifest,
* policy version,
* authority assertion,
* reviewer action,
* decision state,
* timestamp,
* source reference,
* runtime output,
* external verification pointer,
* non-claims,
* unknowns,
* dependencies.

The handoff does not automatically transfer:

* correctness,
* completeness,
* legality,
* admissibility,
* compliance,
* authority,
* audit sufficiency,
* risk acceptance,
* institutional approval,
* decision justification.

## 10. Minimum placement record

A system is not safely placed until the following are explicit:

* system function,
* pipeline position,
* claims,
* non-claims,
* emitted artifacts,
* consumable artifacts,
* authority boundary,
* verification model,
* safe handoffs,
* prohibited claim inheritance,
* unknowns,
* dependencies,
* failure states.

## 11. Output of placement

The output of this layer is not integration.

The output is a disciplined map that states:

```text
System A proves X.
System A does not prove Y.

System B preserves A-artifact C.
System B may re-verify claim D.
System B must not inherit claims E, F, or G.

Artifact H may pass.
Authority I remains outside both systems.
Unknowns J and K remain visible.
```

Only after that map exists should integration be scoped.

## 12. v0.1 non-claims

This placement layer does not claim:

* formal standard status,
* ecosystem adoption,
* legal sufficiency,
* compliance sufficiency,
* market validation,
* runtime enforcement,
* or production interoperability.

It is a doctrine artifact for claim-safe architecture.