# P.1 — Repo, CI, quét giấy phép

Bắt đầu: 2026-09-24  Kết thúc: 2026-09-24  Công thực tế: 0.9 nđ (ước: 1.5 nđ)
Type: INFRA  Level: L2  Repro: không áp dụng
Người kiểm: tự kiểm  Nhánh: `chore/p1-repo-ci`
Plan: https://hub.yawasa.com/app/p/moonegg-p1-plan  Flow: bỏ — Type INFRA, chưa có màn hình  Result: https://hub.yawasa.com/app/p/moonegg-p1-result
Delivery: `docs/Delivery/2026-09-24_P.1/`
Tham chiếu: docs/09 §3P.1 P.1 · docs/07 §2 · docs/01 §13.2 · Test TC-CP-01, TC-CP-02
Phụ thuộc: không có, task đầu của giai đoạn P

**Trạng thái: Xong** — Cổng B duyệt ngày 2026-09-24. Chặn cũ (GitHub Actions) đã gỡ bằng cách chuyển cổng về chạy ở máy; xem Giải thích, mục "Đổi hướng giữa chừng".

## Checklist

- [x] B0 Khởi tạo repo — kết quả: đã làm trước quy trình, commit `1736b31`, repo `hieudelfi/MoonEgg` private, nhánh mặc định `main`. Không init lại (Plan, Decisions log 1).
- [x] B1 Sửa verify_pack.py — kết quả: thêm khối ép UTF-8 ở `tools/checks/verify_pack.py:7-11`. Chạy không cần `PYTHONIOENCODING`: `30 bản ghi · 0 lỗi · 2 cảnh báo`, exit 0, không traceback. Commit `9813fbb`.
- [x] B1b Test khói python — kết quả: thêm `tools/checks/test_smoke.py` 3 test (dữ liệu mẫu tồn tại, verify_pack 0 lỗi, không UnicodeEncodeError). Lý do: `pytest` thoát mã 5 khi không tìm thấy test nào, bộ test rỗng sẽ làm CI đỏ. Commit `9813fbb`.
- [x] B2 Dựng web/ + vitest — kết quả: `npm create vite@latest web -- --template react-ts`, thêm `vitest` dev, `package.json` script `test` = `vitest run` (không phải `vitest`, tránh treo watch mode trong CI). `web/src/__tests__/smoke.test.ts` 1 test. `npm test`: 1 test file, 1 test passed, 702 ms, exit 0. Commit `c59bcc1`.
- [x] B3 mobile/ placeholder — kết quả: `mobile/README.md` ghi Flutter chưa cài (`command -v flutter` không thấy), nêu task nào sẽ dựng (P.3, 3.1, 3.2, 3.6). Commit `40874c7`.
- [x] B4 CI 4 job — kết quả: `.github/workflows/ci.yml` với 4 job, GitHub tạo đúng tên cả bốn nhưng không job nào chạy được (chặn thanh toán). Commit `9f14e01`. **Sau đó đổi hướng**: workflow chuyển sang `on: workflow_dispatch`, giữ làm bản dự phòng, cổng thật chuyển về máy — xem B8, B9.
- [x] B5 vitest vào sdk-allowlist — kết quả: thêm khối "Công cụ dev — không vào bundle" cho 6 gói scaffold sinh ra, không phải 1 như Plan dự tính. Xem "Giải thích". Commit `9f14e01`.
- [x] B6 Ép một lần đỏ — kết quả: **đạt.** Fixture ngoại tuyến `tools/checks/fixtures/gpl-case/` với gói `fake-gpl-pkg@1.0.0` giấy phép GPL-3.0. Cổng trả `1 gói · 1 lỗi giấy phép`, `LỖI fake-gpl-pkg@1.0.0: GPL-3.0 ngoài allowlist`, exit 1. Đóng thành test tự động `tools/checks/test_licenses.py` nên lần sau không phải làm tay, và nó chạy trong cổng mỗi lần commit.
- [x] B7 Bảo vệ nhánh — kết quả: **không bật được.** `gh api repos/hieudelfi/MoonEgg/rulesets` trả `403 Upgrade to GitHub Pro or make this repository public to enable this feature.` Prompt P.1 cho phép ghi lý do thay vì bật. Bù lại bằng luật ở `CLAUDE.md` §7.8: cổng ở máy phải đạt mới được gộp, và `gate.sh merge` tự gỡ merge ra nếu cổng hỏng.
- [x] B8 Cổng chung của máy — kết quả: `~/.config/devgate/` gồm `gate.sh` (chạy cổng, lệnh `merge`, lệnh `doctor`) và `hooks/pre-commit`, `hooks/pre-push`. `git config --global core.hooksPath` trỏ vào đó nên mọi repo trên máy đều đi qua. Repo không có tệp cổng thì bỏ qua im lặng; hook riêng trong `.git/hooks/` vẫn được gọi sau.
- [x] B9 Cổng của MoonEgg — kết quả: `tools/checks/gate.sh` hai mức. `quick` (pytest + verify_pack) đo **2 giây**; `full` (thêm vitest + cổng giấy phép) đo **4,866 giây** bằng `time`. So với chờ runner GitHub: nhanh hơn hẳn và không phụ thuộc tài khoản.

