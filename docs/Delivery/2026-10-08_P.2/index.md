# P.2 delivery - 2026-10-08

Task: `P.2` · Plan: https://hub.yawasa.com/app/p/moonegg-p2-plan
Result: https://hub.yawasa.com/app/p/moonegg-p2-result · Record: `records/P.2.md`
Branch `chore/p2-supabase-r2-pages`, merged into `main` after Gate B on 2026-10-08

This is the QC package: the raw output of every check, exactly as it was printed on the machine.
Nothing here is retyped. The Result drop explains what the task did; this one proves it.

All files were produced on 2026-10-08 by live calls, except one. Tests 1, 2, 3, 6 and 9 need the
two test users, who are now deleted. Their rows are copied by script from the task record.

**Evidence scan before handover:** 0 findings. Patterns searched: JWT strings, AWS keys, private
key blocks, `gho_` and `ghp_` tokens, `sk-` keys, email addresses, long digit strings, URLs.

## Cổng đầy đủ chạy ở máy

`evidence/gate-full.txt`

```
  pytest tools/checks               dat
  verify_pack tren du lieu mau      dat
    30 bản ghi · 0 lỗi · 2 cảnh báo
  vitest                            dat
  cong giay phep (TC-CP-01/02)      dat
    49 gói · 0 lỗi giấy phép · 0 gói thiếu dòng SDK
gate exit=0
```

## Test 1, 2, 3, 6, 9 - đo ngày 2026-09-25 với hai tài khoản thử

`evidence/tests-1-2-3-6-9-from-record.txt`

```
Copied by script from records/P.2.md, not retyped. Measured 2026-09-25 with two test users.
The users were deleted on 2026-10-08, so these five cannot be run again.

| 1 TC-AU-04 | token A gọi `GET /rest/v1/review_event` | A và B mỗi người 1 sự kiện | HTTP 200, 1 dòng, chủ sở hữu A; 0 dòng của B | Đạt |
| 2 RLS thật bật | query `pg_class` + `pg_policy` trong SQL Editor | 7 bảng public | 7/7 `rls_bat = true`; policy: analytics_daily 1, sáu bảng còn lại 2 | Đạt |
| 3 Schema lặp lại được | Run trong SQL Editor | tệp 220 dòng | chạy 3 lần (2 lần bản đầu, 1 lần sau khi sửa), cả 3 `Success. No rows returned` | Đạt |
| 6 event_id duy nhất | POST lại `event_id` đã có | `p2-a-1` | HTTP 409 `duplicate key value violates unique constraint "review_event_pkey"` | Đạt |
| 9 `server_seq` client không đặt được | POST kèm `server_seq: 999999`, 3 lần | token A | máy chủ lưu 8, 9, 10; không lần nào là 999999; bước nhảy 1 | Đạt |
```

## Người không đăng nhập không đọc và không ghi được gì

`evidence/rls-anon-sees-nothing.txt`

```
measured 2026-10-08T05:46:28Z, all calls use the public anon key, no user signed in
{"code":"42501","details":null,"hint":"Grant the required privileges to the current role with: GRANT SELECT ON public.profile TO anon;","message":"permission denied for table profile"}  <- GET profile http=401
{"code":"42501","details":null,"hint":"Grant the required privileges to the current role with: GRANT SELECT ON public.device TO anon;","message":"permission denied for table device"}  <- GET device http=401
[]  <- GET review_event http=200
{"code":"42501","details":null,"hint":"Grant the required privileges to the current role with: GRANT SELECT ON public.user_content TO anon;","message":"permission denied for table user_content"}  <- GET user_content http=401
{"code":"42501","details":null,"hint":"Grant the required privileges to the current role with: GRANT SELECT ON public.settings TO anon;","message":"permission denied for table settings"}  <- GET settings http=401
{"code":"42501","details":null,"hint":"Grant the required privileges to the current role with: GRANT SELECT ON public.sync_cursor TO anon;","message":"permission denied for table sync_cursor"}  <- GET sync_cursor http=401
{"code":"42501","details":null,"hint":"Grant the required privileges to the current role with: GRANT SELECT ON public.analytics_daily TO anon;","message":"permission denied for table analytics_daily"}  <- GET analytics_daily http=401
--- anonymous insert into review_event
{"code":"42501","details":null,"hint":"Grant the required privileges to the current role with: GRANT INSERT ON public.review_event TO anon;","message":"permission denied for table review_event"}  <- POST review_event http=401
```

## Cách đăng nhập đang bật

`evidence/auth-providers.txt`

```
measured 2026-10-08T05:46:31Z
{'email': True, 'google': True, 'apple': False}
```

## Test 4 - R2 đọc được

`evidence/test04-r2-read.txt`

```
measured 2026-10-08T05:46:24Z
--- object ping.txt
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 0
Accept-Ranges: bytes
Server: cloudflare
--- bucket root, expected 404 because R2 does not list a bucket
http=404
```

