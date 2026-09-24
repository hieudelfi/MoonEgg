# Tài liệu kiểm thử — Test cases và mock test

Sep 24, 2026 · @Hugh Nguyen

## 1. Phạm vi và chiến lược

Kiểm thử tập trung vào ba thứ mà nếu sai thì sản phẩm hỏng dù giao diện đẹp: lịch ôn (FSRS và dựng phiên) phải giống nhau trên web và mobile, lịch sử không bao giờ mất hay trùng khi đồng bộ, và nội dung phát ra (audio, khẩu hình, câu) đúng với từ. Giao diện được kiểm bằng E2E theo màn hình với dữ liệu mock cố định.

**Tầng kiểm thử**

| Tầng | Kiểm cái gì | Ở đâu | Công cụ | Chạy khi |
| --- | --- | --- | --- | --- |
| Test vàng (golden) | Lõi học: FSRS, ánh xạ cấp, dựng phiên, placement | Bộ JSON dùng chung; chạy trên cả TS và Dart | Vitest (web), `flutter test` (mobile), cùng file `golden/*.json` | Mỗi commit |
| Unit | Hàm thuần: ánh xạ ARPAbet→viseme, tính streak, gộp sự kiện, xuất/nhập .zip | Từng nền tảng | Vitest / flutter test | Mỗi commit |
| Tích hợp | Lưu trữ cục bộ (Dexie/drift), hàng đợi đồng bộ, cache asset | Từng nền tảng, mock máy chủ | Vitest + fake-indexeddb; flutter test + sqlite in-memory; MSW / mock Supabase | Mỗi commit |
| E2E màn hình | Luồng người dùng qua 15 màn mockup | Web: Playwright; Mobile: Patrol hoặc integration\_test | Gói nội dung mock 30 từ | Mỗi PR và trước phát hành |
| Pipeline nội dung | Gói build ra đúng, đủ, khớp | Python pytest trên máy build | pytest | Mỗi đợt nội dung |
| Phi chức năng | Thời gian, dung lượng, offline, lệch khẩu hình | Máy thật tầm trung | Script đo + tay | Trước phát hành |
| Tuân thủ | SBOM, giấy phép, quyền, gọi mạng, khai báo | CI + tay | Mục 7 | Trước mỗi lần nộp store |

**Quy ước định danh**

- `TC-<nhóm>-<số>`: nhóm = PL (placement), FS (FSRS), SB (session builder), CD (card), EX (exercise), GR (grade), SD (sound), DN (done), QZ (quiz), GM (grammar), SY (sync), BK (backup), AU (auth), CT (content pipeline), NF (phi chức năng), CP (compliance).
- Mỗi test ghi: **Ở đâu** (thành phần hoặc màn), **Điều kiện trước**, **Input**, **Bước**, **Output mong đợi**, **Loại**, **Ưu tiên** (P0 chặn phát hành, P1 phải sửa trước bản kế, P2 ghi nhận).
- Output mong đợi phải kiểm được bằng máy hoặc bằng mắt với tiêu chí rõ; không dùng "hoạt động đúng".

**Tiêu chí đạt để phát hành**

- 100% test vàng và P0 đạt trên cả web và mobile.
- P1 thất bại ≤ 3 và có ghi chú.
- Checklist mục 8 có chữ ký người chạy và ngày.

## 2. Bộ dữ liệu mock

Mọi test dùng chung một gói nội dung nhỏ `pack_test_v1` (30 từ, 5 âm, 2 cột mốc, 3 mẫu ngữ pháp) và bốn hồ sơ người dùng mẫu; dữ liệu cố định để output mong đợi viết được thành số.

**2.1 Gói nội dung mock `pack_test_v1`**

| item\_id | headword | pos | freq\_rank | ipa\_us | stress | hard\_sound | milestone | Ghi chú dùng cho test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| w:hello#1 | hello | interj | 12 | /həˈloʊ/ | 2 | — | m1 | từ dễ, mở phiên |
| w:market#1 | market | n | 480 | /ˈmɑːrkɪt/ | 1 | t cuối | m1 | có ảnh tình huống |
| w:umbrella#1 | umbrella | n | 1.910 | /ʌmˈbrelə/ | 2 | — | m1 | dùng trong câu ngữ pháp |
| w:bargain#1 | bargain | n | 2.340 | /ˈbɑːrɡən/ | 1 | — | m1 | "hé lộ ngày mai" |
| w:reluctant#1 | reluctant | adj | 1.240 | /rɪˈlʌktənt/ | 2 | nt cuối | m2 | từ khó, có ẩn dụ |
| w:think#1 | think | v | 95 | /θɪŋk/ | 1 | θ | m1 | cặp với sink |
| w:sink#1 | sink | v | 3.100 | /sɪŋk/ | 1 | — | m2 | cặp với think |
| w:wind#1 | wind (gió) | n | 610 | /wɪnd/ | 1 | d cuối | m1 | đồng tự khác âm |
| w:wind#2 | wind (quấn) | v | 4.200 | /waɪnd/ | 1 | d cuối | m2 | đồng tự khác âm |
| w:receipt#1 | receipt | n | 2.700 | /rɪˈsiːt/ | 2 | t cuối | m2 | p câm, hay quên |
| … 20 từ còn lại |  |  | 100–4.900 |  |  |  | m1/m2 | đủ 15 từ/cột mốc |
| p:past\_simple#1 | "I went to the market yesterday." | pattern | — | — | — | — | g1 | ngữ pháp cơ bản |
| s:th | /θ/ | sound | — | — | — | có | — | tip\_vi, video mock 2 s |

