# SDK allowlist (CI chặn gói ngoài danh sách; thêm gói = thêm dòng kèm ghi chú Data Safety)

| Gói | Nền tảng | Giấy phép | Thu dữ liệu | Ghi chú Data Safety |
| --- | --- | --- | --- | --- |
| react, react-dom, vite, typescript | web | MIT | không | — |
| dexie | web | Apache-2.0 | không | — |
| ts-fsrs | web | MIT | không | — |
| howler | web | MIT | không | — |
| @rive-app/canvas | web | MIT | không | kiểm logo gói Free |
| @supabase/supabase-js | web | MIT | email, lịch sử học → máy chủ của mình | khai báo |
| firebase (messaging) | web | Apache-2.0 | token thiết bị | "device identifiers for notifications" |
| flutter, drift, just_audio | mobile | BSD/MIT | không | — |
| rive | mobile | MIT | không | kiểm logo gói Free |
| supabase_flutter | mobile | MIT | như trên | khai báo |
| firebase_messaging, flutter_local_notifications | mobile | Apache-2.0/BSD | token thiết bị | khai báo |

## Công cụ dev — không vào bundle, không phát hành

Các gói dưới đây chỉ chạy lúc dev và lúc build. Không gói nào đi vào tệp người dùng tải về, nên
không có dòng Data Safety. Vẫn phải nằm trong allowlist giấy phép như mọi gói khác.

| Gói | Nền tảng | Giấy phép | Vai trò |
| --- | --- | --- | --- |
| vitest | web | MIT | chạy test, `npm test` = `vitest run` |
| @vitejs/plugin-react | web | MIT | plugin build của Vite cho React |
| oxlint | web | MIT | lint, do Vite scaffold thêm |
| @types/react, @types/react-dom, @types/node | web | MIT | khai báo kiểu, biến mất sau khi biên dịch |
