# Bằng chứng xác thực — kiểm duyệt ngày 23/09/2026

Đã mở nguồn gốc cho 14 khẳng định quan trọng nhất trong tài liệu chính: 9 đúng, 3 sai hoặc thiếu (đã sửa ở tab chính), 2 chưa mở được nguồn nên giữ nhãn "theo hiểu biết".

## 1. Giấy phép dữ liệu nguồn

| Khẳng định trong tài liệu | Kết luận | Bằng chứng | Nguồn |
| --- | --- | --- | --- |
| NGSL \~2.800 từ, CC-BY-SA, phủ 92% văn bản phổ thông | Đúng | NGSL 1.2 có 2.809 từ, trung bình 92% coverage; các danh sách NGSL (NGSL-S, NGSL-GR) công bố dưới CC BY-SA 4.0 | [NGSL 1.2](https://www.newgeneralservicelist.com/new-general-service-list), [NGSL-S license](https://www.newgeneralservicelist.com/ngsl-spoken) |
| Oxford 3000/5000 là CC-BY-SA | Sai — đã sửa | File Oxford 3000 chính thức ghi "© Oxford University Press"; không có giấy phép mở | [American Oxford 3000 PDF](https://cdn.hackaday.io/files/1880418045146144/American_Oxford_3000%20In%202022.pdf), [OUP mô tả](https://www.oxfordlearnersdictionaries.com/about/oxford3000) |
| Tatoeba CC-BY | Đúng, kèm lưu ý | Câu văn bản dưới CC BY 2.0 FR, một phần CC0; audio của Tatoeba có giấy phép riêng theo từng người đóng góp, phải kiểm tra trước khi dùng | [Tatoeba downloads](https://tatoeba.org/ca/downloads), [Tatoeba wiki](https://en.wiki.tatoeba.org/history/show-diff-between/25/3365/3366) |
| CMUdict BSD | Chưa mở nguồn trong lần kiểm này | Theo hiểu biết: BSD 2-clause; cần xác nhận khi tải | — |
| Wiktionary/kaikki CC-BY-SA | Chưa mở nguồn trong lần kiểm này | Theo hiểu biết: CC BY-SA 4.0 và GFDL; cần xác nhận khi tải | — |

Lưu ý gộp giấy phép: Tatoeba nêu rõ CC-BY-SA không tương thích ngược với CC-BY, nhưng CC-BY chèn vào CC-BY-SA thì được ([nguồn](https://blog.tatoeba.org/2011/01/legally-valid-content.html)). Vì bộ từ trộn Wiktionary (CC-BY-SA) và Tatoeba (CC-BY), gói dữ liệu phát hành lại sẽ mang giấy phép CC-BY-SA; mã nguồn app không bị ảnh hưởng.

## 2. Công cụ giọng đọc và khẩu hình

| Khẳng định | Kết luận | Bằng chứng | Nguồn |
| --- | --- | --- | --- |
| Kokoro-82M Apache 2.0, có giọng af\_heart, af\_bella, af\_sarah, am\_adam, am\_michael | Đúng | Trang model ghi license apache-2.0; danh sách voicepack có đủ các tên trên | [Kokoro-82M README](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/README.md) |
| Kokoro cho phoneme timing qua misaki | Chưa chứng minh — đã sửa | Tài liệu chỉ cho thấy pipeline trả về chuỗi phoneme và audio; mốc thời gian mức phoneme không được nêu. Dùng Montreal Forced Aligner cho timing mức phoneme | như trên |
| Rhubarb Lip Sync cho timing mức phoneme | Sai — đã sửa | Rhubarb xuất 6–9 hình miệng kiểu Hanna-Barbera (A–H, X) theo thời gian, không xuất phoneme; không phân biệt /θ/ với /s/ | [Rhubarb README](https://github.com/DanielSWolf/rhubarb-lip-sync) |
| Montreal Forced Aligner miễn phí, cho timing mức phoneme | Đúng | License MIT; xuất TextGrid với alignment mức từ và mức phone bằng mô hình english\_us\_arpa | [MFA repo metadata](https://awesome.ecosyste.ms/projects/github.com%2Fmontrealcorpustools%2Fmontreal-forced-aligner), [MFA docs](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/) |
| Rive runtime miễn phí, gói free đủ dùng | Đúng một phần — đã bổ sung | Runtime Flutter là MIT. Gói Free cá nhân: không giới hạn file cá nhân nhưng không dùng font tuỳ chỉnh, không share link; bản ghi giá 2023 nói gói Free có logo Rive trên export runtime, Pro mới bỏ — cần kiểm tra khi export | [Rive pricing](https://rive.app/docs/account-admin/pricing), [Rive blog 2023](https://rive.app/blog/new-pricing), [rive pub package](https://depscope.dev/pkg/pub/rive) |

## 3. Chi phí phát hành và hạ tầng

| Khẳng định | Kết luận | Bằng chứng | Nguồn |
| --- | --- | --- | --- |
| Google Play 25 USD một lần | Đúng | Phí đăng ký một lần 25 USD, không thu hằng năm | [SplitMetrics 2025](https://splitmetrics.com/blog/google-play-apple-app-store-fees/) |
| Apple Developer 99 USD/năm | Đúng | 99 USD mỗi năm, đọc ngày 16/08/2026; miễn phí cho tổ chức phi lợi nhuận, trường học đủ điều kiện | [Playcode 2026](https://playcode.io/blog/how-much-does-it-cost-to-publish-an-app), [Choicely 2026](https://www.choicely.com/tutorials/how-much-does-it-cost-to-publish-an-app) |
| Cloudflare R2 10 GB miễn phí, không phí băng thông ra | Đúng | Free tier 10 GB + 1 triệu thao tác A/tháng; Cloudflare cam kết không thu egress | [R2 free tier](https://www.wmtips.com/technologies/cloud-storages/cloudflare-r2), [Cloudflare PR](https://www.cloudflare.com/en-ca/press/press-releases/2022/cloudflare-makes-r2-storage-available-to-all/) |
| Supabase free 500 MB DB | Đúng, kèm rủi ro mới | 500 MB DB, 50.000 MAU, 5 GB egress/tháng, 2 project; nhưng project free tự tạm dừng sau 1 tuần không hoạt động | [Supabase pricing 2026](https://makerkit.dev/blog/md/saas/supabase-pricing) |

## 4. Khẳng định chưa kiểm được và cách xử lý

- Hạn mức miễn phí cloud TTS (Google, Azure, Polly): không mở nguồn; đã ghi "kiểm tra lúc dùng" và không phụ thuộc vì có Kokoro.
- Chỉ tiêu retention D7/D30: không có nguồn ngành đáng tin để trích; giữ là giả định nội bộ.
- Ước lượng công biên soạn (5 phút/từ, 1 phút/câu): ước lượng của người viết, cần đo lại sau 50 từ đầu.

## 5. Thay đổi đã áp dụng vào tab chính

1. Bỏ Oxford 3000/5000 khỏi nguồn; thay bằng NGSL + NAWL + tần suất kaikki.
2. Rhubarb chỉ còn vai trò lip-sync nhân vật; timing mức phoneme dùng Montreal Forced Aligner.
3. Rive: ghi rõ giới hạn gói Free và điểm cần kiểm tra logo khi export.
4. Supabase: ghi rủi ro tự tạm dừng; dự phòng Firebase Spark hoặc Cloudflare D1.
