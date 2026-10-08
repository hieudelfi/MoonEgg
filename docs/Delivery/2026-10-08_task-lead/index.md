# task-lead delivery - 2026-10-08

Task: `task-lead` · Plan: https://hub.yawasa.com/app/p/moonegg-task-lead-plan
Result: https://hub.yawasa.com/app/p/moonegg-task-lead-result · Record: `records/task-lead.md`
Branch `chore/task-lead-skill`, merged into `main` after Gate B on 2026-10-08

This is the QC package. The agent reports are copied from the session, because the agents'
transcript files were empty. Each file says what is verbatim and what is a summary.
The Result drop explains what the task did; this one proves it.

**Evidence scan before handover:** 0 findings.

## Install, clone status, name collisions

`evidence/install-and-collisions.txt`

```
measured 2026-10-08
$ bash install.sh   (repo hieudelfi/claude-local, PRIVATE)
skill   task-lead -> <home>/.claude/skills/task-lead
agent   evidence-scout.md -> <home>/.claude/agents/
agent   gate-reviewer.md -> <home>/.claude/agents/
--- git status of <home>/.claude/skills (expect '??' for each skill above)
?? task-lead/
$ ls D:/Projects/*/.claude/agents/ | grep -cE '^(gate-reviewer|evidence-scout).md$'
0
$ gh repo view hieudelfi/claude-local --json visibility,url
PRIVATE https://github.com/hieudelfi/claude-local
```

## Tests 1 and 2 - the skill and agents load by name

`evidence/test01-02-skill-loads-by-name.txt`

```
measured 2026-10-08, inside the session that installed the skill
Skill tool, name "task-lead", args "P.4", first call, before the skill list refreshed:
  Unknown skill: task-lead
Skill tool, same call, after the harness listed the new skill:
  Launching skill: task-lead   (the SKILL.md text was loaded, ARGUMENTS: P.4)
Agent tool, subagent_type "evidence-scout", first call:
  Agent type 'evidence-scout' not found. Available agents: api-designer, backend-developer, ...
Agent tool, same type, later in the session after the harness announced the two new agents:
  launched; report received (see scout-2.txt)
Test 2 (word triggers do not fire it): not run. It needs a fresh session where "feature: add X"
is typed and the loaded skills are observed. Recorded as "chưa đo".
```

## Scout run 1 - stand-in agent

`evidence/scout-1-general-purpose-stand-in.txt`

```
Scout run 1, agent general-purpose on sonnet with the evidence-scout definition pasted in the brief.
Reason: the evidence-scout agent was not yet loaded in the session.
Tokens reported by the tool: 71004. Tool uses: 3. Duration: 24.9 s.
Answered 8 of 10 questions. Left question 2 unanswered and did not read prompts/phase-P/P.4.md.
Both gaps are named in its own "Could not find" list. It also wrote:
  "Exact line numbers for rows 6a, 6b and the heading in row 6: derived by counting from
   sed -n 352,372p. I did not run grep -n to confirm them."
Those three numbers were later found to be off by one (357 not 358, 362 not 363, 366 not 365).
Facts it returned that held: CSV header and 31 lines; voices cached = af_heart.pt, am_michael.pt;
_paths.py:20 WORDS, :22 VOICES; tts_sample.py:59 and :65; Piper not installed; web scripts;
records/TEMPLATE.md:4 token line.
It also reported that the session's attribution reminder asked for a Co-Authored-By trailer, that
CLAUDE.md forbids it, and that it made no commits.
```

## Scout run 2 - the evidence-scout agent

`evidence/scout-2-evidence-scout.txt`

```
Scout run 2, agent evidence-scout (sonnet), the real agent, loaded mid-session.
Tokens reported by the tool: 31712. Tool uses: 3. Duration: 31.8 s.
Answered all 5 questions. Key rows:
| 2a | mock-pack table docs/08-kiem-thu.md:39-53; header at :39 |
| 2b | lines 41-50 are 10 word rows incl. wind#1 and wind#2; :51 is a placeholder "... 20 từ còn lại" |
| 2c | no list of example sentences in lines 33-88; :55 prose says 2 sentences per word; :52 has "I went to the market yesterday." |
| 4  | wind#1/#2 at docs/08-kiem-thu.md:48,49,122,139,198,260 and prompts/phase-P/P.4.md:22 |
| 5  | `import kokoro` in the venv fails: ModuleNotFoundError: No module named 'num2words'
       (kokoro/__init__.py:23 -> kokoro/pipeline.py:5 -> misaki/en.py:4). No signatures printed. |
Could not find: KPipeline signatures (import failed); a 30-row word table in docs/08 section 2
(only 10 named); example sentences in docs/08 section 2.
Commands run: 6.
```

