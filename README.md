# Project Integrity Toolkit

A review-only checker skill and a local project-context MCP server.

## Why I Built This

When I return to an existing project or start a new AI session, I often have to
explain the structure and previous decisions again. An agent can follow an old
plan, change something outside the task, or say something works when only mocked
tests have passed.

I ran into these problems in earlier projects. In Market Under Stress, `DESIGN.md`
needed to take priority over older plans. In Financial Analyst Arcade, passing
local tests did not mean the live API worked. As I explain in my
[design document](PROJECT_INTEGRITY_DESIGN.md), I built this toolkit to find the
right context before making changes, then check the work against the task,
current decisions, and test evidence.

## Old Prompt Log Evidence

These excerpts from my earlier prompt logs show the problems behind this project.
They were checked against the linked source lines.

- **Project structure:** “Map the repo: folder structure, entry points, build tooling, dependencies (versions), and how it runs locally.” ([Market Under Stress, line 24](https://github.com/1h-barryy/market-strategy-lab/blob/main/promptlog.txt#L24)) This is the recurring context-gathering task that motivated the MCP inspector.
- **Design decisions:** “Read DESIGN.md first. It is the single source of truth for this project (v0.3).” ([Market Under Stress, line 53](https://github.com/1h-barryy/market-strategy-lab/blob/main/promptlog.txt#L53)) The rest of that instruction gives it priority over the older `TECH_SPEC.md` and `ASSET_BRIEF.md`. This motivated checking which requirements govern the work.
- **Verification:** “Clearly mark live integrations as unverified until credentials are configured and requests succeed.” ([Financial Analyst Arcade, line 82](https://github.com/1h-barryy/2026-09-19_ArcadeFinancialAnalyst/blob/main/prompt_log.md#L82)) This motivated separating observed results from assumptions and unsupported completion claims.

## MCP v0.1

`server.py` exposes exactly one tool, `inspect_project_context(task)`, using the
[official Python SDK](https://py.sdk.modelcontextprotocol.io/) and stdio.
The local environment uses Python 3.14.3 and `mcp==2.3.0`, pinned in
`requirements.txt`. The installed SDK declares Python 3.10+; other Python
versions have not been verified here.

Install locally from the repository root (PowerShell, with uv installed).
Skip environment creation if `.venv` already exists:

```powershell
uv venv .venv
uv pip install --python .venv/Scripts/python.exe -r requirements.txt
```

Run the server with an explicit project root:

```powershell
.venv/Scripts/python.exe -B server.py --project-root "E:/path/to/project"
```

This waits for MCP messages on stdin; it is not an interactive text prompt.
The tool's only argument is `task`; callers cannot select another root.
The root is resolved at startup, relative to the launching directory if needed.
No Codex registration is required for the local smoke client:

```powershell
.venv/Scripts/python.exe -B smoke_client.py --project-root . --task "Change inspect_project_context file scan limits and report their impact"
.venv/Scripts/python.exe -B -m unittest discover -s tests -v
```

On macOS/Linux, use `.venv/bin/python` in place of `.venv/Scripts/python.exe`.
The client launches and closes the server, checks that only the intended tool is
exposed, and prints its actual structured response.

Results separate `verified_findings` (paths, line excerpts, manifest declarations)
from `assumptions` (keyword relevance, likely entry points, candidate import
relationships and shared-file impact). All file paths are relative to the returned
absolute `project_root`. `coverage` reports skipped files and truncation.
`verified_findings.python_constant_definitions` lists module-level uppercase
Python assignments in task-related files, with names, paths, and line excerpts.
It uses already-inspected text, returns at most 20 definitions, and reports
truncation in `coverage.output_truncated.constant_definitions`. These are static
assignment locations, not verified runtime values.

Inspection never executes project code or modifies project files. It does not use
an external API. It skips links/junctions, common dependency/build directories and
credential filenames, and limits file counts and bytes read. This is a static inspector
for trusted, stable local checkouts, not a sandbox or a secret scanner.
It reads UTF-8 text, does not interpret `.gitignore`, and matches basic Python and
JS/TS local imports. Dynamic imports, aliases, full dependency resolution, runtime
behavior and exhaustive impact analysis remain unverified. Other languages can
still appear through file names, keyword excerpts and manifests.

The checker lives in `.agents/skills/delivery-integrity-check/SKILL.md` and is
independent of this server. Neither component is registered automatically.

## Use the MCP in an agent session

Configure the host to launch the Python environment installed for this toolkit.
Keep the executable and server script in the toolkit directory; only
`--project-root` points to the project you want to inspect. For example, replace
these absolute paths with your own (the target must be an existing directory):

```text
Command: C:/tools/project-context/.venv/Scripts/python.exe
Arguments: -B C:/tools/project-context/server.py --project-root D:/work/customer-app
```

The existing local `project-context` registration already targets this toolkit.
Change its launch arguments and restart or reconnect the server to select another
root. `inspect_project_context` accepts only `task`; putting a path in the task
does not switch roots. Relative roots resolve against the server's launch working
directory, so use absolute paths to avoid inspecting the wrong directory. In host
settings with an argument list, enter each argument separately, keeping a path
containing spaces as one argument.

You can check another root without changing host registration by running the
smoke client from PowerShell (replace these example paths):

```powershell
& "C:/tools/project-context/.venv/Scripts/python.exe" -B "C:/tools/project-context/smoke_client.py" --project-root "D:/work/customer-app" --task "Find entry points and dependency declarations"
```

The client launches the toolkit's server, makes a real stdio tool call, and prints
the response. Confirm its absolute `project_root` matches your intended target.
After reconnecting the host, also confirm `project_root` in the registered tool's
response; the smoke client does not update or verify the host's configuration.

Ask the agent: “Call `project-context.inspect_project_context` with task
`Change the file scanning limits in our MCP server.` Report the actual output
and confirm the call succeeded. Do not modify files.”

Seeing the tool listed does not prove it ran. Check the returned paths,
excerpts, assumptions, and coverage before making changes.

## Use the checker skill

Start a separate, fresh agent session with access to the project being reviewed
and [SKILL.md](.agents/skills/delivery-integrity-check/SKILL.md). Ask it to read
and follow that file. Provide the original task, current design and requirements,
a diff or before/after files, and actual test results.

Example: “Use `delivery-integrity-check` to review the supplied task and changes
against the current project design. Report scope, design, and verification with
file evidence. Do not edit files.”

The checker returns `PASS`, `ISSUE`, or `UNVERIFIED` for each area in the
conversation. It does not fix files, save reports, commit, or push. MCP output
can supply context, but the checker does not require the MCP.

## Project files

- `server.py`, `smoke_client.py`, `requirements.txt`: MCP implementation, local client, and dependency pin.
- `tests/test_server.py`: existing tests, including a real local stdio call.
- `.agents/skills/delivery-integrity-check/SKILL.md`: review-only skill.
- [PROJECT_INTEGRITY_DESIGN.md](PROJECT_INTEGRITY_DESIGN.md): scope and completion criteria.
- [DEMONSTRATION.md](DEMONSTRATION.md): both demonstrations, checker findings, and my evaluations.
- [ITERATION.md](ITERATION.md): the failure, skill revision, rerun, and my reflection.
- [iteration-records/01-smoke-test/](iteration-records/01-smoke-test/): preserved original skill and first review; not a post-revision rerun.

## AI Usage & References

- **ChatGPT:** Brainstorming, reviewing problems from previous projects, defining the design, and planning the workflow.
- **Codex CLI:** Implementing the checker skill, Python MCP server, tests, registration, and documentation preparation.
- **Me:** Choosing the direction, setting constraints, reviewing results, and making design decisions. The documentation is AI-assisted; the evaluations and reflections are my own.

Technical references used for this project:

- [Agent Skills specification](https://agentskills.io/specification): the `SKILL.md` format, metadata, and instructions.
- [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture): hosts, clients, servers, and tool discovery versus execution.
- [Official MCP Python SDK](https://py.sdk.modelcontextprotocol.io/): the SDK used by the server and local client. The project pins its installed version in `requirements.txt`.

## Remaining Work

- Test the host's switch to another project root and try the toolkit on more projects.
- Save Checker 2's session provenance and update the evidence checker, which still expects the earlier README snapshot.
- Confirm the course's final submission requirements and submit the public repository link. No new prompt log is needed.
