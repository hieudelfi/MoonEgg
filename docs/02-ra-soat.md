# Rà soát tài liệu v1 — đúng đắn, đầy đủ, khả thi, chi phí

Tài liệu đủ dùng để bước sang thiết kế kiến trúc sau khi sửa 4 lỗi đúng đắn, bổ sung 6 thiếu sót, và chấp nhận 3 khoản chi không thể về 0 nếu phát hành lên App Store.

## 1. Tính đúng đắn

| # | Mục | Vấn đề | Mức | Sửa |
| --- | --- | --- | --- | --- |
| Đ1 | 6.1 | Oxford 3000/5000 ghi là CC-BY-SA: sai. Danh sách này thuộc bản quyền Oxford University Press; chỉ NGSL mới CC-BY-SA | Cao | Bỏ Oxford khỏi nguồn; bù bằng NGSL (2.800) + NAWL (960, CC-BY-SA) + tần suất từ Wiktionary/kaikki hoặc COCA free sample → vẫn đủ 5.000 |
| Đ2 | 7 | Gói 500 từ đầu < 30 MB không đạt nếu sinh câu ở 2 giọng × 2 tốc độ: 1.500 câu × 4 × \~9 KB ≈ 54 MB, chưa kể audio từ | Cao | Tốc độ chậm làm bằng playbackRate 0,75 trên thiết bị (miễn phí, không tốn dung lượng); câu chỉ 1 giọng theo lựa chọn người dùng, tải theo nhu cầu; từ mới tải trước |
| Đ3 | 8.3 | Ghi Kokoro cho "phoneme timing qua misaki": Kokoro trả mốc thời gian ở mức từ, chưa chắc ở mức phoneme | Trung | Ghi rõ là cần xác minh; dự phòng bằng Montreal Forced Aligner (MIT) hoặc Rhubarb, cả hai miễn phí và cho timing mức phoneme |
| Đ4 | 1, 8.1 | Chỉ tiêu D7 ≥ 35%, D30 ≥ 15% chưa có nguồn; mức trung bình app giáo dục D30 thường 5–10% | Trung | Giữ làm mục tiêu tham vọng nhưng ghi là giả định; đặt ngưỡng tối thiểu D30 ≥ 8% |
| Đ5 | 6.1 | Hạn mức miễn phí cloud TTS (Google \~1 triệu ký tự/tháng, Azure \~500 nghìn) là số nhớ, hay thay đổi | Thấp | Ghi "kiểm tra lúc dùng"; không phụ thuộc vì đã có Kokoro |

Các phần còn lại (nguyên lý ghi nhớ, FSRS, giấy phép CMUdict/Wiktionary/Tatoeba/WordNet, bảng viseme 12 hình, Rive runtime mã nguồn mở) đúng theo hiểu biết hiện tại.

## 2. Tính đầy đủ

| # | Thiếu | Ảnh hưởng | Bổ sung vào |
| --- | --- | --- | --- |
| T1 | Ba lớp hình dạy phát âm (video miệng thật tự quay → hình cận cảnh + mặt cắt → nhân vật lip-sync) đã thống nhất trong trao đổi nhưng chưa vào tài liệu | Người học không mimic được nếu chỉ có nhân vật | 5.5 (FR-19→FR-22) và 9.1 thêm hạng mục "tự quay 44 âm + 30 từ" |
| T2 | Chưa có người kiểm tra ngữ âm: ai xác nhận audio và khẩu hình đúng? | Dạy sai phát âm là rủi ro danh tiếng lớn nhất | 6.4: cần 1 người có chuyên môn ngữ âm duyệt 44 âm và 200 từ khó; tìm tình nguyện (giáo viên, sinh viên sư phạm Anh) |
| T3 | Chưa nêu nền tảng phát hành và lưu trữ miễn phí cụ thể | Không đánh giá được "chi phí 0" | Xem mục 4 dưới |
| T4 | Chưa có quy tắc chọn 1–3 nghĩa phổ biến (Wiktionary có 5–20 nghĩa/từ) | Nút thắt biên soạn lớn nhất không có tiêu chí | 6.3: ưu tiên nghĩa có trong NGSL sense list / WordNet sense frequency; LLM xếp hạng rồi người duyệt |
| T5 | Chưa có kế hoạch nội dung cho câu ví dụ: 15.000 câu ai viết, theo mẫu nào | Công sức lớn nhất chưa được ước lượng thật | 6.3: mẫu prompt sinh câu + checklist duyệt; ước 1 phút/câu duyệt = 250 giờ |
| T6 | Chưa có tiêu chí "xong" cho MVP ngoài retention: bao nhiêu từ, bao nhiêu dạng bài, khẩu hình mức nào | Khó chốt phạm vi | 8.1: MVP = 500 từ, 5 dạng bài, khẩu hình tĩnh cho 20 âm khó, 1 giọng Nữ + 1 giọng Nam |

