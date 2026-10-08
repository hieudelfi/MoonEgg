# Giao P.3 — Môi trường pipeline (2026-10-08)

Bản ghi đầy đủ: `records/P.3.md`. Kế hoạch và kết quả trên hub: xem `records/P.3.md` phần đầu.
Cách dựng lại môi trường: `tools/pipeline/ENV.md`.

## Trong thư mục này

| Tệp | Là gì |
| --- | --- |
| `evidence/test01-tts.txt`, `tts_timing.json` | Kokoro sinh 10 tệp, thời gian từng tệp |
| `evidence/test02-opus-loudness.txt`, `opus_report.json` | Âm lượng đo lại trên từng tệp Opus |
| `evidence/test03-align.txt`, `align_timing.json` | MFA căn 10 tệp |
| `evidence/test04-05-06-textgrid-vs-cmudict.txt`, `textgrid_report.json`, `mismatch.csv` | Mốc thời gian và so phone với CMUdict |
| `evidence/textgrid/` | 10 tệp TextGrid nguyên bản |
| `evidence/test07-build-lexicon.txt` | `build_lexicon.py` chạy lại, so với tệp đang theo dõi |
| `evidence/test08-disk.txt` | Ổ đĩa trước và sau |
| `evidence/test09-nothing-heavy-in-git.txt` | Không có audio hay môi trường trong git |
| `evidence/test10-gate-full.txt` | Cổng đầy đủ và bộ test |
| `evidence/test12-licences.txt` | Giấy phép của hai môi trường |
| `evidence/opus-files.txt` | sha256 và kích thước 10 tệp Opus |
| `evidence/scan.txt` | Kết quả quét bằng chứng |

Tệp audio không nằm trong gói này. Chúng ở `content/pack/audio_test/` trên máy dựng, git bỏ qua.
Test 11 (nghe kiểm) do người review làm bằng tai, không có tệp bằng chứng.

## Quét trước khi giao

Ngày 2026-10-08. Kết quả ở `evidence/scan.txt`: 0 phát hiện.
