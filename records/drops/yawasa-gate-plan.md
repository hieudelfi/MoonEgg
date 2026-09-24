# MoonEgg - yawasa gate for every task

**Sprint:** `2026-09-24-yawasa-gate` · **Task:** workflow setup (not a P/1-5 task) · **Started:** 2026-09-24

## Goal

Every MoonEgg task must leave a public record on the hub, not only inside the repo. Today the
8-step process in `CLAUDE.md` writes `records/<task-id>.md` locally and stops there. A reader who
is not in the terminal cannot see what a task intends to do before it runs, or what it produced
after. The goal is two published moments per task - a plan before code, an outcome after test pass -
both reachable from the project page on the hub.

## Scope

- **In:** two new gates in the project process; a fixed hub target for this repo; local drop files
  under `records/drops/`; slug, tag and folder conventions; templates; a worked test pair.
- **Out:** changing what the tasks themselves do; changing `docs/`; publishing anything for
  P.1-5.7 yet; touching the golden files or the pipeline.

## Approach

The repo keeps two kinds of artifact, and they do not replace each other:

| Artifact | Lives in | Audience | Written when |
| --- | --- | --- | --- |
| `records/<task-id>.md` | repo | the person doing the task | during the task, step by step |
| plan drop | hub | anyone reviewing | before the first line of work |
| outcome drop | hub | anyone reviewing | after the checks pass |

The plan drop is the design; the record is the log; the outcome drop is the report. The record
stays the place for raw numbers and step-by-step results, so the drops stay one screen each.

Hub target for this repo: `https://hub.yawasa.com/app/projects/moonegg`. Uploads carry
`--folder "MoonEgg" --create-folders` so they land in that project rather than the private
`Unpublished` drafts folder. Slugs are `moonegg-<task-id>-plan` and `moonegg-<task-id>-outcome`,
so the pair for a task is guessable from its ID. Tags always include `moonegg` plus the phase.

New shape of the process, with the two gates marked:

1. Read the task prompt and check dependencies.
2. Write the plan drop, read it cold, publish it. **Stop - wait for approval.**
3. Create `records/<task-id>.md`, run the checklist, run the tests, run the output checks.
4. Write the outcome drop, publish it. **Stop - wait for sign-off before "Xong".**

## Open questions

- Drop language is English, following the team standard for hub artifacts, while `docs/` and
  `records/` stay Vietnamese. If the reviewer prefers Vietnamese on the hub, this flips with one
  line in `CLAUDE.md` and costs nothing.
- The hub folder for this project may already exist under a different display name. The first
  upload will show which folder it resolved to, and the path can be corrected on the next push.
- Whether a task that fails its checks and is re-run needs a second outcome drop, or an update of
  the first one. Proposal: update the same slug, so the URL stays stable and the hub keeps the
  earlier version in its history.

## Definition of done

- [ ] `CLAUDE.md` has a numbered section naming the hub link, the folder, the slug rule, the tag
      rule and the exact publish command.
- [ ] The 8-step process in `CLAUDE.md` and in `prompts/00-START.md` both show the two new gates,
      and they do not contradict each other.
- [ ] Two template files exist under `records/drops/` so a task does not start from a blank page.
- [ ] A real plan drop and a real outcome drop are published and open at their URLs.
- [ ] Both drops appear at `https://hub.yawasa.com/app/projects/moonegg`.
