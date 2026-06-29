# Fork Experimental Branch Work v0.1

## Purpose

This document separates the public-review baseline from branch-specific work. It exists so external reviewers do not confuse active development, repair branches, localization branches, or experimental doctrine branches with released public-review posture.

## Public-review baseline

Unless a review request explicitly names another branch, the public-review baseline is:

```text
main
```

Tagged GitHub releases are frozen release artifacts. Release packages under `release_packages/` are public/reviewer package materials only within the claims and non-claims declared by each package.

## Branch-work rule

A branch outside `main` is not part of the public-review baseline unless one of the following is true:

1. The branch has been merged into `main`.
2. The branch has been tagged as a release artifact.
3. The branch is explicitly named in a bounded review request.
4. The branch is explicitly listed in a package index or release note as in-scope for a specific review.

## Current observed branch categories as of 2026-06-28

The public GitHub branch list showed active or recent branch work including:

- `boundary-delta-record-v0.1`
- `mhbar-v0.1-token-typo-repair`
- `bdr-localization-v0.1`
- `transition-localization-v0.1`
- `branch/cbo-minimum-packet-requirements-v0.1`
- `branch/fork-glm-declaration-v0.1.1-timing-axis-vocabulary-repair-clean`
- `branch/fork-use-case-boundary-language-v0.1.1`
- `branch/fork-use-case-boundary-language-v0.1`
- `fork-glm-declaration-v0.1`

These names indicate development or bounded review surfaces. Their presence does not mean their contents are released, production-ready, client-ready, or part of the default public-review path.

## How to cite branch work

When branch work is cited externally, use this pattern:

```text
This statement refers to branch `<branch-name>` as branch-specific work, not to the released public-review baseline on `main`.
```

If the branch is later merged, update the citation to the merge commit, tag, or release package that made the work part of the public-review baseline.

## Non-claim boundary for branch work

Branch work does not claim:

- release status;
- production readiness;
- client-specific readiness;
- legal admissibility;
- compliance satisfaction;
- decision correctness;
- source completeness;
- runtime enforcement;
- institutional authority;
- endorsement by external reviewers;
- inclusion in public release packages unless expressly stated.
