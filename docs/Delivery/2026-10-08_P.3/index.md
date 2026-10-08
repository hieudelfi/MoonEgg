# P.3 delivery - 2026-10-08

Task: `P.3` · Plan: https://hub.yawasa.com/app/p/moonegg-p3-plan
Result: https://hub.yawasa.com/app/p/moonegg-p3-result · Record: `records/P.3.md`
Branch `chore/p3-pipeline-env`, merged into `main` after Gate B on 2026-10-08

This is the QC package: the raw output of every check, exactly as it was printed on the machine.
Nothing here is retyped. The Result drop explains what the task did; this one proves it.

Every file comes from one fresh run of the whole chain on 2026-10-08. Machine paths are replaced
by `<repo>` and `<home>`. The audio files are not in this package; their hashes are.

Test 11, the listening check, was done by the reviewer by ear. The verdict was "sounds very good".

**Evidence scan before handover:** 0 findings.

## Test 1 - Kokoro sinh 10 tệp

`evidence/test01-tts.txt`

```
measured 2026-10-08T07:52:17Z
hello__af_heart.wav           1400 ms  synth  0.881 s  /həlˈO/
market__af_heart.wav          1450 ms  synth  0.775 s  /mˈɑɹkət/
reluctant__af_heart.wav       1550 ms  synth  1.255 s  /ɹəlˈʌktᵊnt/
think__af_heart.wav           1275 ms  synth  0.635 s  /θˈɪŋk/
wind__af_heart.wav            1375 ms  synth  0.590 s  /wˈɪnd/
hello__am_michael.wav         1425 ms  synth  0.595 s  /həlˈO/
market__am_michael.wav        1350 ms  synth  0.551 s  /mˈɑɹkət/
reluctant__am_michael.wav     1550 ms  synth  0.607 s  /ɹəlˈʌktᵊnt/
think__am_michael.wav         1225 ms  synth  0.528 s  /θˈɪŋk/
wind__am_michael.wav          1325 ms  synth  0.569 s  /wˈɪnd/
model and voices loaded in 4.08 s, paid once per run
10 files, mean 0.699 s per word
exit=0
```

## Test 2 - âm lượng và nén Opus

`evidence/test02-opus-loudness.txt`

```
measured 2026-10-08T07:52:58Z
hello__af_heart.opus          in  -24.5  gain  +8.5 dB  out  -16.4 LUFS   1406 ms   21.3 kbps   3748 B  1 tries   0.24 s  ok
hello__am_michael.opus        in  -24.9  gain  +9.9 dB  out  -16.5 LUFS   1432 ms   23.1 kbps   4141 B  2 tries   0.29 s  ok
market__af_heart.opus         in  -23.8  gain  +7.8 dB  out  -16.0 LUFS   1456 ms   21.9 kbps   3992 B  1 tries   0.17 s  ok
market__am_michael.opus       in  -24.1  gain +12.1 dB  out  -16.3 LUFS   1356 ms   23.7 kbps   4021 B  4 tries   0.49 s  ok
reluctant__af_heart.opus      in  -24.3  gain  +9.3 dB  out  -16.2 LUFS   1556 ms   22.5 kbps   4371 B  2 tries   0.27 s  ok
reluctant__am_michael.opus    in  -24.0  gain +11.4 dB  out  -16.4 LUFS   1556 ms   24.9 kbps   4838 B  4 tries   0.49 s  ok
think__af_heart.opus          in  -23.9  gain  +8.5 dB  out  -16.2 LUFS   1282 ms   21.3 kbps   3408 B  2 tries   0.27 s  ok
think__am_michael.opus        in  -23.5  gain +10.1 dB  out  -16.5 LUFS   1232 ms   23.1 kbps   3561 B  3 tries   0.37 s  ok
wind__af_heart.opus           in  -23.9  gain  +8.7 dB  out  -16.3 LUFS   1382 ms   21.6 kbps   3730 B  2 tries   0.27 s  ok
wind__am_michael.opus         in  -25.0  gain +11.3 dB  out  -16.5 LUFS   1332 ms   23.7 kbps   3949 B  3 tries   0.36 s  ok
10 files, mean 0.322 s per file, 0 outside the target
exit=0
```

## Test 3 - MFA căn 10 tệp

`evidence/test03-align.txt`

```
measured 2026-10-08T07:53:02Z
MFA 3.4.2, model english_us_arpa
models ready in 9.3 s, paid once per machine
10 of 10 files aligned in 89.9 s, 8.99 s per file including start-up
exit=0
```

## Test 4, 5, 6 - mốc thời gian và so với CMUdict

