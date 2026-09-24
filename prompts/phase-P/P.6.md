# P.6 — Đặc tả lõi và test vàng

**Tham chiếu:** Kế hoạch §3P.1 P.6 · Kiến trúc §5.2, §5.3, §5.6 · Kiểm thử §2.4, §3

## Mục tiêu
Đặc tả 5 module bằng văn bản + file golden JSON sinh từ ts-fsrs, dùng chung TS và Dart.

## Cách làm
1. Viết `core-spec/fsrs.md` (tham số mặc định ts-fsrs, grade 1–4, desired retention 0.9), `levels.md` (ngưỡng FR-60), `session-builder.md` (thuật toán §5.3 + hàng đợi từ mới §5.6), `placement.md`, `quiz-pick.md` (trọng số §5.6, distractors).
2. Script `golden/gen_fsrs.ts` (Node + ts-fsrs): sinh 200 kịch bản (chuỗi grade ngẫu nhiên seed cố định) → `golden/fsrs.json` với state vào/ra đến 3 chữ số thập phân.
3. Viết tay `golden/session.json` (8 kịch bản SB-01→06, SB-09/10), `golden/placement.json` (3), `golden/quiz.json` (3: QZ-06→08) theo docs/08-kiem-thu.md §3, §4.6, dùng hồ sơ U-DAY7/U-BACK mô tả ở §2.2.
4. Người thứ hai review đặc tả (hoặc tự review sau 12 giờ, ghi rõ).

## Checklist (chép vào records/P.6.md, tick từng dòng kèm 'kết quả:')
- [ ] 5 file đặc tả
- [ ] golden/fsrs.json 200 kịch bản
- [ ] golden/session.json, placement.json, quiz.json
- [ ] Review có tên/ngày

## Kiểm tra (test đối chiếu)
- Chạy lại gen_fsrs.ts → file giống hệt (deterministic)

## Xác minh output trước khi đóng
- Mọi kịch bản golden có `expected` không rỗng; JSON hợp lệ
- Chạy `CLAUDE.md` §3 cho loại đầu ra; chưa qua → không đóng.

## Bằng chứng cần nộp
- Link commit
- Tên người review