## 3. Tính khả thi

| Hạng mục | Ước lượng | Nhận định |
| --- | --- | --- |
| Dữ liệu 500 từ đầu (MVP) | Tự động 3 ngày + duyệt 500 × 5 phút ≈ 42 giờ + 1.500 câu × 1 phút ≈ 25 giờ | Khả thi với 1 người trong 3–4 tuần bán thời gian |
| Dữ liệu 5.000 từ | ≈ 420 giờ duyệt từ + 250 giờ duyệt câu | Không khả thi trong 3 tháng với 1–2 người; cần 9–12 tháng hoặc cộng đồng đóng góp |
| Nhân vật + 12 khẩu hình + mặt cắt | 2–4 tuần tự vẽ, đã có SVG khởi điểm | Khả thi |
| Video miệng thật 44 âm + 30 từ | 1 buổi quay + 1 ngày cắt | Khả thi nếu có người phát âm chuẩn |
| Audio 5.000 từ + 15.000 câu bằng Kokoro | Máy chạy 1–2 ngày | Khả thi |
| Web React + Flutter, một đội nhỏ | Hai codebase, dùng chung nội dung và quy tắc | Khả thi nhưng nên ra web (PWA) trước, Flutter sau khi lõi ổn |

Rủi ro khả thi lớn nhất là khối lượng biên soạn nội dung, không phải kỹ thuật. Đề xuất: MVP 500 từ, mở rộng theo đợt 500, và cho phép cộng đồng đề xuất câu ví dụ có kiểm duyệt.

## 4. Chi phí đầu vào — có về 0 được không?

| Khoản | Miễn phí được? | Cách |
| --- | --- | --- |
| Dữ liệu từ, câu, phiên âm | Có | NGSL, NAWL, CMUdict, Wiktionary, Tatoeba, WordNet |
| Audio | Có | Kokoro/Piper trên máy cá nhân |
| Nhân vật, khẩu hình, hình minh hoạ | Có | Inkscape, Krita, Rive free, Stable Diffusion cục bộ |
| Timing khẩu hình | Có | Montreal Forced Aligner hoặc Rhubarb |
| Host web | Có | Cloudflare Pages hoặc GitHub Pages |
| Lưu trữ và phân phối audio/hình | Có | Cloudflare R2 (10 GB, không phí băng thông ra) hoặc GitHub Releases |
| Tài khoản, đồng bộ, đo lường | Có ở quy mô nhỏ | Supabase free (500 MB DB, 50.000 MAU) nhưng project tự tạm dừng sau 1 tuần không hoạt động; dự phòng Firebase Spark hoặc Cloudflare D1 |
| Thông báo đẩy | Có | FCM cho Android/web; APNs qua FCM |
| Tên miền | Không (\~10–15 USD/năm) | Có thể dùng subdomain miễn phí của Pages trước |
| Google Play | Không (25 USD một lần) | Hoặc phát hành APK trực tiếp / F-Droid |
| Apple App Store | Không (99 USD/năm) | Không có cách miễn phí; iOS dùng PWA trên Safari (không có push tốt) |

Kết luận: phần sản xuất về 0 được; phần phát hành có tối thiểu 25 USD (Android) và 99 USD/năm nếu muốn iOS. Đề xuất thứ tự: web PWA (0 đồng) → Android (25 USD) → iOS khi có người dùng thật.

## 5. Việc cần làm ngay trên tài liệu chính

- [ ] Đã sửa Đ1: bỏ Oxford, thêm NAWL và tần suất kaikki (xem tab Bằng chứng)
- [ ] Đã sửa Đ2: tốc độ chậm bằng playbackRate (mục 7, 8.3, 9.1 tab chính)
- [ ] Đã sửa Đ3: timing mức phoneme dùng Montreal Forced Aligner; Rhubarb chỉ cho lip-sync
- [ ] Đã sửa Đ4: retention ghi là giả định, ngưỡng tối thiểu D30 ≥ 8% (mục 1)
- [ ] Đã thêm T1: FR-55 ba lớp hình dạy phát âm (mục 5.5)
- [ ] Đã thêm T2: người duyệt ngữ âm (mục 6.4)
- [ ] Đã thêm T3: nền tảng phát hành và phí (mục 10)
- [ ] Đã thêm T4, T5 (mục 6.3), T6 (mục 8.1)
