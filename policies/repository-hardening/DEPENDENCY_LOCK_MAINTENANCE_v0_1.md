# Dependency Lock Maintenance v0.1

The human-readable inputs remain `requirements-proof-surface.txt` and `requirements-claim-admission.in`. Workflows install only from the corresponding `.lock.txt` files with `pip --require-hashes`.

An update is a review-bearing control change. Regenerate locks in an isolated environment with `pip-compile --generate-hashes`, omit embedded index and trusted-host directives, and verify that Python 3.11 can resolve only binary distributions for both `manylinux2014_x86_64` and `win_amd64` before admission.

Dependabot may propose dependency and GitHub Actions updates. It has no authority to merge, update an admitted action pin registry, or activate a repository ruleset automatically.
