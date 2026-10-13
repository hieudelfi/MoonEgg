# P.5 — Xưởng nội dung (content workbench)

Bắt đầu: 2026-10-09 (Plan) · 2026-10-13 (Cổng A duyệt, bắt đầu làm)  Kết thúc: <ngày>  Công thực tế: <nđ> (ước: 3)
Token: scout: sonnet, 56.061 · reviewer Plan: opus, 91.685 · reviewer trước Cổng B: opus, <chờ> (tổng: <chờ>; phiên dẫn tự dựng mã, công cụ không báo số)
Type: FEATURE  Level: L2  Repro (ISSUE): không áp dụng
Người kiểm: tự kiểm  Nhánh: `chore/p5-content-workbench` (cắt từ `main` tại `b84c4fe`)
Plan: https://hub.yawasa.com/app/p/moonegg-p5-plan  Flow: https://hub.yawasa.com/app/p/moonegg-p5-flow  Result: <link hub>
Delivery: `docs/Delivery/<ngày>_P.5/`
Tham chiếu: Kế hoạch §4.3, §3P.1 P.5 · Yêu cầu §6.2, §6.3, §6.4, §13.1 · Kiến trúc §5.5, §7.1 · TC-CT-06 (nửa độ dài), TC-CT-07
Phụ thuộc: P.1 (Xong 2026-09-24); dùng giọng của P.4 (Xong 2026-10-09)
Chạy bằng: `/task-lead P.5`, mức token "Vừa": không có trợ thủ dựng mã

