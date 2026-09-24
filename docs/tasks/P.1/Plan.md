# Plan - P.1 Repo, CI, licence scan

Status: **not started**, stopped at Gate A, waiting for review.
Task: `P.1` · Prompt: `prompts/phase-P/P.1.md` · Record: `records/P.1.md`
Branch: `chore/p1-repo-ci`, cut from `main` at `cf4c66a`.
Reviewer: `self`
Type: **INFRA** - build tooling, no product behaviour
Level: **L2** - adds logic branches in CI and a gate that can block every later task
Repro: not applicable, this is not an ISSUE
User-visible behaviour: no Flow.md. INFRA, nothing a learner sees changes.
Refs: `docs/09` section 3P.1 row P.1 · `docs/07` section 2 · `docs/01` section 13.2 · Tests TC-CP-01, TC-CP-02
Depends on: none. First task of phase P.

**Decisions log:**
1. 2026-09-24 - Step 1 of the prompt (`git init`, first commit) is already done, outside the
   process, at commit `1736b31`. Agreed with the reviewer: this Plan records it as done and P.1
   covers only what is left. The repo is not re-initialised.
2. 2026-09-24 - Commit tag set fixed at `feature` / `bug` / `docs`. This task uses `feature`.
3. 2026-09-24 - CI pins Python to **3.11**, not the 3.14 on this machine. Reviewer chose the safe
   option: Kokoro and torch, needed at P.3, may not have wheels for 3.14 yet. CI should run the
   version the pipeline tasks can certainly use.
4. 2026-09-24 - Vitest goes into `sdk-allowlist.md` with a **dev only** note. The file stays the
   single list, and the note says the package never reaches the bundle.
5. 2026-09-24 - Branch protection stays off, reason recorded. Instead, a task closes by merging its
   branch into `main` after the tests pass, before the next task starts. Added to `CLAUDE.md`
   section 7.4.
6. 2026-09-24 - Closing a task now goes through a **pull request**, not a local merge: open the PR
   after Gate B, wait for CI, merge with a merge commit, delete the branch. Written as
   `CLAUDE.md` section 7.8 with a PR template at `.github/pull_request_template.md`.
7. 2026-09-24 - This branch carries two process changes as well as P.1 itself, because the rules
   were written while the branch was already open. Its PR therefore contains both. From P.2 on,
   a process change gets its own branch.

Out of scope: any content pipeline work (P.3), the Supabase and R2 setup (P.2), writing real tests.
CI runs empty test suites on purpose; real tests arrive with the tasks that need them.

> **Language rule (B1/B2):** short sentences, 20 words or fewer. Active voice. One idea per sentence.

---

## 0. Does this task need a Flow.md?

No. Type is INFRA and no screen exists yet. Any deliberate behaviour note goes in section 5.

## 1. Goal

A change that breaks a rule should fail before a human reads it. After this task, every push runs
the data checker, the web test runner and a licence scan, and a package with a licence outside the
allowlist stops the build. Phase P can then move without anyone remembering to check by hand.

## 2. Starting point, checked today

Commands were run today on this machine; the output below is real, not remembered.

| Thing | State today | Evidence |
| --- | --- | --- |
| Repo | exists, private, 3 commits on `main` | `git log --oneline`, `gh repo view` |
| `.github/` | does not exist | `ls -A .github` returns "No such file or directory" |
| `web/`, `mobile/` | both empty directories | `ls -A web mobile` prints nothing |
| node, npm | v24.13.0, 11.6.2 | `node --version`, `npm --version` |
| python | 3.14.2 | `python --version` |
| flutter, dart | **not installed** | `command -v flutter` finds nothing |
| `tools/checks/verify_pack.py` | works, 30 rows, 0 errors, 2 warnings | see the bug below |
| `tools/checks/license-allowlist.txt` | 17 licence strings | `grep -c . tools/checks/license-allowlist.txt` |
| `tools/checks/sdk-allowlist.md` | 11 package rows | `grep -c '^| [a-z@]' tools/checks/sdk-allowlist.md` |
| Branch protection | **not available on this plan** | `gh api .../rulesets` returns `403 Upgrade to GitHub Pro or make this repository public` |

