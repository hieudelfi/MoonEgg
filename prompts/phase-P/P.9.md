# P.9 — Danh sách 5.000 từ và đợt 1

**Tham chiếu:** Kế hoạch §3P.2 P.9 · Yêu cầu FR-02, §8.3 · Test TC-CT-09

## Mục tiêu
wordlist_5000.csv chia 5 đợt; pack1_words.csv 500 từ với 3 cột mốc, cờ 20 âm khó; 30 từ giả cho placement.

## Cách làm
1. Xếp: NGSL theo hạng → NAWL → bù bằng tần suất kaikki (hoặc danh sách tần suất mở khác đã ghi nguồn) đến 5.000; loại từ tục/nhạy cảm bằng danh sách cấm.
2. Cờ âm khó: theo bảng 20 âm trong docs/01 §2 và hàm hard_flags của build_lexicon.py.
3. Đợt 1 = 500 từ hạng đầu; chia 3 cột mốc có tên (ví dụ Chào hỏi, Gia đình, Đi chợ đi ăn) bằng gắn chủ đề sơ bộ; ghi milestone_id.
4. 30 từ giả: sinh theo quy tắc âm tiết tiếng Anh, kiểm không có trong kaikki và không tục → `content/lexicon/pseudowords.csv`.

## Checklist (chép vào records/P.9.md, tick từng dòng kèm 'kết quả:')
- [ ] wordlist_5000.csv 5.000 dòng
- [ ] pack1_words.csv 500 dòng, 3 cột mốc mỗi ~167 từ
- [ ] pseudowords.csv 30 dòng

## Kiểm tra (test đối chiếu)
- TC-CT-09: 0 từ giả có trong kaikki
- Kiểm tay: 20 từ ngẫu nhiên đợt 1 đều là từ phổ thông

## Xác minh output trước khi đóng
- Không trùng headword+pos giữa các đợt; mọi từ đợt 1 có trong lexicon_raw.sqlite
- Chạy `CLAUDE.md` §3 cho loại đầu ra; chưa qua → không đóng.

## Bằng chứng cần nộp
- 3 file CSV
- Log kiểm
