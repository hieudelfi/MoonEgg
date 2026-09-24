# Thiết kế UI/UX — so sánh và mô tả theo màn hình

Mockup 12 màn hình nằm trên canvas [Mockup UI — App học từ vựng](https://claude.ai/artifact/BJJpsvciECNVUK4VocwWUq) (bấm Play để đi qua luồng). Tab này giải thích vì sao mỗi màn hình trông như vậy, so với các app tốt nhất, và mô tả behavior để đội xây dựng.

## 1. So sánh với các app tốt nhất

| Tiêu chí | Duolingo | Anki | WordUp | MochiMochi | Elsa Speak | App này |
| --- | --- | --- | --- | --- | --- | --- |
| Cấu trúc luồng | Path tuyến tính, mỗi nút một bài | Hàng đợi thẻ, không có hành trình | Knowledge Map + hàng đợi | Khoá học tuyến tính | Bài theo kỹ năng phát âm | Bản đồ cột mốc + phiên hằng ngày do FSRS dựng |
| Màn hình chính | Path cuộn dài, nhiều nút | Danh sách deck khô | Danh sách từ + bản đồ | Nhân vật + nút học | Dashboard điểm | Một việc hôm nay, rõ số thẻ và phút |
| Thẻ từ | Không có thẻ riêng | Do người dùng tự làm | Trang giàu nội dung, cuộn dài | Flashcard gọn, ảnh + câu | Không tập trung từ vựng | Thẻ gọn như Mochi, thêm khẩu hình và IPA chạm được |
| Phát âm | Chấm bằng nhận dạng giọng, không dạy cách | Audio nếu tự thêm | Audio, không hướng dẫn | Audio 2 tốc độ | Chấm từng âm, có mẹo | Khẩu hình + mặt cắt + video thật; tự so, không chấm |
| Ôn tập | SRS ẩn, không tự chấm | SM-2/FSRS, tự chấm 4 mức | SRS ẩn | "Thời điểm vàng", 5 cấp | Không | FSRS + tự chấm 4 mức, hiển thị 5 cấp |
| Động lực | Streak cứng, league, gems, thông báo dồn dập | Không | Bản đồ tô dần | Nhân vật, thông báo đúng giờ | Điểm phần trăm | Chuỗi có ngày nghỉ, cột mốc nhỏ, bộ sưu tập âm, không league |
| Kết phiên | Hoạt hình XP, kêu gọi mua | Thống kê | Tóm tắt | Nhân vật vui | Tóm tắt đo được + hé lộ ngày mai |  |
| Điểm mạnh đáng học | Phản hồi tức thì, thanh tiến độ phiên, một việc mỗi màn | 4 mức tự chấm có hiện khoảng cách ôn | Bản đồ tri thức, xếp theo tần suất | Phiên ngắn, nhân vật, thông báo cụ thể | Mẹo phát âm theo âm | — |
| Điểm yếu tránh | Áp lực streak, quảng cáo, học để giữ streak thay vì để nhớ | Giao diện khô khan, cần tự tạo nội dung | Trang thẻ quá dài, không dạy phát âm | Khoá học cứng, kho từ nhỏ | Chấm điểm gây sợ, thiên về điểm số | — |

**Nguyên tắc rút ra cho UI**

1. Một màn hình, một việc, một nút chính màu san hô ở đáy (Duolingo làm tốt nhất điều này).
2. Thanh tiến độ phiên luôn hiện để người học biết còn bao lâu thì xong.
3. Không có con số nào không mang ý nghĩa học tập: không XP, không gem; số hiện là từ, phút, cấp nhớ.
4. Khẩu hình có mặt ở mọi thẻ từ mới, không phải mục riêng phải tìm.
5. Nhân vật chỉ xuất hiện ở đầu/cuối và khi phản hồi; trong lúc học, màn hình dành cho từ.
6. Màu: nền kem ấm cho học, nền xanh đêm cho "hành trình" và kết phiên — hai không gian cảm xúc tách biệt.

## 2. Mô tả từng màn hình

**Màn 1 — Kiểm tra đầu vào**

- Mục đích: ước lượng vốn từ trong 3 phút, không tài khoản.
- Behavior: 20 từ trải đều các dải tần suất, trộn 3 từ giả; chọn "Biết, dùng được" cho từ giả → giảm trọng số các câu trả lời "biết". Bấm nút là sang từ kế, không xác nhận. Nút loa phát audio, giúp người chỉ biết từ qua nghe. Thoát giữa chừng giữ kết quả đã trả lời.
- Kết thúc: màn "bạn đã biết \~640 từ" với bản đồ tô sẵn, rồi hỏi giờ học và mục tiêu/ngày.
- Khác Duolingo: không hỏi "vì sao bạn học" 6 màn; chỉ hỏi điều ảnh hưởng lộ trình.

**Màn 2 — Bản đồ lộ trình (trang chính)**

- Mục đích: trả lời "hôm nay làm gì, mất bao lâu" trong 2 giây.
- Behavior: nửa trên là bản đồ không gian với cột mốc đã qua (xanh), đang ở (san hô, có nhân vật), kế tiếp (khoá); chạm cột mốc đã qua để xem từ trong đó. Nửa dưới là thẻ "Hôm nay": số từ mới, từ sắp quên, âm khó, ước lượng phút. Chuỗi hiện kèm "còn 1 ngày nghỉ". Không có tab bar 5 mục: tiến độ và cài đặt nằm sau ảnh nhân vật và chuỗi.
- Sau kỳ nghỉ dài: thẻ hôm nay hiện số nhỏ như bình thường (rải thẻ tồn), dòng chào "Chào mừng trở lại", không nhắc số ngày đã nghỉ.

**Màn 3 — Thẻ từ mới (lần gặp đầu)**

- Mục đích: mã hoá đa kênh trong 20–30 giây: âm → khẩu hình → nghĩa → ảnh → câu.
- Behavior: vào màn tự phát audio 1 lần, khẩu hình cận mặt chạy đồng bộ; âm tiết nhấn tô vàng và nảy nhẹ đúng lúc phát. Chạm từng ô IPA → sheet nhỏ hiện khẩu hình tĩnh + mặt cắt + mẹo tiếng Việt của âm đó. Nút Nghe / Chậm (playbackRate 0,75, khẩu hình chậm theo) / Nói theo (ghi âm 3 giây, tự phát lại cạnh mẫu). Ảnh ẩn dụ + câu ví dụ có từ tô san hô. Hộp "Âm khó" chỉ hiện khi từ có cờ âm khó với người Việt. Nút chính ghi "Tôi đã nói theo" — cam kết nhỏ, không kiểm tra.
- Khác WordUp: không cuộn; mọi thứ vừa một màn để không chia chú ý.

**Màn 4 — Gõ từ trong câu (ôn)**

- Mục đích: truy xuất chủ động có khó khăn mong muốn.
- Behavior: câu mới (không dùng lại câu ở thẻ), chỗ trống hiện chữ cái đầu và số chữ; gõ vào ô lớn, kiểm tra khi bấm nút hoặc Enter. "Thêm 1 chữ cái" cho phép tối đa 2 lần, mỗi lần hạ một bậc tự chấm tối đa. Sai chính tả 1 ký tự → báo "gần đúng", hiện đúng, tính là Khó. Dòng nhân vật giải thích vì sao từ này xuất hiện hôm nay (minh bạch SRS).
- Khác Anki: có ngữ cảnh và gợi ý; khác Duolingo: không ngân hàng từ để chọn (nhận ra, không phải gọi ra).

**Màn 5 — Tự chấm sau khi trả lời**

- Mục đích: cho FSRS dữ liệu thật và củng cố thêm một lần.
- Behavior: băng xanh "Đúng rồi" (hoặc cam "Gần đúng", đỏ nhạt "Chưa đúng" kèm đáp án và audio tự phát). Thẻ tóm tắt có chip kết hợp từ (xuất hiện từ lần ôn 3). Bốn nút Quên/Khó/Nhớ/Dễ hiện khoảng cách ôn kế tiếp (như Anki) — nút "Nhớ" được tô sẵn là gợi ý mặc định theo kết quả, người học đổi được. Dòng 5 ô cho thấy cấp hiện tại và sẽ lên cấp nào. Nút phụ: đổi ảnh của tôi, xem âm khó liên quan.
- Chọn nút → tự chuyển thẻ sau 300 ms, không cần "Tiếp".

**Màn 6 — Trang âm khó**

- Mục đích: dạy một âm theo ba lớp (miệng cận, mặt cắt, video thật) và cho thử ngay.
- Behavior: hai khung trên đồng bộ với audio khi bấm phát; "Xem video miệng thật" mở clip 3 giây tự quay, lặp; "Chậm 0,5×" áp cho cả ba. Cặp dễ nhầm: app phát một từ, người học chọn; sai thì phát lại cả hai liên tiếp để nghe khác biệt. Ghi âm: giữ nút để thu, thả ra tự phát mẫu rồi bản thu; không điểm. Nút đáy "Thuần phục" là tự khai, thêm âm vào bộ sưu tập; âm sẽ được kiểm lại ngẫu nhiên sau 2 tuần.
- Khác Elsa: không chấm điểm phần trăm → không sợ sai; có hình cách đặt lưỡi mà Elsa không có.

**Màn 7 — Xong hôm nay**

- Mục đích: điểm dừng rõ, tiến bộ đo được, móc cho ngày mai.
- Behavior: nhân vật đổi biểu cảm theo kết quả (vui / bình thường / động viên; không buồn). Ba số đều là số học tập. Thanh cột mốc hiện "còn 2 từ" (goal gradient). Hộp "Hé lộ ngày mai" chọn một từ gần gũi nhất trong hàng đợi kèm một dòng tò mò (Zeigarnik). Nút phụ đặt/xác nhận giờ nhắc mai bằng một chạm.
- Khác Duolingo: không hoạt hình XP dài, không đề nghị mua, không "học thêm bài nữa" — tôn trọng điểm dừng.

**Màn 8 — Tiến độ**

- Mục đích: cho thấy từ đang "chín" chứ không chỉ được lướt qua.
- Behavior: thanh 5 cấp; chạm một đoạn → danh sách từ ở cấp đó. Lịch tuần: ngày học, ngày nghỉ (nét đứt vàng), hôm nay (viền vàng); dòng giải thích chuỗi không gãy vì nghỉ. Bộ sưu tập âm: đã thuần (xanh), đang luyện, sắp tới. Hộp "Ý nghĩa thật" quy đổi vốn từ sang % hiểu một mẩu tin, tính từ coverage NGSL.
- Không có bảng xếp hạng, không so với người khác.

**Màn 9 — Luyện tập và thử thách tuần**

- Mục đích: cửa vào mọi bài luyện cho từ đã học; tất cả đều ghi về FSRS (FR-39).
- Behavior: đầu trang hiện số từ "sẵn sàng" (cấp Nhớ tạm trở lên). Khối tối là thử thách tuần: có tên, mô tả, tiến độ, hạn còn lại; người học tự bấm nhận, không tự động gán. Lưới 4 ô: Quiz 60 giây (kèm kỷ lục của mình), Điền đoạn văn (theo chủ đề cột mốc vừa xong), Nói câu, Ghép cặp. Thẻ Cảnh chủ đề hiện cảnh đang mở và số vật đã học. Hộp nhắc ôn tổng hợp thứ bảy. Dòng cuối nhắc "chơi cũng là ôn".
- Không có bảng xếp hạng; kỷ lục chỉ là của mình (FR-40).

**Màn 10 — Quiz 60 giây**

- Mục đích: truy xuất nhanh, cảm giác thành thạo, tự đo tốc độ.
- Behavior: thanh vàng là thời gian còn lại (không đỏ, không kêu); số câu và số đúng hiện cạnh kỷ lục. Chọn đáp án → tô xanh + dấu tick 250 ms rồi sang câu kế; sai → tô chữ đỏ ở đáp án đã chọn, tô xanh đáp án đúng, phát audio, 600 ms rồi sang câu. Hàng chấm dưới đáy là lịch sử 10 câu. Nút Dừng không huỷ kết quả: mọi câu đã trả lời vẫn ghi vào lịch ôn. Hết giờ → màn tóm tắt: số đúng, so với kỷ lục, danh sách từ sai kèm nút nghe.

**Màn 11 — Dữ liệu và sao lưu**

- Mục đích: trả lời nỗi lo mất tiến độ khi xoá app hay đổi máy (mục 11 tài liệu chính).
- Behavior: khối xanh trên cùng luôn nói tình trạng đồng bộ bằng thời gian tương đối và ba con số (từ, ngày học, dung lượng). Ba dòng bật/tắt: đồng bộ lịch sử (mặc định bật khi có tài khoản), đồng bộ ảnh tự chụp (mặc định tắt, hiện dung lượng), bản ghi âm (chỉ máy này, tự xoá 30 ngày). Xuất tệp → tạo .zip định dạng mở, mở share sheet của hệ điều hành; Nhập tệp → chọn tệp, xem trước "N từ, M ngày" rồi mới gộp, không ghi đè. Khối tối giải thích đổi máy chỉ cần đăng nhập, ba cách đăng nhập không cần mật khẩu riêng. Nút xoá tài khoản màu chữ đỏ, bấm → xác nhận hai bước, xoá máy chủ ngay.

**Màn 12 — Chủ điểm ngữ pháp**

- Mục đích: chứng minh mô-đun ngữ pháp chạy trên cùng lõi và cùng ngôn ngữ thiết kế; màu xanh dương phân biệt nhánh ngữ pháp với từ vựng (san hô).
- Behavior: thẻ trên là mẫu câu đang học, phần ngữ pháp tô xanh, chip tóm tắt biến đổi (go → went) và dấu hiệu thời gian. Bài sắp xếp: chạm chip ở dưới để thêm vào hàng trên, chạm chip trên để bỏ; các chip nhiễu là lỗi điển hình (buys, is buying). Hộp xanh nhạt xác nhận câu chỉ dùng từ người học đã biết. Kiểm tra → nếu sai, tô đỏ chữ ở chip sai, hiện câu đúng, phát audio; sai thì mẫu câu về hàng đợi gần.
- Vào nhánh này từ bản đồ khi đạt \~500 từ; tiến độ và thử thách gộp chung với từ vựng.

## 2b. Bản web (desktop)

Web dùng cùng nội dung, cùng lịch ôn và cùng ngôn ngữ hình ảnh với mobile, nhưng tận dụng màn rộng và bàn phím: hai cột thay vì cuộn, phím tắt thay vì chạm, và là nơi người học xem tiến độ kỹ hơn.

| Khác biệt | Mobile | Web |
| --- | --- | --- |
| Điều hướng | Không tab bar; đi từ bản đồ | Thanh trái cố định: Hôm nay, Học, Luyện tập, Âm khó, Tiến độ, Cài đặt |
| Phiên học | Một cột, một thẻ vừa màn | Hai cột 7:5 — thẻ từ bên trái, bảng phát âm bên phải (khẩu hình lớn 200 px, IPA từng âm, mẹo) |
| Thao tác | Chạm | Space nghe, Enter kiểm tra, 1–4 tự chấm, R ghi âm; hiện gợi ý phím ngay trên nút |
| Câu của tôi | Bước riêng sau lần ôn 5 | Ô gõ ngay trên thẻ, tuỳ chọn, vì bàn phím sẵn |
| Tiến độ | Một cột | Biểu đồ phút học 14 ngày, danh sách theo cấp bấm mở được, kiểm tra ngẫu nhiên |
| Dữ liệu | Xuất .zip | Thêm xuất CSV (nhập Anki được) |
| Bản đồ | Dọc | Ngang, thấy cả nhánh ngữ pháp mở ở 500 từ |

**Web 1 — Trang chính**

- Tiêu đề trang nói thẳng việc hôm nay bằng một câu; thanh phải có streak với ngày nghỉ còn lại.
- Bản đồ ngang chiếm 2/3, cột phải là thẻ phiên học với ba con số và nút bắt đầu; thử thách tuần ở dưới.
- Hàng dưới: hé lộ hôm nay, từ khó của tuần, trạng thái đồng bộ với điện thoại ("đã học lúc 07:40"), để người dùng hai thiết bị yên tâm không có thẻ trùng.

**Web 2 — Phiên học**

- Thẻ trái: từ 64 px, IPA có âm tiết nhấn tô vàng, nghĩa Việt, định nghĩa Anh đơn giản, hai câu ví dụ, ảnh ẩn dụ; ô "câu của tôi" tuỳ chọn ở đáy, Enter để tiếp.
- Bảng phải: khẩu hình lớn đồng bộ audio, nhãn cho biết đang phát âm tiết nào; ba nút Nghe/Chậm/Nói theo có phím tắt; hàng IPA từng âm, âm khó tô cam, chọn âm → mẹo hiện ngay dưới, không mở sheet như mobile.
- Thanh tiến độ phiên hiện cả số thẻ và phút còn lại.

**Web 3 — Tiến độ và dữ liệu**

- Cột trái: thanh 5 cấp bấm được (mở danh sách từ), biểu đồ cột phút học 14 ngày (ngày nghỉ nét đứt, hôm nay san hô), bộ lọc Tuần/Tháng/Từ đầu.
- Cột phải: ý nghĩa thật (% hiểu mẩu tin) kèm kết quả kiểm tra ngẫu nhiên gần nhất; bộ sưu tập âm; khối dữ liệu với đồng bộ, xuất .zip/CSV, nhập tệp; từ hay quên gợi thêm liên tưởng.
- Không có bảng xếp hạng ở bất kỳ nền tảng nào.

## 3. Quy ước tương tác chung

| Quy ước | Giá trị |
| --- | --- |
| Nút chính | San hô #E8735A, cao 56–58 px, luôn ở đáy, một nút/màn |
| Nút phụ | Viền #E3D6C4 trên nền trắng, cao 44–50 px |
| Đúng / nhớ | Xanh bạc hà #3FA88F; sai dùng đỏ nhạt #B23A3A chỉ ở chữ, không tô nền đỏ |
| Trọng âm | Vàng #FFD166 trên ô IPA |
| Phản hồi | Ngay khi có kết quả, rung nhẹ 1 lần khi đúng, không âm thanh chê |
| Thoát giữa phiên | Không hộp thoại xác nhận; tiến độ đã lưu từng thẻ |
| Offline | Mọi màn ở đây chạy không mạng; chỉ đồng bộ và video thật cần mạng, có trạng thái thay thế |
| Chữ | Fredoka cho từ và tiêu đề, Nunito cho nội dung; từ đang học ≥ 40 px |
| Chạm | Mọi đích ≥ 44 px; thao tác chính trong tầm ngón cái |

## 4. Chưa có trong mockup, cần làm tiếp

- Sheet chi tiết khi chạm một ô IPA.
- Màn cảnh chủ đề (chạm vật để học từ).
- Trạng thái sai / gần đúng của màn 5.
- Màn quay lại sau nghỉ dài.
- Cài đặt: giọng Nam/Nữ, giờ nhắc, mục tiêu/ngày, xoá tài khoản.
- Bản web (desktop) cùng luồng, bố cục hai cột.
