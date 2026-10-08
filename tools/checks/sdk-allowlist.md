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

## Công cụ pipeline nội dung — chỉ chạy trên máy dựng, không vào app

Cài ở task P.3, xem `tools/pipeline/ENV.md`. Phiên bản ghim ở `tools/pipeline/requirements.txt`.
Không gói nào đi vào bundle hay vào tệp audio phát hành.

| Gói | Nền tảng | Giấy phép | Vai trò |
| --- | --- | --- | --- |
| torch (bản CPU) | pipeline | BSD-3-Clause | chạy model giọng đọc |
| kokoro, model Kokoro-82M | pipeline | Apache-2.0 | sinh giọng đọc |
| misaki | pipeline | Apache-2.0 | chữ thành phoneme cho Kokoro |
| spacy, en_core_web_sm | pipeline | MIT | tách từ cho misaki |
| soundfile | pipeline | BSD-3-Clause | ghi WAV |
| nltk | pipeline | Apache-2.0 | WordNet cho `build_lexicon.py` |
| cmudict | pipeline | GPL-3.0-or-later (mã bọc), dữ liệu BSD | chỉ `build_lexicon.py` nhập; không phát hành script này |
| montreal-forced-aligner, model english_us_arpa | pipeline, môi trường conda riêng | MIT, model CC-BY-4.0 | căn mốc thời gian từng âm |
| ffmpeg | pipeline, cài sẵn trên máy | GPL (bản dựng `--enable-gpl`) | chuẩn hoá âm lượng, nén Opus |

Đã gỡ khỏi môi trường giọng đọc vì giấy phép ngoài allowlist: `phonemizer-fork`, `espeakng-loader`
(GPL-3.0), `num2words` (LGPL). Luật cho công cụ máy dựng: `CLAUDE.md` mục 5.
Môi trường conda của MFA kéo theo 28 gói họ GPL/LGPL không gỡ được; danh sách ở `ENV.md` mục 4.
