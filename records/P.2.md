# P.2 — Supabase, R2, Pages

Bắt đầu: 2026-09-24 (Plan) · 2026-09-25 (Cổng A duyệt, bắt đầu làm)  Kết thúc: <ngày>  Công thực tế: <nđ> (ước: 1,5)
Type: INFRA  Level: L2  Repro (ISSUE): không áp dụng
Người kiểm: tự kiểm  Nhánh: `chore/p2-supabase-r2-pages` (cắt từ `main` tại `789b9c4`)
Plan: https://hub.yawasa.com/app/p/moonegg-p2-plan  Flow: bỏ — Type INFRA, chưa có màn hình  Result: <link hub>
Delivery: `docs/Delivery/2026-09-___P.2/`
Tham chiếu: FR-30, FR-44→47 · Kiến trúc §2, §7.2 · Test TC-AU-04 · Kế hoạch §3P.1 P.2
Phụ thuộc: P.1 (Xong 2026-09-24)

## Checklist
- [x] B1 `supabase/schema.sql`: 7 bảng, index, unique, RLS, trigger `server_seq` — kết quả: 213 dòng, commit `f5c9f0c`. 7 bảng, 3 index, 13 policy, 1 trigger, 4 lệnh grant. `event_id` là khoá chính nên ràng buộc duy nhất có sẵn, không thêm dòng riêng.
- [x] B2 `.env.example`: 3 tên biến, không giá trị — kết quả: `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `R2_PUBLIC_BASE`, tất cả rỗng. Commit `975fbc6`.
- [x] B3 `docs/tasks/P.2/click-list.md`: bước bấm Supabase + Cloudflare — kết quả: 5 phần (A Supabase, B R2, C Pages, D gửi lại gì, E dọn người dùng thử), 6+3+1 bước đánh số, mỗi bước có dòng "trên màn hình sau đó". Commit `975fbc6`.
- [x] B4 `tools/ops/ping-supabase.sh` + `register-ping-task.ps1` — kết quả: `bash -n` sạch; chạy khi thiếu biến trả exit 2 kèm thông báo đúng; PowerShell parse sạch. Log `tools/ops/ping-supabase.log` thêm vào `.gitignore:12`. Commit `2dd673e`.
- [x] B5 `.github/workflows/ping-supabase.yml` (workflow_dispatch, ngủ) — kết quả: chỉ `workflow_dispatch`, khối `schedule` để dạng comment, theo đúng cách `ci.yml` xử ở P.1. Commit `2dd673e`.
- [x] B6 Người review chạy click-list: Supabase project, Auth, SQL — kết quả: project `rxnhounlifmydmdemzok` ở Singapore; 7 bảng + 13 policy + 1 trigger đúng kỳ vọng; 2 người dùng thử đã tạo; `email` và `google` bật, Apple tắt có lý do ghi sẵn.
- [ ] B7 Người review chạy click-list: R2 bucket, Pages project — kết quả: **Chặn** 2026-09-25, cùng lý do B6.
- [ ] B8 Test 1–10 chạy thật, ghi số vào bảng dưới — kết quả:
- [ ] B9 Xoá 2 người dùng thử — kết quả:
- [ ] B10 Cổng B: Result.md + Delivery + quét bằng chứng — kết quả:

## Kiểm tra
| Test | Cách chạy | Input | Output thật | Đạt? |
| --- | --- | --- | --- | --- |
| 1 TC-AU-04 | token A gọi `GET /rest/v1/review_event` | A và B mỗi người 1 sự kiện | HTTP 200, 1 dòng, chủ sở hữu A; 0 dòng của B | Đạt |
| 2 RLS thật bật | query `pg_class` + `pg_policy` trong SQL Editor | 7 bảng public | 7/7 `rls_bat = true`; policy: analytics_daily 1, sáu bảng còn lại 2 | Đạt |
| 3 Schema lặp lại được | Run trong SQL Editor | tệp 220 dòng | chạy 3 lần (2 lần bản đầu, 1 lần sau khi sửa), cả 3 `Success. No rows returned` | Đạt |
| 4 R2 đọc được | `curl -I` một file đã upload | 1 file thử | chưa chạy | |
| 5 Pages trả lời | `curl -I` URL Pages | — | chưa chạy | |
| 6 event_id duy nhất | POST lại `event_id` đã có | `p2-a-1` | HTTP 409 `duplicate key value violates unique constraint "review_event_pkey"` | Đạt |
| 7 Ping chạy tay | `bash tools/ops/ping-supabase.sh` | — | chưa chạy | |
| 7b Task Scheduler bắn | đăng ký rồi Run on demand | — | chưa chạy | |
| 8 Không có khoá trong repo | `gate.sh full` + grep `eyJ…`, `AKIA…`, `service_role`, PEM | 5 tệp mới | cổng 4 mục Đạt trong 21,6 s; grep 0 tệp khớp | Đạt |
| 9 `server_seq` client không đặt được | POST kèm `server_seq: 999999`, 3 lần | token A | máy chủ lưu 8, 9, 10; không lần nào là 999999; bước nhảy 1 | Đạt |
| 10 Dọn người dùng thử | liệt kê auth users | — | chưa chạy | |
| phụ: provider bật | `GET /auth/v1/settings` | — | `email` và `google` true, `apple` false | Đạt |
| phụ: Google nối thật | `GET /auth/v1/authorize?provider=google` | — | HTTP 302 tới `accounts.google.com`, `client_id` `811115347643-fdd9vt0...`, `redirect_uri` khớp callback | Đạt |

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

- 2026-09-25 — **RLS của `sync_cursor` đi vòng qua bảng `device`, không thêm cột.** `docs/07` §7.2 cho
  bảng này ba cột `device_id`, `pulled_seq`, `pushed_seq`, không có `user_id`, nên không viết thẳng
  được policy `user_id = auth.uid()`. Hai lựa chọn: thêm cột `user_id`, hoặc hỏi chủ sở hữu qua
  `device`. Chọn cách thứ hai vì thêm cột là sửa hợp đồng dữ liệu, tức là L3 và phải mở task riêng.
  Đánh đổi: policy chậm hơn một chút vì có subquery, chấp nhận được với bảng một dòng mỗi thiết bị.
- 2026-09-25 — **Không có policy update và delete cho mọi bảng.** RLS bật mà thiếu policy thì hành
  động đó bị từ chối, nên nhật ký sự kiện thành chỉ-ghi-thêm mà không cần luật riêng. Đây là chủ ý,
  không phải bỏ sót.
- 2026-09-25 — **`.env.local` thay cho `.env`, và `.gitignore` phải sửa.** Người review điền giá trị
  vào `.env.local` (đúng quy ước Vite). `.gitignore:10` chỉ có dòng `.env`, không khớp `.env.local`,
  nên tệp chứa khoá thật đang ở trạng thái chưa được bỏ qua — chỉ cần một lệnh `git add .` là lọt vào
  commit. Đã thêm `.env.*` cộng `!.env.example`, kiểm lại: `.env.local` bị bỏ qua, `.env.example` vẫn
  được theo dõi. Script ping sửa để đọc cả hai tệp. Đây là lỗ hổng do P.2 tạo ra trong chính phiên
  này, không phải lỗi có sẵn.
- 2026-09-25 — **Khoá là JWT anon kiểu cũ, không phải publishable key kiểu mới.** Giải mã phần
  payload: `role: anon`, `ref: rxnhounlifmydmdemzok`, khớp URL. Dùng được, không cần đổi.
- 2026-09-25 — **`bigserial` cộng trigger đốt hai số chuỗi mỗi lần ghi.** Đo thật: 2, 4, 7. Giá trị
  mặc định của `bigserial` gọi `nextval` một lần, trigger gọi lần nữa rồi ghi đè. Không sai — `docs/07`
  §5.4 kéo dữ liệu bằng con trỏ "sau số N", không giả định số liền nhau — nhưng lãng phí không có lý
  do. Thêm `alter column server_seq drop default` để trigger là nơi duy nhất cấp số. Đo lại: 8, 9, 10,
  bước nhảy 1.
- 2026-09-25 — **Kiểm thêm ngoài danh sách test: nhật ký có thật sự chỉ-ghi-thêm không.** Token A gọi
  PATCH và DELETE lên chính sự kiện của mình: cả hai HTTP 403. Đúng chủ ý — không viết policy update
  và delete thì hai hành động đó bị từ chối, không cần luật riêng.

## Câu hỏi mở
- Chưa có. Bốn câu của Cổng A đã trả lời trong Decisions log.

## Người kiểm: tự kiểm  Ngày:   Kết luận: Xong / Làm lại (lý do)
