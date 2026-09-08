# When the Result Is Reproducible but the Evidence Isn’t

## Why AI-Assisted Work Needs Recomputable Evidence

AI can generate outputs that are easier to verify than the conditions under which people later rely on them. We need evidence systems that preserve not only what was produced, but what the surviving record can—and cannot—establish.

Something remarkable happened in mathematics this week.

OpenAI published what it describes as a solution to the Navier–Stokes Millennium Prize Problem, together with a written proof and a Lean formalization. The company says an internal model, used through a large coordinated multi-agent effort, produced the result. OpenAI’s published account says the effort began on September 1, reached its proposed Navier–Stokes result on September 5, and completed Lean formalization and verification on September 6.

At almost the same time, a dispute emerged around related work by mathematicians Tristan Buckmaster and Levent Alpöge. Public reporting describes allegations, denials, questions about priority and possible influence, and disagreement about how the relevant work and contributions should be represented. OpenAI denies using the researchers’ prompts, models, or proof. External mathematical and historical assessment is still unfolding.

It is tempting to call all of this one controversy.

It is not.

A mathematical result can be correct while questions about its history remain unresolved. A result can be formally checked without establishing who had access to what. Priority can be acknowledged without proving derivation. The absence of recorded direct access does not establish the absence of every possible prior influence. And a dispute about attribution is not the same question as a dispute about mathematical validity.

AI is beginning to produce outputs that may be easier to verify than the conditions under which others should rely on the claims surrounding them.

That is an evidence problem.

## A verified result has a boundary

OpenAI’s own account illustrates the distinction unusually clearly.

The company says neither its researchers nor its agents saw Buckmaster and Alpöge’s work before it was publicly released, and that no specific user data was accessed to solve the problem.

OpenAI then adds an important qualification: while it considers the possibility unlikely, it says it cannot rule out that de-identified data derived from the researchers’ use of OpenAI products helped improve its models.

Those two statements preserve a boundary that public discussion can easily erase:

```text
NO SPECIFIC WORK ACCESSED
≠
NO POSSIBLE HISTORICAL INFLUENCE
```

But the converse matters just as much:

```text
POSSIBLE HISTORICAL INFLUENCE
≠
DERIVATION ESTABLISHED
```

Neither proposition should be promoted into the other.

This is not a reason to decide the controversy for or against any participant. It is a reason to recognize that “independent” has become too imprecise a category for AI-assisted discovery.

We may need to distinguish execution independence, retrieval independence, prompt independence, human-access independence, model-history independence, and contribution independence.

Those questions are related. They are not identical.

## Reproducibility is necessary

Scientific reproducibility asks whether another investigator can reproduce or verify a result. That remains indispensable.

But a formally checked proof answers a bounded question. It may establish that a formalized sequence follows within a particular system under its encoded assumptions. It does not automatically establish:

- Who first obtained the underlying result.
- What information was available during production.
- What information was actually consumed.
- Whether model capability was affected by earlier interactions.
- Which human contributions materially shaped the work.
- What reviewers knew before evaluating it.
- Whether later claims are entitled to inherit the proof’s standing.

The distinction is simple:

```text
VERIFIED OUTPUT
≠
VERIFIED CONDITIONS OF RELIANCE
```

The same structure appears well beyond mathematics.

Consider AI retrieval. A source exists. A model retrieves it. The model produces a fluent statement with a citation. Everything can look healthy.

Yet the cited source may support only part of the resulting claim. Another system may consume the generated description and repeat it. A third may encounter several versions of the same interpretation and report apparent agreement.

An initially weak proposition can begin to look established without any new independent evidence entering the chain.

**Coherence is not lineage. Citation is not entailment. Repetition is not additional evidence.**

Or consider evaluation. Two reviewers can receive the same artifact and the same rubric while occupying different informational states. One may have seen identities, previous scores, debate, or an expected conclusion. The other may not have.

Those are not necessarily equivalent evidentiary executions.

Or consider audit trails. A system can perfectly preserve every record it received. Its hashes can verify. Its signatures can validate. Its replay can reproduce byte-for-byte.

None of that establishes that every relevant event entered the system in the first place:

```text
ALL CAPTURED RECORDS PRESERVED
≠
ALL RELEVANT EVENTS CAPTURED
```

A trustworthy evidence system therefore has to preserve not only what it knows. It has to preserve what it does not know.

## What Recomputable Evidence changes

