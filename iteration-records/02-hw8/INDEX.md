# HW8 evidence — November 8, 2026

Saved by the coordinating session. Existing smoke-test evidence was not changed.
The previous documentation is preserved in demonstration.before.snapshot and
iteration.before.snapshot. No commit or push was performed.

## Actual session records

| Run | Report | Transcript |
| --- | --- | --- |
| Earlier registered MCP test | [result](earlier-mcp.result.md) | [export](earlier-mcp.transcript.jsonl) |
| Original checker smoke test | [result](original-checker.result.md) | [export](original-checker.transcript.jsonl) |
| Demonstration 1 doer | [result](demo1-doer.result.md) | [export](demo1-doer.transcript.jsonl) |
| Checker 1 | [result](checker1.result.md) | [export](checker1.transcript.jsonl) |
| Revised-skill rerun | [result](skill-rerun.result.md) | [export](skill-rerun.transcript.jsonl) |
| Demonstration 2 doer, pending | No completed result | [partial export](demo2-pending.transcript.jsonl) |

Each export has a corresponding .provenance.json with the original session ID
and rollout path. The JSONL entries retain original timestamps, ordinals, tool
calls, and tool results. Exports omit system/developer context and reasoning;
they are not full raw rollout files. Historical exports stop at the first
completed turn. Report files contain the actual final assistant text, including
its original local links; these links may need the original checkout to open.
No missing tool results were reconstructed.

The new reviews are separate Codex sessions created through create_thread,
not a fork of the implementing conversation. Checkers used read-only commands;
the coordinator exported and saved their reports after completion.

## Change evidence

- [Original doer patch](demo1-doer.patch), extracted from its actual tool call.
  The demo1-server/tests/readme.after.snapshot files preserve its delivered state.
- [Historical label correction](historical-label-fix.diff), compared with the
  already-corrected skill baseline; this correction predates the current run.
- [New skill guard](skill-guard.diff), with skill.before.snapshot and
  skill.after.snapshot. Only the final vocabulary-check paragraph was added.
- demo2-readme.before.snapshot preserves the unchanged README baseline for the
  pending second doer. No completed second-doer diff exists yet.
- documentation-demonstration.diff and documentation-iteration.diff record the
  coordinator's updates from the preserved documents.

## Verification

| Command | Actual result | Evidence |
| --- | --- | --- |
| .venv/Scripts/python.exe -B -m unittest discover -s tests -v | 8 tests passed in 1.671s; exit 0 | [log](final-tests.log), [command/environment](final-tests.command.json) |
| git diff --check | No output; exit 0 | [log](final-diff-check.log), [command](final-diff-check.command.json) |
| verify_records.py | Both completed review hashes match; status cells valid; pending doer made no project changes | [log](record-checks.log), [command](record-checks.command.json) |
| Skill quick_validate.py | Could not start: PyYAML missing; exit 1 | [log](skill-validation.log), [command](skill-validation.command.json) |

The pre-iteration-tests.log also reports eight passing tests, but PowerShell's
stderr redirection produced a NativeCommandError wrapper. It is preserved as-is;
the final test capture uses subprocess and records the actual process exit code.

Hash comparisons cover project files, including the skill and older evidence.
They exclude .git, .venv, __pycache__, and this new evidence directory, where the
coordinator was saving records. They establish unchanged final file contents in
that scope, not absence of every possible temporary write or external action.
The accompanying checker transcripts contain no write commands.

Git diff --check covers tracked changes; most toolkit files remain untracked.
No claim is made that this command alone validates every new artifact.

## Pending work

[The captured host state](demo2-pending.host-state.json) reports waitingOnApproval
for task 01a1bd58-6551-7a20-a1d5-d135443161aa. The user reported approval twice,
but the host had not returned the required MCP result. Resume that doer before
starting Checker 2; preserve a new complete export rather than overwriting this
partial one. The live task may continue after the host gate is resolved.

Still needed for submission: completed Demonstration 2 and Checker 2 evidence,
the author's agreement/reflection, and the reviewed files committed/published
when authorized. No results on the two originally named external projects are
claimed. The current request authorized toolkit-local tasks instead.

capture.py and verify_records.py are coordinator evidence utilities, not changes
to the MCP implementation. They preserve exports with exclusive writes and
check saved records. They do not synthesize reviews or MCP responses.
