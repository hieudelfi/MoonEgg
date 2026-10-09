# P.4 — Chốt giọng đọc

Bắt đầu: 2026-10-09 (Plan viết 2026-10-08 trong lần chạy thử task-lead; Cổng A duyệt 2026-10-09)  Kết thúc: 2026-10-09  Công thực tế: chưa đo (ước: 0,5)
Token: scout và reviewer của Plan đã tính vào `records/task-lead.md` (269.604) · reviewer trước Cổng B: opus, 128.090 (tổng riêng P.4: 128.090; phiên dẫn công cụ không báo)
Type: DATA  Level: L2  Repro (ISSUE): không áp dụng
Người kiểm: tự kiểm  Nhánh: `chore/p4-voices` (cắt từ `main` tại `c54337e`)
Plan: https://hub.yawasa.com/app/p/moonegg-p4-plan  Flow: bỏ — Type DATA, không có màn hình  Result: https://hub.yawasa.com/app/p/moonegg-p4-result
Delivery: `docs/Delivery/2026-10-09_P.4/` · https://hub.yawasa.com/app/p/moonegg-p4-delivery
Tham chiếu: Kế hoạch §3P.1 P.4 · Yêu cầu §8.3 · ngưỡng TC-CT-02, TC-CT-05
Phụ thuộc: P.3 (Xong 2026-10-08)

