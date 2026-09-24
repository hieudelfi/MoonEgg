# docs/Delivery/ — gói bằng chứng cho người kiểm (dựng ở Cổng B)

Một thư mục mỗi lần giao: `<YYYY-MM-DD>_<task-id>/`.

Bên trong: `evidence/` (log, ảnh, mẫu audio, CSV trích), số đo, và bản kết quả dạng đọc được.

Trước khi đẩy: **quét `evidence/` tìm token, khoá, số máy, dữ liệu người thật.** Bản delivery là
tệp đóng băng, đẩy rồi không rút lại được. Ghi ngày quét và kết quả vào `records/<task-id>.md`.

Không đưa vào đây: ghi âm giọng người học (CLAUDE.md §4), khoá API, tệp `.env`.
