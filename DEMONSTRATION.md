# Demonstrations

These are the actual toolkit-local runs from November 8, 2026. The current
request replaces the earlier planned tasks for Market Under Stress and Financial
Analyst Arcade with two tasks in this repository. Neither external project was tested.

Environment: Windows PowerShell, Python 3.14.3, local .venv. Git HEAD was
47a82d146e93f048fd0b67224692beaea6b763a2; most implementation files were already
untracked. The recorded patch and snapshots, not HEAD alone, establish the
Demonstration 1 change. No commit or push was made.

## 1. More precise MCP source locations

Task: improve source locations for file-scanning limits without changing scan
behavior or boundaries. Before editing, the doer called the registered
**project-context.inspect_project_context** with this exact task:

> Inspect this MCP project's file scanning limits and scan boundaries. Identify the relevant implementation and tests, and locate the exact source definitions of the limits so source-location reporting can be improved without changing existing behavior or boundaries.

The [actual transcript](iteration-records/02-hw8/demo1-doer.transcript.jsonl)
contains the call and response at lines 6–7. The response found server.py and
reported the limits, but its three excerpts missed their definitions.

The [recorded patch](iteration-records/02-hw8/demo1-doer.patch) changed server.py,
tests/test_server.py, and five README lines. It adds a bounded list of Python
constant definitions from already-read text, with names, paths, and line excerpts.
Scan limits and existing matching logic stay unchanged.

The transcript records eight passing tests (line 12) and a real stdio rerun
(line 15). The latter returned MAX_ENTRIES, MAX_FILES, MAX_BYTES, and
MAX_TOTAL_BYTES at server.py:27–30, including “MAX_BYTES = 128 * 1024”.
These are local MCP results, not external-project or live API tests.

A fresh independent checker used **$delivery-integrity-check**. Its
[report](iteration-records/02-hw8/checker1.result.md) and
[transcript](iteration-records/02-hw8/checker1.transcript.jsonl) are preserved.

| Area | Result | Relevant finding |
| --- | --- | --- |
| Scope | PASS | Constant evidence, two tests, and README documentation fit the task. |
| Design | PASS | Bounded static evidence uses already-read files and reports truncation. |
| Verification | PASS | Supplied logs support eight tests and exact locations over real stdio. |

Checker excerpt: “Runtime results above are supplied evidence, not independently
rerun tests.” It performed read-only inspection and hash comparisons. The
coordinator's before/after project hashes also match.

TODO (my review): Do I agree with Checker 1? Did the new locations reduce the
extra source inspection I needed?

## My Evaluation
I agree with the checker's assessment. It reviewed the actual implementation changes and supporting test evidence rather than just trusting the doer's report. The three PASS results were reasonable based on what was verified.

## 2. README instructions for another project root — reviewed

### Independent Checker 2 — November 8, 2026

Reviewed task: make a small README-only improvement for using the MCP with
another local project root, inspect with the registered tool before editing,
verify against implementation, run relevant tests, and preserve actual evidence.
The original user request is in
[demo2-direct.transcript.jsonl](iteration-records/02-hw8/demo2-direct.transcript.jsonl):1.
It explicitly authorizes the direct doer run, superseding the pending attempt
described below. The governing design is PROJECT_INTEGRITY_DESIGN.md:13–25
(configured-root, read-only local inspection and evidence-based checking), with
the current task determining this demonstration's scope. The original external
project plan at design lines 29–30 is not evidence those projects were tested.

Baseline: [before snapshot](iteration-records/02-hw8/demo2-direct-readme.before.snapshot)
to [after snapshot](iteration-records/02-hw8/demo2-direct-readme.after.snapshot),
using the [bounded diff](iteration-records/02-hw8/demo2-direct-readme.diff).
The large README diff against Git HEAD includes earlier work and is not the
Demonstration 2 change. Completion claims were checked from the
[doer report](iteration-records/02-hw8/demo2-direct.result.md), not accepted as proof.