## Checklist
- [x] B1 `_paths.py`: 20 từ, 5 câu, 5 giọng ứng viên; `_kokoro.py` dùng chung — kết quả: `_paths.py` thêm `CANDIDATE_VOICES` (5), `SAMPLE_WORDS` (20 headword khác nhau, "wind" một lần), `SENTENCES` (5 câu, 6 đến 9 từ, không chữ số), `VOICES_DIR`, `KEY_DIR`; `WORDS` và `VOICES` không đổi. `_kokoro.py` giữ hai module giả và hai hàm `make_pipeline`, `speak`. `tts_sample.py` chuyển sang dùng nó: chạy lại ra đúng 10 tệp cùng tên như bản ghi P.3. `encode_opus.py` tách hàm `level_and_encode`; chạy lại `10 files, 0 outside the target`.
- [x] B2 `voice_samples.py`: 125 mẫu mù, đã chuẩn âm lượng, `key.csv` để riêng — kết quả: tải 3 tệp giọng còn thiếu (`af_bella.pt`, `af_sarah.pt`, `am_adam.pt`) về bộ nhớ đệm ổ D, sau Cổng A. 125 tệp `s001.opus` đến `s125.opus` ở `content/pack/audio_test/voices/`, 25 tệp mỗi giọng. Từ dài 856 đến 2.031 ms, câu 2.232 đến 3.756 ms. Âm lượng đo lại −16,8 đến −15,9 LUFS. Nạp 5 giọng 43,0 giây (có tải), 0,776 giây mỗi mẫu, cả lượt 3 phút 3 giây. `key.csv` nằm ở `voices/_key/`. Ổ C: 14,35 GB trước và sau.
- [x] B3 `rate.html`: phát ngẫu nhiên, 2 điểm, mã phiên nghe — kết quả: một trang tĩnh, không cần máy chủ. `voice_samples.py` chép nó vào cạnh các mẫu và ghi sẵn danh sách 125 tệp. Chọn phiên R1, R2 hoặc R3; thứ tự xáo riêng từng phiên; hai thang 1 đến 5; phím tắt; dừng giữa chừng được vì điểm lưu trong trình duyệt; cuối phiên lưu `sheet_R<n>.csv`. Trang không chứa tên giọng nào (grep = 0). `node --check` phần script: sạch. **Chưa mở thử trong trình duyệt thật** — phiên này không có trình duyệt; lượt nghe đầu của chủ dự án là phép thử.
- [x] B4 `score.py` + `tools/checks/test_voice_scores.py` — kết quả: `score.py` ghép bảng với khoá, loại bảng thiếu dòng hoặc điểm ngoài thang, in trung bình và độ lệch giữa các phiên theo giọng, chỉ nêu tên giọng thắng khi đủ 3 bảng, báo hoà và báo giọng dưới 3 điểm. Chạy khi chưa có bảng nào: `sheets: 0 complete of 3 needed`, không nêu tên. 11 test mới, cả bộ `25 passed`.
- [x] B5 `measures.csv`: bảng đo của phiên, tách khỏi điểm — kết quả: 125 dòng ở `voices/_key/measures.csv`. Âm lượng gốc trung bình theo giọng: `af_bella` −25,5, `am_michael` −24,7, `af_heart` −24,4, `af_sarah` −22,0, `am_adam` −20,9 LUFS — chênh tới 4,6 dB, nên việc chuẩn âm lượng trước khi chấm là cần. Độ dài từ trung bình: `am_adam` 1.224 ms, `am_michael` 1.390, `af_heart` 1.428, `af_bella` 1.445, `af_sarah` 1.741. Chuỗi âm: 25 văn bản, 0 văn bản có chuỗi khác nhau giữa các giọng, đúng như quyết định 7.
- [x] B6 Chủ dự án nghe 3 phiên, 3 bảng, 375 dòng — kết quả: `sheet_R1.csv` lưu 10:11, `sheet_R2.csv` 16:04, `sheet_R3.csv` 16:11 ngày 2026-10-09, cả ba ở `voices/_key/` (bản trang lúc đó bảo lưu vào đó). Mỗi bảng 125 dòng, 125 mẫu khác nhau, mã phiên trong tệp khớp tên tệp, mọi điểm trong thang 1–5; ba thứ tự phát khác nhau. Trung bình cả bảng Rõ ràng / Tự nhiên: R1 4,34 / 3,59; R2 4,37 / 3,74; R3 3,78 / 3,60. **Nghi vấn ở R3:** 101/125 dòng có hai điểm giống nhau (R1: 41, R2: 52) và R3 lưu sau R2 đúng 7 phút. Trang chấm lúc đó có lỗi phím giữ tự điền cả hai điểm; chưa chứng minh được đó là nguyên nhân. Lượt R1 cũng là phép thử trình duyệt thật của trang: phát được, lưu được.
- [x] B7 Tính trung bình, chọn 1 Nữ + 1 Nam — kết quả: `score.py` trên 3 bảng: `af_heart` 8,59 · `af_sarah` 8,41 · `af_bella` 8,11 · `am_adam` 7,45 · `am_michael` 6,45 (tổng hai trung bình, thang 10). Chọn **Nữ `af_heart`, Nam `am_adam`**. `am_adam` dẫn ở cả 3 phiên (cách 1,60 · 1,08 · 0,32). `af_heart` dẫn ở R1 và R2, thua `af_sarah` 0,20 ở R3; cách biệt chung 0,17. Tính lại theo từng tổ hợp phiên: R1, R2, R1+R2, R1+R2+R3 đều ra cùng hai giọng; chỉ riêng R3 ra `af_sarah`. Reviewer tự cộng lại từ tệp gốc, khớp cả năm số.
- [x] B8 Kiểm "wind" hai cách đọc, ghi `docs/tasks/P.4/wind-check.md` — kết quả: chuỗi âm đạt: đứng riêng `wˈɪnd`, trong câu động từ `wˈInd`, trong câu danh từ "The cold wind and rain…" `wˈɪnd`; giống nhau ở cả 5 giọng. Đã ghi `wind-check.md`. Phần chuỗi âm đủ cho Definition of Done. **Phần tai người không làm trong task này**: chủ dự án chưa nghe riêng bốn mẫu; chuyển sang P.10 và ghi rõ ở đầu `wind-check.md`.
- [x] B9 Ghi quyết định vào `docs/01-yeu-cau.md` dòng 357 — kết quả: ô quyết định của dòng "Giọng đọc" thêm "Chốt 2026-10-09 (task P.4, Kokoro-82M): Nữ `af_heart`, Nam `am_adam`". `git diff --stat`: 1 dòng đổi. Bảng ứng viên ở dòng 366 giữ nguyên làm lịch sử. Đã cập nhật docs/01 §8.3. `tools/pipeline/ENV.md` mục 3 và 4 cũng sửa cho khớp `_kokoro.py`. Commit `859a022`.
- [x] B10 Cổng B: Result.md + Delivery + quét bằng chứng — kết quả: `docs/tasks/P.4/Result.md` viết và đẩy hub. `docs/Delivery/2026-10-09_P.4/` có `index.md`, `README.md`, 14 tệp bằng chứng gồm ba bảng điểm gốc, khoá, bảng đo và báo cáo reviewer. Quét: 0 phát hiện; bảng điểm chỉ có mã R1–R3. Cổng B duyệt 2026-10-09; Delivery đã đẩy hub, riêng tư; nhánh gộp vào `main` bằng `gate.sh merge`.

