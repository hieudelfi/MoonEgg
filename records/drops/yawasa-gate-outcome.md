# MoonEgg - yawasa gate for every task - outcome

**Sprint:** `2026-09-24-yawasa-gate` · **Plan:** https://hub.yawasa.com/app/p/moonegg-yawasa-gate-plan
**Finished:** 2026-09-24 · **Checked by:** pending review · **Commits:** none yet - the repo is not a git repo until task P.1

## What was built

- `CLAUDE.md` section 7 "Day ban ke hoach va ban ket qua len yawasa": the project page link, the
  `--project "moonegg"` rule, the slug rule, the tag rule, the full publish command, the cold-read
  gate and the carve-out for surface-level fixes. It was added as a NEW section 7 on purpose - sections 3 and 4
  are quoted by name inside all 61 task prompts, so renumbering them would have broken those
  references.
- `CLAUDE.md` section 2: the task process went from 8 steps to 10. Step 2 is now gate A (plan drop,
  then stop), step 9 is gate B (outcome drop, then stop).
- `prompts/00-START.md`: the same process, now 11 numbered steps with four pause marks instead of
  three. The short prompt for later sessions was corrected from "8 steps" to "11 steps", so a
  session that only reads the short prompt still gets the gates.
- `records/drops/TEMPLATE-plan.md` and `records/drops/TEMPLATE-outcome.md`: one-screen skeletons.
  The plan template forces a Risks-and-assumptions section; the outcome template carries the same
  real-numbers test table that `records/TEMPLATE.md` already demands, so the two never disagree.
- `README.md`: `records/drops/` added to the folder tree.

## Test results

| Check | How | Real output | Pass |
| --- | --- | --- | --- |
| Hub reachable, token valid | publish this pair | `>> hub reachable: https://hub.yawasa.com`, HTTP 200 twice | yes |
| Plan drop published | `exp-publish.sh ... --slug moonegg-yawasa-gate-plan` | https://hub.yawasa.com/app/p/moonegg-yawasa-gate-plan | yes |
| Outcome drop published | same command, outcome slug | this page | yes |
| First attempt: `--folder "MoonEgg" --create-folders` | open `/app/projects/moonegg` | project page empty - wrong mechanism, see Deviations | no |
| Second attempt: `--project "moonegg"` | re-publish both with `--update` | hub accepted, no `unknown-project` / `forbidden-project` error | yes |
| Both drops on the project page | open `/app/projects/moonegg` | **needs a human with a browser session** | pending |
| Process files agree | read section 2 of `CLAUDE.md` against `00-START.md` | both show gate A before work and gate B before "Xong" | yes |

## Deviations from the plan

- The plan said the two gates would be steps 2 and 4 of a four-line summary. In `CLAUDE.md` they
  landed as steps 2 and 9 of ten, and in `00-START.md` as steps 4 and 11 of eleven, because the
  start prompt already had a task-confirmation pause of its own. The shape is the same; only the
  numbers differ between the two files, which is expected - one is the standing rule, the other is
  the session script.
- **The first publish used the wrong mechanism.** It passed `--folder "MoonEgg"
  --create-folders`, which files a drop into a folder of the uploader's own library. A project is
  a different object. The hub answered `200 uploaded successfully` both times, so nothing in the
  terminal looked wrong - the reviewer found the empty project page. The flag that actually links
  a drop to a project is `--project "moonegg"`, added to `exp-publish` on 2026-09-19; the local
  copy of the skill was eight days behind and did not have it. Fixed by fast-forwarding
  `~/.claude/skills` and re-publishing both drops with `--update`, which kept the two URLs.
- The plan assumed the hub API could confirm where an upload landed. It cannot: the hub exposes
  `/api/upload`, `/api/drop/<slug>/md` and `/api/drop/<slug>/prompt`, and the `/app/projects/...`
  route answers `401 unauthenticated` to an API token because app routes use browser sessions.
  This is why the wrong destination went unnoticed until a human looked.

## What was learned

- **Folder and project are two different objects on this hub.** `--folder` files a drop inside
  the uploader's own library; `--project` links it to a project page and, by default, shares it
  with that project's members. Passing the wrong one is not an error - it succeeds, in the wrong
  place. So "upload successful" is not evidence; only the project page is.
- Without either flag an upload lands in a private `Unpublished` drafts folder, which is why the
  standing rule names the flag instead of leaving it to memory.
- The local skills checkout can lag the hub's API. When a documented flag is missing, run the
  `update-yawasa` skill before working around it.
- `--update` is what keeps a drop's URL stable across revisions; the hub snapshots the previous
  body into its own version history. A revision without the flag mints `-2` and quietly strands
  the link already given to the reviewer.

## Follow-ups

- Confirm on `https://hub.yawasa.com/app/projects/moonegg` that both drops are now listed there.
- The empty `MoonEgg` folder created by the first attempt is still in the personal library and can
  be deleted from the hub UI. Nothing points at it.
- Consider `--section` to split later drops into plans and outcomes inside the project, once the
  project has more than a handful of pages.
- Decide the drop language. English is in place now, following the team standard for hub
  artifacts. Vietnamese is a one-line change in section 7.4.
- The first real pair is P.1. Nothing else in the repo changes until its plan drop is approved.
