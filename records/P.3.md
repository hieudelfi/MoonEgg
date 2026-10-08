# P.3 — Môi trường pipeline

Bắt đầu: 2026-10-08 (Plan và Cổng A duyệt cùng ngày)  Kết thúc: <ngày>  Công thực tế: <nđ> (ước: 1,5)
Type: INFRA  Level: L2  Repro (ISSUE): không áp dụng
Người kiểm: tự kiểm  Nhánh: `chore/p3-pipeline-env` (cắt từ `main` tại `4963232`)
Plan: https://hub.yawasa.com/app/p/moonegg-p3-plan  Flow: bỏ — Type INFRA, không có màn hình  Result: <link hub>
Delivery: `docs/Delivery/<ngày>_P.3/`
Tham chiếu: Kế hoạch §3P.1 P.3 · Kiến trúc §5.5 · Yêu cầu §8.3, §9.3 · ngưỡng của TC-CT-02, TC-CT-04
Phụ thuộc: P.1 (Xong 2026-09-24)

## Checklist
- [ ] B1 Hai môi trường và bộ nhớ đệm trên D: (`.venv`, `.mfa`, `.cache`) — kết quả:
- [ ] B2 Liệt kê giấy phép mọi gói đã cài, trước khi dùng — kết quả:
- [ ] B3 `tts_sample.py`: 5 audio × 2 giọng tồn tại — kết quả:
- [ ] B4 `encode_opus.py`: 10 file Opus loudness −16 ±2 LUFS — kết quả:
- [ ] B5 `align_sample.py`: TextGrid có tier phones — kết quả:
- [ ] B6 `check_textgrid.py` + test trong `tools/checks/`: so phone với CMUdict — kết quả:
- [ ] B7 1 ảnh SD hoặc lý do — kết quả:
- [ ] B8 `build_lexicon.py` chạy lại trong venv — kết quả:
- [ ] B9 `ENV.md` có phiên bản, lệnh cài, bảng thời gian; `requirements.txt`; dòng mới trong `sdk-allowlist.md` — kết quả:
- [ ] B10 Người review nghe 10 file, ghi nhận xét — kết quả:
- [ ] B11 Cổng B: Result.md + Delivery + quét bằng chứng — kết quả:

## Kiểm tra
| Test | Cách chạy | Input | Output thật | Đạt? |
| --- | --- | --- | --- | --- |

## Xác minh output trước khi đóng (CLAUDE.md §3)
- [ ] `bash tools/checks/gate.sh full` sạch:
- [ ] Audio: duration trong ngưỡng, loudness −16 ±2 LUFS, đủ 2 giọng:
- [ ] Timing: mốc tăng đơn điệu, kết ≤ duration, có `mismatch.csv`:

## Bằng chứng
- Commit/PR:
- File đầu ra:
- Ảnh/số đo:
- Delivery đã quét khoá/token/dữ liệu người thật:

## Giải thích
Sáu quyết định của Cổng A nằm trong Decisions log của `docs/tasks/P.3/Plan.md`, không chép lại ở đây.

Số đo máy trước khi cài (2026-10-08): C: trống 7,9 GB, D: trống 161,4 GB.

Quyết định trong lúc làm:

## Câu hỏi mở
- Chưa có.

## Người kiểm: tự kiểm  Ngày:   Kết luận: Xong / Làm lại (lý do)
