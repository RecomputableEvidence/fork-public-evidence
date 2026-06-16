\# CBC v0.2 Hardening Plan



\*\*Status\*\*: ACCEPTED\_PLAN

\*\*Author\*\*: Ryan Feller

\*\*Date\*\*: 2026-06-16

\*\*Dependency\*\*: `claim-boundary-contract-v0.1` (LOCKED)

\*\*Target Tags\*\*:

\- `claim-boundary-contract-v0.2`

\- `claim-consumption-events-v0.2`



\---



\## 🎯 Purpose

CBC v0.1 established \*\*doctrine\*\* (bounded claims, non-claims, verification scope).

CBC v0.2 \*\*hardens the schema\*\* against implementation misuse while preserving all v0.1 semantics.



\*\*Core Doctrine (Locked)\*\*:

> A Claim Boundary Contract is a \*\*node\*\*.

> A Claim Consumption Event is an \*\*edge\*\*.

> If consumption expands the boundary, the CCE \*\*points to a new CBC\*\*.

> The CCE \*\*records the transformation\*\*; it does \*\*not\*\* contain the expanded claim.



\---



\## ❌ Non-Goals

\- Do \*\*not\*\* rename CBC or CCE.

\- Do \*\*not\*\* move or delete v0.1 tags.

\- Do \*\*not\*\* weaken non-claim inheritance (`must\_travel\_downstream: true` remains).

\- Do \*\*not\*\* make JSON Schema carry relational graph logic (use Python tests for that).



\---



\## 🔧 Hardening Targets (Must Ship)



\### 1. Versioning

\*\*Add\*\*: `claim\_boundary\_contract\_version` (required, string, enum: `\["0.2"]`)

\*\*Why\*\*: Future-proofing. Recomputability requires self-identifying version.

\*\*Enforcement\*\*: JSON Schema.



\### 2. Verification Scope Guardrail

\*\*Add\*\*: Schema-level constraint that `verification\_status: PASS` \*\*requires\*\* `verification\_scope: RECORD\_INTEGRITY\_AND\_BOUNDARY\_STRUCTURE\_ONLY`

\*\*Why\*\*: Prevents `PASS + RECORD\_INTEGRITY\_ONLY` from implying boundary structure was checked.

\*\*Enforcement\*\*: JSON Schema (`if/then`).



\### 3. Downstream Narrowing

\*\*Change\*\*: Force `downstream\_may\_narrow: true` in `inheritance\_policy`

\*\*Why\*\*: Downstream narrowing must \*\*always\*\* be allowed to prevent overbroad claims.

\*\*Enforcement\*\*: JSON Schema (`const: true`).



\### 4. Sealing Accountability

\*\*Add\*\*: `sealed\_by` to `sealed\_at` (required object with `name`, `type`; optional `system\_id`)

\*\*Why\*\*: Adds structural accountability for the sealing actor or process.

\*\*Enforcement\*\*: JSON Schema.



\### 5. Nodes vs. Edges Doctrine (CCE)

\*\*Add\*\*: Explicit clarification in `CLAIM\_CONSUMPTION\_EVENTS\_v0\_2.md`:

\- CBC = \*\*node\*\* (contains claims, non-claims, evidence).

\- CCE = \*\*edge\*\* (records consumption/transformation).

\- If `boundary\_action: EXPANDED`, CCE \*\*must\*\* include `new\_claim\_boundary\_contract\_id` (points to new CBC node).

\- CCE \*\*does not\*\* contain the expanded claim body.



\*\*Enforcement\*\*:

\- JSON Schema: `EXPANDED` requires `new\_claim\_boundary\_contract\_id`.

\- Python tests: Validate that `new\_claim\_boundary\_contract\_id` points to a real CBC.



\---



\## 🔍 Enforcement Split

&#x20;  \*\*Rule\*\* | \*\*Enforcement Layer\*\* | \*\*Rationale\*\* |

&#x20;|----------|----------------------|---------------|

&#x20;| Required fields | JSON Schema | Structural validation |

&#x20;| Enum values (`verification\_status`, `boundary\_action`) | JSON Schema | Prevent invalid states |

&#x20;| SHA-256 patterns | JSON Schema | Ensure cryptographic integrity |

&#x20;| `additionalProperties: false` | JSON Schema | Prevent silent field creep |

&#x20;| `PASS` requires `RECORD\_INTEGRITY\_AND\_BOUNDARY\_STRUCTURE\_ONLY` | JSON Schema | Critical guardrail |

&#x20;| `EXPANDED` requires `new\_claim\_boundary\_contract\_id` | JSON Schema | Prevent edge-as-node |

&#x20;| `upstream\_claims\_relied\_on` subset of `upstream\_claims\_received` | Python tests | Relational invariant |

&#x20;| `evidence\_refs` referenced by `relied\_on\_evidence\_refs` exist | Python tests | Cross-field reference |

&#x20;| CCE source CBC ID exists | Python tests | Integration validation |

&#x20;| EXPANDED CCE points to actual new CBC | Python tests | Graph integrity |



\---



\## 📁 File Changes (Exact Order)

&#x20;| \*\*#\*\* | \*\*File\*\* | \*\*Action\*\* | \*\*Status\*\* |

&#x20;|-------|----------|------------|------------|

&#x20;| 1 | `docs/CBC\_V0\_2\_HARDENING\_PLAN.md` | Create | ✅ \*\*THIS DOCUMENT\*\* |

