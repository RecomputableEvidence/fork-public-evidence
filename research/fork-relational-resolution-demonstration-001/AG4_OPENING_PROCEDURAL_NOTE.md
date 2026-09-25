# AG4 Opening Procedural Note

During AG4 opening, an unintended temporary file commit was created on the AG3 branch:

`57857f76023c12dfe5137a52b8fd6255d6685259`

The file was `.tmp` with content `x`. It was not part of AG3, did not alter any research-object evidence or standing, and was not used by AG4.

The AG3 branch ref was restored to the intended AG3 semantic commit:

`874947205b9cd1dac5f3268d9d6f25e1a97be7c1`

AG4 was then opened from that exact intended parent.

```text
PROCEDURAL_BRANCH_WRITE_ERROR
!= RESEARCH_OBJECT_CHANGE

REF_RESTORED_TO_INTENDED_AG3_COMMIT
!= NEGATIVE_PROCEDURAL_EVENT_ERASED_FROM_RECORD
```

This note preserves the operational deviation without importing it into the target evidence graph.