`evidence/test04-05-06-textgrid-vs-cmudict.txt`

```
measured 2026-10-08T07:54:53Z
hello__af_heart.TextGrid         HH AH0 L OW1                 cmudict HH AH0 L OW1                 ok
hello__am_michael.TextGrid       HH AH0 L OW1                 cmudict HH AH0 L OW1                 ok
market__af_heart.TextGrid        M AA1 R K IH0 T              cmudict M AA1 R K AH0 T              sound_mismatch
market__am_michael.TextGrid      M AA1 R K IH0 T              cmudict M AA1 R K AH0 T              sound_mismatch
reluctant__af_heart.TextGrid     R IH0 L AH1 K T AH0 N T      cmudict R IH0 L AH1 K T AH0 N T      ok
reluctant__am_michael.TextGrid   R IH0 L AH1 K T AH0 N T      cmudict R IH0 L AH1 K T AH0 N T      ok
think__af_heart.TextGrid         TH IH1 NG K                  cmudict TH IH1 NG K                  ok
think__am_michael.TextGrid       TH IH1 NG K                  cmudict TH IH1 NG K                  ok
wind__af_heart.TextGrid          W IH1 N D                    cmudict W IH1 N D                    ok
wind__am_michael.TextGrid        W IH1 N D                    cmudict W IH1 N D                    ok
10 files, 4 of 5 words match CMUdict, 2 rows in mismatch.csv, 2 hard failures
exit=1
--- mismatch.csv
file,item_id,kind,cmudict,aligned
market__af_heart.TextGrid,w:market#1,sound_mismatch,M AA1 R K AH0 T,M AA1 R K IH0 T
market__am_michael.TextGrid,w:market#1,sound_mismatch,M AA1 R K AH0 T,M AA1 R K IH0 T
```

## Một tệp TextGrid nguyên bản: wind, giọng af_heart

`evidence/textgrid/wind__af_heart.TextGrid`

```
File type = "ooTextFile"
Object class = "TextGrid"

xmin = 0 
xmax = 1.375 
tiers? <exists> 
size = 2 
item []: 
    item [1]:
        class = "IntervalTier" 
        name = "words" 
        xmin = 0 
        xmax = 1.375 
        intervals: size = 3 
        intervals [1]:
            xmin = 0.0 
            xmax = 0.37 
            text = "" 
        intervals [2]:
            xmin = 0.37 
            xmax = 0.88 
            text = "wind" 
        intervals [3]:
            xmin = 0.88 
            xmax = 1.375 
            text = "" 
    item [2]:
        class = "IntervalTier" 
        name = "phones" 
        xmin = 0 
        xmax = 1.375 
        intervals: size = 6 
        intervals [1]:
            xmin = 0.0 
            xmax = 0.37 
            text = "" 
        intervals [2]:
            xmin = 0.37 
            xmax = 0.47 
            text = "W" 
        intervals [3]:
            xmin = 0.47 
            xmax = 0.61 
            text = "IH1" 
        intervals [4]:
            xmin = 0.61 
            xmax = 0.71 
            text = "N" 
        intervals [5]:
            xmin = 0.71 
            xmax = 0.88 
            text = "D" 
        intervals [6]:
            xmin = 0.88 
            xmax = 1.375 
            text = "" 
```

## Test 7 - build_lexicon.py chạy lại

`evidence/test07-build-lexicon.txt`

```
measured 2026-10-08T07:54:55Z
30 từ
w:hello#1        /həlˈoʊ/         nhấn=1 khó=[] viseme=DD aa DD O
w:market#1       /mˈɑrkət/        nhấn=0 khó=[cuối /t/;r] viseme=PP aa O DD aa DD
w:umbrella#1     /əmbrˈɛlə/       nhấn=1 khó=[r] viseme=aa PP PP O E DD aa
w:bargain#1      /bˈɑrɡən/        nhấn=0 khó=[r] viseme=PP aa O DD aa DD
w:reluctant#1    /rɪlˈʌktənt/     nhấn=1 khó=[cuối nt;r] viseme=O I DD aa DD DD aa DD DD
w:think#1        /θˈɪŋk/          nhấn=0 khó=[cuối /k/;θ] viseme=TH I DD DD
w:sink#1         /sˈɪŋk/          nhấn=0 khó=[cuối /k/] viseme=SS I DD DD
w:wind#1         /wˈɪnd/          nhấn=0 khó=[cuối nd] viseme=U I DD DD
w:wind#2         /wˈaɪnd/         nhấn=0 khó=[cuối nd] viseme=U aa DD DD
w:thorough#1     /θˈɝoʊ/          nhấn=0 khó=[θ] viseme=TH E O
w:through#1      /θrˈu/           nhấn=0 khó=[r;θ] viseme=TH O U

ví dụ WordNet: unwillingness to do something contrary to your custom | disinclined to become involved | not eager
đồng nghĩa (loại khỏi nhiễu): loath;loth

Phủ: có IPA 30 / 30 ; có nghĩa WordNet 28 ; đa cách đọc 11
exit=0
--- compare with content/lexicon/lexicon_raw_test.csv
byte-identical
lines: 31
```

