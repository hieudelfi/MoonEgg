# P.4 delivery - 2026-10-09

Task: `P.4` · Plan: https://hub.yawasa.com/app/p/moonegg-p4-plan
Result: https://hub.yawasa.com/app/p/moonegg-p4-result · Record: `records/P.4.md`
Branch `chore/p4-voices`, merged into `main` after Gate B on 2026-10-09

This is the QC package: raw output, the three score sheets, the key, and the second reader's report.
The Result drop explains what the task did; this one proves it.

**Evidence scan before handover:** 0 findings. The sheets carry codes R1 to R3, no names.

## Tests 4 and 5 - the scores

`evidence/test04-05-scores.txt`

```
measured 2026-10-09
$ python tools/pipeline/env/score.py
sheets: 3 complete of 3 needed (R1, R2, R3); one listener, 3 sitting(s)
note - R3: 101 of 125 rows have the same number for both scores. Check that this sitting was not scored with a held or doubled key.

measured, not scored (words only)
voice         mean ms  raw LUFS  limiter dB
af_bella         1445     -25.5         0.7
af_heart         1428     -24.2         0.8
af_sarah         1741     -21.6         1.0
am_adam          1224     -20.9         1.8
am_michael       1390     -24.3         2.6

scores
voice        sex     rows  clarity  natural    sum  spread     R1     R2     R3
af_heart     female    75     4.48     4.11   8.59    0.84   8.60   9.00   8.16
af_sarah     female    75     4.40     4.01   8.41    0.32   8.28   8.60   8.36
af_bella     female    75     4.29     3.81   8.11    0.84   8.36   8.40   7.56
am_adam      male      75     4.04     3.41   7.45    1.44   8.00   7.80   6.56
am_michael   male      75     3.59     2.87   6.45    0.48   6.40   6.72   6.24

chosen
female  af_heart  UNSTEADY: leads in 2 of 3 sittings, overall margin 0.17: confirm by ear
male    am_adam  leads in every sitting, margin 1.00
exit=0
```

## Which sittings decide the result; the sample set

`evidence/sittings-and-samples.txt`

```
measured 2026-10-09
rows with the same number for both scores
  R1 41 of 125
  R2 52 of 125
  R3 101 of 125
winners by which sittings are counted
  R1+R2+R3  {'af_bella': 8.11, 'af_heart': 8.59, 'af_sarah': 8.41, 'am_adam': 7.45, 'am_michael': 6.45} -> af_heart am_adam
  R1+R2     {'af_bella': 8.38, 'af_heart': 8.8, 'af_sarah': 8.44, 'am_adam': 7.9, 'am_michael': 6.56} -> af_heart am_adam
  R1        {'af_bella': 8.36, 'af_heart': 8.6, 'af_sarah': 8.28, 'am_adam': 8.0, 'am_michael': 6.4} -> af_heart am_adam
  R2        {'af_bella': 8.4, 'af_heart': 9.0, 'af_sarah': 8.6, 'am_adam': 7.8, 'am_michael': 6.72} -> af_heart am_adam
  R3        {'af_bella': 7.56, 'af_heart': 8.16, 'af_sarah': 8.36, 'am_adam': 6.56, 'am_michael': 6.24} -> af_sarah am_adam
samples: 125 | per voice: {'am_michael': 25, 'am_adam': 25, 'af_bella': 25, 'af_heart': 25, 'af_sarah': 25}
word 100 files, 856 to 2031 ms
sentence 25 files, 2232 to 3756 ms
levelled loudness -16.8 to -15.9 LUFS
```

## Test 6 - the two readings of "wind"

`evidence/wind-check.md`

```
# P.4 - the two readings of "wind"

Checked on 2026-10-09 with the five candidate voices. Chosen voices: `af_heart` and `am_adam`.

Kokoro turns text into sounds before a voice is applied. So the sound string is the same for all
five voices, and this result holds for both chosen voices.

| Input | Sound string from Kokoro | Expected | Result |
| --- | --- | --- | --- |
| `wind`, alone | `wˈɪnd` | contains `wˈɪnd`, the noun, `w:wind#1` | pass |
| `Please wind the clock before you leave the kitchen.` | `plˈiz wˈInd ðə klˈɑk bəfˈɔɹ ju lˈiv ðə kˈɪʧᵊn.` | contains `wˈInd`, the verb, `w:wind#2` | pass |

In Kokoro's own symbols the letter `I` stands for the sound /aɪ/. So `wˈInd` is /waɪnd/.

What this means for task P.10:

- Alone, "wind" is always the noun. To get the verb sound for the card `w:wind#2`, the word must
  be spoken inside a verb sentence and cut out, or the sound string must be given to Kokoro directly.
- A noun sentence was also in the set: `The cold wind and rain left everyone exhausted.` gave
  `wˈɪnd`, the noun. Context decides, and it decided right in both sentences tried.
- Two sentences are not proof for every sentence. P.10 should check the sound string of every
  audio it makes for a word with two readings.

By ear: the listener scored the four samples below without knowing the voice. The scores say the
samples were clear. They do not say which reading was heard; that needs one direct listen.

