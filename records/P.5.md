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
- [ ] B1 `tools/workbench/store.py` + `review.py`: lưu an toàn, bảng trạng thái, luật R1–R7 — kết quả:
- [ ] B2 `tools/workbench/server.py` + `static/`: máy chủ 127.0.0.1 và trang một-từ-một-màn — kết quả:
- [ ] B3 `export.py`, `check_files.py`, `report.py` — kết quả:
- [ ] B4 `tools/checks/test_workbench.py`: 44 test — kết quả:
- [ ] B5 Dữ liệu thử: `seed_trial.py`, `content/pack/trial/`, ảnh SVG giữ chỗ — kết quả:
- [ ] B6 Audio thử: `make_trial_audio.py`, 58 tệp — kết quả:
- [ ] B7 `.gitattributes`; hình dạng tệp làm việc vào `docs/07` §5.5 — kết quả:
- [ ] B8 Mở được 30 từ, duyệt hết bằng phím (chủ dự án duyệt ≥ 12 từ) — kết quả:
- [ ] B9 CSV cập nhật đúng cột review_* (so trước/sau) — kết quả:
- [ ] B10 Hàng đợi needs_second hoạt động — kết quả:
- [ ] B11 Báo cáo giây/từ — kết quả:
- [ ] B12 Hai ảnh chụp màn hình của chủ dự án — kết quả:
- [ ] B13 Cổng B: reviewer đọc diff, Result.md + Delivery + quét bằng chứng — kết quả:

## Kiểm tra
| Test | Cách chạy | Input | Output thật | Đạt? |
| --- | --- | --- | --- | --- |

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

## Câu hỏi mở
- Chưa có.

## Người kiểm: tự kiểm  Ngày:   Kết luận: Xong / Làm lại (lý do)
