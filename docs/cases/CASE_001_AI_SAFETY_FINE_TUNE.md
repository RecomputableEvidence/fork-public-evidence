# Case 001: AI Safety Evaluation → Fine-Tuned Derivative Model

## Case Status

- Purpose: Calibration case for Transition Localization procedure execution.
- Status: Draft complete — ready for reviewer execution test.

## Case Purpose

This case is a calibration exercise for the Transition Localization procedure.  
It examines whether a property claim established for one artifact state has a traceable transition path into a changed artifact state.  
This case evaluates only the localization of the authority path.

This case does not determine:

- whether the destination artifact is safe,
- whether the transformation is acceptable,
- whether the property persists,
- whether deployment is appropriate,
- or whether the destination artifact should be trusted.

The analysis concerns only:

- Establishment Event → Transition → Transfer Mechanism → Determination → Classification

## Non-Generalization Statement

This case does not classify fine-tuning transitions categorically.  
The classification applies only to the specific transition described:

- A fine-tuned derivative artifact is claiming applicability of a prior safety evaluation without an identified preservation mechanism, authorized transfer mechanism, or new establishment event.

This case does not establish:

- “fine-tuning always invalidates prior evaluations,” or
- “fine-tuned systems cannot inherit prior properties.”

A different transition with a different mechanism may produce a different classification.

## Domain

- AI model evaluation and fine-tuning.

## Artifact

### Source Artifact / State

**Artifact:**  
General-purpose large language model: Model X — Version V1.

Model X V1 was evaluated through an internal safety evaluation process.  
The evaluation considered:

- model behavior,
- safety properties,
- documented limitations,
- intended use conditions.

### Destination Artifact / State

**Artifact:**  
Fine-tuned derivative model: Model X-FT — Version V2.

Model X-FT was created through:

- supervised instruction fine-tuning,
- domain-specific training data,
- updated parameter state.

The resulting model is deployed within a customer support agent system.  
The deployment context includes:

- customer-facing workflows,
- system prompts,
- orchestration logic,
- possible external tool access.

## Claimed Authority

### Original Property Claim

**Claim:**  
Model X V1 satisfies Safety Protocol Y under specified evaluation conditions.  

The claim was established through an evaluation event applied to Model X V1.

### Destination Applicability Claim

**Claim being examined:**  
The safety evaluation results established for Model X V1 apply to Model X-FT V2 in the customer support agent context.

This case examines the authority path supporting that transition claim.

## Evidence Artifacts

Evidence artifacts include:

### Safety Evaluation Report

A report describing:

- execution of Safety Protocol Y,
- evaluation methodology,
- tested scenarios,
- observed results,
- limitations.

### Model Safety Card

A summary artifact describing:

- evaluated properties,
- intended uses,
- known limitations.

### Fine-Tuning Report

A record describing:

- training data,
- training configuration,
- checkpoints,
- transformation process.

### Evidence Boundary Note

Evidence artifacts record or reference events.  
They are not themselves assumed to be the establishment event.  
A report describing an evaluation does not automatically create authority unless the underlying establishment event is identified.

## Establishment Event

### Identified Establishment Event

**Event:**  
Execution of Safety Protocol Y against Model X V1.

**Authority:**  
Internal safety evaluation team operating under organizational evaluation procedures.

**Artifact State:**  
Model X V1 with:

- specific model parameters,
- architecture,
- configuration,
- evaluation environment.

### Scope

The establishment event applies within:

- Safety Protocol Y test conditions,
- evaluated prompt/task categories,
- documented deployment assumptions,
- stated limitations.

### Conditions

Conditions include:

- tested input distributions,
- red-team scenarios,
- evaluation methodology,
- operational constraints.

### Evidence References

Referenced evidence:

- Safety Protocol Y evaluation report.
- Model X V1 safety documentation.

### Establishment Localization Statement

The evaluated safety property is localized to:

- Model X V1 under Safety Protocol Y and its specified conditions.

## Transition Under Examination

### Source

Model X V1 as evaluated under Safety Protocol Y.

### Destination

Model X-FT V2 deployed in a customer support agent context.

### Property Attempting to Transfer

**Claim:**  
Safety evaluation results established for Model X V1 apply to Model X-FT V2.

## Boundary Inventory

A transition may cross multiple boundary categories.  
Boundary categories are descriptive and may overlap.

### Primary Boundary Crossed

**Identity**  
Changed.  
Model X-FT V2 is a derivative artifact with a distinct model state.

### Additional Boundaries

**State**  
Changed.  
Changes include:

- updated parameters,
- fine-tuning process,
- different training data distribution.

**Scope**  
Partially changed.  

Original scope:

- general-purpose text interactions under Safety Protocol Y.

Destination scope:

- customer support workflows,
- agent integration,
- additional operational context.

**Composition**  
Unchanged for this case.  
This case does not evaluate multi-model composition.