Mỗi từ có: 1 sense, 2 câu ví dụ (khó 1 và 2), audio 2 giọng (file 0,5 s tone thuần để test, có duration\_ms thật), viseme\_timeline hợp lệ (mốc tăng dần, kết ở duration). Từ giả cho placement: `x:flimber`, `x:tovant`, `x:gresh` (không có trong gói, chỉ trong danh sách placement).

**2.2 Hồ sơ người dùng mẫu**

| ID | Mô tả | Event log | Dùng cho |
| --- | --- | --- | --- |
| U-NEW | Chưa học gì, chưa tài khoản | rỗng | Onboarding, placement, phiên đầu |
| U-DAY7 | Học 7 ngày liên tục, 42 từ, streak 7 | 380 sự kiện, ts cách đều | Phiên thường, dựng phiên, tiến độ |
| U-BACK | Học 20 ngày rồi nghỉ 12 ngày, 90 thẻ tồn | 900 sự kiện, khoảng trống 12 ngày | Rải thẻ tồn, thông báo quay lại |
| U-TWO | Có tài khoản, dùng 2 thiết bị, mỗi bên 30 sự kiện chưa đồng bộ, 5 sự kiện trùng event\_id | 2 log | Đồng bộ, gộp, không trùng |

**2.3 Event log mẫu (trích U-DAY7)**

```json
[
  {"event_id":"01J8K0A0000000000000000001","ts":1758067200000,"type":"exposure","item_type":"word","item_id":"w:hello#1","payload":{"session_id":"s-d1"}},
  {"event_id":"01J8K0A0000000000000000002","ts":1758067230000,"type":"answer","item_type":"word","item_id":"w:hello#1","payload":{"exercise":"choose_meaning","correct":true,"latency_ms":2100,"hints":0}},
  {"event_id":"01J8K0A0000000000000000003","ts":1758067235000,"type":"review","item_type":"word","item_id":"w:hello#1","payload":{"grade":4}},
  {"event_id":"01J8K0A0000000000000000004","ts":1758153600000,"type":"review","item_type":"word","item_id":"w:hello#1","payload":{"grade":3}}
]
```

**2.4 Test vàng FSRS (trích `golden/fsrs.json`)**

| # | Trạng thái vào | grade | ts (ngày) | stability ra | difficulty ra | due (ngày) | level |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G1 | mới | 3 | 0 | 2,4 | 5,0 | 2 | Nhớ tạm |
| G2 | G1 | 3 | 2 | 6,8 | 4,9 | 7 | Nhớ tạm |
| G3 | G2 | 4 | 7 | 22,1 | 4,6 | 22 | Nhớ chắc |
| G4 | G3 | 1 | 22 | 1,1 | 5,4 | 0 (10 phút) | Đang học |
| G5 | mới | 1 | 0 | 0,4 | 6,0 | 0 (10 phút) | Đang học |

Giá trị số ở bảng là mẫu định dạng; số thật được sinh một lần từ `ts-fsrs` với tham số mặc định và khoá lại trong file vàng — Dart phải khớp đến 3 chữ số thập phân.

## 3. Test lõi học

Đây là các test vàng: cùng file JSON, chạy trên cả TS và Dart; sai lệch giữa hai nền tảng tự nó là một lỗi P0.

**3.1 Placement (kiểm tra đầu vào)**

| ID | Ở đâu | Điều kiện trước | Input | Output mong đợi | Loại | Ưu tiên |
| --- | --- | --- | --- | --- | --- | --- |
| TC-PL-01 | `placement.estimate()` | U-NEW | 20 câu trả lời: 15 "biết" ở hạng < 1.000, 5 "chưa" ở hạng > 2.000; 3 từ giả đều "chưa" | vốn từ ước lượng trong \[900, 1.300\]; các từ hạng ≤ 800 đánh dấu known | vàng | P0 |
| TC-PL-02 | `placement.estimate()` | U-NEW | như trên nhưng 3 từ giả đều "biết" | trọng số "biết" giảm ≥ 50%; ước lượng ≤ 700; cờ `unreliable=true` | vàng | P0 |
| TC-PL-03 | `placement.estimate()` | U-NEW | thoát sau 7 câu | ước lượng từ 7 câu, cờ `partial=true`; 13 câu còn lại không sinh sự kiện | vàng | P1 |
| TC-PL-04 | Màn 1 | U-NEW, offline | mở app lần đầu, gói đã có | 20 từ hiện lần lượt, không gọi mạng (proxy ghi 0 request) | E2E | P0 |

**3.2 FSRS và ánh xạ cấp**

| ID | Ở đâu | Điều kiện trước | Input | Output mong đợi | Loại | Ưu tiên |
| --- | --- | --- | --- | --- | --- | --- |
| TC-FS-01 | `fsrs.next()` | — | 200 kịch bản `golden/fsrs.json` | stability, difficulty, due khớp 3 chữ số thập phân trên TS và Dart | vàng | P0 |
| TC-FS-02 | `level.of(state)` | — | 6 trạng thái ở đúng ngưỡng 2, 14, 60 ngày và reps 2/3 | Mới/Đang học/Nhớ tạm/Nhớ chắc/Thành thạo đúng bảng FR-15; ngưỡng bao gồm cận dưới | vàng | P0 |
| TC-FS-03 | `state.rebuild(log)` | U-DAY7 | 380 sự kiện theo thứ tự thời gian | item\_state của 42 từ khớp file vàng; rebuild 2 lần cho cùng kết quả (idempotent) | vàng | P0 |
| TC-FS-04 | `state.rebuild(log)` | U-DAY7 | cùng 380 sự kiện nhưng xáo trộn thứ tự mảng | kết quả giống TC-FS-03 (sắp theo ts trước khi fold) | vàng | P0 |
| TC-FS-05 | `fsrs.next()` | — | grade=1 trên từ Thành thạo | về Đang học, due ≤ 10 phút, lapses +1 | vàng | P1 |
| TC-FS-06 | `fsrs.optimize()` | U-DAY7 nối thêm 620 sự kiện giả | log ≥ 1.000 | sinh `setting_changed{fsrs_params}` với 17 tham số, loss giảm so với mặc định | unit | P2 |