## Test 5 - địa chỉ web trả lời

`evidence/test05-web-address.txt`

```
measured 2026-10-08T05:46:22Z
GET [] http=200 type=text/html bytes=453
GET [session/3] http=200 type=text/html bytes=453
GET [favicon.svg] http=200 type=image/svg+xml bytes=9522
GET [assets/index-BRDr3nmD.js] http=200 type=text/javascript bytes=222523
GET [assets/index-D64VDMd1.css] http=200 type=text/css bytes=4105
--- headers of the root page
HTTP/1.1 200 OK
Content-Type: text/html
Cache-Control: public, max-age=0, must-revalidate
Server: cloudflare
```

## Test 7 và 7b - ping chạy tay, và nhật ký các lần tự chạy

`evidence/test07-ping.txt`

```
measured 2026-10-08T05:46:27Z
2026-10-08T05:46:27Z  http=200  ok
exit=0
--- tools/ops/ping-supabase.log, whole file
2026-09-29T01:01:10Z  http=200  ok
2026-09-29T01:01:41Z  http=200  ok
2026-09-29T01:01:58Z  http=200  ok
2026-09-29T02:00:01Z  http=200  ok
2026-10-02T02:00:02Z  http=200  ok
2026-10-05T02:00:02Z  http=200  ok
2026-10-08T02:00:02Z  http=200  ok
2026-10-08T05:46:27Z  http=200  ok
```

## Test 8 - không có khoá trong repo

`evidence/test08-no-secret-in-repo.txt`

```
measured 2026-10-08T05:46:32Z
--- tracked files, patterns: JWT, AWS key, private key block, github token, sk- key
findings=0
--- the words service_role and client_secret, every hit must be a warning sentence, not a value
.env.example:6:# not the key. The service_role key is a different thing: it bypasses row level
docs/tasks/P.2/click-list.md:13:**What must never be sent:** the database password, the `service_role` key, an
docs/tasks/P.2/click-list.md:40:4. Do **not** copy the `service_role` key. It bypasses row level security and 
docs/tasks/P.2/click-list.md:203:Never put in this file, or anywhere else in the repo: the database password, 
records/P.2.md:34:| 8 Không có khoá trong repo | `gate.sh full` + grep `eyJ…`, `AKIA…`, `service_role`,
```

## Test 10 - hai tài khoản thử đã xoá

`evidence/test10-test-users-gone.txt`

```
measured 2026-10-08T05:46:27Z
{"code":400,"error_code":"invalid_credentials","msg":"Invalid login credentials"}  <- p2-test-a@moonegg.invalid http=400
{"code":400,"error_code":"invalid_credentials","msg":"Invalid login credentials"}  <- p2-test-b@moonegg.invalid http=400
```

## Các tệp task này để lại trong repo

`evidence/files-in-repo.txt`

```
schema.sql: 190 non-empty lines
create table: 7
create policy: 13 (lines that start a statement)
enable row level security: 7
create trigger: 1
--- web/wrangler.jsonc
{
  // Static site on Cloudflare Workers. No Worker script: the build output is served as-is.
  // "name" must match the Worker name in the Cloudflare dashboard, or the build is rejected.
  "name": "moonegg",
  "compatibility_date": "2026-10-08",
  "assets": {
    "directory": "./dist",
    // A deep link such as /session/3 gets index.html, not a 404. Task 2.11 needs this.
    "not_found_handling": "single-page-application"
  }
}
--- .env.example, values must be empty
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=
R2_PUBLIC_BASE=
--- git check-ignore
.gitignore:11:.env.*	.env.local
.gitignore:14:tools/ops/ping-supabase.log	tools/ops/ping-supabase.log
```

## Kết quả quét bằng chứng trước khi giao

`evidence/scan.txt`

```
Quet ngay 2026-10-08, thu muc evidence/ cua P.2.
0 phat hien.
Mau tim: JWT (eyJ...), AKIA, private key, gho_/ghp_, sk-, dia chi email, chuoi 9-12 chu so, URL.
Khop nhung khong phai phat hien:
- 2 dia chi p2-test-a/b@moonegg.invalid: tai khoan thu, ten mien .invalid khong nhan thu, da xoa.
- chu "password" trong 2 cau canh bao trich tu click-list.md, khong co gia tri nao.
Khong co URL nao trong evidence/: dia chi Supabase va R2 doc tu .env.local, khong ghi ra tep.
```

## What a reader should take from this

- A signed-in user reads only their own events. A visitor with no account reads nothing.
- The server assigns the sync sequence number. A client cannot set it.
- The bucket serves a public file, and the web address serves the app, deep links included.
- The keep-alive ran by itself on four dates, three days apart, each with HTTP 200.
- The two test users are gone, and no key is in the repo or in this package.