## Test 8 - ổ đĩa

`evidence/test08-disk.txt`

```
measured 2026-10-08T08:02:48Z
C free GB: 12.63
D free GB: 155.5
C free GB before the install, same day: 9.17
folder sizes, measured earlier today with du -sh:
  tools/pipeline/.venv 1.2G | tools/pipeline/.mfa 2.4G | tools/pipeline/.cache 1.9G | D:/tools/miniforge3 621M
left on C by MFA: Documents/MFA, 2.0K (global_config.yaml and an empty joblib_cache)
```

## Test 9 - không có audio trong git

`evidence/test09-nothing-heavy-in-git.txt`

```
measured 2026-10-08T08:02:49Z
--- git status --short (pyc caches left out)
 M CLAUDE.md
 M tools/checks/sdk-allowlist.md
 M tools/pipeline/ENV.md
 M tools/pipeline/build_lexicon.py
 M tools/pipeline/requirements.txt
?? docs/Delivery/2026-10-08_P.3/
?? tools/checks/test_lexicon_encoding.py
--- git check-ignore
.gitignore:3:content/pack/audio*/	content/pack/audio_test/wav/hello__af_heart.wav
.gitignore:3:content/pack/audio*/	content/pack/audio_test/opus/hello__af_heart.opus
.gitignore:7:tools/pipeline/.venv/	tools/pipeline/.venv
.gitignore:15:tools/pipeline/.mfa/	tools/pipeline/.mfa
.gitignore:16:tools/pipeline/.cache/	tools/pipeline/.cache
--- tracked audio or environment files: 0
```

## Test 10 - cổng đầy đủ

`evidence/test10-gate-full.txt`

```
  pytest tools/checks               dat
  verify_pack tren du lieu mau      dat
    30 bản ghi · 0 lỗi · 2 cảnh báo
  vitest                            dat
  cong giay phep (TC-CP-01/02)      dat
    49 gói · 0 lỗi giấy phép · 0 gói thiếu dòng SDK
gate exit=0
--- pytest
..............                                                           [100%]
14 passed in 1.88s
```

## Test 12 - giấy phép

`evidence/test12-licences.txt`

```
measured 2026-10-08T08:02:58Z
--- speech environment, pip-licenses, grouped
packages: 96
 25  MIT
 23  MIT License
 11  BSD License
 10  Apache Software License
  8  BSD-3-Clause
  3  Apache-2.0
  2  BSD-2-Clause
  1  Mozilla Public License 2.0 (MPL 2.0)
  1  MIT-0
  1  GNU General Public License v3 or later (GPLv3+)
  1  Python Software Foundation License
  1  BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0
  1  Apache-2.0 OR BSD-2-Clause
  1  Apache Software License; BSD License
  1  Apache-2.0 AND CNRI-Python
  1  ISC License (ISCL)
  1  Apache-2.0 AND Apache-2.0 WITH LLVM-exception AND BSD-2-Clause AND BSD-3-Clause 
  1  MPL-2.0 AND MIT
  1  Apache 2.0 License
  1  PSF-2.0
  1  BSD 3-Clause OR Apache-2.0
GPL family or unknown: [('cmudict', '1.1.3', 'GNU General Public License v3 or later (GPLv3+)')]
--- MFA environment, conda-meta licence fields
packages: 204 | GPL family: 28
   cairo 1.18.6 LGPL-2.1-only or MPL-1.1
   ffmpeg 8.1.2 GPL-2.0-or-later
   freetype 2.14.3 GPL-2.0-only OR FTL
   fribidi 1.0.17 LGPL-2.1-or-later
   gdk-pixbuf 2.44.8 LGPL-2.1-or-later
   getopt-win32 0.1 LGPL-3.0-only
   graphite2 1.3.15 LGPL-2.0-or-later
   gts 0.7.6 LGPL-2.0-or-later
   lame 3.100 LGPL-2.0-only
   libfreetype 2.14.3 GPL-2.0-only OR FTL
   libfreetype6 2.14.3 GPL-2.0-only OR FTL
   libgcc 16.2.0 GPL-3.0-only WITH GCC-exception-3.1
   libglib 2.90.1 LGPL-2.1-or-later
   libgomp 16.2.0 GPL-3.0-only WITH GCC-exception-3.1
   libiconv 1.18 LGPL-2.1-only
   libintl 0.22.5 LGPL-2.1-or-later
   libmad 0.15.1b GPL-2.0-only
   librsvg 2.62.4 LGPL-2.1-or-later
   libsndfile 1.2.2 LGPL-2.1-or-later
   libusb 1.0.30 LGPL-2.1-or-later
   mpg123 1.32.9 LGPL-2.1-only
   pango 1.58.2 LGPL-2.1-or-later
   psycopg2 2.9.9 LGPL-3.0-or-later
   sox 14.4.2 GPL-2.0-only
   soxr 0.1.3 LGPL-2.1-or-later
   soxr-python 1.1.0 LGPL-2.1-or-later
   x264 1!164.3095 GPL-2.0-or-later
   x265 3.5 GPL-2.0-or-later
key: ('montreal-forced-aligner', '3.4.2', 'MIT')
key: ('kalpy', '0.10.5', 'MIT')
key: ('kaldi', '5.5.1172', 'Apache-2.0')
key: ('openfst', '1.8.4', 'Apache-2.0')
--- system ffmpeg
ffmpeg version 9.0.2-full_build-www.gyan.dev Copyright (c) 2000-2026 the FFmpeg developers
enable-gpl
enable-libopus
```