## Reviewer run 1 - the real P.4 plan, 15 defects

`evidence/reviewer-1-real-plan.txt`

```
gate-reviewer (opus) on docs/tasks/P.4/Plan.md, first version. Tokens: 53532. Tool uses: 15. Duration: 82.0 s.

COLD READ
1. strong - The goal is stated: one female and one male voice, chosen blind by three raters, written into docs/01 section 8.3 so task 1.4 does not guess. Plan.md:35-37.
2. weak - The goal is clear to an outsider. But the line numbers it points at in docs/01 are wrong, so a newcomer would edit the wrong row. Plan.md:46, :118, :177.
3. weak - Three assumptions are written down. Others are hidden: the chosen voices may differ from P.3's pair, raw WAV loudness will not bias the scores, and mismatch.csv will survive until P.10 reads it.
4. weak - key.csv goes into the same voices/ folder as the 125 WAV files (Plan.md:71, :100-101). Plan.md:153 sends raters "a zip" of that folder. Nothing says key.csv stays out of the zip. If it goes in, the blind test is broken.

DEFECTS: 15 rows. Summary of each, with the reviewer's File:line:
 1. Plan.md:46  docs/01 line 358 cited as the voice row; the row is 357, 358 is the mascot row; phrase "cần nghe thử" is at 362 not 363.
 2. Plan.md:45  candidate list cited at docs/01:365; 365 is the table separator, the Kokoro row is 366.
 3. Plan.md:118 "edit the row at line 358" edits the wrong decision row.
 4. Plan.md:177 test 5 passes on the wrong row.
 5. Plan.md:119 vs :139,:179,:191  VOICES is changed, yet test 7 requires tts_sample.py to produce P.3's file names; names come from stem(word, voice).
 6. Plan.md:162 impact table omits align_sample.py:16,63, which also reads VOICES.
 7. Plan.md:125 "one line in mismatch.csv" has no path; check_textgrid.py:106 rewrites that file every run and .gitignore:3 ignores its folder; P.10 may never see it.
 8. Plan.md:178 test 6 has no pass/fail point; TC-CT-05 (docs/08:260) is cited but never applied.
 9. Plan.md:173 one duration range 300-8,000 ms; TC-CT-02 (docs/08:257) is 300-4,000 for words, 800-8,000 for sentences.
10. Plan.md:183-184 CLAUDE.md section 3 loudness check and 5 percent listening list dropped with no Decisions log line.
11. Plan.md:140,:212-213 raters hear raw WAV; a louder voice wins on "rõ ràng" for being louder; learners hear -16 LUFS.
12. Plan.md:106,:151 rater names typed into the page reach the Delivery; no scan step; CLAUDE.md 7.4.2.
13. Plan.md:147 vs :175-176,:189 a 60-row sheet is accepted in situation 2 but the DoD needs 375; nobody decides.
14. Plan.md:149 "the 10 named in docs/08" are 10 rows, 9 headwords (wind twice); the 125 maths changes.
15. Plan.md:6 branch not cut; the P.4 plan can land in a task-lead commit (CLAUDE.md 7.8).

LOOKED FOR, FOUND NONE: prompt steps all present; _paths.py:20,22 and tts_sample.py:59,65 match; CSV 30 rows 14 columns; docs/08:52,55 and docs/09:105 match; .gitignore:3 holds; branch and commit style match P.3; DATA without Flow.md allowed; L2 fits; gate.sh merge exists; no emojis; no forbidden source. Not checked: misaki/en.py:4.

Lead's action: all 15 fixed, Plan.md Decisions log 2 (row 15 handled by task-lead decision 3, approved by the owner).
```

## Test 5, run 1 - planted assumption missed

`evidence/reviewer-2-planted-variant-before-fix.txt`

