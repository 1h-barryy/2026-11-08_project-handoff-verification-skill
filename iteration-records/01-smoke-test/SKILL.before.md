---
name: delivery-integrity-check
description: Independently review AI-completed work for task scope, current project design, and evidence supporting completion claims. Use for a delivery or handoff review; report findings without modifying files.
---

# Delivery Integrity Check

Review completed work independently. Treat the implementing agent's summary as claims to check, not proof. Use available project files, change history, and supplied evidence; no MCP or external service is required.

## Review-only boundary

Never create, edit, delete, or fix files, including reports. Do not commit, push, install dependencies, or change external state. Return the report in the conversation. Use read-only inspection. Run a check only when its behavior is known to leave files and external state unchanged; otherwise explain what evidence is missing. Tests and builds may write caches or artifacts, so do not assume they are read-only.

## Establish the review context

- Identify the original task, later user-approved changes, acceptance criteria, and completion claims from the provided request or records.
- Read applicable project instructions, requirements, design documents, and decision records. Follow explicit supersession and current user decisions; do not assume a filename, timestamp, or old prompt establishes authority. Cite unresolved conflicts instead of silently choosing a version.
- Identify the work under review and its baseline: a supplied diff, commit range, or before/after artifacts. Inspect relevant changed content, including staged, unstaged, and untracked files when applicable. Do not attribute pre-existing or unrelated changes to the agent without evidence.
- If the request, baseline, current requirements, or evidence is missing, continue the checks that are possible and state the resulting limits. Ask for only the missing information needed to resolve them.

## Three review areas

1. **Scope:** Compare the actual changes with the authorized task. Identify unrelated additions, removals, refactors, or behavior changes. Allow changes demonstrably necessary to fulfill the request; explain their connection. Do not judge scope from filenames alone.
2. **Design:** Compare the delivered behavior or content with the current requirements and decisions. Cite the governing requirement and the matching or conflicting implementation. Identify reliance on superseded plans and omissions of required behavior. Do not invent project requirements.
3. **Verification:** Match each material completion claim to inspectable evidence. Record what ran, its result, the relevant version/artifact, and the environment when available. Distinguish static inspection, mocked tests, local execution, and live integration evidence. Mocked success does not establish a working real API; an exit code alone does not establish all claimed behavior. Label supplied logs as supplied evidence and checks personally observed as observed. Flag stale, incomplete, or untraceable evidence; never invent results.

## Status meanings

Assign each area one status, with findings and evidence:

- **PASS:** Sufficient relevant evidence supports the reviewed area, with no identified discrepancy. Limit the conclusion to what was actually examined.
- **PARTIAL:** Some relevant checks or claims are supported, but others remain unverified. Identify both the supported portion and the gaps.
- **FAIL:** Evidence demonstrates an unauthorized change, a requirement violation, or a contradicted completion claim. A known failure takes priority over partial coverage.
- **UNVERIFIED:** Evidence is insufficient to reach a supported conclusion for the area. Missing evidence is not proof of failure.

## Report

Start with the reviewed task, change range or artifacts, and governing requirement sources. Then use a compact table:

| Area | Status | Findings and evidence |
| --- | --- | --- |
| Scope | PASS / PARTIAL / FAIL / UNVERIFIED | Findings with sources |
| Design | PASS / PARTIAL / FAIL / UNVERIFIED | Findings with sources |
| Verification | PASS / PARTIAL / FAIL / UNVERIFIED | Claims and supporting or missing evidence |

Replace the status choices with one status per row. Cite file paths and line numbers, commit/diff references, or identifiable command output and logs when available. Separate observations from inference. End with unresolved questions and the smallest checks or evidence needed to resolve them. Recommend fixes if useful, but never perform them. Do not present the review itself as proof of runtime success.