## Kiểm tra

| Test | Cách chạy | Input | Output thật | Đạt? |
| --- | --- | --- | --- | --- |
| TC-CP-01 | `node tools/checks/check_licenses.mjs` | `web/` sau `npm install` | `49 gói · 0 lỗi giấy phép · 0 gói thiếu dòng SDK`, exit 0 | Đạt |
| TC-CP-02 | cùng lệnh, phần thứ hai | 10 dependency trực tiếp của `web/package.json` | 0 gói thiếu dòng. Trước khi thêm khối dev: 6 gói thiếu, exit 1 | Đạt |
| Test 3 — cổng giấy phép có cắn | `node tools/checks/check_licenses.mjs tools/checks/fixtures/gpl-case` | gói GPL-3.0 giả | `1 lỗi giấy phép`, `GPL-3.0 ngoài allowlist`, exit 1 | Đạt |
| Test 4 — checker trên Windows | `python tools/checks/verify_pack.py content/lexicon/lexicon_raw_test.csv` | 30 dòng CSV mẫu | `30 bản ghi · 0 lỗi · 2 cảnh báo`, exit 0, không traceback | Đạt |
| Test 6 — bộ test chạy được | `python -m pytest tools/checks -q` | 2 tệp test | `5 passed in 1.59s`, exit 0 | Đạt |
| Test 6b — web test | `npm test` trong `web/` | 1 tệp test | `Test Files 1 passed (1)`, exit 0 | Đạt |
| Test 5 — checker trong cổng | `bash tools/checks/gate.sh quick` | dữ liệu mẫu | `30 bản ghi · 0 lỗi · 2 cảnh báo`, exit 0 | Đạt |
| Test 7 — cổng chặn commit hỏng | thêm `test_tam_hong.py` rồi `git commit` | 1 test `assert False` | `1 failed, 5 passed`, `devgate: hong (ma 1) sau 2s`, commit bị từ chối, `HEAD` vẫn `e571539` | Đạt |
| Cổng full | `time bash tools/checks/gate.sh full` | toàn repo | 4 mục đều `dat`, `real 0m4.866s`, exit 0 | Đạt |
| devgate bỏ qua repo ngoài | repo thử trong thư mục tạm, không có tệp cổng | 1 commit | commit lọt, không in gì | Đạt |
| devgate chặn repo có cổng hỏng | cùng repo thử, thêm `tools/checks/gate.sh` trả 1 | 1 commit | commit không vào, tổng số commit vẫn 1 | Đạt |
| CI trên GitHub (bỏ) | `gh run list` | commit `40874c7` | 4 job `failure` sau 3 giây, 0 bước chạy | Không đạt — đã bỏ, xem Giải thích |

## Xác minh output trước khi đóng (CLAUDE.md §3)

- [x] Mã: `pytest tools/checks -q` → 5 passed, exit 0. `npm test` → 1 passed, exit 0.
- [x] Không thêm dependency ngoài `tools/checks/sdk-allowlist.md`: cổng giấy phép trả 0 gói thiếu dòng.
- [x] Cổng đạt: `bash tools/checks/gate.sh full` → 4 mục `dat`, 4,866 giây, exit 0.
- [x] Không có bản ghi thiếu source/license: `verify_pack.py` 0 lỗi trên dữ liệu mẫu.

## Bằng chứng