Recomputable Evidence begins from a narrower proposition than “AI governance.” It does not try to become an oracle.

It asks whether enough bounded evidence can survive an AI-assisted workflow that another party can later independently inspect, replay where applicable, and recompute what the surviving record supports—and, just as importantly, what it does not.

That makes “recomputable” operational rather than aspirational.

A reviewer should be able to:

- Inspect preserved artifacts, event populations, claims, and stated boundaries.
- Replay a recorded procedure where the subject is replayable.
- Recompute a stated verification or narrowly scoped conclusion.
- Refuse promotion when necessary premises, observations, or authority are absent.

A bounded recomputation can therefore succeed while a larger question remains unresolved:

```text
RECOMPUTATION OF A RESULT
≠
RECONSTRUCTION OF EVERY CONDITION RELEVANT TO RELIANCE
```

Imagine that an AI-assisted scientific workflow produced a record like this:

```text
EVENT
AI_PROOF_GENERATION_017

INPUT
prompt_digest: 91f...
model_identity: recorded
external_context: none declared
execution_time: T1

OUTPUT
proof_digest: a82...

HUMAN CLAIM
"Produced independently of Researcher A's proof"

CLAIM STANDING
CLAIMED — NOT INDEPENDENTLY ESTABLISHED

OBSERVATION
No Researcher-A artifact recorded as loaded during execution.

NON-IMPLICATION
NO_RECORDED_ARTIFACT_ACCESS
    does not establish
NO_PRIOR_MODEL_INFLUENCE

MISSINGNESS
Training / post-training causal provenance unavailable.

VERIFICATION
Formal proof checker: PASS

RESULT
Mathematical verification preserved.
Independence question remains partially unresolved.
```

Nothing mysterious is happening there.

The record does not ask us to trust an AI. It does not decide who deserves credit. It does not determine whether anyone behaved ethically. It does not manufacture missing model history.

It keeps several propositions separate enough that a later reader cannot legitimately turn “no artifact was recorded as loaded” into “no prior influence was possible.”

> **The unresolved status is not an embarrassment. It is the point.**

## Preservation without inheritance

Information acquires authority remarkably easily when it moves.

An upstream system reports that an action was authorized. A downstream record preserves that statement. A later system consumes the record.

Soon the distinction between “the upstream system reported authorization” and “this artifact authorizes the action” can disappear.

Nothing necessarily failed locally. The failure occurred at the seam.

Recomputable Evidence therefore requires a deceptively simple rule:

```text
PRESERVATION DOES NOT CONFER INHERITANCE
```

A signature establishes certain properties of a signature. A hash establishes certain properties of bytes. A replay establishes certain properties of an execution. A citation establishes that something was cited.

None automatically establishes the truth, authority, completeness, semantic correctness, or continued standing of the underlying proposition.

That is why this is not merely another audit log.


**Intellectual lineage.** The Fork formulation used here derives from and applies Peter Kahl’s prior framework concerning distribution versus answerability, representational sealing, durable-record overread, and semantic promotion. See Peter Kahl, *Distribution Is Not Answerability: Automated Discretion, the Distributive Turn, and the Rule-of-Law Check* (Lex et Ratio Ltd Working Paper LXR-POL-ANSWGAP-2026-01, v1.0, 25 June 2026), DOI 10.5281/zenodo.20847114, and *The Inside of Generatedness: Representational Sealing and the Materials of Temporal Order* (23 May 2026), DOI 10.5281/zenodo.20353457. A later four-step Semantic Promotion / Seal Self-Authentication pressure test applying this territory to Fork was co-developed by Peter Kahl and Ryan Feller. This attribution does not imply Kahl’s endorsement of Fork, NGAST, or any implementation, and does not make Kahl a co-author of this article.

## Fork in practice

Fork is being developed through bounded experimental artifacts rather than broad assurance claims. One public example is the **Boundary-State Interoperability Human Recomputation Sandbox v0.1.1**, which provides a preserved evidence packet, an executable recomputation path, reviewer instructions, and explicit non-claims.

Its public runner extracts the evidence package and nested checker, reruns the canonical, adversarial, and reviewer-regression suites, and writes fresh local receipts. A filed exterior report separately records integrity verification of the supplied artifacts and successful reproduction of the shipped structural results under its stated environment and commands, including comparison with packaged receipts. The same report also records newly constructed bypass and false-positive cases for further triage.

