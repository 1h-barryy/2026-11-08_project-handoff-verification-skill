# Demonstration 2 — direct doer result

Completed November 8, 2026, in session
01a1bd4e-4f08-7033-9c3c-4d54680aa418, following the user's explicit request to
perform this doer task directly here. This supplements the earlier pending
attempt; it does not overwrite it or claim a fresh independent checker review.

## Task and actual MCP call

Improve README instructions for another local project root. Keep the change
small; do not edit the MCP server, checker skill, or tests. Save actual evidence.

Before editing, called project-context.inspect_project_context. The
[complete arguments and returned result](demo2-direct.mcp.json) show isError=false
and project_root=E:\1h-barryy\Dev\2026-11-08_project-handoff-verification-skill.
The response identified README.md, server.py, smoke_client.py, and the tests.
It inventoried 63 files and read 37; task-match output was truncated, while the
inventory was not. The saved JSON preserves the full returned payload, including
its coverage limits, rather than the shortened display in the conversation.

The [current-turn transcript](demo2-direct.transcript.jsonl) preserves the actual
request, MCP invocation/result, README patch, and test output through evidence
capture. Its [provenance](demo2-direct.provenance.json) states the export boundary.

## Change and source verification

The [README diff](demo2-direct-readme.diff) clarifies toolkit paths versus the
target root, absolute paths and spaces, restarting/reconnecting the server,
the task-only API, and checking the returned project_root. It includes a
PowerShell smoke-client example and explains that it does not change host config.

Verified against actual implementation:

- server.py:275–279 requires a startup --project-root, resolves it strictly,
  and rejects a non-directory. Relative resolution uses the launch directory.
- server.py:283–286 exposes only task and closes over the configured root.
- server.py:238 returns the resolved project_root.
- smoke_client.py:13–26 uses the current Python executable, launches its sibling
  server.py with the resolved target, and calls the tool over stdio.
- smoke_client.py:30–35 parses the CLI arguments and prints the structured result.

The [before](demo2-direct-readme.before.snapshot) and
[after](demo2-direct-readme.after.snapshot) copies preserve the exact README states.
The [scope comparison](demo2-direct-scope.json), supported by the before/after
hash manifests, confirms README.md is the only existing project file changed.
New evidence files are excluded from that comparison and saved beside this report.
The server, smoke client, checker skill, and tests are unchanged.

## Checks and limits

- Existing suite: **8 tests passed in 1.589 seconds; exit 0**.
  [Actual output](demo2-direct-tests.log), [command/environment](demo2-direct-tests.command.json).
  This includes real stdio inspection of a temporary project and confirmation of
  its returned root, plus the scan-limit location regression test.
- git diff --check: **exit 0, no output**.
  [Log](demo2-direct-diff-check.log), [command](demo2-direct-diff-check.command.json).

The example C:/tools and D:/work paths are placeholders, not tested real projects.
No host registration was changed, and no external-project test or Checker 2
success is claimed. The old blocked task was sent a stop instruction because
this direct task supersedes it; delivery of that instruction is not proof that
its host approval gate has cleared.

No commit or push. Checker 2 and the consolidated demonstration/iteration
documentation update remain separate follow-up work; their earlier pending
records describe the previous attempt, not this successful direct doer run.