- Commit: `9813fbb` verify_pack + test khói · `c59bcc1` web + vitest · `9f14e01` CI + cổng giấy phép · `40874c7` mobile placeholder
- File đầu ra: `.github/workflows/ci.yml`, `tools/checks/check_licenses.mjs`, `tools/checks/test_smoke.py`, `tools/checks/test_licenses.py`, `tools/checks/fixtures/gpl-case/`, `web/`, `mobile/README.md`
- Lần chạy CI: https://github.com/hieudelfi/MoonEgg/actions/runs/35976963632 — 4 job `failure`
- Nguyên văn GitHub trả về (annotation của check-run 107559618956): `The job was not started because recent account payments have failed or your spending limit needs to be increased. Please check the 'Billing & plans' section in your settings`
- Bảo vệ nhánh: `403 Upgrade to GitHub Pro or make this repository public to enable this feature.`
- Delivery đã quét khoá/token/dữ liệu người thật: 2026-09-24, 0 phát hiện (xem `docs/Delivery/2026-09-24_P.1/`)

## Giải thích

**Khác Plan ở ba chỗ nhỏ:**

1. Plan viết "vitest thêm một dòng vào sdk-allowlist". Thực tế scaffold Vite sinh ra 6 gói dev: `vitest`, `@vitejs/plugin-react`, `oxlint`, `@types/node`, `@types/react`, `@types/react-dom`. Thêm cả 6 vào một khối "Công cụ dev — không vào bundle" thay vì một dòng. Quyết định vì TC-CP-02 đòi mọi dependency có dòng, và gộp thành khối rõ hơn là rải 6 dòng lẫn vào bảng gói phát hành.

2. Plan viết "CI chạy bộ test rỗng". `pytest` thoát mã 5 khi không có test nào, nên bộ rỗng sẽ làm CI đỏ. Thay bằng ba test khói thật, kiểm đúng thứ CI cần tin: `verify_pack` chạy được và in được tiếng Việt. Đây cũng chính là test 5 trong Plan, chỉ là đóng thành test tự động thay vì một bước riêng trong workflow.

3. Plan viết test 3 ép đỏ bằng cách cài một gói GPL thật rồi gỡ. Làm bằng fixture ngoại tuyến thay thế: nhanh hơn, không phụ thuộc mạng, và thành test thường trực chứ không phải thao tác tay một lần.

**Đổi hướng giữa chừng (Plan, Decisions log 8–10):** CI trên GitHub không chạy được vì chặn thanh toán ở cấp tài khoản. Thay vì chờ sửa billing, cổng chuyển về chạy ở máy: nhanh hơn (4,9 giây so với vài phút chờ runner) và không phụ thuộc tài khoản. Kéo theo ba thay đổi: bỏ pull request, gộp nhánh tại máy bằng `gate.sh merge`, và `ci.yml` chuyển sang chỉ chạy khi bấm tay. Cổng dựng ở mức **máy**, dùng chung cho mọi dự án, không phải script riêng của MoonEgg.

**Lỗi tìm thấy trong lúc làm:** `verify_pack.py:41` in tiếng Việt ra console cp1252 của Windows nên ném `UnicodeEncodeError` và thoát 1 **dù dữ liệu không lỗi**. Vì `CLAUDE.md` §3 bắt chạy script này trước khi đóng mọi task dữ liệu, lỗi này sẽ làm mọi task dữ liệu báo hỏng giả. Đã sửa và có test chặn hồi quy.

Chưa cập nhật tài liệu nào trong `docs/01..09` — task này không đổi quyết định nào.

## Câu hỏi mở

1. `core.hooksPath` toàn cục đổi hành vi git của **mọi repo trên máy này**, không riêng MoonEgg. Cổng bỏ qua im lặng repo không tham gia, và vẫn gọi hook riêng của từng repo sau đó, nên tôi tin là an toàn — nhưng nếu bạn có repo nào đang dựa vào hook đặt trong `.git/hooks/`, kiểm lại một lượt cho chắc. Gỡ bằng `git config --global --unset core.hooksPath`.
2. Actions trên GitHub vẫn đang bị chặn thanh toán. Không còn chặn việc gì, nhưng nếu ngày nào muốn CI đám mây trở lại thì phải sửa billing trước, rồi đổi `on:` trong `.github/workflows/ci.yml`.
3. Cổng hiện chưa kiểm `tsc` và `oxlint` của `web/`. Chưa thêm vì `web/` mới chỉ có scaffold, thêm lúc này chỉ tốn giây mà chưa bắt được gì. Đề xuất thêm ở task 2.1 khi bắt đầu viết mã thật.

## Người kiểm: tự kiểm  Ngày: 2026-09-24  Kết luận: **Xong** — mọi mục Definition of Done đạt, Cổng B duyệt
