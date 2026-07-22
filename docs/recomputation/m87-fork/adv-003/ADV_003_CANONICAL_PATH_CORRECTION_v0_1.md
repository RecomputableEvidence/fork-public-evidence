# ADV_003 canonical-path correction v0.1

Status: `CORRECTION_CANDIDATE_RECOMPUTATION_PENDING`

## Reviewed predecessor

The correction follows the model-assisted exact-head review of PR #65 at:

`c15c105f7277494b335d1d038bda58c1dbc78b16`

That review reproduced the principal packet-root and exact-inventory protections, but found that a manifest path containing an equivalent-looking `./` segment was silently normalized before validation. After the manifest sidecar and outer receipt were recomputed, the successor checker returned a passing artifact-path result.

The preserved adversarial representation was:

```text
docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/./README.md
```

This finding narrows the predecessor claim. The reviewed checker confined artifact resolution beneath the packet root and compared the declared and actual inventories, but it did not reject every noncanonical input representation it claimed to reject.

## Bounded correction

The successor checker now validates the original path string before constructing a `PurePosixPath`. Accepted manifest paths must:

- use POSIX `/` separators;
- contain no backslash or mixed separator;
- contain no empty, `.` or `..` segment;
- contain no duplicate or trailing separator;
- be neither POSIX absolute nor UNC-style;
- be neither Windows drive-qualified nor drive-relative;
- equal their canonical POSIX representation rather than depending on silent normalization.

The derivative harness retains the original seven cases and adds ten independently named path-representation cases. Each path case recomputes the manifest sidecar and outer receipt after mutation so stale binding metadata cannot be the reason for rejection.

## Preserved standing

Still supported, subject to fresh exact-head execution:

- packet-root controls artifact resolution;
- actual packet inventory must equal the declared set;
- unmanifested additions are detected;
- manifested scratch mutations are detected;
- path escape and symlink substitution are rejected;
- ADV_001 and ADV_002 historical standings remain unchanged.

Corrected claim:

- noncanonical path representations are rejected under the explicit canonical POSIX path contract added by this correction; this requires fresh exact-head recomputation and workflow results before reliance.

## Required recomputation

Run from the repository root:

```powershell
python tools/check_longitudinal_reconstruction_day0_packet_v0_1_1.py --json
python tools/check_longitudinal_day0_adv_003_recomputation_v0_1.py --repo-root . --json
python -m pytest tests/test_longitudinal_day0_adv_003_v0_1.py -q
```

Then run the applicable repository workflows against the new exact head. Preserve any failure or platform-specific inability to execute.

## Residuals and non-claims

This correction does not remediate ADV_001 or ADV_002, resolve F-02 or F-03, certify security, establish source truth or completeness, authorize merge, create admission standing, approve production use, or confer execution or institutional authority. The reviewed predecessor head and its adverse result remain part of the history and are not rewritten by a later passing result.
