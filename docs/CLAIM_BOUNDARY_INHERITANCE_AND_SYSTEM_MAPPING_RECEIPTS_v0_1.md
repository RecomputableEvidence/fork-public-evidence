
# Claim Boundary Inheritance and System Mapping Receipts v0.1

## Status

This document is a position paper and category-definition artifact.

It defines the evidence-boundary handoff mapping problem and proposed `SYSTEM_MAPPING_RECEIPT` semantics.

It is not, by itself, a claim that all described schema behavior is fully implemented in production.

Illustrative JSON examples in this document are non-canonical unless separately implemented as a published schema, checker, fixture set, and test suite.

## Purpose

AI-assisted governance systems increasingly rely on multi-system handoffs.

One system observes a workflow.

Another system normalizes it.

Another system summarizes it.

Another system routes it.

Another system evaluates it.

Another system produces a report.

Another system archives the result.

Another system exposes it to audit, compliance, legal review, risk review, executive review, or operational review.

At each handoff, claims can change.

A bounded observation can become a conclusion.

A local validation can become an institutional approval.

A schema pass can become a compliance claim.

A human review flag can become legal sufficiency.

A model output can become a source of truth.

An unresolved pointer can become accepted context.

A synthetic dry-run can become perceived production readiness.

The problem is not merely that downstream systems may make bad claims.

The deeper problem is that downstream systems often inherit upstream claims without explicitly recording what was inherited, what was rejected, what remained unresolved, what non-claims traveled, and what was newly asserted.

Fork treats this as a boundary problem.

A claim boundary is not preserved merely because two systems exchanged data.

A claim boundary is preserved only when the receiving system records what it consumed, what it did not consume, what non-claims remained attached, and whether the downstream artifact stayed within the inherited boundary.

This document defines the category of claim boundary inheritance and explains how `SYSTEM_MAPPING_RECEIPT` artifacts can make reported system handoffs inspectable.

## Core Position

Claims do not safely inherit across handoffs by default.

Every handoff is a claim-boundary event.

A downstream system receiving an upstream artifact may perform one or more of the following boundary behaviors:

1. preserve part of the upstream claim boundary;
2. narrow part of the upstream claim boundary;
3. expand beyond part of the upstream claim boundary;
4. reject part of the upstream claim boundary;
5. leave part of the boundary unresolved.

These behaviors are not mutually exclusive.

A single handoff may preserve one claim, narrow another, reject a third, expand a fourth, and leave a fifth unresolved.

The boundary behavior should not be inferred from prose, workflow intent, successful data transport, or system role.

It should be recorded.

Fork’s posture is that system handoffs can be mapped by preserving evidence of the boundary relationship between producer, consumer, artifact, schema, claim, non-claim, pointer, and structural outcome.

## Early Definition: SYSTEM_MAPPING_RECEIPT

A `SYSTEM_MAPPING_RECEIPT` is an evidence-boundary artifact that records how a handoff between systems was represented, consumed, bounded, and structurally mapped.

It does not certify that the handoff was safe, compliant, legally sufficient, operationally authorized, correct, approved, aligned, or true.

It preserves inspectable evidence of how the handoff was represented.

A `SYSTEM_MAPPING_RECEIPT` may record:

* which system produced the upstream artifact;
* which system consumed it;
* which artifact, field, claim, receipt, or pointer was consumed;
* which claims were referenced;
* which claims were reportedly relied upon;
* which claims were reportedly rejected;
* which non-claims were reportedly preserved;
* which non-claims were reportedly dropped;
* which pointers remained unresolved;
* which downstream claims were added;
* whether added claims included authority and evidence references;
* what resolution state those authority and evidence references reached;
* what structural mapping outcomes were emitted;
* where the mapping remains incomplete.

A `SYSTEM_MAPPING_RECEIPT` does not prove that a handoff was correct.

It preserves inspectable evidence of how the handoff was represented, what claims were reportedly consumed, what non-claims reportedly traveled, what expansions were reported or structurally detected, and where the mapping remains incomplete.

## Silent Expansion Disclosure

