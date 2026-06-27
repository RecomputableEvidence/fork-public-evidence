# Fork Evidence Boundary Walkthrough v0.1

**Artifact ID:** FORK-EVIDENCE-BOUNDARY-WALKTHROUGH-v0.1-001  
**Related release candidate:** `esal-v0.1-rc6`  

---

## 1. Purpose

This walkthrough explains how Fork evidence-boundary infrastructure can be understood through a concrete AI-assisted workflow.

It is not a product claim, compliance claim, legal sufficiency claim, authorization claim, or external-validity claim.

It shows how claim boundaries can be preserved across a workflow without turning recorded evidence into approval, compliance, or truth.

---

## 2. Example Workflow

Example:

> AI-assisted vendor risk summary

A human team uses an AI system to summarize vendor-risk materials. The organization wants to preserve what happened without treating the AI output, the human review, or the replay result as proof that the decision was correct.

---

## 3. Step-by-Step Evidence Boundary

**Step 1 â€” AI Produces a Summary**

The AI system produces a vendor-risk summary.

Fork records:

- what was requested  
- what the AI produced  
- what input artifacts were referenced  
- what was not claimed  

Fork does **not** claim that the AI summary is true, complete, legally sufficient, compliant, or safe.

**Step 2 â€” Human Reviews and Annotates**

A human reviewer inspects the AI output and adds review notes.

Fork records:

- reviewer identity or role as declared by the workflow  
- review timestamp  
- review notes  
- accepted or rejected claims  
- unresolved unknowns  
- preserved non-claims  

Fork does **not** claim that human review makes the result legally sufficient, compliant, authorized, approved, or correct.

**Step 3 â€” Claim Boundary Is Recorded**

A claim boundary records the scope of what is being asserted.

Example bounded claim:

> The record preserves that this vendor-risk summary was generated, reviewed, and sealed under the stated workflow.

Example non-claims:

- The record does not establish that the vendor is safe.  
- The record does not establish that the decision is legally sufficient.  
- The record does not establish that the review was compliant with all applicable policies.  
- The record does not establish that the underlying facts are true.

**Step 4 â€” BDR Records Boundary Transition**

A Boundary Delta Record can capture a transition between evidence contexts.

Fork preserves:

- what changed  
- what was preserved  
- what narrowed  
- what expanded  
- what became unresolved  
- what evidence references were carried forward  

Fork does not allow authority, compliance, approval, or external validity to silently transfer merely because an adjacent record exists.

**Step 5 â€” ESAL Replays Events and Fingerprints State**

ESAL consumes events and reconstructs state under ESAL v0.1 reference-oracle rules.

ESAL can produce:

- classification  
- reduced state  
- fingerprint  
- replay evidence  

ESAL does **not** determine whether the vendor decision was correct, approved, compliant, legally sufficient, authorized in the world, or externally governance-valid.

**Step 6 â€” Release Gate States What Verified**

The release gate records that the ESAL v0.1 reference-oracle release candidate has a closed review chain, stable verification distribution, stable permutation-invariance evidence, explicit commit-role metadata, and explicit non-claims.

The release gate does **not** make the underlying workflow externally valid.

---

## 4. What Fork Preserves

Fork preserves evidence about:

- requests  
- outputs  
- reviews  
- boundaries  
- transitions  
- non-claims  
- evidence references  
- replay classifications  
- fingerprints  

Fork helps show what was claimed, what was not claimed, and whether the recorded trace still verifies under stated oracle rules.

---

## 5. What Fork Does Not Decide

Fork does **not** decide:

- whether the business decision was right  
- whether the output was true  
- whether the action was legally sufficient  
- whether the workflow was compliant  
- whether a person had real-world authority  
- whether an organization should approve the result  
- whether a vendor is safe  
- whether the process satisfies a regulator  
- whether the evidence is externally governance-valid  

This list is illustrative, not exhaustive.

---

## 6. Buyer-Facing Line

Fork does not tell you the decision was right. It preserves what was claimed, what was not claimed, what evidence was referenced, and whether the recorded trace still verifies under the stated oracle rules.

---

## 7. Boundary Principle

The central boundary is:

- Evidence may be preserved.  
- Replay may be verified.  
- Claims may be bounded.  
- Authority does not silently transfer.  
- External validity is not inherited.

This is the bridge between the technical oracle and the governance value of Fork.