**Temporal**  
Not primary.  
Assume evaluation and deployment occur within a limited time period.  
Temporal drift is not the focus of this case.

## Assumptions Required

For the original property claim to apply to Model X-FT V2, the following assumptions would be required.

### Assumption A1

The fine-tuning process preserves relevant safety properties established for Model X V1.

Classification:

- Established mechanism
- Explicit governance rule
- Unverified assumption

### Assumption A2

Parameter changes and new training data do not materially affect behaviors evaluated under Safety Protocol Y.

Classification:

- Established mechanism
- Explicit governance rule
- Unverified assumption

### Assumption A3

Integration into the customer support agent context does not introduce behavior outside the original evaluation scope.

Classification:

- Established mechanism
- Explicit governance rule
- Unverified assumption

### Assumption Summary

These assumptions may or may not be reasonable.  
This procedure does not evaluate their desirability.  

The procedure asks:

- What mechanism converts these assumptions into an authorized transition?

## Transition Determination

### Preservation Analysis

**Question:**  
Does the original establishment remain applicable without a boundary change?

**Result:**  

- Yes
- No
- Unclear

**Rationale:**  
The evaluated artifact state changed:

- V1 → V2 identity change.
- Parameter state change.
- Deployment context change.

No preservation mechanism was identified that keeps the original establishment applicable without transition.

### Authorized Transfer Analysis

**Question:**  
Does an explicit transfer authorization mechanism define applicability in the new context?

**Examples:**

- governance rule,
- contract,
- policy,
- validated transfer procedure.

**Result:**  

- Yes
- No
- Unclear

**Transfer mechanism identified:**  
None within the reviewed transition context.

### New Establishment Analysis

**Question:**  
Was a new establishment event created for Model X-FT V2?

**Result:**  

- Yes
- No
- Unclear

**New establishment identified:**  
None.  
Fine-tuning records document transformation activity but do not establish the safety property for V2.

### Determination Path

Based on the analysis:

- Preservation path: No.
- Governed transfer path: No.
- New establishment path: No.

**Determination:**

- Preservation path  
- Governed transfer path  
- New establishment path  
- Unlocalized path  

## Transition Localization Classification

### Classification

**Class D — Unlocalized transfer path**

### Classification Basis

The assigned classification is based on:

- **Identified Establishment Event**  
  Execution of Safety Protocol Y against Model X V1.
- **Examined Transition**  
  Transfer of the safety evaluation property claim from Model X V1 to Model X-FT V2.
- **Boundary Crossed**  
  - Primary: Identity  
  - Additional: State, Scope
- **Transfer Mechanism Present**  
  No preservation mechanism, explicit transfer authorization mechanism, or new establishment event was identified within the reviewed transition context.
- **Determination Path Selected**  
  Unlocalized path.

### Classification Rationale

The original property claim was established for Model X V1 under defined conditions.  
The transition to Model X-FT V2 changes artifact identity and state.  

No mechanism was identified that:

- preserves the original establishment,
- authorizes transfer,
- or establishes the property independently for V2.

Therefore, the authority path for applying the property claim to V2 is unlocalized.

## Reviewer Disagreement Boundary

Reviewers may disagree about:

- whether Model X-FT V2 retains the safety property,
- whether fine-tuning is acceptable,
- whether deployment is appropriate,
- whether the property is important.

Such disagreement does not affect transition localization unless it changes:

- the identified establishment event,
- the transition being examined,
- or the existence of a transfer mechanism.

This case evaluates authority-path localization, not artifact judgment.

## Potential Transition Resolution

The classification could change if a mechanism were introduced.

**Examples:**

### Class B Candidate

A validated transformation process establishes:

- permitted fine-tuning methods,
- evaluation requirements,
- equivalence criteria,
- validation boundaries.

### Class C Candidate

A governance mechanism explicitly authorizes transfer:

- defined fine-tuning categories,
- required controls,
- documented applicability rules.

This case identifies a mechanism gap, not a permanent prohibition.

## Bounded Conclusion

The establishment event for the evaluated safety property was localized to Model X version V1 under Safety Protocol Y and its specified conditions.  
The examined transition from Model X V1 to the fine-tuned derivative Model X-FT V2 identified no preservation mechanism, authorized transfer mechanism, or new establishment event for application of the safety evaluation property to the destination state.  

The transition is therefore classified as:

- **Class D — Unlocalized transfer path.**

## Localization Confidence

- Mechanism identified  
- Mechanism explicitly absent in the reviewed transition context  
- Information insufficient to determine  

**Rationale:**  
No preservation mechanism, transfer authorization mechanism, or new establishment event was identified in the case materials.

## Invariant Check

- Establishment event identified  
- Evidence artifacts distinguished from establishment event  
- Transition under examination defined  
- Boundary inventory completed  
- Assumptions catalogued  
- Mechanism analysis completed  
- Determination path selected  
- Classification assigned from authority path  
- No conclusion made about safety, risk, legality, or deployment suitability