# P.4 — Chốt giọng đọc

**Tham chiếu:** Kế hoạch §3P.1 P.4 · Yêu cầu §8.3

## Mục tiêu
Chọn 1 giọng Nữ + 1 giọng Nam từ Kokoro (dự phòng Piper), có bảng điểm của 3 người nghe.

## Cách làm
1. Sinh 20 từ + 5 câu (từ lexicon_raw_test) với af_heart, af_bella, af_sarah, am_michael, am_adam.
2. Tạo trang HTML đơn giản phát ngẫu nhiên, 3 người chấm rõ ràng/tự nhiên 1–5, ghi CSV.
3. Tính trung bình; chọn; ghi quyết định vào docs/01-yeu-cau.md §8.3 (bảng giọng) và bản ghi.

## Checklist (chép vào records/P.4.md, tick từng dòng kèm 'kết quả:')
- [ ] 125 file mẫu
- [ ] 3 người chấm, CSV có 375 dòng
- [ ] Quyết định ghi vào docs

## Kiểm tra (test đối chiếu)
- Kiểm tay: bảng điểm trung bình theo giọng

## Xác minh output trước khi đóng
- Từ đồng tự khác âm (wind#1/#2) đọc đúng ở giọng đã chọn — nếu sai, ghi vào mismatch để P.10 xử lý bằng SSML/ngữ cảnh câu
- Chạy `CLAUDE.md` §3 cho loại đầu ra; chưa qua → không đóng.

## Bằng chứng cần nộp
- CSV điểm
- Diff docs/01-yeu-cau.md