**3.3 Dựng phiên**

| ID | Ở đâu | Điều kiện trước | Input | Output mong đợi | Loại | Ưu tiên |
| --- | --- | --- | --- | --- | --- | --- |
| TC-SB-01 | `session.build()` | U-DAY7, daily\_new=10, 7 thẻ đến hạn | ngày 8 | 17 thẻ; 2 thẻ đầu là ôn có stability cao nhất; 2 thẻ cuối là ôn; tỉ lệ mới:ôn ở giữa ≈ 1:2 ±1 | vàng | P0 |
| TC-SB-02 | `session.build()` | U-BACK (90 thẻ tồn) | ngày quay lại | ≤ 25 thẻ; 65 thẻ tồn được dời đều trong 3–5 ngày; không thẻ nào dời quá 5 ngày | vàng | P0 |
| TC-SB-03 | `session.build()` | U-NEW sau placement, 640 từ known | ngày 1 | không thẻ nào thuộc known; 10 từ mới có freq\_rank nhỏ nhất ngoài known | vàng | P0 |
| TC-SB-04 | `session.build()` | U-DAY7, chủ đề ưu tiên = "công việc" | ngày 8 | ≥ 6/10 từ mới thuộc chủ đề công việc | vàng | P1 |
| TC-SB-05 | `session.assignExercise()` | U-DAY7 | 17 thẻ với cấp khác nhau | Mới→choose\_meaning; Đang học→listen\_type; Nhớ tạm→fill\_sentence; Nhớ chắc→type\_from\_meaning; Thành thạo→speak hoặc own\_sentence; hai thẻ liền nhau không cùng dạng | vàng | P0 |
| TC-SB-06 | `session.build()` | U-DAY7 có w:wind#1 và w:wind#2 chưa học | ngày 8 | hai từ này không cùng phiên (giao thoa) | vàng | P1 |
| TC-SB-07 | `session_state` | U-DAY7 | dựng phiên, trả lời 5 thẻ, tắt app, mở lại | con trỏ = 5, 12 thẻ còn lại giống danh sách ban đầu | tích hợp | P0 |
| TC-SB-08 | `session_state` | U-DAY7 | dựng phiên 23:50, mở lại 04:10 hôm sau | phiên cũ hết hạn; thẻ chưa làm về hàng đợi; phiên mới dựng | tích hợp | P1 |

## 4. Test theo màn hình

E2E chạy trên gói `pack_test_v1` với hồ sơ U-DAY7 trừ khi ghi khác; mỗi test kiểm cả điều nhìn thấy trên màn và sự kiện được ghi vào log.

**4.1 Màn 3 — Thẻ từ mới**

| ID | Điều kiện trước | Input | Output mong đợi | Loại | Ưu tiên |
| --- | --- | --- | --- | --- | --- |
| TC-CD-01 | thẻ w:reluctant#1 | vào màn | audio tự phát 1 lần trong 300 ms; khẩu hình chạy; ô IPA "ˈlʌk" tô vàng; log có `exposure` | E2E | P0 |
| TC-CD-02 | như trên | bấm Chậm | audio phát với playbackRate 0,75; timeline viseme kéo dài tương ứng; không tải file mới (0 request) | E2E | P0 |
| TC-CD-03 | như trên | chạm ô IPA "nt" | sheet hiện khẩu hình tĩnh + mặt cắt + mẹo "đừng nuốt /t/"; đóng sheet không mất trạng thái thẻ | E2E | P1 |
| TC-CD-04 | mic được cấp | bấm Nói theo, giữ 2 s | file ghi âm 2 s tồn tại cục bộ; phát lại mẫu rồi bản thu; log `speak_attempt{has_recording:true}`; không upload | E2E | P0 |
| TC-CD-05 | mic bị từ chối | bấm Nói theo | thông báo giải thích, không crash; log `speak_attempt{has_recording:false}` | E2E | P1 |
| TC-CD-06 | thẻ w:wind#2 | vào màn | audio và IPA /waɪnd/ (không phải /wɪnd/); nghĩa "quấn" | E2E | P0 |
| TC-CD-07 | từ có cờ âm khó | vào màn | hộp "Âm khó" hiện; từ không có cờ → hộp ẩn | E2E | P1 |
| TC-CD-08 | audio chưa cache, online | vào màn | tải 1 file từ CDN, cache; vào lại lần 2 → 0 request | tích hợp | P0 |

**4.2 Màn 4 — Bài luyện, Màn 5 — Tự chấm**