## Checklist
- [x] B1 `tools/workbench/store.py` + `review.py`: lưu an toàn, bảng trạng thái, luật R1–R7 — kết quả: `store.py` đọc/ghi 5 tệp làm việc: ghi qua tệp tạm rồi đổi tên, LF, giữ cột lạ đúng chỗ, từ chối ghi khi tệp trên đĩa đã đổi; nhật ký chỉ ghi thêm. `review.py` có lớp `Review` với đủ bảng trạng thái của Plan §4.3: lưu ngay lựa chọn, tick, ảnh; sửa thì bản ghi thành `needs_second` và xoá 5 tick; A kiểm R1–R7 rồi mới đổi trạng thái; X chỉ đụng từ; U hoàn tác. Commit `8acdab2`.
- [x] B2 `tools/workbench/server.py` + `static/`: máy chủ 127.0.0.1 và trang một-từ-một-màn — kết quả: máy chủ thư viện chuẩn, 4 đường dẫn API và phục vụ tệp dưới `content/`. Chạy thật trên thư mục thử: `/api/words` trả 30 từ; trang, `app.js`, `style.css`, bảng khẩu hình, tệp Opus (`audio/ogg`) và ảnh SVG đều HTTP 200; `/files/../CLAUDE.md` và `/files/lexicon/../../CLAUDE.md` trả 404; gọi bằng tên máy thay vì 127.0.0.1 không kết nối được. Trang gồm `index.html`, `app.js` (15.241 byte), `style.css`; `node --check app.js` sạch. **Chưa mở trong trình duyệt thật** — phiên này không có trình duyệt. Commit `7f1f720`.
- [x] B3 `export.py`, `check_files.py`, `report.py` — kết quả: chạy thật trên một bản sao dùng-xong-xoá của thư mục thử, sau khi lái cả luồng duyệt qua API: `check_files.py` 0 lỗi; `export.py` không có `--trial` bị từ chối với "4 approved records are drafts", exit 1; có `--trial` ghi `lexicon_reviewed_trial.csv` 1 dòng; `verify_pack.py --strict` trên tệp đó: `1 bản ghi · 0 lỗi`; `report.py` in 1 từ có quyết định, 42,5 giây, và 2 từ chờ ứng viên (`hello`, `through`). Commit `b4f5271`.
- [x] B4 `tools/checks/test_workbench.py`: 44 test — kết quả: `44 passed in 2.53s` ngay lần chạy đầu; cả bộ của cổng `77 passed`. Đánh số T1–T13 đúng bảng ở Plan §7. Hai test T9 dựng máy chủ thật trên cổng ngẫu nhiên.
- [x] B5 Dữ liệu thử: `seed_trial.py`, `content/pack/trial/`, ảnh SVG giữ chỗ — kết quả: 74 nghĩa (định nghĩa WordNet; 66 có nghĩa Việt nháp, 8 để trống cho người duyệt điền), 90 câu nháp, 20 ảnh SVG giữ chỗ cho 5 từ; tất cả `pending`. Hai từ không có nghĩa ứng viên: `w:hello#1`, `w:through#1`. Hai câu cố ý phạm luật: `w:market#1/e3` 14 từ, `w:umbrella#1/e3` 3 từ. Không câu nào có chữ số, không nghĩa Việt nào quá 8 từ. `check_files.py`: 0 lỗi; với `--for-pack`: 176 lỗi, đúng chủ ý vì toàn bản nháp. 25 tệp được git theo dõi. Commit `84346eb`.
- [x] B6 Audio thử: `make_trial_audio.py`, 58 tệp — kết quả: 29 mục × 2 giọng (`af_heart`, `am_adam`) = 58 tệp Opus ở `content/pack/audio_test/workbench/`, git bỏ qua. Âm lượng −16,9 đến −15,9 LUFS, mọi tệp `ok` và dài 300–4.000 ms; chạy 1 phút 36 giây. `w:wind#2` cố ý không có audio (chưa có bản đọc từ đơn của động từ); `w:wind#1` có 2 tệp.
- [x] B7 `.gitattributes`; hình dạng tệp làm việc vào `docs/07` §5.5 — kết quả: `.gitattributes` 2 dòng, LF cho CSV và SVG dưới `content/pack/`. `docs/07-kien-truc.md` §5.5 thêm một đoạn, bảng 5 tệp và 9 gạch đầu dòng, gồm ánh xạ sang SENSE, EXAMPLE và `WORD.image_asset`. Đã cập nhật docs/07 §5.5; mục 7.1 không đổi. Commit `ce12b6d`.
- [ ] B8 Mở được 30 từ, duyệt hết bằng phím (chủ dự án duyệt ≥ 12 từ) — kết quả:
- [ ] B9 CSV cập nhật đúng cột review_* (so trước/sau) — kết quả:
- [ ] B10 Hàng đợi needs_second hoạt động — kết quả:
- [ ] B11 Báo cáo giây/từ — kết quả:
- [ ] B12 Hai ảnh chụp màn hình của chủ dự án — kết quả:
- [ ] B13 Cổng B: reviewer đọc diff, Result.md + Delivery + quét bằng chứng — kết quả:

## Kiểm tra
| Test | Cách chạy | Input | Output thật | Đạt? |
| --- | --- | --- | --- | --- |
| 1 Test luật | `python -m pytest tools/checks/test_workbench.py -q` | 44 test | `44 passed in 2.53s` | Đạt |
| 2 Mở 30 từ | chạy `server.py content/pack/trial`, `GET /api/words?queue=1` | thư mục thử | 30 mục, người duyệt `hieudelfi` | Đạt |
| phụ: cả luồng qua API | script gọi `/api/action` trên bản sao dùng-xong-xoá | `w:market#1`, `w:hello#1` | A khi chưa chọn gì: 422 R1; thiếu ảnh: 422 R7; bản sửa đổi cũ: 409; sau khi sửa câu: bản ghi `needs_second`, tick `00000`, từ vẫn `pending`; A khi tick bị xoá: 422 R5; A: từ `needs_second`, hàng đợi 2 có đúng 1 từ; A lần 2: từ `approved`, hàng đợi 2 rỗng; từ không có nghĩa: 422 R1; X rồi U: `pending` | Đạt |
| phụ: tệp sau một lượt duyệt | `diff` `examples.csv` trước và sau trên bản sao | 1 từ duyệt, 1 câu sửa | 6 dòng khác nhau (3 dòng của `w:market#1`, mỗi dòng cũ và mới); 87 dòng còn lại y nguyên | Đạt |
| 8 Bản nháp không đóng gói được | `check_files.py content/pack/trial --for-pack`; `export.py <bản sao>` | — | 176 lỗi "a draft cannot be packed"; export exit 1 "4 approved records are drafts" | Đạt |
| 10 Audio (phần máy) | `make_trial_audio.py` | 29 mục × 2 giọng | 58 tệp, −16,9 đến −15,9 LUFS, exit 0 | Đạt phần máy; phần nghe chờ chủ dự án |
| 12 Cổng | `bash tools/checks/gate.sh full` | — | 4 mục Đạt, `77 passed` | Đạt |