A `SYSTEM_MAPPING_RECEIPT` makes reported handoff behavior inspectable.

It does not prove that the receiving system accurately characterized its own behavior.

A structurally valid receipt records what the system reported and what the validator could structurally observe from the mapped fields.

It does not verify that the reported behavior accurately describes everything that occurred.

A downstream consumer may negligently or dishonestly self-characterize an expansion as preservation.

Fork does not claim omniscient detection of such behavior.

The value of the receipt is that it creates a reviewable surface where consumer declarations, preserved non-claims, dropped non-claims, unresolved pointers, added claims, authority references, evidence references, and structural outcomes can be inspected.

Silent expansion that is not reported and not structurally observable from the receipt remains outside the claim made by the receipt.

Therefore:

* a receipt is evidence of reported boundary behavior;
* a receipt is not proof of substantive boundary correctness;
* a structurally complete receipt is not proof that the downstream decision was correct;
* a structurally incomplete receipt is evidence that the mapping surface is incomplete.

## Claim Boundary Inheritance

Claim boundary inheritance occurs when a downstream system relies on a claim, artifact, receipt, schema result, model output, human review state, policy reference, or prior workflow record produced upstream.

Inheritance may be explicit or implicit.

Explicit inheritance occurs when a downstream system identifies the upstream claim it is relying on.

Implicit inheritance occurs when a downstream system uses upstream data in a way that makes the upstream claim appear accepted, incorporated, or extended without recording that reliance.

Implicit inheritance is dangerous because it allows transitive meaning to form without inspectable authority.

For example:

* “The record structurally verified” becomes “the decision was valid.”
* “A human reviewed the output” becomes “the output is legally sufficient.”
* “The model cited a policy” becomes “the answer is compliant.”
* “The packet hash matches” becomes “the underlying claim is true.”
* “The upstream system marked the item complete” becomes “the institution approved the result.”
* “The synthetic corpus passed tests” becomes “the workflow is production-ready.”

These are not merely wording mistakes.

They are inheritance failures.

A downstream system has consumed a bounded upstream claim and allowed a broader downstream meaning to emerge.

## Non-Claims as Portable Boundary Constraints

A claim boundary is incomplete if it records only what is claimed.

Every bounded claim carries a shadow surface: the things it does not claim.

These non-claims are not disclaimers in the weak sense.

They are part of the boundary.

If an upstream artifact says:

> This receipt verifies structural integrity only.

Then the downstream consumer should not inherit the receipt as evidence of truth, safety, compliance, legal sufficiency, clinical appropriateness, production readiness, or institutional authorization unless those claims are separately made and separately evidenced.

A non-claim should therefore be treated as a portable boundary constraint.

When a downstream system consumes an upstream artifact, the inherited non-claims should remain attached unless the downstream system explicitly records a new claim, identifies its authority, supplies evidence references for the expansion, and records the resolution state of those references.

The safer default is:

> Claims should be consumed only with their non-claims attached.

A system that consumes the claim while dropping the non-claim has not preserved the boundary.

It has created an expansion surface.

## Consumer-Side Responsibility

Most governance artifacts focus on the producer.

Fork also treats the consumer as structurally important.

A producer may emit a bounded artifact correctly.

A consumer may still misuse it.

Therefore, the receiving system should record its own boundary behavior.

The relevant question is not only:

> What did the upstream system claim?

It is also:

> What did the downstream system do with that claim?

Consumer-side responsibility in this document means evidentiary mapping responsibility only.

It does not assign legal responsibility, regulatory accountability, liability, fault, negligence, duty, or institutional blame.

It means that a consumer-side system can be represented as part of the evidentiary handoff chain and can record how it reportedly handled inherited claims and non-claims.

## Schema Behavior Choices

Schemas are not neutral.

A schema determines what kinds of meaning can enter, pass, fail, remain unresolved, or disappear during handoff.

A schema that validates only shape can accidentally endorse semantic expansion.

A schema that permits vague strings can allow boundary mutation.

A schema that uses overloaded enum values can import domain meaning the system does not intend.