| ID | Điều kiện trước | Input | Output mong đợi | Loại | Ưu tiên |
| --- | --- | --- | --- | --- | --- |
| TC-EX-01 | fill\_sentence cho w:reluctant#1 | gõ "reluctant", Enter | băng xanh "Đúng rồi"; log `answer{correct:true,hints:0}`; câu dùng là câu 2, không phải câu ở thẻ | E2E | P0 |
| TC-EX-02 | như trên | gõ "reluctent" | "Gần đúng", hiện đúng, log `answer{correct:false,near:true}`; nút tự chấm tối đa là Khó | E2E | P0 |
| TC-EX-03 | như trên | bấm Thêm chữ cái ×2 rồi gõ đúng | log `hints:2`; nút Dễ bị vô hiệu | E2E | P1 |
| TC-EX-04 | listen\_type | phát audio, gõ đúng | không hiện chữ trước khi trả lời | E2E | P1 |
| TC-GR-01 | sau TC-EX-01 | xem 4 nút | khoảng cách trên nút khớp `fsrs.preview()` với 4 grade (so bằng số) | E2E | P0 |
| TC-GR-02 | như trên | bấm Nhớ | log `review{grade:3}`; item\_state cập nhật trong cùng transaction; sang thẻ kế sau ≤ 400 ms | E2E | P0 |
| TC-GR-03 | bấm Nhớ rồi tắt app ngay | mở lại | log và item\_state hoặc cả hai có, hoặc cả hai không; không có trạng thái lệch | tích hợp | P0 |
| TC-GR-04 | thẻ ở cấp Nhớ tạm | bấm Quên | về Đang học; thẻ xuất hiện lại trong cùng phiên sau ≥ 3 thẻ | E2E | P1 |

**4.3 Màn 6 — Trang âm, Màn 7 — Xong hôm nay, Màn 8 — Tiến độ**

| ID | Điều kiện trước | Input | Output mong đợi | Loại | Ưu tiên |
| --- | --- | --- | --- | --- | --- |
| TC-SD-01 | s:th | bấm phát | hai khung (cận + mặt cắt) đổi trạng thái đồng bộ audio | E2E | P1 |
| TC-SD-02 | offline | bấm Xem video miệng thật | nút xám + chú thích; hai lớp còn lại vẫn dùng được | E2E | P1 |
| TC-SD-03 | cặp think/sink | app phát "sink", chọn "think" | báo sai, phát lại cả hai liên tiếp; log `sound_practice{correct:false}` | E2E | P1 |
| TC-SD-04 | — | bấm Thuần phục | log `sound_claim`; âm vào bộ sưu tập; lịch `spot_check` sau 14 ngày | E2E | P1 |
| TC-DN-01 | phiên 17 thẻ, 15 đúng | hết thẻ | màn hiện "15/17", thời lượng thật ±2 s; log `session_end`; hé lộ là từ mới đầu tiên của ngày mai | E2E | P0 |
| TC-DN-02 | như trên | bấm Nhắc tôi lúc 21:00 | thông báo cục bộ được đặt đúng 21:00, nội dung "N từ, M phút" với N = due ngày mai | E2E | P0 |
| TC-DN-03 | U-BACK | mở app | dòng "Chào mừng trở lại"; không hiện số ngày nghỉ; thẻ hôm nay ≤ 25 | E2E | P0 |
| TC-PG-01 | U-DAY7 | mở Tiến độ | 5 số cấp cộng lại = 42; streak = 7; lịch tuần đúng ngày; "% hiểu" tính từ (known + nhớ chắc)/NGSL coverage | E2E | P1 |
| TC-PG-02 | U-DAY7 bỏ 1 ngày trong tuần | mở Tiến độ | streak vẫn 8 sau ngày kế; ô ngày nghỉ nét đứt; "còn 1 ngày nghỉ" | E2E | P0 |
| TC-PG-03 | U-DAY7 bỏ 3 ngày | mở Tiến độ | streak về 0 sau ngày thứ 3; không có thông điệp trách | E2E | P1 |

**4.4 Màn 9–10 — Luyện tập, Quiz; Màn 12 — Ngữ pháp**

| ID | Điều kiện trước | Input | Output mong đợi | Loại | Ưu tiên |
| --- | --- | --- | --- | --- | --- |
| TC-QZ-01 | U-DAY7 | mở Luyện tập | "N từ sẵn sàng" = số từ cấp ≥ Nhớ tạm; thử thách tuần ở trạng thái chưa nhận | E2E | P1 |
| TC-QZ-02 | quiz 60 s | trả lời 12 câu, 10 đúng, hết giờ | màn tóm tắt 10; kỷ lục cập nhật nếu > cũ; log 12 `answer{kind:practice}`; item\_state 12 từ thay đổi | E2E | P0 |
| TC-QZ-03 | quiz 60 s | bấm Dừng sau 4 câu | 4 sự kiện đã ghi vẫn còn; không có 8 sự kiện giả | E2E | P0 |
| TC-QZ-04 | quiz | từ chưa học có trong đáp án? | không có từ nào ngoài kho đã học (cấp ≥ Nhớ tạm) xuất hiện làm câu hỏi | E2E | P0 |
| TC-QZ-05 | thử thách tuần | nhận, làm 15/15 | huy hiệu vào bộ sưu tập; log `challenge_progress` 15 dòng; không có bảng xếp hạng ở bất kỳ đâu | E2E | P1 |
| TC-GM-01 | p:past\_simple#1 | sắp "She bought an umbrella last week" | đúng; log `answer{item_type:pattern}`; item\_state pattern có due | E2E | P1 |
| TC-GM-02 | như trên | dùng chip "buys" | sai; chip tô chữ đỏ; câu đúng hiện; audio phát | E2E | P1 |
| TC-GM-03 | U-DAY7 (42 từ) | mở bản đồ | nhánh ngữ pháp khoá; U với 500 từ known → mở | E2E | P1 |
| TC-GM-04 | pattern dùng từ chưa biết | dựng bài | bài không được chọn (mọi từ trong câu phải known hoặc cấp ≥ Nhớ tạm) | vàng | P1 |

