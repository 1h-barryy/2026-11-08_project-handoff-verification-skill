# Project Integrity Toolkit — Design

## 1. Idea

When I work on an old project or open a new AI session, I often have to explain the same decisions again. Sometimes an agent follows an outdated plan, changes things I didn't ask for, or says something works when it has only been tested with mock data.

I've run into this in my previous assignments. **Market Under Stress** had different versions of the design, and the newer `DESIGN.md` needed to take priority. In **Financial Analyst Arcade**, passing mocked tests did not mean the real API was working.

I want a small toolkit I can reuse with Codex or Claude Code: **find the right project context, then check whether the finished work actually matches it.**

## 2. What I'm building

**MCP tool — `inspect_project_context(task)`**

A small local Python MCP server using the official SDK and stdio. Before changes, it inspects only a configured project root for structure, likely entry points, task-related files, dependency declarations, and shared areas that may be affected. Results include real paths and line evidence, separating observed facts from assumptions and reporting inspection limits. It uses bounded, read-only file inspection: no vector database, external API, or automatic code changes. v0.1 is tested locally before registration in Codex.

**Checker skill — `delivery-integrity-check`**

A `SKILL.md` that tells a separate agent how to review finished work. It checks:

- **Scope:** Did the agent change something outside the request?
- **Decisions:** Does the result conflict with the current project requirements, rather than an outdated version?
- **Evidence:** Are claims like “tested” or “working” supported by actual results, not just mock tests or assumptions?

The checker **only reports** `PASS`, `ISSUE`, or `UNVERIFIED`, with evidence. It never edits or fixes the project.

## 3. How I'll test it

1. **Market Under Stress:** Make a small, real update to its project description using the design records. Run the checker in a fresh session.
2. **Financial Analyst Arcade:** Make a short handoff/update that distinguishes the local game from the Web Edition backend. Check the project boundaries and any claims about live API testing.

For both runs I'll save the MCP calls, the actual work, and the checker report. If the tool or skill gets something wrong, I'll change it and run the test again. The failure and improvement must come from what actually happens.

## 4. Done when

- The MCP runs locally, is registered, and an agent actually calls it.
- Context results point to real project files; assumptions, missing information, and inspection limits are reported honestly.
- The checker runs in a separate, fresh session and makes no changes.
- Two real tasks are demonstrated, with a recorded failure, revision, and rerun.
- A new public GitHub repo contains the skill, MCP code, setup instructions, and the required `README.md`, `DEMONSTRATION.md`, and `ITERATION.md`.
- I use 2–3 lines from my HW3–HW7 prompt logs as the original problem evidence, and write my own submission reflections.

## 5. Scope

For this version, I'll start with **two projects, one MCP tool, and one checker skill**. No full RAG database, automatic code fixes, deployment, or GitHub write access. The goal is to make a small workflow that works, not build a whole agent platform.
