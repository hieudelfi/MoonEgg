# P.2 — Supabase, R2, Pages

**Tham chiếu:** Kế hoạch §3P.1 P.2 · Kiến trúc §2, §7.2 · Test TC-AU-04

## Mục tiêu
Máy chủ, CDN và web tĩnh có địa chỉ; RLS chặn đọc chéo người dùng; cron ping chống Supabase tạm dừng.

## Cách làm
1. Tạo project Supabase (free). Bật Auth: Google, Apple (ghi chú: Apple cần tài khoản dev, để sau), Email magic link.
2. Chạy SQL từ Kiến trúc §7.2: bảng profile, device, review_event (event_id text PK, user_id uuid, device_id uuid, ts bigint, type text, item_type text, item_id text, payload jsonb, server_seq bigserial), user_content, settings, sync_cursor, analytics_daily. Index (user_id, server_seq); unique(event_id).
3. RLS: enable trên mọi bảng người dùng; policy `user_id = auth.uid()` cho select/insert; analytics_daily chỉ insert.
4. Cloudflare: tạo R2 bucket `vocab-content` public-read; Pages project trỏ `web/dist` (deploy trang trống).
5. GitHub Action `ping-supabase.yml` chạy mỗi 3 ngày: gọi REST select 1 dòng bằng anon key.
6. Lưu URL và anon key vào `.env.example` (không commit key thật).

## Checklist (chép vào records/P.2.md, tick từng dòng kèm 'kết quả:')
- [ ] Auth 3 cách bật (Apple ghi TODO)
- [ ] Bảng + index + RLS tạo bằng file `supabase/schema.sql` trong repo
- [ ] R2 public-read thử bằng curl một file
- [ ] Pages có URL
- [ ] Ping action chạy thử thành công

## Kiểm tra (test đối chiếu)
- TC-AU-04 sơ bộ: tạo 2 user thử, insert 1 event mỗi user, dùng token user A select → 0 dòng của B

## Xác minh output trước khi đóng
- `supabase/schema.sql` chạy lại trên project sạch không lỗi (idempotent: dùng IF NOT EXISTS)
- Chạy `CLAUDE.md` §3 cho loại đầu ra; chưa qua → không đóng.

## Bằng chứng cần nộp
- Ảnh dashboard Supabase (ẩn key)
- URL Pages
- Output curl R2
- Log ping action