**4.5 Bổ sung sau rà soát đồng nhất (FR-55, FR-59, FR-61)**

| ID | Điều kiện trước | Input | Output mong đợi | Loại | Ưu tiên |
| --- | --- | --- | --- | --- | --- |
| TC-GR-05 | vừa bấm Dễ nhầm | bấm Hoàn tác trong 5 s, chọn Khó | log có review{grade:4} → review\_undo → review{grade:2}; item\_state theo grade 2; sau 5 s nút hoàn tác biến mất | E2E | P1 |
| TC-SD-05 | online, s:th có video mock | bấm Xem video miệng thật | video phát lặp; lần 2 offline vẫn phát từ cache; ghi âm không rời thiết bị (proxy ghi 0 upload) | E2E | P0 |
| TC-DN-04 | thông báo 2 lần/ngày | bỏ qua 3 lần liên tiếp, rồi 7 ngày | 3 notification\_ignored → còn 1 lần/ngày; sau 7 ngày app hỏi có nhận nữa không; mở 1 lần → notification\_opened, tần suất giữ nguyên | E2E | P1 |

**4.6 Danh sách từ và chọn mục cho quiz (FR-62→65, Kiến trúc §5.6)**

| ID | Ở đâu | Điều kiện trước | Input | Output mong đợi | Loại | Ưu tiên |
| --- | --- | --- | --- | --- | --- | --- |
| TC-SB-09 | `next_new(10)` | U-DAY7; danh sách của tôi 4 từ chưa học bật ưu tiên; chủ đề ưu tiên "công việc" | ngày 8 | 4 từ danh sách đứng đầu; tiếp là từ cột mốc hiện tại; rồi từ chủ đề công việc hạng thấp nhất; không có từ known | vàng | P0 |
| TC-SB-10 | `next_new(10)` | vừa học w:wind#1 hôm qua | ngày 8 | w:wind#2 không xuất hiện trong 3 ngày | vàng | P1 |
| TC-QZ-06 | `quiz.pick(10, seed)` | U-DAY7: 5 từ due ≤ 2 ngày, 3 từ lapses ≥ 2, 20 từ thành thạo, 14 từ khác | seed cố định | 10 từ; ≥ 4 trong nhóm due, ≥ 2 nhóm hay quên, ≤ 2 thành thạo; cùng seed → cùng kết quả; đổi seed → khác | vàng | P0 |
| TC-QZ-07 | `quiz.pick` | 2 quiz trước có w:bargain#1 | quiz thứ 3 | xác suất bargain giảm ×0,2 (đo trên 1.000 lần lấy mẫu: tần suất ≤ 25% mức nền) | vàng | P1 |
| TC-QZ-08 | `quiz.distractors(w:reluctant#1)` | kho đã học có 40 tính từ, trong đó "unwilling" đồng nghĩa | — | 3 nhiễu đều là tính từ đã học, không chứa "unwilling", ưu tiên cùng chủ đề; không lặp giữa 2 câu liền nhau | vàng | P0 |
| TC-QZ-09 | Màn 9 | chọn bộ lọc chủ đề "Đi chợ" | mở quiz | mọi câu hỏi thuộc chủ đề; nếu < 8 từ đủ điều kiện, app báo và gợi ý bỏ lọc | E2E | P1 |
| TC-LS-01 | Danh sách của tôi | tạo danh sách "Phỏng vấn", thêm 5 từ từ thẻ, bật ưu tiên | dựng phiên ngày kế | 5 từ xuất hiện đầu; log `list_changed` 6 sự kiện; đồng bộ sang máy B thấy đúng danh sách | E2E + tích hợp | P0 |
| TC-LS-02 | Danh sách của tôi | thêm từ thứ 201 | — | từ chối kèm thông báo; danh sách vẫn 200 | E2E | P2 |
| TC-LS-03 | Danh sách động | U-BACK | mở Luyện tập | "Sắp quên" = số từ due ≤ 2 ngày; "Hay quên" = từ lapses ≥ 2; số khớp truy vấn item\_state | E2E | P1 |
| TC-CT-11 | Pipeline | gói đợt 1 | — | mọi từ có 1–3 chủ đề; mỗi chủ đề ≥ 10 từ; tổng chủ đề ≤ 30 | pytest | P1 |

## 5. Test đồng bộ, sao lưu, khôi phục, xác thực

Nhóm này dùng máy chủ giả (mock Supabase: bảng review\_event trong SQLite + REST tối thiểu) để test được offline và lặp lại; một lần trước phát hành chạy lại TC-SY-01→04 trên Supabase thật.

**5.1 Đồng bộ**

