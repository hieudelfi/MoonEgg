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
- [ ] B1 `_paths.py`: 20 từ, 5 câu, 5 giọng ứng viên; `_kokoro.py` dùng chung — kết quả:
- [ ] B2 `voice_samples.py`: 125 mẫu mù, đã chuẩn âm lượng, `key.csv` để riêng — kết quả:
- [ ] B3 `rate.html`: phát ngẫu nhiên, 2 điểm, mã phiên nghe — kết quả:
- [ ] B4 `score.py` + `tools/checks/test_voice_scores.py` — kết quả:
- [ ] B5 `measures.csv`: bảng đo của phiên, tách khỏi điểm — kết quả:
- [ ] B6 Chủ dự án nghe 3 phiên, 3 bảng, 375 dòng — kết quả:
- [ ] B7 Tính trung bình, chọn 1 Nữ + 1 Nam — kết quả:
- [ ] B8 Kiểm "wind" hai cách đọc, ghi `docs/tasks/P.4/wind-check.md` — kết quả:
- [ ] B9 Ghi quyết định vào `docs/01-yeu-cau.md` dòng 357 — kết quả:
- [ ] B10 Cổng B: Result.md + Delivery + quét bằng chứng — kết quả:

## Kiểm tra
| Test | Cách chạy | Input | Output thật | Đạt? |
| --- | --- | --- | --- | --- |

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

## Câu hỏi mở
- Chưa có.

## Người kiểm: tự kiểm  Ngày:   Kết luận: Xong / Làm lại (lý do)