**Bug found while checking:** `verify_pack.py:41` prints Vietnamese text. On a Windows console the
default code page is cp1252, so the print raises `UnicodeEncodeError` and the script exits 1 even
when the data has no errors. With `PYTHONIOENCODING=utf-8` the same file reports
`30 bản ghi · 0 lỗi · 2 cảnh báo` and exits 0. `CLAUDE.md` section 3 requires this script before
closing any data task, so every data task on Windows would report a false failure.

## 3. Flow

```mermaid
graph TB
    A["push or pull request"]:::amber --> B["job python: pytest tools/checks"]:::green
    A --> C["job web: npm test"]:::green
    A --> D["job mobile: skipped, no flutter"]:::grey
    A --> E["job license: scan against allowlist"]:::green
    B --> F["all green, merge allowed"]:::cyan
    C --> F
    E --> F
    E --> G["licence outside allowlist, build fails"]:::red

    classDef amber fill:transparent,stroke:#f4b860,stroke-width:2px,color:#fff
    classDef green fill:transparent,stroke:#c4f47c,stroke-width:2px,color:#fff
    classDef cyan fill:transparent,stroke:#7cc4ff,stroke-width:2px,color:#fff
    classDef red fill:transparent,stroke:#fca5a5,stroke-width:2px,color:#fff
    classDef grey fill:transparent,stroke:#888,stroke-width:2px,color:#fff
```

Four jobs, one of them dormant until Flutter is installed.

## 4. Plan of work

### 4.1 `tools/checks/verify_pack.py` - required, fix first

Force UTF-8 on the script's own output, so the exit code reports the data and not the console code
page. One line near the top, guarded so it does nothing on a platform that is already UTF-8. Fixed
before CI is written, because CI will call this script.

### 4.2 `web/` - required

`npm create vite@latest web -- --template react-ts`, then add Vitest with one test that asserts
`true`. Dependencies must stay inside `tools/checks/sdk-allowlist.md`: react, react-dom, vite,
typescript are listed. Vitest gains a row in the same file marked **dev only**, so the allowlist
stays the single list and a reader can see at a glance that it never reaches the bundle.

### 4.3 `mobile/` - placeholder only

Flutter is not installed, so `flutter create` cannot run. `mobile/README.md` records what the
folder will hold and which task fills it. The CI job exists but is skipped by a guard, so turning
it on later is one line, not a new job.

### 4.4 `.github/workflows/ci.yml` - required

Four jobs, each able to run alone:

| Job | Runs | Fails when |
| --- | --- | --- |
| `python` | `pytest tools/checks` on **Python 3.11**, with `PYTHONIOENCODING=utf-8` | a check fails |
| `web` | `npm ci`, then `npx vitest run` in `web/` | a test fails |
| `mobile` | guarded, skipped while there is no `mobile/pubspec.yaml` | never, for now |
| `license` | `npm ci`, then `npx license-checker --json` in `web/`, compared with the allowlist | a package is outside the allowlist, or reports `UNKNOWN` |

The licence job reads `tools/checks/license-allowlist.txt` rather than holding its own copy, so
the list has one home.

### 4.5 Branch protection - record the reason, do not buy

The API refuses rulesets on a private repo on this plan. The prompt allows "protected, or write
down why not". Written down here and in the record. The gate that matters right now is the human
one at Gate B; protection can be turned on later if the repo goes public or the plan changes.

### Options considered, not chosen

- Make the repo public to get branch protection. Rejected: the repo holds unreleased content plans
  and the team default is private.
- Write the licence check as a shell pipeline inside the workflow. Rejected: it belongs in
  `tools/checks/` where a person can run it locally before pushing.
- Install Flutter now to fill `mobile/`. Rejected: it is P.3 and phase 3 work, and it would add an
  hour to a 1.5 day task for nothing usable today.

### Do not touch

- `docs/01..09`, `golden/`, `content/`, `prompts/`.
- `tools/pipeline/build_lexicon.py`. Only the checker changes, and only its output encoding.
- The three commits already on `main`.

## 5. Situations and edge cases