| ID | Ở đâu | Điều kiện trước | Input | Output mong đợi | Loại | Ưu tiên |
| --- | --- | --- | --- | --- | --- | --- |
| TC-SY-01 | Hàng đợi đồng bộ | U-TWO thiết bị A, online | push 30 sự kiện | máy chủ có 30 dòng; A nhận server\_seq = 30; hàng đợi rỗng | tích hợp | P0 |
| TC-SY-02 | Hàng đợi | U-TWO, B có 30 sự kiện trong đó 5 trùng event\_id với A | B push | máy chủ có 55 dòng (không 60); B không lỗi | tích hợp | P0 |
| TC-SY-03 | Pull | sau TC-SY-02, A pull | A nhận 25 sự kiện mới của B; log A có 55; item\_state của các từ chung tính lại; `state.rebuild` cho kết quả bằng nhau trên A và B | tích hợp | P0 |  |
| TC-SY-04 | Pull phân trang | máy chủ có 2.500 sự kiện | pull với limit 1.000 | 3 trang; cursor lưu sau mỗi trang; ngắt mạng sau trang 2 rồi nối lại → không tải lại trang 1–2 | tích hợp | P0 |
| TC-SY-05 | Hàng đợi bền | offline 3 ngày, 120 sự kiện | có mạng | push tự động trong ≤ 60 s; thứ tự theo ts | tích hợp | P0 |
| TC-SY-06 | Liên kết tài khoản | U-NEW học 5 ngày ẩn danh, 200 sự kiện | đăng nhập Google (mock) | 200 sự kiện được gán user\_id và push; máy chủ có 200; không sự kiện nào mất | tích hợp | P0 |
| TC-SY-07 | Cài đặt xung đột | A đặt voice=F lúc t1, B đặt voice=M lúc t2 > t1 | cả hai đồng bộ | cả hai máy hiện voice=M | tích hợp | P1 |
| TC-SY-08 | Máy chủ trả 5xx | push | thử lại theo backoff 1/2/4/8 phút; hàng đợi giữ nguyên; app vẫn học được | tích hợp | P1 |  |

**5.2 Sao lưu và khôi phục**

| ID | Ở đâu | Điều kiện trước | Input | Output mong đợi | Loại | Ưu tiên |
| --- | --- | --- | --- | --- | --- | --- |
| TC-BK-01 | Xuất .zip | U-DAY7, 3 câu tự viết, 2 ảnh | bấm Xuất | zip có manifest.json, events.ndjson (380 dòng), user\_content.ndjson (3), settings.json, images/ (2); mở được bằng unzip chuẩn | tích hợp | P0 |
| TC-BK-02 | Nhập .zip | máy sạch U-NEW | nhập tệp từ TC-BK-01 | màn xem trước "42 từ, 7 ngày"; sau xác nhận: log 380, item\_state khớp file vàng của U-DAY7 | tích hợp | P0 |
| TC-BK-03 | Nhập .zip trùng | U-DAY7 nhập chính tệp của mình | log vẫn 380 (không nhân đôi) | tích hợp | P0 |  |
| TC-BK-04 | Nhập tệp hỏng | tệp thiếu manifest hoặc dòng JSON lỗi | báo lỗi rõ dòng; không thay đổi dữ liệu hiện có | tích hợp | P1 |  |
| TC-BK-05 | Đổi máy | U-TWO, máy mới sạch | đăng nhập | pull xong < 10 s với 1.000 sự kiện; bản đồ đúng cột mốc; giờ nhắc khôi phục; ảnh tự chụp không có (đồng bộ ảnh tắt) | E2E | P0 |
| TC-BK-06 | Xuất CSV (web) | U-DAY7 | bấm Xuất CSV | cột item\_id, headword, level, due, reps, lapses; 42 dòng; nhập Anki qua Import CSV không lỗi | tích hợp | P2 |
| TC-BK-07 | Nhắc sao lưu | U-NEW ẩn danh | học ngày 3, ngày 14 | nhắc đúng 2 lần, không nhắc lần 3 | E2E | P1 |

**5.3 Xác thực và xoá tài khoản**

| ID | Ở đâu | Điều kiện trước | Input | Output mong đợi | Loại | Ưu tiên |
| --- | --- | --- | --- | --- | --- | --- |
| TC-AU-01 | Đăng nhập | — | Google, Apple, magic link (mock) | cả ba tạo cùng cấu trúc phiên; token lưu secure storage (mobile) / IndexedDB (web); không cookie bên thứ ba | tích hợp | P0 |
| TC-AU-02 | Refresh | token hết hạn | mở app | refresh nền; người dùng không thấy màn đăng nhập | tích hợp | P0 |
| TC-AU-03 | Hết hạn dài | refresh thất bại 8 ngày | mở app | học vẫn được; đồng bộ dừng; banner nhẹ "đăng nhập lại để đồng bộ" | E2E | P1 |
| TC-AU-04 | RLS | user A có token | GET events của user B | 0 dòng, không lỗi 500 | tích hợp (Supabase thật) | P0 |
| TC-AU-05 | Xoá tài khoản | U-DAY7 đã đồng bộ, 2 ảnh trên Storage | xác nhận 2 bước | máy chủ: 0 sự kiện, 0 user\_content, 0 ảnh trong ≤ 5 phút; app về U-NEW; tệp cục bộ hỏi giữ hay xoá | E2E (Supabase thật) | P0 |
| TC-AU-06 | Đăng xuất | U-DAY7 | chọn "giữ dữ liệu trên máy" | log cục bộ còn; đăng nhập lại cùng tài khoản → không trùng sự kiện | tích hợp | P1 |

## 6. Test pipeline nội dung và phi chức năng

Pipeline được kiểm bằng pytest trên chính gói vừa build; phi chức năng đo trên hai máy cố định (một Android tầm trung \~ Snapdragon 6xx, một laptop thường) để số liệu so sánh được giữa các lần phát hành.

**6.1 Pipeline nội dung (chạy sau mỗi đợt build)**