&#x20;| 2 | `docs/CLAIM\_BOUNDARY\_CONTRACT\_v0\_2.md` | Create (v0.1 + hardening notes + "Contract" clarification) | ⏳ |

&#x20;| 3 | `schemas/claim\_boundary\_contract\_v0\_2.schema.json` | Create (v0.1 + hardening) | ⏳ |

&#x20;| 4 | `examples/claim\_boundary\_contract\_v0\_2/runtime\_blocked\_tool\_call.json` | Copy v0.1 + add `claim\_boundary\_contract\_version`, `sealed\_by` | ⏳ |

&#x20;| 5 | `examples/claim\_boundary\_contract\_v0\_2/eval\_benchmark\_pass.json` | Copy v0.1 + add `claim\_boundary\_contract\_version`, `sealed\_by` | ⏳ |

&#x20;| 6 | `tests/test\_claim\_boundary\_contract\_v0\_2.py` | Create (v0.1 tests + adversarial) | ⏳ |

&#x20;| 7 | `docs/CLAIM\_CONSUMPTION\_EVENTS\_v0\_2.md` | Create (v0.1 doctrine + nodes/edges + "Event" clarification) | ⏳ |

&#x20;| 8 | `schemas/claim\_consumption\_event\_v0\_2.schema.json` | Create | ⏳ |

&#x20;| 9 | `examples/claim\_consumption\_event\_v0\_2/preserved\_boundary.json` | Create | ⏳ |

&#x20;| 10 | `examples/claim\_consumption\_event\_v0\_2/expanded\_boundary.json` | Create | ⏳ |

&#x20;| 11 | `tests/test\_claim\_consumption\_event\_v0\_2.py` | Create | ⏳ |



\---

\## 🧪 Adversarial Tests (Must Pass)



\### CBC Tests (`test\_claim\_boundary\_contract\_v0\_2.py`)

1\. \*\*PASS + partial scope\*\*: Reject `verification\_status: PASS` with `verification\_scope` not equal to `RECORD\_INTEGRITY\_AND\_BOUNDARY\_STRUCTURE\_ONLY`.

2\. \*\*Missing version\*\*: Reject if `claim\_boundary\_contract\_version` absent.

3\. \*\*`downstream\_may\_narrow: false`\*\*: Reject.

4\. \*\*`sealed\_by` missing\*\*: Reject.

5\. \*\*`upstream\_claims\_relied\_on` not subset of `upstream\_claims\_received`\*\*: Reject (Python test).



\### CCE Tests (`test\_claim\_consumption\_event\_v0\_2.py`)

1\. \*\*EXPANDED without new CBC\*\*: Reject if `boundary\_action: EXPANDED` but `new\_claim\_boundary\_contract\_id` missing.

2\. \*\*EXPANDED without description\*\*: Reject if `boundary\_action: EXPANDED` but `boundary\_expansion\_description` missing.

3\. \*\*Invalid `boundary\_action`\*\*: Reject if not in enum.

4\. \*\*CCE contains expanded claim body\*\*: Reject (CCE is an edge, not a node).



\---

\## 🏷️ Tagging Plan

1\. \*\*Do not touch\*\*:

&#x20;  - `claim-boundary-contract-v0.1`

&#x20;  - `claim-consumption-events-v0.1`

2\. \*\*New tags\*\* (after all artifacts pass tests):

&#x20;  - `claim-boundary-contract-v0.2`

&#x20;  - `claim-consumption-events-v0.2`



\---

\## 📌 Doctrine Locked for v0.2

> A \*\*Claim Boundary Contract\*\* is a \*\*node\*\*.

> A \*\*Claim Consumption Event\*\* is an \*\*edge\*\*.

> If consumption \*\*expands\*\* the boundary, the CCE \*\*points to a new CBC\*\*.

> The CCE \*\*records the transformation\*\*; it does \*\*not\*\* contain the expanded claim.

> This prevents \*\*edge-as-node collapse\*\* and keeps Fork \*\*narrow\*\*.



\---

\## 🚀 Implementation Order

1\. \*\*This document\*\* (`CBC\_V0\_2\_HARDENING\_PLAN.md`) → \*\*COMMIT FIRST\*\*

2\. \*\*CBC v0.2 artifacts\*\* (docs, schema, examples, tests) → \*\*NEXT COMMIT\*\*

3\. \*\*CCE v0.2 artifacts\*\* (docs, schema, examples, tests) → \*\*THIRD COMMIT\*\*

4\. \*\*Tag both\*\* → \*\*FINAL TAG STEP\*\*



\---

\## ❗ Hard Blockers (Must Fix Before Tagging)

\- \[ ] `claim\_boundary\_contract\_version` missing in schema.

\- \[ ] `PASS` not enforced to require full scope.

\- \[ ] `downstream\_may\_narrow` not forced to `true`.

\- \[ ] `sealed\_by` missing in `sealed\_at`.

\- \[ ] CCE schema allows `EXPANDED` without `new\_claim\_boundary\_contract\_id`.

\- \[ ] Adversarial tests not passing.



\---

\## 📅 Timeline

&#x20;| \*\*Phase\*\* | \*\*Target\*\* | \*\*Owner\*\* |

&#x20;|-----------|------------|-----------|

&#x20;| CBC v0.2 artifacts | 2026-06-23 | NextGen |

&#x20;| CCE v0.2 artifacts | 2026-06-30 | NextGen |

&#x20;| Tagging | 2026-07-07 | NextGen |