The standing belongs to that artifact and those procedures—not to Fork generally. A successful rerun supports only the bounded claim that the structural procedure reproduced under the stated conditions. It does not establish truth, compliance, safety, production readiness, reliance sufficiency, adversarial exhaustiveness, reviewer endorsement, or authority.

Public recomputation package:  
https://github.com/RecomputableEvidence/fork-public-evidence/tree/fd93d051235ec43bee925878bc916d09179b3c90/docs/recomputation/boundary-state-interop-v0.1.1

Exterior recomputation record:  
https://github.com/RecomputableEvidence/fork-public-evidence/blob/fd93d051235ec43bee925878bc916d09179b3c90/docs/recomputation/boundary-state-interop-v0.1.1/exterior-receipts/INDEPENDENT_VERIFICATION_REPORT_v0_1_1.md

The filed exterior report records **87 of 87** top-level evidence-packet checksum checks, **18 of 18** canonical cases, **15 of 15** adversarial cases, and **1 of 1** reviewer-regression case reproducing. It reports the three suite outputs as byte-identical to their packaged receipts. The same report also records **five constructed paraphrase bypasses** and **four false-positive over-rejections** for further triage.

That is not a contradiction. It is the point: **a bounded procedure can reproduce as specified while further examination identifies limits that the shipped procedure did not establish or detect.**

The relevance is not that one sandbox settled the question of trustworthy AI. It is that the evidence process preserved both outcomes at once: the packaged structural result reproduced under a defined procedure, and additional testing exposed cases the package did not adequately cover.

## The larger problem

The Navier–Stokes episode may ultimately matter for reasons beyond the present dispute.

Suppose OpenAI’s claimed proof survives extensive mathematical scrutiny. Suppose the competing accounts are clarified. Suppose everyone involved acted substantially in good faith.

A deeper infrastructure problem remains.

Frontier AI systems have developmental histories far more complex than the provenance model traditionally assumed for a human investigator. A model may generate a result at time `T_5` using capabilities affected by training, post-training, evaluations, interaction data, tool access, and model transitions occurring across `T_0` through `T_4`.

The model cannot simply introspect that causal history for us.

And a perfectly reproducible `T_5` output does not reconstruct it.

The next major AI-assisted discovery may be correct. Its proof may reproduce. Its formal verification may pass. Its artifacts may be perfectly preserved.

And years later, we may still be unable to establish what information was available, what influenced the model, which human contributions mattered, what evaluators actually knew, whether the surviving record was complete, or which later claims acquired standing they never earned.

That is not principally a model-performance problem. It is an evidence-infrastructure problem.

We already know how to preserve outputs. The harder task is preserving the conditions under which those outputs may later be relied upon—and preserving, with equal fidelity, the boundary beyond which the evidence cannot speak.

**Recomputable Evidence is not infrastructure for converting uncertainty into certainty. It is infrastructure for preserving the difference between a result that reproduced, a claim that is supported, a claim that is merely asserted, a question that remains open, and a conclusion the surviving evidence cannot justify.**

That is what Recomputable Evidence is for.

## Sources

- OpenAI, “On the Navier–Stokes Millennium Prize Problem”  
  https://openai.com/index/navier-stokes-solution/

- Scientific American, “OpenAI Claims Blockbuster Math Breakthrough Amid Swirl of Controversy”  
  https://www.scientificamerican.com/article/openai-claims-blockbuster-math-breakthrough-amid-swirl-of-controversy/

- Peter Kahl, “Distribution Is Not Answerability: Automated Discretion, the Distributive Turn, and the Rule-of-Law Check” (2026), DOI 10.5281/zenodo.20847114  
  https://doi.org/10.5281/zenodo.20847114

- Peter Kahl, “The Inside of Generatedness: Representational Sealing and the Materials of Temporal Order” (2026), DOI 10.5281/zenodo.20353457  
  https://doi.org/10.5281/zenodo.20353457

- Fork public recomputation package, commit-pinned  
  https://github.com/RecomputableEvidence/fork-public-evidence/tree/fd93d051235ec43bee925878bc916d09179b3c90/docs/recomputation/boundary-state-interop-v0.1.1

- Filed exterior recomputation record, commit-pinned  
  https://github.com/RecomputableEvidence/fork-public-evidence/blob/fd93d051235ec43bee925878bc916d09179b3c90/docs/recomputation/boundary-state-interop-v0.1.1/exterior-receipts/INDEPENDENT_VERIFICATION_REPORT_v0_1_1.md