| ID | Ở đâu | Input | Output mong đợi | Loại | Ưu tiên |
| --- | --- | --- | --- | --- | --- |
| TC-CT-01 | `content_v.N.sqlite` | gói vừa build | mọi WORD có ≥ 1 SENSE, ≥ 2 EXAMPLE, AUDIO cho 2 giọng, VISEME\_TIMELINE cho 2 giọng, image\_asset không rỗng cho danh từ cụ thể | pytest | P0 |
| TC-CT-02 | AUDIO | mọi file | tồn tại trên R2; duration\_ms trong \[300, 4.000\] cho từ, \[800, 8.000\] cho câu; loudness −16 ±2 LUFS | pytest | P0 |
| TC-CT-03 | VISEME\_TIMELINE | mọi timeline | mốc tăng đơn điệu; mốc cuối ≤ duration\_ms; viseme\_id ∈ 0..11; ≥ 1 mốc/âm tiết | pytest | P0 |
| TC-CT-04 | So khớp phoneme | ARPAbet của CMUdict vs phoneme MFA đã căn | khớp ≥ 98% từ; danh sách từ lệch xuất ra `mismatch.csv` để duyệt tay | pytest | P0 |
| TC-CT-05 | Đồng tự khác âm | w:wind#1, w:wind#2, w:read#1/#2, w:live#1/#2 | audio khác nhau (hash khác), ARPAbet khác nhau | pytest | P0 |
| TC-CT-06 | EXAMPLE | mọi câu | 6–12 từ; mọi từ trong câu có freq\_rank ≤ freq\_rank của từ đang học + 500 hoặc nằm trong 500 từ đầu | pytest | P1 |
| TC-CT-07 | Giấy phép | mọi bản ghi và asset | trường `source`, `license` không rỗng; giá trị ∈ allowlist (CC-BY, CC-BY-SA, BSD, MIT, Apache, tự tạo); trang ghi công sinh ra liệt kê đủ nguồn ở mục 6.1 tài liệu yêu cầu | pytest | P0 |
| TC-CT-08 | Manifest | manifest.json | sha256 mọi tệp khớp; kích thước gói 1.000 từ ≤ 8 MB (không audio); tổng audio 1 giọng ≤ 35 MB | pytest | P0 |
| TC-CT-09 | Từ giả placement | 30 từ giả | không trùng từ thật trong Wiktionary; không phải từ tục | pytest | P1 |
| TC-CT-10 | Nội dung nhạy cảm | mọi câu, nghĩa Việt | danh sách từ cấm không xuất hiện; LLM chấm "phù hợp 13+" ≥ 0,95 | pytest | P1 |

**6.2 Phi chức năng (đo trước phát hành)**

| ID | Chỉ tiêu (NFR) | Cách đo | Input | Output mong đợi | Ưu tiên |
| --- | --- | --- | --- | --- | --- |
| TC-NF-01 | Mở app → thẻ đầu < 2 s | timestamp log `app_open` → `card_shown`, 10 lần, máy Android tầm trung | U-DAY7 | p90 < 2.000 ms | P0 |
| TC-NF-02 | Chuyển thẻ < 150 ms | `review` ts → `card_shown` ts, 50 thẻ | U-DAY7 | p90 < 150 ms | P0 |
| TC-NF-03 | Lệch khẩu hình | ghi màn hình 60 fps, so mốc viseme với dạng sóng audio, 20 từ | pack\_test\_v1 | p90 < 50 ms web; < 80 ms Android cũ (chỉ tiêu đã nới) | P0 |
| TC-NF-04 | Gói 500 từ < 30 MB | đo dung lượng thư mục cache sau tải gói + audio 1 giọng cho từ và câu | gói thật đợt 1 | ≤ 30 MB | P0 |
| TC-NF-05 | Offline trọn phiên | chế độ máy bay từ trước khi mở app | U-DAY7 | phiên 17 thẻ hoàn thành; 0 lỗi; proxy ghi 0 request | P0 |
| TC-NF-06 | Khôi phục < 10 s | đo TC-BK-05 | 1.000 sự kiện | ≤ 10 s | P0 |
| TC-NF-07 | Pin | 30 phút học liên tục | máy Android | tiêu hao ≤ 4% | P2 |
| TC-NF-08 | Bộ nhớ | phiên 25 thẻ | Flutter DevTools / Chrome | RSS ổn định, không tăng > 30 MB qua phiên (rò rỉ) | P1 |
| TC-NF-09 | Dung lượng máy chủ | mô phỏng 1 năm U-DAY7 | Postgres | ≈ 3 MB/người; index (user\_id, server\_seq) trả trang 1.000 dòng < 100 ms | P1 |
| TC-NF-10 | Tiếp cận web | axe-core trên 15 màn | — | 0 lỗi mức serious/critical; tương phản ≥ 4,5:1 | P1 |
| TC-NF-11 | Thiếu dung lượng web | trình duyệt ở chế độ eviction | — | `navigator.storage.persist()` được xin; nếu bị từ chối, banner nhắc tạo tài khoản | P1 |

## 7. Test tuân thủ store

Chạy trước mỗi lần nộp; phần tự động nằm trong CI, phần tay theo mục 13 tài liệu yêu cầu.

