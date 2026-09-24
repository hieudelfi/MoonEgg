# P.10 — Thử pipeline đầu-cuối trên 30 từ

**Tham chiếu:** Kế hoạch §3P.2 P.10 · Kiểm thử §2.1, §6.1

## Mục tiêu
pack_test_v1 (30 từ của tài liệu kiểm thử) đi hết pipeline → đóng gói → pytest 10/10; đo phút/từ.

## Cách làm
1. Từ lexicon_raw: chọn 30 item_id ở docs/08 §2.1. Chạy xưởng (P.5): duyệt nghĩa Việt, 2 câu/từ (lấy Tatoeba, thiếu thì tự viết và ghi source=self).
2. Sinh audio 2 giọng (đã chốt P.4) cho từ và câu; Opus; loudnorm.
3. MFA căn từng file từ → TextGrid → `tools/pipeline/textgrid_to_viseme.py` → timeline JSON (mốc ms, viseme id 0–11).
4. So phoneme MFA với CMUdict → mismatch.csv; xử lý tay.
5. Ảnh: sinh SD cho ~10 danh từ cụ thể (hoặc placeholder có ghi chú nếu không GPU).
6. Đóng gói: `tools/pipeline/pack.py` → content/pack/pack_test_v1.sqlite + assets/ + manifest.json (sha256). Viết `tools/checks/test_pack.py` (pytest) cho TC-CT-01→11 ở mức 30 từ.
7. Đẩy lên R2. Ghi tổng phút/từ.

## Checklist (chép vào records/P.10.md, tick từng dòng kèm 'kết quả:')
- [ ] 30 từ approved trong xưởng
- [ ] 60 audio từ + 120 audio câu
- [ ] 30 timeline JSON
- [ ] mismatch.csv ≤ 2% hoặc đã xử lý
- [ ] pack_test_v1 trên R2
- [ ] pytest 10/10

## Kiểm tra (test đối chiếu)
- pytest tools/checks/test_pack.py -k pack_test_v1
- verify_pack.py --strict content/pack/pack_test_v1.sqlite

## Xác minh output trước khi đóng
- manifest sha256 khớp mọi tệp; chỉ bản ghi approved trong gói
- Chạy `CLAUDE.md` §3 cho loại đầu ra; chưa qua → không đóng.

## Bằng chứng cần nộp
- manifest.json
- Log pytest
- Số phút/từ