| Area | Status | Findings and evidence |
| --- | --- | --- |
| Scope | PASS | The bounded diff changes only the agent-session instructions at README.md:87–116. Toolkit paths, target paths, reconnection, and the smoke-client example directly serve the request. Observed SHA-256 comparison of demo2-direct-before.hashes.json and demo2-direct-after.hashes.json found only README.md changed across the 12 recorded files. All 12 current files matched the after manifest before saving this report; both README snapshots matched their respective manifest hashes. Server, client, tests, and skill were unchanged. Evidence capture was explicitly authorized; the manifests exclude .git, .venv, __pycache__, and iteration-records/02-hw8, so this is not an exhaustive filesystem audit. |
| Design | PASS | README.md:87–116 matches server.py:275–285: the root is required, strictly resolved at startup, checked as a directory, and captured by a task-only tool. server.py:238 returns that root. smoke_client.py:13–26 launches its sibling server with sys.executable and a resolved root; lines 30–35 parse arguments and print the response. Observed C:/Users/Barry/.codex/config.toml:151–153 configures the toolkit Python and server with this toolkit as --project-root, supporting the local-registration statement. Restart/reconnect guidance follows from startup root capture. The instructions preserve the design's configured-root boundary and distinguish smoke execution from host configuration. |
| Verification | PASS | Supplied transcript lines 5–6 record the registered MCP invocation and returned output before the README patch at line 10. The display is truncated; demo2-direct.mcp.json preserves the supplied full payload. Supplied demo2-direct-tests.log and demo2-direct-tests.command.json record eight tests passing in 1.589 seconds, exit 0, using local .venv Python 3.14.3 on Windows; transcript line 11 corroborates the output. Observed tests/test_server.py:93–98 calls the real stdio client on a temporary root, asserts the returned root, and checks its file snapshot; lines 117–128 check scan-limit locations over stdio. The supplied diff-check command/log record exit 0 with no output. This supports the bounded claims, not a host switch or external-project run. |

Evidence classification: implementation/configuration reads and hash comparisons
were personally observed by this checker. Runtime results are supplied evidence,
not independently rerun tests. The transcript export ends during evidence capture
as stated in demo2-direct.provenance.json; it is not a complete final-turn export.
The checker ran no tests because they create temporary files. No host setting,
reviewed source, README, test, or skill was changed. The sole report write to this
file follows the user's explicit save instruction, an exception to the skill's
normal no-report-writing boundary; this run is not literally a zero-write run.

Unresolved limits and smallest follow-ups: there is no evidence of changing and
reconnecting the registered host to a different root. If that outcome is later
claimed, supply the changed launch arguments and a post-reconnection tool response
whose absolute project_root matches the intended directory. The placeholder
C:/tools and D:/work commands were not executed verbatim. No further runtime check
is needed to support the narrower documentation claims reviewed here. The old
pending host task's final state is not established by its stop instruction; inspect
that task's current host state if closure must be established. ITERATION.md and the
historical notes below still describe the earlier pending attempt; they do not
override the direct-run evidence. Full toolkit/submission completion is outside
this review. Personal agreement and final reflection remain for the author.

## My Evulation

I agree with the checker's assessment. The MCP tool was successfully called, all 8 tests passed, and git diff --check found no issues. The server, checker skill, and tests remained unchanged, so the README update stayed within the intended scope.

However, using the MCP with a different project root was documented but not actually tested in another environment. I would still consider that part unverified.

### Earlier pending attempt (historical record)

Task: improve only README instructions using the actual server.py and
smoke_client.py: distinguish toolkit executable paths from the inspected root,
explain startup/reconnection, and confirm the returned project_root.

A separate doer session was started. Its
[captured transcript](iteration-records/02-hw8/demo2-pending.transcript.jsonl)
contains the actual attempted **project-context.inspect_project_context** call
and complete task argument. Argument excerpt:

> Improve only README.md instructions for using our MCP with a different project root, based on actual server.py and smoke_client.py.

The call has no returned result in that capture. The
[host state](iteration-records/02-hw8/demo2-pending.host-state.json) still reports
**waitingOnApproval**, even after the user reported resolving approval twice.
At that capture, the README was unchanged from its saved baseline. This was an attempted call,
not a successful demonstration. Checker 2 had not yet run because there was no
completed change to review. The direct run and review above supersede that status.

The earlier recovery instruction was to resume **HW8 Demonstration 2 — README doer**, task
**01a1bd58-6551-7a20-a1d5-d135443161aa**, at its pending MCP tool approval.
After the real call returns and the doer finishes, save its complete transcript
and README diff, then start a new read-only checker session with
**$delivery-integrity-check**. Add completed records without replacing the
pending capture. If the host cannot resume it, stop that task before starting
a replacement fresh doer session to avoid two writers.

TODO (after completion): Record Checker 2's actual findings and my agreement.

## Session and verification records

Separate sessions were created with the Codex host's create_thread, not by
simulating reports in the coordinator. Each received a bounded task and artifact
paths. The coordinator saved reports; the checkers did not write them.

| Run | Session ID |
| --- | --- |
| Original doer | 01a1bd4e-4f08-7033-9c3c-4d54680aa418 (first completed turn) |
| Checker 1 | 01a1bd55-b642-7da3-b065-124a45d57657 |
| Skill rerun | 01a1bd57-4dac-7443-9eed-cde03d4b4507 |
| Doer 2, pending | 01a1bd58-6551-7a20-a1d5-d135443161aa |

See the [evidence index](iteration-records/02-hw8/INDEX.md) for exports, snapshots,
commands, final verification results, and the scope of hash checks.

TODO (my final reflection): Explain what these runs showed, what I agree with,
and what still needs testing. Demonstration 2 and the final submission review
are not complete.
