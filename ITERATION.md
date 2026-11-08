# Iteration

This records what failed, what was already fixed, and what changed in the rerun
on November 8, 2026. The original evidence is kept unchanged.

## Status labels

The [first smoke-test report](iteration-records/01-smoke-test/result.md) identified
a mismatch: the original skill used PARTIAL and FAIL, while the design
requires PASS, ISSUE, and UNVERIFIED. The old report itself used the mismatched
labels. Its [original session export](iteration-records/02-hw8/original-checker.transcript.jsonl)
is saved too. That review happened before the fix.

The labels were already fixed before this run. Direct inspection and
[Checker 1](iteration-records/02-hw8/checker1.result.md) confirmed the current
skill uses the right labels. The [historical diff](iteration-records/02-hw8/historical-label-fix.diff)
shows that earlier correction; it was not a new change in this iteration.

The new small improvement adds a final report check:

> Before returning, check each status cell against the current governing status vocabulary. Keep superseded labels from historical reports only in clearly marked quotations, not in the current status cells.

This extra check addresses the label mismatch found in the first report. The
[before snapshot](iteration-records/02-hw8/skill.before.snapshot),
[after snapshot](iteration-records/02-hw8/skill.after.snapshot), and
[exact diff](iteration-records/02-hw8/skill-guard.diff) preserve the change.

A fresh independent session used the revised skill to review the old and current
files separately. Its [report](iteration-records/02-hw8/skill-rerun.result.md)
and [transcript](iteration-records/02-hw8/skill-rerun.transcript.jsonl) show:

| Artifact reviewed | Scope | Design | Verification |
| --- | --- | --- | --- |
| Historical skill/report | UNVERIFIED | ISSUE | UNVERIFIED |
| Current iteration | PASS | PASS | PASS |

All six status cells use the required labels. The checker quotes the old labels
only in its explanation and separates the earlier fix from the new check.
Project-file hashes matched before and after the review.

Checker excerpt: “This demonstrates one compliant report after revision. It does
not establish that the guard caused compliance, general reliability,
external-project testing, or completion of the full toolkit.”

The optional skill-format validator could not start because this environment
lacks PyYAML ([command and exit status](iteration-records/02-hw8/skill-validation.command.json),
[error log](iteration-records/02-hw8/skill-validation.log)). Format validation did
not pass, but the separate checker rerun did run.

## MCP retrieval

The [earlier registered call](iteration-records/02-hw8/earlier-mcp.transcript.jsonl)
found the limit values but not their exact definitions. Demonstration 1 reproduced
that gap, added bounded constant-definition evidence, and reran the relevant
tests and real stdio call. It returned all four definitions at server.py:27–30.
The [demonstration record](DEMONSTRATION.md) links the actual patch and output.

## What remains

Both demonstrations and the skill rerun are complete. Demonstration 2's first
attempt was blocked at host approval; the later direct run and Checker 2 findings
are recorded in DEMONSTRATION.md. The original pending evidence is still saved.

The two external projects were not tested, and switching the registered host to
another root remains unverified. Checker 2's session provenance still needs to be
saved. The evidence-checking script still expects the earlier README snapshot,
and the optional skill-format validator still needs PyYAML.

### My Reflection

This project helped me better understand the difference between giving an AI agent instructions and giving it tools to work with.

During the first skill test, we found that the status labels were inconsistent with the design document. Although that issue had already been corrected before the formal iteration, we added a small guard and tested the checker again.

The rerun passed, but I also realized that passing tests doesn't mean everything has been verified. For example, our MCP worked in the current project, but we haven't fully tested it across different projects.

I think the most useful part of this toolkit is that it helps agents understand an existing project and makes their work easier to verify. I would like to keep improving it as I use it in more projects.
