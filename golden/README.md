# golden/ — bộ test vàng dùng chung TS và Dart (tạo ở P.6)

- fsrs.json — 200 kịch bản sinh từ ts-fsrs tham số mặc định (script gen_fsrs.ts). Khoá; sửa cần review.
- session.json — kịch bản dựng phiên SB-01→06, SB-09/10 (viết tay theo docs/08 §3.3, §4.6).
- placement.json — PL-01→03.
- quiz.json — QZ-06→08.
Mỗi kịch bản: { id, given: {...}, expected: {...} }. Cả web/ và mobile/ đọc trực tiếp thư mục này trong test.
