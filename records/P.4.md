# P.4 — Chốt giọng đọc

Bắt đầu: 2026-10-09 (Plan viết 2026-10-08 trong lần chạy thử task-lead; Cổng A duyệt 2026-10-09)  Kết thúc: <ngày>  Công thực tế: <nđ> (ước: 0,5)
Token: scout và reviewer của Plan đã tính vào `records/task-lead.md` (269.604); phần dựng làm trực tiếp trong phiên dẫn, công cụ không báo số
Type: DATA  Level: L2  Repro (ISSUE): không áp dụng
Người kiểm: tự kiểm  Nhánh: `chore/p4-voices` (cắt từ `main` tại `c54337e`)
Plan: https://hub.yawasa.com/app/p/moonegg-p4-plan  Flow: bỏ — Type DATA, không có màn hình  Result: <link hub>
Delivery: `docs/Delivery/<ngày>_P.4/`
Tham chiếu: Kế hoạch §3P.1 P.4 · Yêu cầu §8.3 · ngưỡng TC-CT-02, TC-CT-05
Phụ thuộc: P.3 (Xong 2026-10-08)

## Checklist
- [x] B1 `_paths.py`: 20 từ, 5 câu, 5 giọng ứng viên; `_kokoro.py` dùng chung — kết quả: `_paths.py` thêm `CANDIDATE_VOICES` (5), `SAMPLE_WORDS` (20 headword khác nhau, "wind" một lần), `SENTENCES` (5 câu, 6 đến 9 từ, không chữ số), `VOICES_DIR`, `KEY_DIR`; `WORDS` và `VOICES` không đổi. `_kokoro.py` giữ hai module giả và hai hàm `make_pipeline`, `speak`. `tts_sample.py` chuyển sang dùng nó: chạy lại ra đúng 10 tệp cùng tên như bản ghi P.3. `encode_opus.py` tách hàm `level_and_encode`; chạy lại `10 files, 0 outside the target`.
- [x] B2 `voice_samples.py`: 125 mẫu mù, đã chuẩn âm lượng, `key.csv` để riêng — kết quả: tải 3 tệp giọng còn thiếu (`af_bella.pt`, `af_sarah.pt`, `am_adam.pt`) về bộ nhớ đệm ổ D, sau Cổng A. 125 tệp `s001.opus` đến `s125.opus` ở `content/pack/audio_test/voices/`, 25 tệp mỗi giọng. Từ dài 856 đến 2.031 ms, câu 2.232 đến 3.756 ms. Âm lượng đo lại −16,8 đến −15,9 LUFS. Nạp 5 giọng 43,0 giây (có tải), 0,776 giây mỗi mẫu, cả lượt 3 phút 3 giây. `key.csv` nằm ở `voices/_key/`. Ổ C: 14,35 GB trước và sau.
- [x] B3 `rate.html`: phát ngẫu nhiên, 2 điểm, mã phiên nghe — kết quả: một trang tĩnh, không cần máy chủ. `voice_samples.py` chép nó vào cạnh các mẫu và ghi sẵn danh sách 125 tệp. Chọn phiên R1, R2 hoặc R3; thứ tự xáo riêng từng phiên; hai thang 1 đến 5; phím tắt; dừng giữa chừng được vì điểm lưu trong trình duyệt; cuối phiên lưu `sheet_R<n>.csv`. Trang không chứa tên giọng nào (grep = 0). `node --check` phần script: sạch. **Chưa mở thử trong trình duyệt thật** — phiên này không có trình duyệt; lượt nghe đầu của chủ dự án là phép thử.
- [x] B4 `score.py` + `tools/checks/test_voice_scores.py` — kết quả: `score.py` ghép bảng với khoá, loại bảng thiếu dòng hoặc điểm ngoài thang, in trung bình và độ lệch giữa các phiên theo giọng, chỉ nêu tên giọng thắng khi đủ 3 bảng, báo hoà và báo giọng dưới 3 điểm. Chạy khi chưa có bảng nào: `sheets: 0 complete of 3 needed`, không nêu tên. 11 test mới, cả bộ `25 passed`.
- [x] B5 `measures.csv`: bảng đo của phiên, tách khỏi điểm — kết quả: 125 dòng ở `voices/_key/measures.csv`. Âm lượng gốc trung bình theo giọng: `af_bella` −25,5, `am_michael` −24,7, `af_heart` −24,4, `af_sarah` −22,0, `am_adam` −20,9 LUFS — chênh tới 4,6 dB, nên việc chuẩn âm lượng trước khi chấm là cần. Độ dài từ trung bình: `am_adam` 1.224 ms, `am_michael` 1.390, `af_heart` 1.428, `af_bella` 1.445, `af_sarah` 1.741. Chuỗi âm: 25 văn bản, 0 văn bản có chuỗi khác nhau giữa các giọng, đúng như quyết định 7.
- [ ] B6 Chủ dự án nghe 3 phiên, 3 bảng, 375 dòng — kết quả: **1/3 phiên.** `sheet_R1.csv` lưu 2026-10-09 10:11 ở `voices/_key/`: 125 dòng, 125 mẫu khác nhau, thứ tự 1 đến 125 liền mạch, mọi điểm trong thang 1–5, `check_sheet` không báo lỗi. Phân bố chung cả bảng (chưa tách theo giọng, để giữ mù cho hai phiên sau): Rõ ràng 1:0 2:1 3:14 4:52 5:58, trung bình 4,34; Tự nhiên 1:1 2:17 3:39 4:43 5:25, trung bình 3,59. Lượt này cũng là phép thử trình duyệt thật của `rate.html`: phát được, lưu được tệp. Còn R2 và R3.
- [ ] B7 Tính trung bình, chọn 1 Nữ + 1 Nam — kết quả:
- [ ] B8 Kiểm "wind" hai cách đọc, ghi `docs/tasks/P.4/wind-check.md` — kết quả:
- [ ] B9 Ghi quyết định vào `docs/01-yeu-cau.md` dòng 357 — kết quả:
- [ ] B10 Cổng B: Result.md + Delivery + quét bằng chứng — kết quả:

