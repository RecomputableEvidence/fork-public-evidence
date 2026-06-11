# GitHub Publication Readiness Checklist

## Repository

- [ ] Repository root is `C:\N\fork-public-evidence`
- [ ] `technical-disclosure/` contains the verified public disclosure
- [ ] `receipts/` contains the frozen ZIP and detached receipt
- [ ] `white-paper/Reconstructive_Fidelity_in_the_Age_of_AI_v1_0.md` exists
- [ ] `README.md`, `COPYRIGHT.md`, `CITATION.cff`, and `.gitignore` exist
- [ ] `docs/index.md` and `docs/_config.yml` exist
- [ ] Internal-residue inspection passes

## Frozen disclosure

- [ ] ZIP SHA-256 equals:

```text
1361dd12b1f249372f240cb5226cac289319bc6da4ce219ea47538a0716c1410
```

- [ ] Detached receipt contains the same hash
- [ ] Included verifier exits `0`
- [ ] Gate result is `9 PASS / 1 NOT_CHECKED / 0 FAIL`

## GitHub publication

- [ ] Public repository created at `https://github.com/SentinelQuantumAegis/fork-public-evidence`
- [ ] Main branch pushed
- [ ] Tag `fork-public-disclosure-v0.1.1` pushed
- [ ] GitHub Release created
- [ ] Frozen ZIP attached
- [ ] Detached receipt attached
- [ ] Release copy downloaded and rehashed
- [ ] Downloaded copy clean-extracted and reverified
- [ ] GitHub Pages enabled from `main` / `docs`

## Publication boundaries

- [ ] Synthetic fixture status is visible
- [ ] Live institutional deployment remains unestablished
- [ ] Production readiness remains unestablished
- [ ] Third-party verifier independence remains unestablished
- [ ] No aggregate trust, compliance, validity, or admissibility verdict is emitted
