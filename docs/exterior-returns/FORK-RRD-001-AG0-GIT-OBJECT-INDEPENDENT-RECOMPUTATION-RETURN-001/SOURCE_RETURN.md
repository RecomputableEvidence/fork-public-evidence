# Independent Recomputation Report

## Object: `883e4aad6667b06a9e4d2eb6a5d23f435afcfe68`
## Base: `f43b49dc42eb8df6ca3355f19e7b7b385a6b01bf`
## Repository: `RecomputableEvidence/fork-public-evidence`

---

## Summary

All structural claims in the source document have been independently recomputed from a fresh clone of the repository. The object hash, object type, parent-child relationship, and tree binding are **confirmed**. Two claims in the source document contain **errors**: the timestamp conversion and the elapsed-time calculation. Additionally, `main` has moved since the document was written — the base commit is no longer the tip of `main`, though it remains an ancestor.

---

## 1. Object Identity Recomputation

### SHA-1 recomputation (primary method)

```bash
object=883e4aad6667b06a9e4d2eb6a5d23f435afcfe68
type=$(git cat-file -t "$object")    # → commit
size=$(git cat-file -s "$object")    # → 322
{ printf '%s %s\0' "$type" "$size"; git cat-file "$type" "$object"; } | sha1sum
```

**Result: `883e4aad6667b06a9e4d2eb6a5d23f435afcfe68`** — matches exactly.

### Cross-check (git hash-object)

```bash
git cat-file commit 883e4aad6667b06a9e4d2eb6a5d23f435afcfe68 | git hash-object -t commit --stdin
```

**Result: `883e4aad6667b06a9e4d2eb6a5d23f435afcfe68`** — matches exactly.

**Verdict: Object identity CONFIRMED by two independent methods.**

---

## 2. Object Type and Content

| Property | Document claim | Recomputed value | Match |
|:--|:--|:--|:--|
| Object type | commit | commit | ✅ |
| Object size | 322 bytes | 322 bytes | ✅ |
| Tree | `0643660d9657b00b3d1c531d9e4aa0a0777bd04a` | `0643660d9657b00b3d1c531d9e4aa0a0777bd04a` | ✅ |
| Parent | `f43b49dc42eb8df6ca3355f19e7b7b385a6b01bf` | `f43b49dc42eb8df6ca3355f19e7b7b385a6b01bf` | ✅ |
| Author | RecomputableEvidence | RecomputableEvidence | ✅ |
| Committer | RecomputableEvidence | RecomputableEvidence | ✅ |
| Subject | Instantiate relational resolution demonstration at AG0 | Instantiate relational resolution demonstration at AG0 | ✅ |

The tree object `0643660d9657b00b3d1c531d9e4aa0a0777bd04a` was also independently recomputed via SHA-1 — **matches exactly**.

---

## 3. Parent-Child Binding

| Test | Command | Exit code | Interpretation |
|:--|:--|:--|:--|
| Object exists as commit | `git rev-parse --verify '883e…fe68^{commit}'` | 0 | Confirmed commit object |
| Base exists as commit | `git rev-parse --verify 'f43b…01bf^{commit}'` | 0 | Confirmed commit object |
| Base is ancestor of object | `git merge-base --is-ancestor f43b…01bf 883e…fe68` | 0 | **Direct parent confirmed** |
| Object is ancestor of base | `git merge-base --is-ancestor 883e…fe68 f43b…01bf` | 1 | Object is a child, not an ancestor of base — expected |

The object's `parent` line explicitly names `f43b49dc42eb8df6ca3355f19e7b7b385a6b01bf`, and the ancestry test confirms this is a direct parent-child relationship.

**Verdict: Parent-child binding CONFIRMED.**

---

## 4. Repository Integrity

```
git fsck --full --strict
```

**Result: No errors reported.** Checked all objects in the pack (10,800 packed objects). The document's transcript reported 15,849 objects checked — this is because the document's clone had additional branches/objects fetched. My fresh clone has 10,800 packed objects. Both runs report zero integrity errors.

---

## 5. Base Commit and `main` Reference