## Kiểm tra
| Test | Cách chạy | Input | Output thật | Đạt? |
| --- | --- | --- | --- | --- |
| 1 125 mẫu, đúng độ dài | `.venv/Scripts/python tools/pipeline/env/voice_samples.py` | 20 từ + 5 câu × 5 giọng | 125 Opus, 25 mỗi giọng; từ 856–2.031 ms (ngưỡng 300–4.000); câu 2.232–3.756 ms (ngưỡng 800–8.000); exit 0 | Đạt |
| 2 Mẫu đều âm lượng | đo `ebur128` trên từng tệp Opus, trong cùng script | 125 tệp | −16,8 đến −15,9 LUFS (ngưỡng −18 đến −14); mức tăng âm +5,0 đến +12,8 dB | Đạt |
| 3 Tên mù | `ls voices`, grep trong `rate.html` | — | 0 tên tệp chứa `af_` hay `am_`; 0 tên giọng và 0 chữ `key.csv` trong trang; `key.csv` chỉ ở `_key/` | Đạt |
| 5b Bảng đo | `voices/_key/measures.csv` | — | 125 dòng, đủ độ dài, âm lượng gốc và sau chuẩn, chuỗi âm | Đạt |
| 6 Hai cách đọc "wind" (chuỗi âm) | cùng script | "wind" đứng riêng; "Please wind the clock before you leave the kitchen." | đứng riêng `/wˈɪnd/`; trong câu `/plˈiz wˈInd ðə klˈɑk .../`; cả hai có mặt đúng. Chuỗi này giống nhau ở cả 5 giọng, nên đúng cho mọi giọng thắng. Tai người vẫn phải xác nhận ở B8 | Đạt (chuỗi âm) |
| 8 Script của P.3 còn chạy | `tts_sample.py`, `encode_opus.py` | — | 10 WAV cùng tên như `records/P.3.md`; `10 files, 0 outside the target` | Đạt |
| 9 Không có gì nặng trong git | `git status --short` | — | chỉ tệp mã; không Opus, WAV, CSV của `audio_test/` | Đạt |
| 11 Cổng xanh, có test mới | `bash tools/checks/gate.sh full` | — | 4 mục Đạt; `25 passed` | Đạt |

## Xác minh output trước khi đóng (CLAUDE.md §3)
- [ ] `bash tools/checks/gate.sh full` sạch:
- [ ] Audio: duration trong ngưỡng, loudness −16 ±2 LUFS, mỗi từ đủ 5 giọng đang thử:

## Bằng chứng
- Commit/PR:
- File đầu ra:
- Ảnh/số đo:
- Delivery đã quét khoá/token/dữ liệu người thật:

## Giải thích
Bảy quyết định trước khi làm nằm trong Decisions log của `docs/tasks/P.4/Plan.md`.

Quyết định trong lúc làm:
- 2026-10-09 — **Làm trực tiếp trong phiên dẫn, không gọi trợ thủ dựng mã.** Plan P.4 đã qua scout và
  ba lượt reviewer ở task `task-lead` (269.604 token). Phần dựng là bốn tệp nhỏ; gọi thêm agent
  dựng trong worktree sẽ tốn token mà chủ dự án chưa đặt ngân sách. Reviewer sẽ được gọi lại một
  lần trước Cổng B để đọc diff.
- 2026-10-09 — **`key.csv` nằm trong `voices/_key/`, tức là thư mục con cạnh các mẫu.** Trang chấm
  không đọc nó và tên tệp mẫu không lộ gì, nhưng người chấm vẫn mở được nếu muốn. Với một người
  chấm cũng là chủ dự án, kỷ luật là: không mở `_key/` cho tới khi xong ba phiên.
- 2026-10-09 — **Kiểm "wind" bằng chuỗi âm đã có kết quả cho mọi giọng.** Kokoro đổi chữ thành âm
  trước khi áp giọng, nên chuỗi âm không phụ thuộc giọng nào thắng. B8 còn lại phần tai người.
- 2026-10-09 — **Chưa thử trang chấm trong trình duyệt.** Phiên này không có trình duyệt. Đã kiểm
  cú pháp script bằng `node --check`. Nếu lượt nghe đầu lộ lỗi, sửa `rate.html` rồi chạy lại
  `voice_samples.py`; hạt giống cố định nên tên mẫu không đổi và điểm đã chấm vẫn dùng được.

## Câu hỏi mở
- Chưa có.

## Người kiểm: tự kiểm  Ngày:   Kết luận: Xong / Làm lại (lý do)