## Mười tệp Opus: sha256 và kích thước

`evidence/opus-files.txt`

```
sha256 of the ten Opus files. The audio stays on the build machine: *.opus is ignored by git.
b363be1771316fc115436911e6b770e42d33b520658cb326103b2fb79197ec2a *hello__af_heart.opus
2fec1d0307fbaa6e8ea0d9dace189490e3a5da64aa8414fdc830ee07194f37e2 *hello__am_michael.opus
b0f4177f830083559a01a575a6acd91d6873afb179115516ae9f15617fede3f2 *market__af_heart.opus
74a82420beee019d173410e0d69e364001eaf2e14ec6a488e5be6264631a328a *market__am_michael.opus
890876a5d863985636c66da001a52047a6b80a6a96b92cac5a94fb87f83657ad *reluctant__af_heart.opus
28440cdb3e145e1243b966be7409c253ee8ff09e4d005d44d2b0ccdb2a4a7d4c *reluctant__am_michael.opus
7e45ebae7c9162df7dac034b7658538058e19ccf4c36c94ca1d8c9149e50981c *think__af_heart.opus
1a29aa4e314d286453c022a16eaefe31cda77b70f7e23100f421d0db9752b8a4 *think__am_michael.opus
68437fa868d0e9acdbbdd0e13b52a05aa270562da7e6c881f967f898ff7fd7c5 *wind__af_heart.opus
3b50fb81892ce9bfecede7baaabc59b84bf91abb5b3fa0f34bbd7417c833807f *wind__am_michael.opus
--- sizes in bytes
 3748 hello__af_heart.opus
 4141 hello__am_michael.opus
 3992 market__af_heart.opus
 4021 market__am_michael.opus
 4371 reluctant__af_heart.opus
 4838 reluctant__am_michael.opus
 3408 think__af_heart.opus
 3561 think__am_michael.opus
 3730 wind__af_heart.opus
 3949 wind__am_michael.opus
39759 total
```

## Kết quả quét bằng chứng trước khi giao

`evidence/scan.txt`

```
Quet ngay 2026-10-08, thu muc docs/Delivery/2026-10-08_P.3/.
0 phat hien.
Mau tim: JWT, AKIA, private key, gho_/ghp_, sk-, hf_, dia chi email, ten tai khoan may,
duong dan thu muc nguoi dung, chu token va password.
Duong dan may da duoc thay bang <repo> va <home> luc ghi tep.
Khong co tep audio trong goi: chi co sha256 va kich thuoc cua 10 tep Opus.
```

## What a reader should take from this

- The chain word to speech to Opus to timings runs on this machine, on the processor alone.
- All 10 Opus files sit between -16.5 and -16.0 LUFS, measured on the files themselves.
- Four of five words match CMUdict. "market" does not, and `mismatch.csv` says how.
- The aligner costs about 89 seconds to start and about 0.1 seconds per file after that.
- Drive C: was not reduced, and no audio or environment file is tracked in git.
