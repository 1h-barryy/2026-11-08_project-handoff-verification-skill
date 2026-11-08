# Iteration

This record separates the original failures, earlier fixes, and the fresh rerun
on November 8, 2026. The original evidence is preserved rather than rewritten.

## Status labels

The [first smoke-test report](iteration-records/01-smoke-test/result.md) identified
a real mismatch: the original skill prescribed PARTIAL and FAIL, while the design
requires PASS, ISSUE, and UNVERIFIED. The old report itself used the mismatched
labels. Its [original session export](iteration-records/02-hw8/original-checker.transcript.jsonl)
is now saved too; that historical review is not a post-fix test.

The mismatch was already fixed before this workflow. Both direct inspection and
[Checker 1](iteration-records/02-hw8/checker1.result.md) confirmed that it is absent
from the current skill. The [historical diff](iteration-records/02-hw8/historical-label-fix.diff)
shows the earlier correction. I am not claiming that correction as a new change.

The new small improvement adds a final report check:

> Before returning, check each status cell against the current governing status vocabulary. Keep superseded labels from historical reports only in clearly marked quotations, not in the current status cells.

This guard addresses the demonstrated report-format failure. The
[before snapshot](iteration-records/02-hw8/skill.before.snapshot),
[after snapshot](iteration-records/02-hw8/skill.after.snapshot), and
[exact diff](iteration-records/02-hw8/skill-guard.diff) preserve the change.

A fresh independent session used the revised skill to review historical and
current artifacts separately. Its [actual report](iteration-records/02-hw8/skill-rerun.result.md)
and [transcript](iteration-records/02-hw8/skill-rerun.transcript.jsonl) show:

| Artifact reviewed | Scope | Design | Verification |
| --- | --- | --- | --- |
| Historical skill/report | UNVERIFIED | ISSUE | UNVERIFIED |
| Current iteration | PASS | PASS | PASS |

All six status cells use the governing vocabulary. The checker quotes the old
labels only in its explanation and distinguishes the earlier correction from
the new guard. Its project-file hashes are unchanged before and after review.

Checker excerpt: “This demonstrates one compliant report after revision. It does
not establish that the guard caused compliance, general reliability,
external-project testing, or completion of the full toolkit.”

The optional skill-format validator could not start because this environment
lacks PyYAML ([command and exit status](iteration-records/02-hw8/skill-validation.command.json),
[error log](iteration-records/02-hw8/skill-validation.log)). That is not a passing
format-validation test; the separate behavioral review did run.

## MCP retrieval

The [earlier registered call](iteration-records/02-hw8/earlier-mcp.transcript.jsonl)
found the limit values but not their exact definitions. Demonstration 1 reproduced
that gap, added bounded constant-definition evidence, and reran the relevant
tests and real stdio call. It returned all four definitions at server.py:27–30.
The [demonstration record](DEMONSTRATION.md) links the actual patch and output.

## What remains

Demonstration 1 and the fresh skill rerun are complete. Demonstration 2 remains
paused at a host approval gate before its MCP result and README edit; no Checker 2
result is claimed. The saved pending transcript must be supplemented after the
host resumes. The two originally named external projects were not tested.

TODO (my review): Decide whether I agree with the checker findings and whether
the extra final-status check is useful. Edit this explanation in my own words.

TODO (my final reflection): After Demonstration 2 finishes, explain whether the
workflow reduced repeated explanation and made handoff claims easier to verify.

### My Reflection

This project helped me better understand the difference between giving an AI agent instructions and giving it tools to work with.

During the first skill test, we found that the status labels were inconsistent with the design document. Although that issue had already been corrected before the formal iteration, we added a small guard and tested the checker again.

The rerun passed, but I also realized that passing tests doesn't mean everything has been verified. For example, our MCP worked in the current project, but we haven't fully tested it across different projects.

I think the most useful part of this toolkit is that it helps agents understand an existing project and makes their work easier to verify. I would like to keep improving it as I use it in more projects.