## Kiểm tra
| Test | Cách chạy | Input | Output thật | Đạt? |
| --- | --- | --- | --- | --- |
| 1 125 mẫu, đúng độ dài | `.venv/Scripts/python tools/pipeline/env/voice_samples.py` | 20 từ + 5 câu × 5 giọng | 125 Opus, 25 mỗi giọng; từ 856–2.031 ms (ngưỡng 300–4.000); câu 2.232–3.756 ms (ngưỡng 800–8.000); exit 0 | Đạt |
| 2 Mẫu đều âm lượng | đo `ebur128` trên từng tệp Opus, trong cùng script | 125 tệp | −16,8 đến −15,9 LUFS (ngưỡng −18 đến −14); mức tăng âm +5,0 đến +12,8 dB | Đạt |
| 3 Tên mù | `ls voices`, grep trong `rate.html` | — | 0 tên tệp chứa `af_` hay `am_`; 0 tên giọng và 0 chữ `key.csv` trong trang; `key.csv` chỉ ở `_key/` | Đạt |
| 4 Ba bảng đủ | `score.py` đọc `voices/_key/` | 3 tệp | `sheets: 3 complete of 3 needed (R1, R2, R3)`; 375 dòng; kèm ghi chú `R3: 101 of 125 rows have the same number for both scores` | Đạt, có nghi vấn ở R3 |
| 5 Trung bình | `python tools/pipeline/env/score.py` | 3 bảng + `key.csv` | 5 giọng × 75 dòng; in cột từng phiên; `female af_heart UNSTEADY: leads in 2 of 3 sittings, overall margin 0.17`; `male am_adam leads in every sitting, margin 1.00` | Đạt |
| 5b Bảng đo | `voices/_key/measures.csv` | — | 125 dòng, đủ độ dài, âm lượng gốc và sau chuẩn, chuỗi âm | Đạt |
| 6 Hai cách đọc "wind" (chuỗi âm) | cùng script | "wind" đứng riêng; "Please wind the clock before you leave the kitchen." | đứng riêng `/wˈɪnd/`; trong câu `/plˈiz wˈInd ðə klˈɑk .../`; cả hai có mặt đúng. Chuỗi này giống nhau ở cả 5 giọng, nên đúng cho mọi giọng thắng. Tai người vẫn phải xác nhận ở B8 | Đạt (chuỗi âm) |
| 7 Quyết định đã ghi | `git diff docs/01-yeu-cau.md` | — | 1 dòng đổi, dòng 357, hai tên giọng và ngày | Đạt |
| 8 Script của P.3 còn chạy | `tts_sample.py`, `encode_opus.py` | — | 10 WAV cùng tên như `records/P.3.md`; `10 files, 0 outside the target` | Đạt |
| 9 Không có gì nặng trong git | `git status --short` | — | chỉ tệp mã; không Opus, WAV, CSV của `audio_test/` | Đạt |
| 10 Delivery sạch | quét `docs/Delivery/2026-10-09_P.4/` | 16 tệp | 0 khớp mẫu khoá, email, tên máy, đường dẫn người dùng; bảng điểm chỉ có mã R1–R3 | Đạt |
| 11 Cổng xanh, có test mới | `bash tools/checks/gate.sh full` | — | 4 mục Đạt; `33 passed` (19 test của P.4) | Đạt |
| phụ: từ lạ giữa câu | `speak()` với "Please wind the zzyxqa before you leave." | — | dừng: `Kokoro has no sounds for ['zzyxqa']` | Đạt |
| phụ: bộ hãm đỉnh theo giọng | `measures.csv`, mức tăng âm vượt mức cần để chuẩn | 100 từ | `am_michael` 2,6 dB · `am_adam` 1,8 · `af_sarah` 1,0 · `af_heart` 0,8 · `af_bella` 0,7 | ghi nhận, không có ngưỡng |

## Xác minh output trước khi đóng (CLAUDE.md §3)
- [x] `bash tools/checks/gate.sh full` sạch: 2026-10-09, 4 mục Đạt, `33 passed`, nguyên văn ở `docs/Delivery/2026-10-09_P.4/evidence/test11-gate-full.txt`
- [x] Audio: duration trong ngưỡng (từ 856–2.031 ms, câu 2.232–3.756 ms); loudness −16,8 đến −15,9 LUFS; mỗi văn bản đủ 5 giọng; người nghe nghe 100% mẫu ba lần, danh sách là ba bảng điểm