| Assertion | Document claim | Recomputed value | Match |
|:--|:--|:--|:--|
| Base commit hash | `f43b49dc42eb8df6ca3355f19e7b7b385a6b01bf` | `f43b49dc42eb8df6ca3355f19e7b7b385a6b01bf` | ✅ |
| Base is a merge commit | Yes (Merge: ed9b8b1 da0e5fa) | Yes (Merge: ed9b8b1 da0e5fa) | ✅ |
| Base commit message | Merge PR #181 | Merge PR #181 | ✅ |
| Base author date | Thu Sep 24 17:56:45 2026 -0700 | Thu Sep 24 17:56:45 2026 -0700 | ✅ |
| `origin/main` == base commit | Claimed yes | **`734bf2cc1981a52d8b9d0c0b9eeb2aece6253f52`** | ❌ **CHANGED** |

**`main` has moved.** The document claimed `main` pointed to `f43b49d…` at the time of its writing. As of this recomputation (2026-09-25), `origin/main` resolves to `734bf2c…`. The base commit `f43b49d…` is still an ancestor of current `main` (exit code 0 from ancestry test), and the object `883e…fe68` is also reachable from current `main`. The branch `routing/current-standing-v0.10-20260925` also contains both commits.

**This does not invalidate the document's claim** — it was likely true at the time of writing. The document itself acknowledges that a mutable branch name cannot serve as a freeze anchor. The base commit hash remains the stable reference.

---

## 6. Timestamp Analysis — ERRORS FOUND

### The commit's raw timestamp

The commit object stores: `1790310255 -0700`

### Correct conversion

| Timezone | Converted time |
|:--|:--|
| UTC | 2026-09-25 04:24:15 |
| PDT (UTC-7) | 2026-09-24 21:24:15 |

### Document's claimed conversion

The source document states:
> Commit `883e…fe68` has authored/committed timestamp `1790310255 -0700`, which converts to **Thursday, September 24, 2026, 18:30:55 PDT**.

**This is incorrect.** The epoch timestamp `1790310255` converts to **21:24:15 PDT**, not 18:30:55 PDT. The document's claimed time (18:30:55 PDT) corresponds to epoch `1790299855`, which is 10,400 seconds (~2 hours 53 minutes 20 seconds) earlier than the actual value stored in the commit.

### Elapsed time from parent

| | Document claim | Correct value |
|:--|:--|:--|
| Parent commit time | 17:56:45 PDT | 17:56:45 PDT |
| Object commit time | 18:30:55 PDT (claimed) | 21:24:15 PDT (actual) |
| Elapsed | 34 minutes 10 seconds | **3 hours 27 minutes 30 seconds** |

The document claims the object was created "34 minutes and 10 seconds after" the parent commit. The actual elapsed time is **3 hours, 27 minutes, and 30 seconds** (12,450 seconds). The document's arithmetic is internally consistent (18:30:55 − 17:56:45 = 34:10) but based on the wrong timestamp conversion.

---

## 7. Commit Content

The commit adds a single file: `research/fork-relational-resolution-demonstration-001/AG0_QUESTION_FREEZE.md` (334 lines, new file).

This file contains the standing label `INSTANTIATED_AT_QUESTION_FREEZE_ONLY` and the repository base coordinate `main@f43b49dc42eb8df6ca3355f19e7b7b385a6b01bf`. A repository-wide search confirms this label appears only in this one file.

The file describes a "question freeze" stage (AG0) in a multi-stage demonstration (AG0 through AG8) about fork-relational resolution. It freezes a bounded question, fixture selection, and predeclared relation-edge classes, while explicitly stating that no substantive observation, verification, or execution is performed at this stage.

---

## 8. Recomputed Standing Table

