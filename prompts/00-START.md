# 00 — Prompt khởi động (dán vào Claude Code ở thư mục repo)

Dán nguyên khối dưới đây. Mỗi phiên sau chỉ cần dán prompt của task (`prompts/<phase>/<id>.md`).

---

Bạn đang ở repo dự án "App học từ vựng tiếng Anh". Đọc `CLAUDE.md` trước, sau đó làm đúng thứ tự sau và dừng lại báo cáo ở mỗi bước ghi **DỪNG**:

1. Đọc `docs/09-ke-hoach.md` §1–§3P và `records/TRACKING.md`. Liệt kê các task ở trạng thái "Chưa" mà không còn phụ thuộc chưa xong; đề xuất task tiếp theo (mặc định P.1 nếu chưa có gì).
2. **DỪNG.** Hỏi tôi xác nhận task. Không bắt đầu khi chưa xác nhận.
3. Mở `prompts/<phase>/<id>.md`. Phân loại Type / Level / Repro theo CLAUDE.md §7.1. Level L3 → dừng, báo cáo, mở task riêng, không code. `git switch main && git pull`, rồi cắt nhánh `feature|fix|chore/<id>-<slug>`.
4. **CỔNG A.** Viết `docs/tasks/<id>/Plan.md`, và `Flow.md` nếu không thuộc diện bỏ ở §7.2. Bằng chứng về mã và dữ liệu lấy từ grep chạy hôm nay kèm `File.ext:dòng`. Đọc lại nguội 4 câu (§7.3). Đẩy lên yawasa, mở trang dự án kiểm bằng mắt, báo link.
5. **DỪNG.** Chờ tôi đọc trên hub và duyệt. Chưa duyệt thì chưa chạm mã, chưa tải dữ liệu. Tôi yêu cầu sửa → sửa cả hai tệp cho khớp nhau, ghi dòng có ngày vào Decisions log, đẩy lại cùng slug kèm `--update`.
6. Tạo `records/<id>.md` từ `records/TEMPLATE.md`: ngày bắt đầu, nhánh, link Plan và Flow. `records/TRACKING.md` chuyển "Đang làm".
7. Thực hiện checklist từng bước. Sau mỗi bước ghi "kết quả: …" vào bản ghi. Phụ thuộc thiếu → "Chặn", ghi lý do, **DỪNG**, hỏi tôi. Kế hoạch đổi giữa chừng → sửa Plan.md, ghi Decisions log, đẩy lại `--update`, nói rõ chỗ đổi.
8. Chạy phần "Kiểm tra" của prompt. Ghi bảng kết quả với số thật.
9. Chạy phần "Xác minh output trước khi đóng" (CLAUDE.md §3). Bất kỳ lỗi nào → sửa, chạy lại; không đóng task khi còn lỗi. Nếu task đổi quyết định, sửa `docs/` đúng mục và ghi vào bản ghi.
10. **CỔNG B.** Viết `docs/tasks/<id>/Result.md`, đẩy lên yawasa. Dựng `docs/Delivery/<ngày>_<id>/`, quét bằng chứng tìm khoá, token, dữ liệu người thật trước khi đẩy.
11. **DỪNG.** Trình bày tóm tắt ≤ 15 dòng: đã làm gì, test đạt/không, file đầu ra, câu hỏi mở, link hub, và câu lệnh commit dự định. Chờ tôi duyệt rồi mới commit, chạy `gate.sh merge` để gộp vào `main` tại máy, xoá nhánh, đẩy Delivery, đổi trạng thái sang "Xong" và ghi người kiểm/ngày (CLAUDE.md §7.8).

Quy tắc trong suốt phiên:
- Không tải nội dung không có giấy phép mở (CLAUDE.md §4). Nếu một bước cần dữ liệu ngoài allowlist, dừng và hỏi.
- Không bịa số đo; chưa đo thì ghi "chưa đo".
- Không sửa `golden/` trừ khi task nói rõ.
- Hai drop viết tiếng Anh B1/B2; `docs/` và `records/` giữ tiếng Việt (CLAUDE.md §7.4).
- Mọi lần đẩy đều kèm `--project "moonegg"`, nếu không bản đẩy rơi vào thư mục nháp chỉ mình tôi thấy. Không dùng `--folder` thay thế.
- Ba tệp Plan/Flow/Result viết tiếng Anh B1/B2; `docs/01..09`, `records/` và trao đổi giữ tiếng Việt.
- Không làm task trên `main`. Commit `<type>(<id>): <việc>`, không ghi công công cụ, không emoji.
- Commit theo `<id>: <việc>` sau mỗi bước hoàn chỉnh, build được.

Bắt đầu bằng bước 1.

---

## Prompt rút gọn cho phiên tiếp theo

```
Đọc CLAUDE.md. Tiếp tục task <ID> theo prompts/<phase>/<ID>.md và records/<ID>.md; nếu chưa có bản ghi thì tạo. Làm theo quy trình 11 bước trong prompts/00-START.md, dừng ở mọi bước ghi DỪNG (Cổng A trước khi làm, Cổng B trước khi commit).
```

## Prompt cho phiên rà soát cuối tuần

```
Đọc CLAUDE.md. Với mọi task trạng thái "Xong" trong tuần này ở records/TRACKING.md: mở bản ghi, kiểm mỗi task có (a) mọi bước có dòng kết quả, (b) bảng kiểm tra có số thật, (c) mục xác minh output đã tick, (d) bằng chứng có link/đường dẫn tồn tại. Task thiếu bất kỳ mục nào → đổi về "Chờ kiểm", ghi thiếu gì. Tổng hợp ước–thực cho tuần.
```