A schema that collapses unresolved states into pass/fail output can erase epistemic uncertainty.

A schema that allows missing non-claims can let downstream consumers inherit claims without inherited limits.

Fork-style schema behavior should therefore be designed around boundary preservation, not mere structural convenience.

### Behavior Choice 1 — Default Non-Transitivity

The default schema behavior should be non-transitive.

An upstream claim should not automatically become a downstream claim merely because the downstream record references it.

A downstream record should distinguish:

* referenced claim;
* relied-upon claim;
* rejected claim;
* unresolved claim;
* newly asserted claim.

Reference is not reliance.

Reliance is not endorsement.

Endorsement is not legal sufficiency.

Structural verification is not truth.

### Behavior Choice 2 — Required Non-Claims

A schema should require non-claims when an artifact is likely to be misread.

For example, a receipt involving AI-assisted review may need to state that it does not claim:

* model correctness;
* decision correctness;
* legal sufficiency;
* compliance;
* policy sufficiency;
* human-review adequacy;
* production readiness;
* source truth;
* institutional approval.

These non-claims should be machine-readable where possible.

They should not exist only in a README.

### Behavior Choice 3 — Explicit Structural Outcomes

A schema should avoid overloaded labels where domain readers may import the wrong meaning.

Terms such as `APPROVED`, `VALID`, `PASS`, `FAIL`, `COMPLIANT`, `AUTHORIZED`, `ALIGNED`, or `READY` may appear harmless in generic software contexts.

In governance contexts, they can become claims.

Fork-native structural outcomes should say what structurally happened:

* `BOUNDARY_MAPPING_PRESENT`
* `BOUNDARY_PRESERVED`
* `BOUNDARY_NARROWED`
* `BOUNDARY_EXPANSION_DETECTED`
* `BOUNDARY_EXPANSION_RECORDED`
* `POINTER_UNRESOLVED`
* `CLAIM_REJECTED`
* `NON_CLAIM_DROPPED`
* `AUTHORITY_REF_MISSING`
* `AUTHORITY_REF_SUPPLIED_NOT_VERIFIED`
* `AUTHORITY_REF_UNRESOLVED`
* `AUTHORITY_REF_STRUCTURALLY_VERIFIED`
* `EVIDENCE_REF_MISSING`
* `EVIDENCE_REF_SUPPLIED_NOT_VERIFIED`
* `EVIDENCE_REF_UNRESOLVED`
* `EVIDENCE_REF_STRUCTURALLY_VERIFIED`
* `MAPPING_INCOMPLETE`
* `RECEIPT_STRUCTURALLY_COMPLETE`

These labels do not say whether the underlying claim is true, safe, compliant, legal, approved, aligned, or operationally authorized.

They say how the boundary mapping behaved.

### Behavior Choice 4 — First-Class Unresolved State

Unresolved evidence is not failure, and it is not success.

It is a factual state.

A system that cannot resolve an upstream pointer should preserve that unresolved state rather than collapsing it into a binary result.

If a downstream system converts unresolved evidence into accepted context, it has performed a boundary expansion.

If a dashboard aggregates unresolved records into “passed” totals, it has erased uncertainty.

A schema should therefore make unresolved states explicit and non-collapsible.

### Behavior Choice 5 — Per-Claim Boundary Records

A handoff-level scalar cannot safely represent a multi-claim handoff.

A single handoff may include different boundary behaviors across different claims.

Therefore, a `SYSTEM_MAPPING_RECEIPT` should model boundary behavior at per-claim or per-boundary-record granularity.

A receipt may include an aggregate structural posture, but that aggregate should not erase the per-claim record.

The per-claim record is where boundary behavior is inspectable.

## Authority and Evidence Reference Scope

Fork should remain evidentiary-passive at runtime.

Fork does not block a downstream system, approve a downstream expansion, or adjudicate whether an added claim is substantively valid.

But a schema should not treat a boundary expansion as structurally mapped unless the expansion names:

* the added claim;
* the authority reference asserted for that added claim;
* the evidence references asserted for that added claim;
* the resolution state of the authority reference;
* the resolution state of the evidence references;
* the integrity state of any resolved authority or evidence artifact, where checked.