| ID | Ở đâu | Input | Output mong đợi | Loại | Ưu tiên |
| --- | --- | --- | --- | --- | --- |
| TC-CP-01 | CI: giấy phép | SBOM web + mobile | 0 gói GPL/AGPL/SSPL/unknown; báo cáo lưu cùng build | tự động | P0 |
| TC-CP-02 | CI: allowlist SDK | dependency tree | mọi gói ∈ allowlist hoặc có ghi chú duyệt trong `sdk-allowlist.md` | tự động | P0 |
| TC-CP-03 | CI: quyền | AndroidManifest, Info.plist | chỉ RECORD\_AUDIO, POST\_NOTIFICATIONS, INTERNET (Android); NSMicrophoneUsageDescription có chuỗi tiếng Việt (iOS) | tự động | P0 |
| TC-CP-04 | CI: host mạng | grep mã và cấu hình | chỉ miền của mình, \*.supabase.co, \*.r2.dev/miền R2, fonts.googleapis.com, fcm.googleapis.com | tự động | P0 |
| TC-CP-05 | Proxy 30 phút | chạy U-DAY7 qua mitmproxy: onboarding, phiên, quiz, sao lưu | danh sách host thực tế ⊆ TC-CP-04; không request nào chứa email trong URL; dữ liệu gửi khớp Data Safety form | tay | P0 |
| TC-CP-06 | Xcode Privacy Report | archive bản iOS | 0 SDK thiếu privacy manifest; mọi required-reason API có lý do | tay | P0 |
| TC-CP-07 | Play Pre-launch report | bản AAB nội bộ | 0 cảnh báo chính sách; 0 crash trên 5 máy | tay | P0 |
| TC-CP-08 | Xoá tài khoản | TC-AU-05 | dữ liệu máy chủ về 0; đường dẫn xoá tìm thấy ≤ 3 chạm từ Cài đặt | tay | P0 |
| TC-CP-09 | Chính sách riêng tư | app + 2 console | link mở được trong app không cần đăng nhập; cùng nội dung ở console | tay | P0 |
| TC-CP-10 | Trang ghi công | app | liệt kê đủ nguồn TC-CT-07; mở được offline | tay | P1 |
| TC-CP-11 | Nội dung store | ảnh chụp, mô tả | không hứa chấm phát âm tự động, không "1000 từ/30 ngày"; đối tượng 13+ | tay | P1 |
| TC-CP-12 | Rive export | file .riv trong bản build | không có logo Rive hiển thị (kiểm bằng mắt 12 khẩu hình + 6 biểu cảm) | tay | P1 |
| TC-CP-13 | Closed test Google | 14 tester × 14 ngày | Play Console xác nhận đủ điều kiện production | tay | P0 |

## 8. Checklist theo dõi mỗi lần chạy

Sao chép bảng này cho mỗi bản phát hành; ghi số bản build, người chạy, ngày; mỗi dòng ghi Đạt / Không đạt / Bỏ qua kèm ID test thất bại và link lỗi.

**Bản build:** \[số\] · **Nền tảng:** web / Android / iOS · **Người chạy:** \[tên\] · **Ngày:** \[ngày\]

| Nhóm | Số test | Chạy ở | Kết quả | Test thất bại | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| Test vàng TS (PL-01→03, FS-01→05, SB-01→06, GM-04) | 15 | CI |  |  |  |
| Test vàng Dart (cùng bộ với TS) | 15 | CI |  |  |  |
| Khớp TS–Dart (so file kết quả) | 1 | CI |  |  |  |
| Unit và tích hợp lõi (FS-06, SB-07/08, PL-04, GR-03, CD-08) | 6 | CI |  |  |  |
| E2E Thẻ từ (CD-01→07) | 7 | Playwright / Patrol |  |  |  |
| E2E Bài luyện, Tự chấm (EX-01→04, GR-01/02/04) | 7 | Playwright / Patrol |  |  |  |
| E2E Âm, Kết phiên, Tiến độ (SD-01→04, DN-01→03, PG-01→03) | 10 | Playwright / Patrol |  |  |  |
| E2E Quiz, Ngữ pháp (QZ-01→05, GM-01→03) | 8 | Playwright / Patrol |  |  |  |
| E2E bổ sung (GR-05, SD-05, DN-04) | 3 | Playwright / Patrol |  |  |  |
| Đồng bộ (SY) mock | 8 | CI |  |  |  |
| Đồng bộ (SY-01→04) Supabase thật | 4 | Tay |  |  |  |
| Sao lưu, khôi phục (BK) | 7 | CI + tay BK-05 |  |  |  |
| Xác thực, xoá (AU) | 6 | CI + tay AU-04/05 |  |  |  |
| Pipeline nội dung (CT) | 10 | pytest, mỗi đợt |  |  |  |
| Phi chức năng (NF) | 11 | Máy thật |  |  |  |
| Tuân thủ tự động (CP-01→04) | 4 | CI |  |  |  |
| Tuân thủ tay (CP-05→13) · Danh sách từ và quiz (SB-09/10, QZ-06→09, LS-01→03, CT-11): thêm 10 test, tổng 121 | 9 | Tay |  |  |  |
| **Tổng** | **111** |  |  |  |  |

**Số đo phi chức năng lần này** (điền số thật để so lần sau)

| Chỉ tiêu | Mục tiêu | Lần này | Lần trước | Xu hướng |
| --- | --- | --- | --- | --- |
| Mở app → thẻ đầu (p90, ms) | < 2.000 |  |  |  |
| Chuyển thẻ (p90, ms) | < 150 |  |  |  |
| Lệch khẩu hình (p90, ms) | < 50 web / < 80 Android |  |  |  |
| Gói 500 từ (MB) | ≤ 30 |  |  |  |
| Khôi phục 1.000 sự kiện (s) | ≤ 10 |  |  |  |
| Bộ nhớ tăng qua phiên (MB) | ≤ 30 |  |  |  |
| axe serious/critical | 0 |  |  |  |

**Quyết định phát hành**

- [ ] 100% test vàng và P0 đạt trên cả web và mobile
- [ ] P1 thất bại ≤ 3, mỗi cái có link lỗi và người phụ trách
- [ ] Số đo phi chức năng không xấu hơn lần trước quá 10%
- [ ] Tuân thủ tay CP-05→13 có chữ ký
- [ ] Trang ghi công và chính sách riêng tư đúng phiên bản

Kết luận: Phát hành / Hoãn — lý do: \[ghi\]