| Assertion | Result | Basis |
|:--|:--|:--|
| Repository identity | ✅ Confirmed | Public GitHub repo `RecomputableEvidence/fork-public-evidence` cloned successfully |
| Base commit exists | ✅ Confirmed | `git rev-parse --verify` succeeds; commit object present |
| Object exists | ✅ Confirmed | `git rev-parse --verify` succeeds; commit object present |
| Object type = commit | ✅ Confirmed | `git cat-file -t` returns `commit` |
| Object size = 322 bytes | ✅ Confirmed | `git cat-file -s` returns `322` |
| SHA-1 recomputation | ✅ Confirmed | Two independent methods produce `883e4aad6667b06a9e4d2eb6a5d23f435afcfe68` |
| Parent = base commit | ✅ Confirmed | Parent line in commit object + ancestry test (exit 0) |
| Tree hash recomputation | ✅ Confirmed | `0643660d9657b00b3d1c531d9e4aa0a0777bd04a` matches |
| `git fsck --full --strict` | ✅ Pass | No integrity errors |
| Object reachable from current `main` | ✅ Confirmed | Ancestry test exit 0 |
| `main` == base commit | ❌ No longer | `main` now at `734bf2c…`; was likely at `f43b49d…` when document was written |
| Timestamp conversion | ❌ Incorrect | Document says 18:30:55 PDT; actual is 21:24:15 PDT |
| Elapsed time from parent | ❌ Incorrect | Document says 34m10s; actual is 3h27m30s |
| `INSTANTIATED_AT_QUESTION_FREEZE_ONLY` standing | ⚠️ Structurally present | Label found in the commit's added file; its semantic authority is not assessable from Git alone |

---

## 9. Boundary Statement

This recomputation establishes only structural Git facts: object identity, type, size, content, parent-child binding, tree integrity, and repository integrity. It does not establish:

- That the object existed at a particular historical instant (the timestamp is author-controlled and not cryptographically attested).
- That `main` was frozen at the base commit at any specific time (mutable branch names cannot prove this).
- That the label `INSTANTIATED_AT_QUESTION_FREEZE_ONLY` has any enforceable semantic meaning beyond its presence in the committed file.
- Any claim about truth, authorization, compliance, legal sufficiency, or institutional authority.

A signed annotated tag, signed commit, or append-only transparency-log receipt would be materially stronger evidence for a freeze claim than a mutable branch reference.

---

## Verification commands used

All commands were executed in a fresh clone on a Linux system (not PowerShell, avoiding the shell-syntax issues documented in the source transcript):

```bash
git clone https://github.com/RecomputableEvidence/fork-public-evidence.git
cd fork-public-evidence
git fetch --tags --prune origin

# Object existence and type
git rev-parse --verify '883e4aad6667b06a9e4d2eb6a5d23f435afcfe68^{commit}'
git cat-file -t 883e4aad6667b06a9e4d2eb6a5d23f435afcfe68
git cat-file -s 883e4aad6667b06a9e4d2eb6a5d23f435afcfe68
git cat-file -p 883e4aad6667b06a9e4d2eb6a5d23f435afcfe68

# SHA-1 recomputation (method 1)
object=883e4aad6667b06a9e4d2eb6a5d23f435afcfe68
type=$(git cat-file -t "$object")
size=$(git cat-file -s "$object")
{ printf '%s %s\0' "$type" "$size"; git cat-file "$type" "$object"; } | sha1sum

# SHA-1 recomputation (method 2 — cross-check)
git cat-file commit 883e4aad6667b06a9e4d2eb6a5d23f435afcfe68 | git hash-object -t commit --stdin

# Ancestry tests
git merge-base --is-ancestor f43b49dc42eb8df6ca3355f19e7b7b385a6b01bf 883e4aad6667b06a9e4d2eb6a5d23f435afcfe68
git merge-base --is-ancestor 883e4aad6667b06a9e4d2eb6a5d23f435afcfe68 f43b49dc42eb8df6ca3355f19e7b7b385a6b01bf

# Integrity
git fsck --full --strict

# Branch state
git rev-parse origin/main
git branch -a --contains 883e4aad6667b06a9e4d2eb6a5d23f435afcfe68

# Timestamp verification
python3 -c "from datetime import datetime, timezone, timedelta; print(datetime.fromtimestamp(1790310255, tz=timezone(timedelta(hours=-7))))"
```