A populated `authority_ref` does not prove that the referenced authority exists, resolves, verifies, or substantively supports the added claim.

A populated `evidence_refs` array does not prove that the evidence exists, resolves, verifies, or substantively supports the added claim.

The receipt should record the level of resolution actually achieved.

Example authority and evidence states include:

* `MISSING`
* `SUPPLIED_NOT_VERIFIED`
* `UNRESOLVED`
* `RESOLVED`
* `STRUCTURALLY_VERIFIED`
* `NOT_CHECKED`

These states preserve the difference between reference presence and reference verification.

Fork may record:

> The expansion was mapped and an authority reference was supplied.

Fork may also record:

> The expansion was mapped and the referenced authority artifact structurally resolved.

Fork should not claim:

> The expansion was authorized.

## Aggregate Structural Posture

When structural outcomes are represented as a list, the receipt should also carry an aggregate structural posture.

The aggregate posture prevents dashboards or downstream tools from collapsing unresolved or incomplete states into a false success state.

Suggested aggregate posture values include:

* `NO_MAPPING_PRESENT`
* `BOUNDARY_MAPPING_PRESENT`
* `MAPPED_WITH_UNRESOLVED_REFERENCES`
* `INCOMPLETE_MAPPING`
* `RECEIPT_STRUCTURALLY_COMPLETE`

Suggested precedence rules:

1. If no mapping receipt is present where one is expected, the aggregate posture is `NO_MAPPING_PRESENT`.
2. If any required claim, non-claim, authority, or evidence field is missing, the aggregate posture is `INCOMPLETE_MAPPING`.
3. If any authority, evidence, or upstream pointer is supplied but unresolved or not checked, the aggregate posture is `MAPPED_WITH_UNRESOLVED_REFERENCES`.
4. If all required records are present, all non-claim handling is declared, all unresolved pointers are explicitly represented, and all required authority/evidence references structurally resolve where the selected verification mode requires resolution, the aggregate posture may be `RECEIPT_STRUCTURALLY_COMPLETE`.

No aggregate posture claims substantive correctness, legal sufficiency, compliance, safety, clinical appropriateness, production readiness, institutional approval, or truth.

## Illustrative SYSTEM_MAPPING_RECEIPT Shape

The following JSON is illustrative.

It is not a canonical schema.

It demonstrates the repaired direction: per-claim boundary records, consumer self-report separated from validator-observed behavior, authority/evidence resolution states, structural outcomes as a list, aggregate structural posture, schema version, and timestamps.

```json
{
  "receipt_type": "SYSTEM_MAPPING_RECEIPT",
  "schema_id": "system_mapping_receipt_v0_1",
  "schema_version": "0.1",
  "receipt_generated_at": "2026-06-17T00:00:00Z",
  "handoff_observed_at": "2026-06-17T00:00:00Z",
  "producer_system": "UPSTREAM_SYSTEM_IDENTIFIER",
  "consumer_system": "DOWNSTREAM_SYSTEM_IDENTIFIER",
  "handoff_artifact_ref": "ARTIFACT_OR_RECEIPT_POINTER",
  "boundary_behavior_records": [
    {
      "claim_ref": "claim_001",
      "consumer_declared_behavior": "BOUNDARY_PRESERVED",
      "validator_observed_behavior": "BOUNDARY_PRESERVED",
      "referenced_claims": [
        "claim_001"
      ],
      "relied_claims": [
        "claim_001"
      ],
      "rejected_claims": [],
      "consumer_declared_preserved_non_claims": [
        "does_not_claim_truth"
      ],
      "consumer_declared_dropped_non_claims": [],
      "unresolved_pointers": [],
      "consumer_added_claims": []
    },
    {
      "claim_ref": "claim_002",
      "consumer_declared_behavior": "BOUNDARY_PRESERVED",
      "validator_observed_behavior": "BOUNDARY_EXPANSION_DETECTED",
      "referenced_claims": [
        "claim_002"
      ],
      "relied_claims": [
        "claim_002"
      ],
      "rejected_claims": [],
      "consumer_declared_preserved_non_claims": [
        "does_not_claim_legal_sufficiency"
      ],
      "consumer_declared_dropped_non_claims": [],
      "unresolved_pointers": [],
      "consumer_added_claims": [
        {
          "claim": "downstream_legal_sufficiency_claim",
          "authority_ref": "legal_review_record_123",
          "authority_ref_type": "EXTERNAL_RECORD_POINTER",
          "authority_resolution_state": "SUPPLIED_NOT_VERIFIED",
          "authority_integrity_state": "NOT_CHECKED",
          "evidence_refs": [
            "evidence_ref_456"
          ],
          "evidence_resolution_state": "SUPPLIED_NOT_VERIFIED"
        }
      ]
    }
  ],
  "structural_outcomes": [
    "BOUNDARY_MAPPING_PRESENT",
    "BOUNDARY_EXPANSION_DETECTED",
    "AUTHORITY_REF_SUPPLIED_NOT_VERIFIED",
    "EVIDENCE_REF_SUPPLIED_NOT_VERIFIED",
    "MAPPING_INCOMPLETE"
  ],
  "aggregate_structural_posture": "INCOMPLETE_MAPPING"
}
```

