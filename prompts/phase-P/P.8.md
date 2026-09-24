# P.8 — Chuẩn hoá và ghép nguồn

**Tham chiếu:** Kế hoạch §3P.2 P.8 · Kiến trúc §5.5, §7.1

## Mục tiêu
lexicon_raw.sqlite cho toàn bộ headword NGSL+NAWL: hạng, pos, ARPAbet, IPA US/UK, nghĩa kaikki, câu Tatoeba có bản Việt; báo cáo phủ.

## Cách làm
1. Mở rộng tools/pipeline/build_lexicon.py: đọc danh sách từ P.7 thay vì danh sách cứng; giữ ánh xạ ARPAbet→IPA/viseme và tách đồng tự khác âm (mỗi cách đọc CMUdict một dòng khi pos khác nhau; cùng pos → giữ cách đọc đầu, ghi n_variants).
2. Ghép kaikki: stream JSONL (file lớn), lọc `lang=English`, khớp `word` + `pos`; lấy senses[].glosses, sounds[].ipa (tags us/uk), synonyms. Lưu `senses_raw` (item_id, order, gloss_en, ipa_uk).
3. Ghép Tatoeba: sentences eng, links tới vie; tìm câu chứa từ ở dạng đúng (regex biên từ, cả biến tố đơn giản -s/-ed/-ing); lưu `examples_raw` (item_id, en, vi, tatoeba_id, license=CC-BY-2.0-FR).
4. Sửa IPA: AH0→ə, đặt dấu trọng âm ở đầu âm tiết (tách âm tiết theo nguyên âm + phụ âm đầu đơn giản), đối chiếu với IPA kaikki khi có, ghi `ipa_source`.
5. Báo cáo `content/lexicon/COVERAGE.md`: % có IPA, ≥1 nghĩa kaikki, ≥1 câu Việt, đa cách đọc.

## Checklist (chép vào records/P.8.md, tick từng dòng kèm 'kết quả:')
- [ ] lexicon_raw.sqlite có bảng word, senses_raw, examples_raw
- [ ] COVERAGE.md
- [ ] verify_pack.py 0 lỗi

## Kiểm tra (test đối chiếu)
- verify_pack.py content/lexicon/lexicon_raw.sqlite → 0 lỗi
- Kiểm tay 20 từ ngẫu nhiên: IPA, nghĩa, câu hợp lý

## Xác minh output trước khi đóng
- Số dòng word = số headword đầu vào + số dòng đồng tự khác âm bổ sung; không item_id trùng
- Chạy `CLAUDE.md` §3 cho loại đầu ra; chưa qua → không đóng.

## Bằng chứng cần nộp
- COVERAGE.md
- Log verify
