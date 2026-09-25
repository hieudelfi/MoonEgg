# P.2 — Supabase, R2, Pages

Bắt đầu: 2026-09-24 (Plan) · 2026-09-25 (Cổng A duyệt, bắt đầu làm)  Kết thúc: <ngày>  Công thực tế: <nđ> (ước: 1,5)
Type: INFRA  Level: L2  Repro (ISSUE): không áp dụng
Người kiểm: tự kiểm  Nhánh: `chore/p2-supabase-r2-pages` (cắt từ `main` tại `789b9c4`)
Plan: https://hub.yawasa.com/app/p/moonegg-p2-plan  Flow: bỏ — Type INFRA, chưa có màn hình  Result: <link hub>
Delivery: `docs/Delivery/2026-09-___P.2/`
Tham chiếu: FR-30, FR-44→47 · Kiến trúc §2, §7.2 · Test TC-AU-04 · Kế hoạch §3P.1 P.2
Phụ thuộc: P.1 (Xong 2026-09-24)

## Checklist
- [ ] B1 `supabase/schema.sql`: 7 bảng, index, unique, RLS, trigger `server_seq` — kết quả:
- [ ] B2 `.env.example`: 3 tên biến, không giá trị — kết quả:
- [ ] B3 `docs/tasks/P.2/click-list.md`: bước bấm Supabase + Cloudflare — kết quả:
- [ ] B4 `tools/ops/ping-supabase.sh` + `register-ping-task.ps1` — kết quả:
- [ ] B5 `.github/workflows/ping-supabase.yml` (workflow_dispatch, ngủ) — kết quả:
- [ ] B6 Người review chạy click-list: Supabase project, Auth, SQL — kết quả:
- [ ] B7 Người review chạy click-list: R2 bucket, Pages project — kết quả:
- [ ] B8 Test 1–10 chạy thật, ghi số vào bảng dưới — kết quả:
- [ ] B9 Xoá 2 người dùng thử — kết quả:
- [ ] B10 Cổng B: Result.md + Delivery + quét bằng chứng — kết quả:

## Kiểm tra
| Test | Cách chạy | Input | Output thật | Đạt? |
| --- | --- | --- | --- | --- |
| 1 TC-AU-04 | token user A select review_event | 2 user, 1 event mỗi user | chưa chạy | |
| 2 RLS thật bật | query `pg_tables`, `pg_policies` | 7 bảng | chưa chạy | |
| 3 Schema lặp lại được | chạy `schema.sql` hai lần | project sạch | chưa chạy | |
| 4 R2 đọc được | `curl -I` một file đã upload | 1 file thử | chưa chạy | |
| 5 Pages trả lời | `curl -I` URL Pages | — | chưa chạy | |
| 6 event_id duy nhất | insert trùng `event_id` | 1 event | chưa chạy | |
| 7 Ping chạy tay | `bash tools/ops/ping-supabase.sh` | — | chưa chạy | |
| 7b Task Scheduler bắn | đăng ký rồi Run on demand | — | chưa chạy | |
| 8 Không có khoá trong repo | cổng + grep mẫu khoá | repo | chưa chạy | |
| 9 `server_seq` client không đặt được | insert `server_seq = 999999` | token user | chưa chạy | |
| 10 Dọn người dùng thử | liệt kê auth users | — | chưa chạy | |

## Xác minh output trước khi đóng (CLAUDE.md §3)
- [ ] `bash tools/checks/gate.sh full` sạch: <lệnh và kết quả>
- [ ] Không có bản ghi thiếu source/license: không áp dụng, task này không sinh dữ liệu nội dung
- [ ] Số đo (nếu NFR): không áp dụng

## Bằng chứng
- Commit/PR:
- File đầu ra:
- Ảnh/số đo:
- Delivery đã quét khoá/token/dữ liệu người thật: <ngày, kết quả>

## Giải thích
Năm quyết định của Cổng A nằm trong Decisions log của `docs/tasks/P.2/Plan.md`, không chép lại ở đây.

Quyết định trong lúc làm:
- 2026-09-25 — **Commit từng bước trong lúc làm, không dồn đến Cổng B.** CLAUDE.md §7.4 nói "chưa qua
  Cổng B thì không commit", nhưng §5 và `prompts/00-START.md` nói commit sau mỗi bước build được, và
  P.1 đã làm như vậy. Đọc §7.4 là cấm *đóng task* sớm (gộp vào `main`, đổi TRACKING sang Xong), không
  cấm commit trên nhánh. Chọn commit từng bước vì hook `pre-commit` chạy cổng mỗi lần, phát hiện hỏng
  sớm hơn là dồn một cục. Nhánh vẫn không gộp trước khi Cổng B duyệt.

## Câu hỏi mở
- Chưa có. Bốn câu của Cổng A đã trả lời trong Decisions log.

## Người kiểm: tự kiểm  Ngày:   Kết luận: Xong / Làm lại (lý do)
