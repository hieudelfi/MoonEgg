# MoonEgg <task-id> - <task name>

**Task:** `<task-id>` · **Phase:** `<phase>` · **Prompt:** `prompts/<phase>/<task-id>.md` · **Started:** <YYYY-MM-DD>
**Refs:** FR-xx · Architecture SS<x.y> · Tests TC-xx-nn · Depends on: <task ids, or "none">

## Goal
One or two sentences. The outcome this task must produce, not the list of steps.
Say what becomes possible after it that was not possible before.

## Scope
- **In:** ...
- **Out:** ... (name the nearby thing a reader would expect and is NOT doing)

## Approach
Design sketch in two or three short paragraphs, or a small table. No code.
Name the tools, the data sources and the file paths that will be created.
If the task chooses between options, say which one and why in one line.

## Risks and assumptions
- Assumption: ...
- Risk: <what could go wrong> - <what we do then>
Or: "None known." Never leave this section out.

## Definition of done
Copy the checklist from the task prompt, plus the output checks from CLAUDE.md SS3.
- [ ] ...
- [ ] Test <TC-xx-nn> passes with real numbers written into `records/<task-id>.md`
- [ ] ...

## Open questions
- ...
Or: "None."
