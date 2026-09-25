**Worked for 2m 17s · 12 steps**svg

svgRan cd /home/user/fork-p...

The branch exists. Let's check out its actual head and verify the claimed commit hashes.

svgRan cd /home/user/fork-p...

Both commit hashes are real and exactly match. `main` is indeed at `56b4e06`, branch resolves to `d181191`, parent is `704b1da`. Now let's inspect the actual implementation and run the verifier myself.

3 tools usedsvg

Good, files pulled in. Now let's install deps and independently run the verifier fresh — not their receipt, my own execution.

4 tools usedsvg

Deps installed cleanly in a fresh venv. Now run the verifier myself.

svgRan cd /home/user/fork-p...

Genuine independent PASS — fresh venv, fresh checkout, unmodified package. Now the tamper probe claim — let's actually try to break it, in a scratch copy so we don't touch the real one.

2 tools usedsvg

I'll tamper with the signed proposal intent field (this is what their claimed tamper probe attacks) and confirm the verifier rejects it.

svgRan cd /tmp/qsa_tamper &...

Tamper probe confirmed independently — modifying the signed proposal field breaks Ed25519 verification and the checker correctly fails with a non-zero exit. Let me also check a couple of the adversarial matrix cases (A11 duplicate JSON key, A2 substitute public key) since those were only *proposed*, not run, in the source doc.

2 tools usedsvg

A2 (substitute public key) also correctly rejects — not in their predeclared matrix results yet, but I verified it independently.

2 tools usedsvg

Good — it explicitly rejects duplicate keys via `no_dupes` in the JSON parser hook, and rejects floats/non-string keys/out-of-range ints in `assert_profile`. Let's actually test A11 and A12 directly.

svgRan cd /tmp/qsa_a11 pyth...

A11 confirmed to fail correctly, exactly as designed. Now A12 (float/noncanonical encoding):

svgRan rm -rf /tmp/qsa_a12 ...

All four probes I ran independently (A2, A11, A12, plus their own claimed proposal-tamper case) fail exactly as the spec predicts. Confirming the untampered baseline still passes clean, for the record.

svgRan cd /home/user/fork-p...

Confirmed, clean, in this fresh venv, untouched original copy — real independent recomputation, not their receipt.

## Verification result: technical claims check out

I did this in a fresh sandbox environment (new venv, fresh git checkout), not by trusting the committed receipt.

**Commit/branch claims — confirmed exact:**

- `main` is at `56b4e06...` ✓ (their claim)
- Branch `research/qsa-001-v0.1-freeze-reference` resolves to `d181191...` exactly ✓
- `704b1da...` is the immediate parent of `d181191...` ✓ ("one exact successor commit atop that freeze")
- Diff between `main` and the branch tip is 20 files / 833 lines added, no modification to existing repo files — consistent with "additive freeze," not a rewrite

**Independent recomputation:**

- `pip install -r requirements.txt` in a clean venv, ran `qsa_verify.py --compare-expected` on the untouched checkout → **PASS**, all 21 named checks green, matching the four bounded outcomes (P0/P1/P2/P3) and the non-authority disclaimers exactly as described.

**Tamper/adversarial pressure — I ran 4 attacks myself, not just their one claimed probe:**

svgsvg

| AttackTargetResult                                 |                                 |                                                                        |
| -------------------------------------------------- | ------------------------------- | ---------------------------------------------------------------------- |
| Modify signed proposal field (their claimed probe) | `p2.json` proposal_intent       | **FAIL** — `signature verification failed: p2-proposal` ✓              |
| A2: substitute public key                          | `trusted_keys.json` builder key | **FAIL** — `signature verification failed: p0-mark` ✓                  |
| A11: duplicate JSON key                            | `manifest.json`                 | **FAIL** — `duplicate JSON object key: artifact_id` ✓                  |
| A12: inject float                                  | `manifest.json`                 | **FAIL** — `QSA-CANONICAL-JSON-001 prohibits floating-point numbers` ✓ |

All four rejections match what the code is designed to catch (`no_dupes` hook, `no_float` parser, Ed25519 verification) — this isn't a checker that "only knows how to pass."

**What this establishes vs. doesn't:** this confirms the *mechanical* claims — commits are real, the reference implementation runs, signatures/schema/canonicalization checks fire as designed, and the tamper probe generalizes beyond the one case they described. It does **not** touch, and I make no claim about, the higher-order framing (whether "QSA governance" as a concept is meaningful, whether this should govern anything real, or any of the non-technical claims layered on top). That part remains exactly what it was: an unverified design narrative.

This is a meaningfully different situation than the original `fork-public-evidence` review — that repo was mostly prose-as-process with lexical checkers. This QSA-001 artifact is a real, small, working cryptographic verifier whose stated adversarial guarantees I could independently reproduce failing correctly.