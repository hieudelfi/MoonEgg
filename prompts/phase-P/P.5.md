# P.5 — Xưởng nội dung (content workbench)

**Tham chiếu:** Kế hoạch §4.3, §3P.1 P.5 · Yêu cầu §6.3, §6.4, §13.1

## Mục tiêu
Công cụ duyệt cục bộ: mỗi màn một từ, nghĩa/câu/ảnh ứng viên, nghe audio, khẩu hình tĩnh, link nguồn, phím tắt, ghi review_status.

## Cách làm
1. Tạo `tools/workbench/` bằng Vite React TS (hoặc Python FastAPI + HTML nếu thích). Đọc/ghi `content/lexicon/*.csv` và `content/pack/senses.csv`, `examples.csv`, `images.csv`.
2. Màn từ: headword, IPA, audio 2 giọng (nút nghe), danh sách nghĩa ứng viên (kaikki/WordNet) với nút chọn/sửa, ô nghĩa Việt ≤ 8 từ, câu ứng viên với checklist 5 mục, 4 ảnh ứng viên (chọn 1 hoặc loại), link nguồn và cờ giấy phép.
3. Phím: J/K chuyển từ, 1–4 chọn ảnh, A duyệt, E sửa, X loại, R nghe lại.
4. Ghi `review_status` (pending/approved/rejected/needs_second), `reviewed_by`, `reviewed_at`; bản ghi bị sửa → needs_second.
5. Bộ đếm thời gian/từ, xuất báo cáo giây/từ.
6. Chạy thử trên 30 từ test; quay video 2 phút.

## Checklist (chép vào records/P.5.md, tick từng dòng kèm 'kết quả:')
- [ ] Mở được 30 từ, duyệt hết bằng phím
- [ ] CSV cập nhật đúng cột review_*
- [ ] Hàng đợi needs_second hoạt động
- [ ] Báo cáo giây/từ

## Kiểm tra (test đối chiếu)
- Kiểm tay: duyệt 10 từ, so CSV trước/sau
- verify_pack.py --strict trên 10 từ đã approved: 0 lỗi

## Xác minh output trước khi đóng
- Không có bản ghi approved thiếu source/license
- Chạy `CLAUDE.md` §3 cho loại đầu ra; chưa qua → không đóng.

## Bằng chứng cần nộp
- Video/ảnh xưởng
- CSV mẫu
- Số đo giây/từ
