# Demonstrations

I ran both demonstrations in this repository on November 8, 2026. I chose these
tasks instead of the planned tasks in Market Under Stress and Financial Analyst
Arcade. Neither external project was tested.

Environment: Windows PowerShell, Python 3.14.3, local .venv. Git HEAD was
47a82d146e93f048fd0b67224692beaea6b763a2; most implementation files were already
untracked, so the patch and snapshots show the Demonstration 1 changes more
precisely than HEAD alone. No commit or push was made during those runs.

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

### My Evaluation

I agree with the checker's assessment. It reviewed the actual implementation changes and supporting test evidence rather than just trusting the doer's report. The three PASS results were reasonable based on what was verified.

## 2. README instructions for another project root — reviewed

### Independent Checker 2 — November 8, 2026

The task was to improve the README instructions for another local project root.
The doer had to call the registered tool first, check the instructions against
the code, run the relevant tests, and save the evidence.
The original user request is in
[demo2-direct.transcript.jsonl](iteration-records/02-hw8/demo2-direct.transcript.jsonl):1.
That request allowed the direct run to replace the pending attempt below.
The review used PROJECT_INTEGRITY_DESIGN.md:13–25: inspect the configured root
without changing it, and support findings with evidence. The task defined the
scope of this demonstration; the external projects planned at design lines 29–30
were not tested.

The checker compared the [before snapshot](iteration-records/02-hw8/demo2-direct-readme.before.snapshot)
and [after snapshot](iteration-records/02-hw8/demo2-direct-readme.after.snapshot)
using the [diff](iteration-records/02-hw8/demo2-direct-readme.diff).
The README diff against HEAD at the time also included earlier work. The checker
checked the claims in the [doer report](iteration-records/02-hw8/demo2-direct.result.md)
against the files and logs. Source line numbers below refer to the reviewed version.

| Area | Status | Findings and evidence |
| --- | --- | --- |
| Scope | PASS | The bounded diff changes only the agent-session instructions at README.md:87–116. Toolkit paths, target paths, reconnection, and the smoke-client example directly serve the request. Observed SHA-256 comparison of demo2-direct-before.hashes.json and demo2-direct-after.hashes.json found only README.md changed across the 12 recorded files. All 12 current files matched the after manifest before saving this report; both README snapshots matched their respective manifest hashes. Server, client, tests, and skill were unchanged. Evidence capture was explicitly authorized; the manifests exclude .git, .venv, __pycache__, and iteration-records/02-hw8, so this is not an exhaustive filesystem audit. |
| Design | PASS | README.md:87–116 matches server.py:275–285: the root is required, strictly resolved at startup, checked as a directory, and captured by a task-only tool. server.py:238 returns that root. smoke_client.py:13–26 launches its sibling server with sys.executable and a resolved root; lines 30–35 parse arguments and print the response. Observed C:/Users/Barry/.codex/config.toml:151–153 configures the toolkit Python and server with this toolkit as --project-root, supporting the local-registration statement. Restart/reconnect guidance follows from startup root capture. The instructions preserve the design's configured-root boundary and distinguish smoke execution from host configuration. |
| Verification | PASS | Supplied transcript lines 5–6 record the registered MCP invocation and returned output before the README patch at line 10. The display is truncated; demo2-direct.mcp.json preserves the supplied full payload. Supplied demo2-direct-tests.log and demo2-direct-tests.command.json record eight tests passing in 1.589 seconds, exit 0, using local .venv Python 3.14.3 on Windows; transcript line 11 corroborates the output. Observed tests/test_server.py:93–98 calls the real stdio client on a temporary root, asserts the returned root, and checks its file snapshot; lines 117–128 check scan-limit locations over stdio. The supplied diff-check command/log record exit 0 with no output. This supports the bounded claims, not a host switch or external-project run. |

The checker read the code and configuration and compared file hashes. It reviewed
the supplied test logs without rerunning tests, which create temporary files.
As demo2-direct.provenance.json explains, the transcript ends during evidence
capture, before the final turn was complete. The checker changed no host settings,
source, README, tests, or skill. At my request, it saved its report in this file.
That was an exception to the skill's usual rule against writing reports.

The review did not verify reconnecting the registered host to another root. That
would need the changed launch arguments and a tool response with the intended
absolute project_root after reconnection. The C:/tools and D:/work paths are
placeholders and were not run as written. The documentation claims did not need
another runtime check. A stop instruction was sent to the old pending task, but
its final state still needs a host-state check if closure must be confirmed.
The earlier pending records describe that attempt, not the completed direct run.
This review did not establish that the whole toolkit or submission was complete.

### My Evaluation

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

The call has no returned result in that capture. The saved
[host state](iteration-records/02-hw8/demo2-pending.host-state.json) reports
**waitingOnApproval**, even after the user reported resolving approval twice.
At that point, the README was unchanged and there was no completed change for
Checker 2 to review. The direct run and review above replaced this blocked attempt.

The earlier recovery instruction was to resume **HW8 Demonstration 2 — README doer**, task
**01a1bd58-6551-7a20-a1d5-d135443161aa**, at its pending MCP tool approval.
The plan was to save the completed transcript and README diff, then start a fresh
read-only checker using **$delivery-integrity-check**. If the task could not resume,
it was to be stopped before starting a replacement, to avoid two writers.
The pending capture was kept alongside the later direct-run evidence.

## Session and verification records

The sessions listed below were created with the Codex host's create_thread.
Each received a specific task and file paths. The coordinator saved the reports
for Checker 1 and the skill rerun. Checker 2 saved its findings above at my request;
its session provenance is not saved here.

| Run | Session ID |
| --- | --- |
| Original doer | 01a1bd4e-4f08-7033-9c3c-4d54680aa418 (first completed turn) |
| Checker 1 | 01a1bd55-b642-7da3-b065-124a45d57657 |
| Skill rerun | 01a1bd57-4dac-7443-9eed-cde03d4b4507 |
| Doer 2, pending | 01a1bd58-6551-7a20-a1d5-d135443161aa |

See the [evidence index](iteration-records/02-hw8/INDEX.md) for exports, snapshots,
commands, final verification results, and the scope of hash checks.

Both demonstrations and my evaluations are recorded above. My overall reflection
is in ITERATION.md. Testing across other projects and the host root-switch check
remain open.