| # | Situation | Expected behaviour |
| --- | --- | --- |
| 1 | Windows console, cp1252 | checker prints correctly and exits on the data, not the encoding |
| 2 | `mobile/` still empty | mobile job skips, whole run still reports green |
| 3 | A GPL package is added to `web/` | licence job fails, and says which package and which licence |
| 4 | `license-checker` reports `UNKNOWN` | treated as a failure, not a warning |
| 5 | A licence string is new but acceptable | the allowlist file is edited in the same pull request, so the change is visible in review |
| 6 | No test files exist yet | pytest and vitest must still exit 0 on an empty suite |
| 7 | Vitest started in watch mode | CI calls `vitest run`, never bare `vitest`, or the job hangs until it times out |
| 8 | `npm ci` without a lock file | the scaffold commits `package-lock.json` in the same change, or `npm ci` fails |

## 6. Impact - who else touches this

| Thing changed | Consumer | Effect |
| --- | --- | --- |
| `.github/pull_request_template.md` | every PR from now on | new, added on this branch |
| `verify_pack.py` output encoding | every DATA task, and `CLAUDE.md` section 3 | fixed for all of them |
| `tools/checks/license-allowlist.txt` | the new licence job, P.7 source records | read, not changed |
| `tools/checks/sdk-allowlist.md` | the new licence job, every later web task | gains one row for vitest |
| `web/package.json` | tasks 1.10 onward | created here, extended later |
| `.github/workflows/ci.yml` | every push from now on | new |

Found by reading `CLAUDE.md` section 3, `tools/checks/`, and `prompts/phase-P/P.1.md`.

## 7. Tests and Definition of Done

| # | Test | How to run | Expected result |
| --- | --- | --- | --- |
| 1 | TC-CP-01 | `npx license-checker --json` in `web/` | 0 packages outside the allowlist |
| 2 | TC-CP-02 | compare `web/package.json` with `sdk-allowlist.md` | every dependency has a row |
| 3 | Licence gate really bites | install a GPL package, push, then remove it | the run fails on that commit and passes after removal |
| 4 | Checker on Windows | `python tools/checks/verify_pack.py content/lexicon/lexicon_raw_test.csv` | `30 bản ghi · 0 lỗi · 2 cảnh báo`, exit 0, no traceback |
| 5 | Checker in CI | the python job | same output, exit 0 |
| 6 | Empty suites pass | the python and web jobs on this branch | both green |

**Definition of done:**

- [ ] All four jobs appear in one CI run, three green and one skipped
- [ ] Test 3 shows a real red run, with its link recorded, before the package is removed
- [ ] `verify_pack.py` exits 0 on Windows with no traceback
- [ ] `web/` builds and `npm test` passes
- [ ] `mobile/README.md` says what is missing and which task fills it
- [ ] Branch protection: the refusal is recorded in `records/P.1.md` with the API message
- [ ] `records/P.1.md` carries a result line per step and the table above with real numbers
- [ ] CI runs on Python 3.11, not on whatever the runner defaults to
- [ ] `chore/p1-repo-ci` is merged into `main` through a PR, with CI green on that PR, and the
      branch deleted afterwards

## 8. After Gate B

Planned commit messages:

```
feature(P.1): force utf-8 output in verify_pack
feature(P.1): scaffold web app with vitest
feature(P.1): add ci workflow with licence gate
docs(P.1): record mobile placeholder and branch protection limit
```

Then close the task through a pull request: push the branch, open the PR with the title
`feature(P.1): add CI, licence gate and web scaffold`, wait for the CI run to go green, merge with
a merge commit, delete the branch. The next task then starts from a trunk that already has CI.

Record note: `records/P.1.md` gets the CI run links, the licence-checker output, the red run from
test 3, and the branch-protection refusal message. `records/TRACKING.md` gets status, real effort
and the test result.

## 9. Open questions for the reviewer

None. All three were answered on 2026-09-24 and moved into the Decisions log above.

One note, not a question: the machine runs Python 3.14 and CI will run 3.11. A check can pass in
one place and fail in the other. Test 4 runs the checker locally on 3.14 and test 5 runs it in CI
on 3.11, so the gap is covered by the test list rather than assumed away.
