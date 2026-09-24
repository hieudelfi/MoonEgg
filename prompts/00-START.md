# 00 — Prompt khởi động (dán vào Claude Code ở thư mục repo)

Dán nguyên khối dưới đây. Mỗi phiên sau chỉ cần dán prompt của task (`prompts/<phase>/<id>.md`).

---

Bạn đang ở repo dự án "App học từ vựng tiếng Anh". Đọc `CLAUDE.md` trước, sau đó làm đúng thứ tự sau và dừng lại báo cáo ở mỗi bước có dấu ⏸:

1. Đọc `docs/09-ke-hoach.md` §1–§3P và `records/TRACKING.md`. Liệt kê các task ở trạng thái "Chưa" mà không còn phụ thuộc chưa xong; đề xuất task tiếp theo (mặc định P.1 nếu chưa có gì).
2. ⏸ Hỏi tôi xác nhận task. Không bắt đầu khi chưa xác nhận.
3. Mở `prompts/<phase>/<id>.md` của task đó. Viết `records/drops/<id>-plan.md` từ `records/drops/TEMPLATE-plan.md`, đọc lại nguội theo 4 câu ở CLAUDE.md §7.3, đẩy lên yawasa (CLAUDE.md §7.2), báo link.
4. ⏸ **CỔNG A.** Chờ tôi đọc plan trên hub và duyệt. Chưa duyệt thì chưa viết mã, chưa tải dữ liệu. Tôi yêu cầu sửa → sửa file rồi đẩy lại cùng slug kèm `--update`.
5. Tạo `records/<id>.md` từ `records/TEMPLATE.md`, điền tham chiếu, link plan drop và ngày bắt đầu; đổi trạng thái trong `records/TRACKING.md` thành "Đang làm".
6. Thực hiện checklist từng bước. Sau mỗi bước: ghi "kết quả: …" vào bản ghi. Gặp phụ thuộc thiếu → trạng thái "Chặn", ghi lý do, ⏸ hỏi tôi. Kế hoạch đổi giữa chừng → sửa plan drop, đẩy lại `--update`, nói rõ chỗ đổi; không lặng lẽ đi hướng khác.
7. Chạy phần "Kiểm tra" của prompt. Ghi bảng kết quả với số thật.
8. Chạy phần "Xác minh output trước khi đóng" (CLAUDE.md §3). Bất kỳ lỗi nào → sửa, chạy lại; không đóng task khi còn lỗi.
9. Ghi "Bằng chứng", "Giải thích", "Câu hỏi mở". Nếu task đổi quyết định, sửa `docs/` đúng mục và ghi vào bản ghi.
10. Viết `records/drops/<id>-outcome.md` từ `records/drops/TEMPLATE-outcome.md`, đẩy lên yawasa, báo link.
11. ⏸ **CỔNG B.** Trình bày tóm tắt ≤ 15 dòng: đã làm gì, test đạt/không, file đầu ra, câu hỏi mở, hai link hub. Chờ tôi kiểm rồi mới đổi trạng thái sang "Xong" và ghi người kiểm/ngày.

Quy tắc trong suốt phiên:
- Không tải nội dung không có giấy phép mở (CLAUDE.md §4). Nếu một bước cần dữ liệu ngoài allowlist, dừng và hỏi.
- Không bịa số đo; chưa đo thì ghi "chưa đo".
- Không sửa `golden/` trừ khi task nói rõ.
- Hai drop viết tiếng Anh B1/B2; `docs/` và `records/` giữ tiếng Việt (CLAUDE.md §7.4).
- Mọi lần đẩy đều kèm `--project "moonegg"`, nếu không bản đẩy rơi vào thư mục nháp chỉ mình tôi thấy. Không dùng `--folder` thay thế.
- Commit theo `<id>: <việc>` sau mỗi bước hoàn chỉnh, build được.

Bắt đầu bằng bước 1.

---

## Prompt rút gọn cho phiên tiếp theo

```
Đọc CLAUDE.md. Tiếp tục task <ID> theo prompts/<phase>/<ID>.md và records/<ID>.md; nếu chưa có bản ghi thì tạo. Làm theo quy trình 11 bước trong prompts/00-START.md, dừng ở các ⏸ (Cổng A trước khi làm, Cổng B trước khi đóng).
```

## Prompt cho phiên rà soát cuối tuần

```
Đọc CLAUDE.md. Với mọi task trạng thái "Xong" trong tuần này ở records/TRACKING.md: mở bản ghi, kiểm mỗi task có (a) mọi bước có dòng kết quả, (b) bảng kiểm tra có số thật, (c) mục xác minh output đã tick, (d) bằng chứng có link/đường dẫn tồn tại. Task thiếu bất kỳ mục nào → đổi về "Chờ kiểm", ghi thiếu gì. Tổng hợp ước–thực cho tuần.
```