## Bằng chứng
- Commit/PR: không mở PR. Mã: `455d5ff`, `1427e07`, `a6e6cc7`; tài liệu: `859a022`. Xem `git log main..chore/p4-voices`.
- File đầu ra: `tools/pipeline/env/{_kokoro.py, voice_samples.py, rate.html, score.py}`, `tools/checks/test_voice_scores.py`, `docs/tasks/P.4/wind-check.md`, `docs/01-yeu-cau.md` dòng 357. Ngoài git: `content/pack/audio_test/voices/` với 125 Opus, khoá, bảng đo, ba bảng điểm.
- Ảnh/số đo: `docs/Delivery/2026-10-09_P.4/evidence/`.
- Delivery đã quét khoá/token/dữ liệu người thật: 2026-10-09, 0 phát hiện.

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

- 2026-10-09 — **Gọi reviewer trước Cổng B, 128.090 token, 24 lỗi.** 20 lỗi sửa trong commit `a6e6cc7` và
  `859a022`; 4 lỗi để lại có lý do. Danh sách đầy đủ ở `evidence/reviewer-gate-b.txt`. Reviewer cũng
  tự cộng lại năm tổng điểm từ tệp gốc và khớp.
- 2026-10-09 — **Sửa trang chấm sau khi đã chấm xong.** Không sinh lại audio: thêm chế độ
  `voice_samples.py --page-only` chỉ viết lại trang, vì sinh lại có thể làm audio khác đi so với
  thứ đã được chấm. Trang đã sửa chưa được dùng cho phiên nghe nào.
- 2026-10-09 — **Sơ suất của phiên dẫn: ghi độ dài trung bình theo giọng vào bản ghi (B5) trước phiên 2 và 3.**
  `af_sarah` dài hơn hẳn (1.741 ms so với khoảng 1.430), và trang chấm hiện độ dài từng mẫu, nên
  người chấm đọc bản ghi có thể nhận ra giọng đó. Không gỡ lại được. Từ nay số đo theo giọng chỉ
  ghi sau khi đủ bảng điểm; `score.py` giờ cũng không in gì về giọng trước ba phiên.
- 2026-10-09 — **Bản ghi đi sau đĩa một nhịp.** Quyết định giọng đã vào `docs/01` trước khi B7–B9
  có dòng kết quả. Trái bước 5 của quy trình. Đã ghi bù trong lượt này.
- 2026-10-09 — **Không tự loại bảng R3.** Kết quả không đổi dù có hay không có R3, nên giữ nguyên
  375 dòng và nêu nghi vấn; có chấm lại R3 hay không là việc của chủ dự án ở Cổng B.
- 2026-10-09 — **Cờ "UNSTEADY" chỉ bật khi giọng thắng thua ở ít nhất một phiên.** Bản đầu bật cả
  khi cách biệt nhỏ hơn độ lệch giữa các phiên, và báo nhầm `am_adam` dù nó dẫn cả ba phiên: một
  phiên chấm thấp đều tay làm độ lệch tăng mà thứ tự không đổi.

- 2026-10-09 — **Cổng B, ba quyết định của chủ dự án.** Giọng nữ: duyệt `af_heart`. Bảng R3: giữ nguyên;
  nguyên văn "thực sự giọng nam khó nghe hơn", tức điểm thấp ở phiên đó là có chủ ý, không phải lỗi
  phím. Nghi vấn về 101 dòng trùng điểm vì thế khép lại theo lời người chấm, không theo bằng chứng
  máy. Nghe thẳng "wind": chủ dự án chưa rõ phải làm gì nên không làm; chuyển sang P.10.

## Câu hỏi mở
- Không còn câu nào chặn. Một việc chuyển tiếp: P.10 xác nhận bằng tai hai cách đọc của "wind".

## Người kiểm: tự kiểm  Ngày: 2026-10-09  Kết luận: **Xong** — 12/12 dòng phép thử Đạt; chọn Nữ `af_heart`, Nam `am_adam`; Cổng B duyệt. Chuyển P.10: nghe xác nhận "wind", và xem lại trần đỉnh của bước chuẩn âm lượng cho giọng nam.