| Sample | Voice | Text | Clarity, natural in sittings R1, R2, R3 |
| --- | --- | --- | --- |
| `s025` | `af_heart` | wind | 5,4 · 5,4 · 4,4 |
| `s037` | `af_heart` | Please wind the clock... | 5,4 · 5,5 · 5,5 |
| `s121` | `am_adam` | wind | 5,3 · 5,4 · 4,4 |
| `s090` | `am_adam` | Please wind the clock... | 4,3 · 5,3 · 3,3 |
```

## Test 3 - blind names

`evidence/test03-blind-names.txt`

```
measured 2026-10-09
files in the samples folder that are not sNNN.opus: ['_key', 'rate.html', 'sheets']
sample files: 125
file names containing af_ or am_: 0
voice names or the word _key inside rate.html: 0
sheets folder: []
note: the three sheets of this run were saved into _key/, as the first version of the page asked.
```

## Test 9 - nothing heavy in git

`evidence/test09-nothing-heavy-in-git.txt`

```
measured 2026-10-09
--- git status --short
?? docs/Delivery/2026-10-09_P.4/
--- tracked audio or audio_test files: 0
```

## Test 11 - the gate

`evidence/test11-gate-full.txt`

```
  pytest tools/checks               dat
  verify_pack tren du lieu mau      dat
    30 bản ghi · 0 lỗi · 2 cảnh báo
  vitest                            dat
  cong giay phep (TC-CP-01/02)      dat
    49 gói · 0 lỗi giấy phép · 0 gói thiếu dòng SDK
gate exit=0
--- pytest
.................................                                        [100%]
33 passed in 2.23s
```

## Second reader before Gate B

`evidence/reviewer-gate-b.txt`

```
gate-reviewer (opus) on the P.4 code, records and data, before Gate B. Tokens: 128090. Tool uses: 42. Duration: 286.7 s.
Copied from the session; the agent's transcript file was empty. Summary of each row, with the reviewer's File:line.

FOUR ANSWERS: all "weak".
1. Code does the plan, with extras, and one gap: score.py printed the per-voice table from one sheet.
2. A wrong winner was possible: "sheet_R1 (1).csv" counted as a new sitting; check_sheet never read the rater column; Enter could re-press the last clicked score button.
3. Record numbers for B1 to B5 match the disk. The record stopped at "1/3 sittings" while the disk had three sheets and the decision was already in docs/01.
4. A held or repeated digit key fills both scores with one number. R3 has clarity equal to natural in 101 of 125 rows, and R3 is the sitting that flips the female order.

RECOMPUTED BY THE REVIEWER from key.csv and the three sheets: af_heart 644/75 = 8.59, af_sarah 631/75 = 8.41, af_bella 608/75 = 8.11, am_adam 559/75 = 7.45, am_michael 484/75 = 6.45. All five match score.py.
FEMALE MARGIN: not stable. af_heart leads in R1 (+0.32) and R2 (+0.40); af_sarah leads in R3 (+0.20). Overall margin 13 raw points of 750. The gap is in single words; sentences are level (145 vs 144 of 150).
MALE: stable. am_adam leads in all three sittings (+1.60, +1.08, +0.32).

DEFECTS, 24 rows:
rate.html:170-174  held digit key fills both scores                          FIXED: e.repeat ignored
rate.html:174      keyboard cannot correct clarity once both are set         FIXED: third digit starts the sample over
rate.html:175      Enter re-presses the last clicked score button            FIXED: Enter always cancelled; buttons blur after a click
rate.html:176      Space on keyup presses a focused button in Firefox        FIXED: keyup cancelled
rate.html:132,139  done screen shows 125 over a shorter CSV                  FIXED: shows scored count, warns when short
rate.html:90       localStorage errors swallowed                             FIXED: visible warning
rate.html:145,157  resume by length only; old scores on new audio            FIXED: saved state carries an id of the audio
rate.html:74       page says "move the sheet into _key"                      FIXED: sheets/ folder
score.py:24-40     rater column never read                                   FIXED: must equal the code in the file name
score.py:83-84     glob takes any stem                                       FIXED: only sheet_R1/R2/R3.csv, others listed as ignored
score.py:136       four or more sheets accepted                              FIXED: exactly the three names
score.py:121-134   per-voice table and scores.csv before three sheets        FIXED: nothing about voices before three
score.py:74        thin margin and lost sitting invisible                    FIXED: per-sitting columns, UNSTEADY flag
score.py:59        sex re-derived from prefix                                FIXED: read from key.csv; unknown prefix stops voice_samples.py
_kokoro.py:50      unknown word inside a sentence is skipped silently        FIXED: stops and names the word; proven with a nonsense word
voice_samples.py:70 limiter works unevenly by voice                          LEFT: recorded, Plan decision 10, note for P.10
test_voice_scores.py:10 main() and find_sheets untested                      FIXED: 8 new tests, two run the script end to end
test_voice_scores.py:88 importing _kokoro pollutes sys.modules               FIXED: test reads the source
records/P.4.md:18-21 record behind the disk                                  FIXED: B6 to B9 written
records/P.4.md:17  mean length per voice written before sittings 2 and 3     LEFT: cannot be undone; recorded as a lapse
wind-check.md:24-25 by-ear check of the two readings not done                LEFT: asked of the owner at Gate B
Plan.md:3          commits before Gate B                                     LEFT: step-by-step commits are a recorded practice since P.2; no merge before Gate B
ENV.md:79,96       stale lines about tts_sample.py                           FIXED
Plan.md:176        heading names measure.py                                  FIXED
```

## Evidence scan

`evidence/scan.txt`

```
Quet ngay 2026-10-09, thu muc docs/Delivery/2026-10-09_P.4/.
0 phat hien.
Mau tim: JWT, AKIA, private key, gho_/ghp_, sk-, hf_, dia chi email, ten tai khoan may, duong dan thu muc nguoi dung, token, password.
Ba bang diem chi mang ma R1, R2, R3, khong co ten nguoi.
Khong co tep audio trong goi.
```

## What a reader should take from this

- `am_adam` leads `am_michael` in all three sittings.
- `af_heart` leads overall and in two of three sittings. `af_sarah` leads in the third.
- The third sitting has the same number twice in 101 of 125 rows. The result is the same without it.
- One listener, three sittings: this shows steadiness, not agreement between people.
