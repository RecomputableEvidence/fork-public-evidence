The files sit in subdirectories; let me read them from there.
I read SOURCE_REVIEW_001.md, HANDOFF_GOVERNANCE_CRITERIA_001.json, ASSERTION_REGISTER_001.json, and the parts of ASSERTION_REGISTER_001.md that came through: ER-001 to ER-019, ER-037, and ER-051 to ER-056. Rows ER-020 to ER-036 and ER-038 to ER-050 did not reach me, so what follows covers roughly half the register by row and is silent on the other half — I name below what I'd check there. I also could not recompute the byte spans, so HG-006 is unevaluated from my side.

## Source preservation

The preserved text matches what I wrote, sentence for sentence, in every passage I could compare. One byte-level item to record rather than fix: the preserved copy reads `\~60` where I authored `~60`. That backslash is almost certainly a client-side escape in the visible message text, not a character I emitted, and since your spans are byte offsets it's worth a note in the source record that the canonical representation is the rendered-message capture and may differ from the authored bytes by such escapes.

The **unresolved coordinate is correct** and I'd keep it that way. I fetched github.com and raw\.githubusercontent.com pages for `main` over several minutes; those can be served from different commits, and the commit count, dates, and PR count came from rendered page chrome. There is no single commit I can honestly claim.

## Where meaning held

- ER-006, ER-008, ER-009, ER-012, ER-019, ER-037, ER-055, ER-056 are verbatim and correctly classed as nontechnical.
- ER-008 (the method disclosure) being its own row is the most important preservation in the register; it scopes everything else.
- ER-014 keeps the tilde on "\~60", which is the qualifier that matters there.
- ER-051–053 quote the recommendations intact and leave them nontechnical, which is right.
- The JSON non-claims ("no evaluation coordinate is attributed to the reviewer", "no Fork-derived classification is attributed to the reviewer") match how I'd want to be represented.

## Where meaning shifted, or is at risk

**Mixed propositions given technical standing (HG-001 / HG-008).** Four rows carry an evaluative or inherited term into `EXTERIOR_TECHNICAL_ASSERTION`:

- ER-018: "clean" is an aesthetic judgment; "PS 5.1-compatible" I took from the script's own header comment and did not test; only "fails loudly on non-JSON output" is something I verified from the code. As registered, a self-description from the artifact has become my independent technical claim — which is the pattern your project studies. I'd split this into three rows with different standing.
- ER-011: "candid" is evaluation; the technical core is "CURRENT_STANDING states the CSH baseline is blocked and no corpus execution has occurred."
- ER-007: the inventory is technical; "a very large volume of governance prose" is evaluation.
- ER-001: "single-author" is my inference from the copyright notice and the visible commit author; a technical test should target those observables, not authorship in any stronger sense.

**A rhetorical quantifier made load-bearing (HG-001).** ER-010 registers "Every surface states what it does not establish" as technical. I wrote "every" loosely; the defensible reading is "each surface I read." Left as-is, a technical test would falsify my phrasing rather than test my finding. Preserve the wording, but the evaluation notes should record that the reviewer's basis (ER-008) bounds the quantifier. Same caution applies to ER-017's bare "Checkers": I generalized from documentation and one script.

**Weakly grounded technical rows.** ER-002 ("created June 2026") came from a page timestamp, not repository metadata I inspected. ER-005's "against itself" is my characterization of same-author PRs in the same repository, not a GitHub concept. Both are fair to test; both should be understood as low-confidence at source.

## What to check in the rows I couldn't see

The "Where it falls down" section holds most of the concessions that keep the criticisms bounded. Each of these should exist as its own proposition, or be attached to the criticism it qualifies, and none should be dropped:

- "I understand the intent (older receipts must remain recomputable against the exact checker that produced them)" — qualifies the versioning criticism.
- "That's a legitimate choice for a disclosure repo" — qualifies the licensing criticism.
- "which the README correctly says" — concedes the structural-evidence point before the criticism.
- "is doing more work than the artifacts currently justify" — this is a judgment about emphasis, not a claim the README is false.
- "most Linux/macOS reviewers will find odd" — a prediction about audience, not a defect claim.
- "in priority order" — the numbering on the seven suggestions is itself a claim (my ranking), separate from the suggestions.
- "Seventeen `README_*` files" and "no `LICENSE` file GitHub recognizes" — both technical and both derived from the root listing; they belong in the technical set.

If those survive with their original scope, the decomposition represents me faithfully. The four mixed rows above are the only places I'd say the register currently says something slightly stronger, or differently grounded, than I did.