```
gate-reviewer (opus) on the planted variant (scratchpad/planted/P4-Plan-variant.md). Tokens: 56029. Tool uses: 22. Duration: 100.1 s.
Planted: the row "Voice files on this machine: 2 of 5" and the download assumption were removed; line 96 reads "Runs offline in about two minutes."; situation 1 (a voice does not download) was removed.

COLD READ
1. strong - goal stated at line 35.
2. weak - sends the reader to the wrong row of docs/01; says "Kokoro fails on digits" where the evidence shows the project's num2words stand-in.
3. weak - hidden: changing VOICES leaves P.3's names unchanged; Kokoro prints IPA; mismatch.csv keeps a hand-added line; raters never see key.csv; three raters exist.
4. weak - smallest thing: setting VOICES to the winners renames every file tts_sample.py writes; test 7 fails unless the winners are af_heart and am_michael.

DEFECTS: 16 rows. The planted assumption (three voice files not on the machine, "runs offline") is NOT among them.
New defects not found in run 1, and later applied to the real plan:
 - :121 Kokoro prints misaki symbols; misaki/en.py:43 writes /aɪ/ as the single letter I, so the verb reads wˈInd; a plain /waɪnd/ comparison would mark a correct reading wrong.
 - :180 "code tests green" claimed but no pytest planned for score.py, voice_samples.py or the shared Kokoro code; gate.sh:15 runs only tools/checks.
 - :110 no path to Piper if every Kokoro voice scores badly.
 - :9   Level line counts "one new script, one new page"; section 4 adds two scripts, a page, a module, a refactor.
 - :48  docs/08:55 does not say "written later".

TEST 5 VERDICT: FAIL. The reader checked every cited claim against the files, but did not look for a resource the plan never mentioned.
```

## Test 5, run 2 - planted assumption found

`evidence/reviewer-3-planted-variant-after-fix.txt`

```
gate-reviewer (opus) on the same planted variant, after gate-reviewer.md gained step 3 "Inventory what the plan needs, then check each item exists" and a RESOURCES table. The brief also named that step. Tokens: 57327. Tool uses: 22. Duration: 105.3 s.

COLD READ
1. strong - goal stated in section 1 (line 35).
2. weak - lines 4, 7, 41 assume the reader knows the task-lead dry run, "scout" and "lead"; the scout's table is not linked.
3. weak - hidden ones: all five voices are already on disk (they are not), raw WAV loudness is fair, mismatch.csv survives, situation 4 never happens.
4. weak - Three of the five voice files (af_bella.pt, af_sarah.pt, am_adam.pt) are not in tools/pipeline/.cache/hf/.../voices/. Line 96 says "Runs offline", so the first run fails or downloads files without a plan step.

RESOURCES THE PLAN NEEDS (the agent wrote: "This section is not in my agent definition. I added it because the brief asked for it." - so the edited definition was not yet loaded; the brief carried the step)
| Kokoro voices af_bella, af_sarah, am_adam | Not said. Line 96 claims offline | MISSING. Only af_heart.pt and am_michael.pt are cached |
| five-voice list for voice_samples.py | Not said; VOICES shrinks to two | missing as a defined place |
| three raters | owner to confirm | unknown |
| mismatch.csv | not said which | exists, git-ignored, overwritten by check_textgrid.py:106 |
| Piper fallback | out of scope | not installed, no install path |
| pytest for new scripts | not said | none planned |

DEFECTS: 18 rows. Row 1: ":96 Runs offline in about two minutes. Only af_heart.pt and am_michael.pt are in the cache. Three of five voices must be downloaded from Hugging Face. The plan has no step, source or licence line for that download."
New rows applied to the real plan: rate.html opened from file:// cannot list a folder and has no copy step (:100-102); the three sheets have no fixed file names (:109); how the "wind" token is found in a sentence string is not said (:120).

TEST 5 VERDICT: PASS. The planted assumption was named in cold-read answer 4 and as defect row 1.
```

## Test 10 - the gate

`evidence/test10-gate-full.txt`

```
  pytest tools/checks               dat
  verify_pack tren du lieu mau      dat
    30 bản ghi · 0 lỗi · 2 cảnh báo
  vitest                            dat
  cong giay phep (TC-CP-01/02)      dat
    49 gói · 0 lỗi giấy phép · 0 gói thiếu dòng SDK
gate exit=0
```

## Evidence scan

`evidence/scan.txt`

```
Quet ngay 2026-10-08, thu muc docs/Delivery/2026-10-08_task-lead/.
0 phat hien.
Mau tim: JWT, AKIA, private key, gho_/ghp_, sk-, hf_, dia chi email, ten tai khoan may, duong dan thu muc nguoi dung, token, password.
Luu y: cac bao cao cua agent duoc chep tu phien lam viec, vi tep nhat ky cua agent trong thu muc tasks/ rong (0 byte). Khong co tep nao duoc go lai; cac doan trich la nguyen van hoac tom tat co ghi ro.
```

## What a reader should take from this

- The skill loads by name and the two agents are callable; both were picked up mid-session.
- The reviewer found 15 real defects in a plan the lead had just written. Three were line numbers off by one.
- The reviewer missed a hidden resource the first time. After a resource-inventory step it found it.
- Five helper runs cost 269,604 tokens. The owner approved nothing by batch; every stop stayed.