## Handoff Boundary Mapping

Handoff boundary mapping is the condition in which the relationship between an upstream artifact and a downstream consumer is made inspectable.

It does not mean the handoff is approved, aligned, correct, compliant, authorized, or safe.

A mapped handoff should show:

* what was received;
* what was referenced;
* what was relied upon;
* what was rejected;
* what non-claims were reportedly preserved;
* what non-claims were reportedly dropped;
* what remained unresolved;
* what was newly claimed;
* what authority reference was supplied for new claims;
* what evidence references were supplied for new claims;
* whether those references resolved or structurally verified;
* which structural outcomes were emitted;
* which aggregate posture applies.

A handoff is not mapped merely because data transferred successfully.

Transport success is not boundary preservation.

## Boundary Expansion

Boundary expansion occurs when a downstream system asserts more than the upstream artifact supported.

Boundary expansion is not always wrong.

Some expansions are legitimate.

A legal reviewer may add a legal conclusion.

A clinician may add a clinical judgment.

A compliance officer may add a compliance determination.

A risk officer may add an operational risk classification.

A production owner may add deployment authorization.

But those expansions require their own authority and evidence references.

Fork’s concern is not that expansions exist.

Fork’s concern is unmapped expansion.

The correct behavior is not to ban expansion.

The correct behavior is to make expansion visible and to distinguish:

* expansion with authority and evidence references missing;
* expansion with authority and evidence references supplied but not checked;
* expansion with authority and evidence references unresolved;
* expansion with authority and evidence artifacts structurally verified;
* expansion that remains substantively unverified by Fork.

## Boundary Narrowing

Boundary narrowing occurs when a downstream system uses only part of an upstream claim.

This can be appropriate.

For example, an upstream packet may preserve a full workflow trace, while a downstream audit summary relies only on the timestamp, hash, reviewer identity, and artifact pointer.

That downstream summary should not imply that it consumed or validated the whole packet.

A narrowed handoff should identify the subset consumed and preserve or explicitly account for the non-claims applicable to that subset.

Boundary narrowing is often safer than boundary expansion, but it still needs to be recorded.

A narrowed claim without recorded scope can later be mistaken for a full inherited claim.

## Boundary Rejection

Boundary rejection occurs when a downstream system declines to rely on an upstream claim.

Rejection should also be recorded.

A rejected claim may still be part of the evidentiary record.

The record should show that the downstream system saw the upstream artifact but did not rely on it.

This prevents later reviewers from assuming that because an artifact was present, it was consumed as support.

Presence is not reliance.

## Claim Consumption Events

Claim Consumption Event is a related future or companion artifact.

It can be used to record a consumer’s reliance on a specific claim.

This document does not define the full Claim Consumption Event schema.

For purposes of this document:

