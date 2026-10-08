# Giao P.2 — Supabase, R2, địa chỉ web (2026-10-08)

Bản ghi đầy đủ: `records/P.2.md`. Kế hoạch và kết quả trên hub: xem `records/P.2.md` phần đầu.

## Trong thư mục này

| Tệp | Là gì |
| --- | --- |
| `evidence/gate-full.txt` | Cổng đầy đủ chạy ở máy, 4 mục |
| `evidence/tests-1-2-3-6-9-from-record.txt` | Năm phép thử đo ngày 2026-09-25 bằng hai tài khoản thử, chép bằng script từ bản ghi |
| `evidence/rls-anon-sees-nothing.txt` | Người không đăng nhập đọc 7 bảng và thử ghi |
| `evidence/auth-providers.txt` | Cách đăng nhập đang bật |
| `evidence/test04-r2-read.txt` | Đọc một tệp công khai trên R2 |
| `evidence/test05-web-address.txt` | Địa chỉ web trả lời, kể cả đường dẫn con |
| `evidence/test07-ping.txt` | Ping chạy tay và toàn bộ nhật ký ping |
| `evidence/test08-no-secret-in-repo.txt` | Tìm khoá trong các tệp git theo dõi |
| `evidence/test10-test-users-gone.txt` | Hai tài khoản thử bị từ chối đăng nhập |
| `evidence/files-in-repo.txt` | Số đếm trong `schema.sql`, `wrangler.jsonc`, `.env.example`, luật bỏ qua |
| `evidence/scan.txt` | Kết quả quét bằng chứng |

## Quét trước khi giao

Ngày 2026-10-08. Tìm token, khoá API, chuỗi JWT, số máy, dữ liệu người thật trong `evidence/`.
Kết quả ghi ở `evidence/scan.txt`: 0 phát hiện.
