# P.7 — Tải và ghi nhận nguồn

**Tham chiếu:** Kế hoạch §3P.2 P.7 · Yêu cầu §6.1, §13 · docs/03-bang-chung-xac-thuc.md

## Mục tiêu
6 nguồn thô trong content/raw với SOURCES.md ghi URL, ngày, hash, giấy phép; đóng hai mục 'chưa mở nguồn'.

## Cách làm
1. Tải: NGSL 1.2 (newgeneralservicelist.com), NAWL, CMUdict (pip cmudict hoặc github cmusphinx), kaikki English JSONL (kaikki.org/dictionary/English), Tatoeba: sentences.csv, links.csv, sentences_with_audio.csv (tatoeba.org/downloads), WordNet (nltk).
2. Mỗi nguồn: `sha256sum`, kích thước, ngày, URL, trang giấy phép (chụp ảnh) → `content/raw/SOURCES.md`.
3. Mở tận trang giấy phép của Wiktionary (CC BY-SA 4.0 + GFDL) và CMUdict (BSD 2-clause): ghi nguyên văn 1 dòng + link; cập nhật docs/03 hai dòng 'Chưa mở nguồn' → 'Đúng'.
4. KHÔNG tải từ YouTube, Oxford, Forvo hay nguồn không mở.

## Checklist (chép vào records/P.7.md, tick từng dòng kèm 'kết quả:')
- [ ] 6 nguồn có mặt
- [ ] SOURCES.md đủ 6 dòng + hash
- [ ] Ảnh 2 trang giấy phép
- [ ] docs/03 cập nhật

## Kiểm tra (test đối chiếu)
- Kiểm tay: `sha256sum -c` khớp

## Xác minh output trước khi đóng
- Mọi giấy phép trong SOURCES.md ∈ tools/checks/license-allowlist.txt
- Chạy `CLAUDE.md` §3 cho loại đầu ra; chưa qua → không đóng.

## Bằng chứng cần nộp
- SOURCES.md
- Ảnh giấy phép