* a Claim Consumption Event may answer: “What claim did this consumer rely on?”
* a `SYSTEM_MAPPING_RECEIPT` may answer: “How did this system handoff preserve, narrow, expand, reject, or leave unresolved the inherited boundary?”

The two concepts are related but not identical.

A future specification may define how Claim Consumption Events attach to or reference `SYSTEM_MAPPING_RECEIPT` records.

## Category: Evidence-Boundary Handoff Mapping

The category forming here is not AI audit logs.

It is not compliance automation.

It is not workflow observability.

It is not model governance.

It is not data lineage in the ordinary sense.

The category is evidence-boundary handoff mapping.

Evidence-boundary handoff mapping asks:

> When one system hands an AI-assisted governance artifact to another system, what claim boundary crossed the handoff, what non-claims crossed with it, what did the receiving system reportedly do to that boundary, and what can the mapping structurally show or not show?

This category matters because modern AI-assisted workflows are not single-system events.

They are chains.

A claim may begin as a bounded observation, pass through summarization, routing, policy mapping, human review, dashboard aggregation, export, archive, and later investigation.

The risk is not only that a model makes an unsupported statement.

The risk is that a system chain makes unsupported inheritance appear normal.

Fork’s role is to preserve evidence of those boundary transitions without converting the receipt into a substantive approval artifact.

## Practical Handoff Questions

A reviewer examining a system handoff should be able to ask:

* What did the upstream artifact actually claim?
* What did it explicitly not claim?
* Which downstream system consumed it?
* Did the downstream system rely on the claim or merely reference it?
* Were the non-claims reportedly preserved?
* Were any non-claims reportedly dropped?
* Did the downstream system add a new claim?
* Was that new claim accompanied by authority and evidence references?
* Did those references resolve?
* Did those references structurally verify?
* Did any pointer remain unresolved?
* Did the schema collapse unresolved state into success?
* Did the output label import domain meaning?
* Could a hurried reviewer mistake the structural outcome for substantive approval?
* Does the receipt distinguish reported behavior from structurally observed behavior?
* Does the aggregate structural posture preserve incomplete and unresolved states?

If these questions cannot be answered from the record, the handoff is not fully mapped.

## Non-Claims

This document does not claim that mapping a handoff proves the downstream decision was correct.

It does not claim that a `SYSTEM_MAPPING_RECEIPT` proves the receiving system accurately characterized its own behavior.

It does not claim that a structurally complete receipt proves substantive boundary correctness.

It does not claim that preserved boundaries establish legal sufficiency, compliance, safety, clinical appropriateness, policy adequacy, production readiness, institutional approval, or truth.

It does not claim that every downstream expansion is invalid.

It does not claim that an authority reference proves authority.

It does not claim that an evidence reference proves evidentiary sufficiency.

It does not claim that externally referenced authority or evidence artifacts exist, resolve, structurally verify, or substantively support the added claim unless those states are separately recorded.

It does not claim that schemas can prevent every misuse.

It does not assign legal responsibility, regulatory accountability, liability, fault, negligence, or duty to any consumer system or institution.

It claims only that claim inheritance across AI-assisted system handoffs can be made more inspectable when claims, non-claims, schema behavior, unresolved pointers, consumer declarations, authority references, evidence references, and downstream boundary effects are explicitly recorded.

## Conclusion

The next phase of AI governance will not be solved by asking whether a single model output was logged.

The harder problem is whether the institutional chain can show what happened to a claim as it moved.

Did the claim remain bounded?

Did the non-claims travel with it?

Did a receiving system expand it?

Was the expansion reported?

Was the expansion accompanied by authority and evidence references?

Did those references resolve?

Were unresolved states preserved?

Did schema behavior force ambiguity into a false binary?

Can a later reviewer reconstruct the handoff without inheriting claims no one actually made?

Claim boundary inheritance is the name for this problem.

Evidence-boundary handoff mapping is the category.

`SYSTEM_MAPPING_RECEIPT` is one way to make the reported handoff boundary inspectable.

Fork’s position is that system handoffs should not rely on assumed transitivity.

They should produce evidence of boundary behavior.