## Xác minh output trước khi đóng (CLAUDE.md §3)
- [ ] `bash tools/checks/gate.sh full` sạch:
- [ ] Dữ liệu: `verify_pack.py --strict` trên bản xuất; `check_files.py` trên thư mục làm việc:
- [ ] Audio thử: duration, loudness, 2 giọng:
- [ ] Màn hình: hai ảnh chụp:

## Bằng chứng
- Commit/PR:
- File đầu ra:
- Ảnh/số đo:
- Delivery đã quét khoá/token/dữ liệu người thật:

## Giải thích
Bốn quyết định trước khi làm nằm trong Decisions log của `docs/tasks/P.5/Plan.md`.

Quyết định trong lúc làm:
- 2026-10-13 — **Thêm phím Q đổi hàng đợi.** Plan chỉ có hai nút bấm. Tab đã dùng để nhảy giữa các bản ghi nên
  không với tới nút bằng bàn phím, mà test 3 đòi duyệt cả lượt 2 không chạm chuột. Ghi vào Plan
  quyết định 5 và Flow §3.
- 2026-10-13 — **Tách `store.py` khỏi `review.py`.** Plan nói luật nằm ở `review.py`; phần đọc/ghi tệp tách
  riêng để `export.py`, `check_files.py`, `report.py` dùng chung mà không kéo theo luật duyệt.
- 2026-10-13 — **"Duyệt lần 2 hay chưa" phân biệt bằng mốc thời gian, không thêm cột.** Một bản ghi
  `needs_second` được duyệt ở lượt 2 khi `reviewed_at` của nó không muộn hơn `reviewed_at` của từ (lúc A
  lượt 1). Sửa lại trong lượt 2 thì mốc của bản ghi muộn hơn, nên nó ở lại hàng đợi. Giới hạn đã biết:
  mốc tính theo giây; một lần sửa rơi đúng cùng giây với lần A trước đó sẽ được coi là đã qua lượt 2.
  Với người thao tác tay thì không xảy ra; ghi lại để reviewer cân nhắc.
- 2026-10-13 — **Thử luồng thật trên bản sao, không trên thư mục thử.** Để `content/pack/trial/` còn nguyên
  `pending` cho chủ dự án duyệt. Bản sao đặt ở `content/pack/audio_test/_wb_live`, đã xoá.
- 2026-10-13 — **8 nghĩa không có nghĩa Việt nháp.** Định nghĩa thứ ba của `cold`, `egg`, `kettle`,
  `exhausted`, `decision`, `rain` và hai định nghĩa của `mother` lúc viết nháp tôi không thấy trọn câu
  hoặc không phải nghĩa thông dụng, nên để trống thay vì đoán. Cũng là dữ liệu thử cho luật R2.
- 2026-10-13 — **Chưa thử trang trong trình duyệt.** Như P.4: chỉ kiểm cú pháp và gọi API thật. Lượt duyệt
  đầu của chủ dự án là phép thử trình duyệt.

## Câu hỏi mở
- Chưa có.

## Người kiểm: tự kiểm  Ngày:   Kết luận: Xong / Làm lại (lý do)
