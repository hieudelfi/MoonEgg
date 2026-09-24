# P.1 — Repo, CI, quét giấy phép

Bắt đầu: 2026-09-24  Kết thúc: <chưa>  Công thực tế: 0.6 nđ (ước: 1.5 nđ)
Type: INFRA  Level: L2  Repro: không áp dụng
Người kiểm: tự kiểm  Nhánh: `chore/p1-repo-ci`
Plan: https://hub.yawasa.com/app/p/moonegg-p1-plan  Flow: bỏ — Type INFRA, chưa có màn hình  Result: <chưa, đang Chặn>
Delivery: `docs/Delivery/2026-09-24_P.1/` — chưa dựng
Tham chiếu: docs/09 §3P.1 P.1 · docs/07 §2 · docs/01 §13.2 · Test TC-CP-01, TC-CP-02
Phụ thuộc: không có, task đầu của giai đoạn P

**Trạng thái: CHẶN** — CI không chạy được vì chặn thanh toán ở cấp tài khoản GitHub, không phải lỗi mã. Xem "Câu hỏi mở".

## Checklist

- [x] B0 Khởi tạo repo — kết quả: đã làm trước quy trình, commit `1736b31`, repo `hieudelfi/MoonEgg` private, nhánh mặc định `main`. Không init lại (Plan, Decisions log 1).
- [x] B1 Sửa verify_pack.py — kết quả: thêm khối ép UTF-8 ở `tools/checks/verify_pack.py:7-11`. Chạy không cần `PYTHONIOENCODING`: `30 bản ghi · 0 lỗi · 2 cảnh báo`, exit 0, không traceback. Commit `9813fbb`.
- [x] B1b Test khói python — kết quả: thêm `tools/checks/test_smoke.py` 3 test (dữ liệu mẫu tồn tại, verify_pack 0 lỗi, không UnicodeEncodeError). Lý do: `pytest` thoát mã 5 khi không tìm thấy test nào, bộ test rỗng sẽ làm CI đỏ. Commit `9813fbb`.
- [x] B2 Dựng web/ + vitest — kết quả: `npm create vite@latest web -- --template react-ts`, thêm `vitest` dev, `package.json` script `test` = `vitest run` (không phải `vitest`, tránh treo watch mode trong CI). `web/src/__tests__/smoke.test.ts` 1 test. `npm test`: 1 test file, 1 test passed, 702 ms, exit 0. Commit `c59bcc1`.
- [x] B3 mobile/ placeholder — kết quả: `mobile/README.md` ghi Flutter chưa cài (`command -v flutter` không thấy), nêu task nào sẽ dựng (P.3, 3.1, 3.2, 3.6). Commit `40874c7`.
- [x] B4 CI 4 job — kết quả: `.github/workflows/ci.yml` với `python` (3.11, `PYTHONIOENCODING=utf-8`, pytest + verify_pack), `web` (`npm ci`, `npm test`), `mobile` (tự bỏ qua khi chưa có `mobile/pubspec.yaml`), `license` (`node tools/checks/check_licenses.mjs`). Cả 4 job được GitHub tạo đúng tên. Commit `9f14e01`.
- [x] B5 vitest vào sdk-allowlist — kết quả: thêm khối "Công cụ dev — không vào bundle" cho 6 gói scaffold sinh ra, không phải 1 như Plan dự tính. Xem "Giải thích". Commit `9f14e01`.
- [x] B6 Ép một lần đỏ — kết quả: **đạt ở mức máy, chưa đạt ở mức CI.** Fixture ngoại tuyến `tools/checks/fixtures/gpl-case/` với gói `fake-gpl-pkg@1.0.0` giấy phép GPL-3.0. Cổng trả `1 gói · 1 lỗi giấy phép`, `LỖI fake-gpl-pkg@1.0.0: GPL-3.0 ngoài allowlist`, exit 1. Đóng thành test tự động `tools/checks/test_licenses.py` nên lần sau không phải làm tay. Link CI đỏ chưa có vì CI không chạy được.
- [x] B7 Bảo vệ nhánh — kết quả: **không bật được.** `gh api repos/hieudelfi/MoonEgg/rulesets` trả `403 Upgrade to GitHub Pro or make this repository public to enable this feature.` Prompt P.1 cho phép ghi lý do thay vì bật. Bù lại bằng luật PR ở `CLAUDE.md` §7.8: CI xanh mới gộp.

## Kiểm tra

| Test | Cách chạy | Input | Output thật | Đạt? |
| --- | --- | --- | --- | --- |
| TC-CP-01 | `node tools/checks/check_licenses.mjs` | `web/` sau `npm install` | `49 gói · 0 lỗi giấy phép · 0 gói thiếu dòng SDK`, exit 0 | Đạt |
| TC-CP-02 | cùng lệnh, phần thứ hai | 10 dependency trực tiếp của `web/package.json` | 0 gói thiếu dòng. Trước khi thêm khối dev: 6 gói thiếu, exit 1 | Đạt |
| Test 3 — cổng có cắn | `node tools/checks/check_licenses.mjs tools/checks/fixtures/gpl-case` | gói GPL-3.0 giả | `1 lỗi giấy phép`, `GPL-3.0 ngoài allowlist`, exit 1 | Đạt ở máy; **chưa có lần đỏ trên CI** |
| Test 4 — checker trên Windows | `python tools/checks/verify_pack.py content/lexicon/lexicon_raw_test.csv` | 30 dòng CSV mẫu | `30 bản ghi · 0 lỗi · 2 cảnh báo`, exit 0, không traceback | Đạt |
| Test 5 — checker trong CI | job `python` | như trên | **chưa chạy được** | Chặn |
| Test 6 — bộ test chạy được | `python -m pytest tools/checks -q` | 2 tệp test | `5 passed in 1.59s`, exit 0 | Đạt |
| Test 6b — web test | `npm test` trong `web/` | 1 tệp test | `Test Files 1 passed (1)`, exit 0 | Đạt |
| DoD — 4 job một lần chạy | `gh run list --branch chore/p1-repo-ci` | commit `40874c7` | 4 job đều `failure` sau 3 giây, 0 bước chạy | **Không đạt** |

## Xác minh output trước khi đóng (CLAUDE.md §3)

- [x] Mã: `pytest tools/checks -q` → 5 passed, exit 0. `npm test` → 1 passed, exit 0.
- [x] Không thêm dependency ngoài `tools/checks/sdk-allowlist.md`: cổng giấy phép trả 0 gói thiếu dòng.
- [ ] CI xanh: **chưa**, xem Câu hỏi mở.
- [x] Không có bản ghi thiếu source/license: `verify_pack.py` 0 lỗi trên dữ liệu mẫu.

## Bằng chứng

- Commit: `9813fbb` verify_pack + test khói · `c59bcc1` web + vitest · `9f14e01` CI + cổng giấy phép · `40874c7` mobile placeholder
- File đầu ra: `.github/workflows/ci.yml`, `tools/checks/check_licenses.mjs`, `tools/checks/test_smoke.py`, `tools/checks/test_licenses.py`, `tools/checks/fixtures/gpl-case/`, `web/`, `mobile/README.md`
- Lần chạy CI: https://github.com/hieudelfi/MoonEgg/actions/runs/35976963632 — 4 job `failure`
- Nguyên văn GitHub trả về (annotation của check-run 107559618956): `The job was not started because recent account payments have failed or your spending limit needs to be increased. Please check the 'Billing & plans' section in your settings`
- Bảo vệ nhánh: `403 Upgrade to GitHub Pro or make this repository public to enable this feature.`
- Delivery đã quét khoá/token/dữ liệu người thật: chưa dựng, task đang Chặn

## Giải thích

**Khác Plan ở ba chỗ, không chỗ nào đổi hướng:**

1. Plan viết "vitest thêm một dòng vào sdk-allowlist". Thực tế scaffold Vite sinh ra 6 gói dev: `vitest`, `@vitejs/plugin-react`, `oxlint`, `@types/node`, `@types/react`, `@types/react-dom`. Thêm cả 6 vào một khối "Công cụ dev — không vào bundle" thay vì một dòng. Quyết định vì TC-CP-02 đòi mọi dependency có dòng, và gộp thành khối rõ hơn là rải 6 dòng lẫn vào bảng gói phát hành.

2. Plan viết "CI chạy bộ test rỗng". `pytest` thoát mã 5 khi không có test nào, nên bộ rỗng sẽ làm CI đỏ. Thay bằng ba test khói thật, kiểm đúng thứ CI cần tin: `verify_pack` chạy được và in được tiếng Việt. Đây cũng chính là test 5 trong Plan, chỉ là đóng thành test tự động thay vì một bước riêng trong workflow.

3. Plan viết test 3 ép đỏ bằng cách cài một gói GPL thật rồi gỡ. Làm bằng fixture ngoại tuyến thay thế: nhanh hơn, không phụ thuộc mạng, và thành test thường trực chứ không phải thao tác tay một lần. Phần còn thiếu là **link một lần chạy CI đỏ**, không làm được khi CI không chạy.

**Lỗi tìm thấy trong lúc làm:** `verify_pack.py:41` in tiếng Việt ra console cp1252 của Windows nên ném `UnicodeEncodeError` và thoát 1 **dù dữ liệu không lỗi**. Vì `CLAUDE.md` §3 bắt chạy script này trước khi đóng mọi task dữ liệu, lỗi này sẽ làm mọi task dữ liệu báo hỏng giả. Đã sửa và có test chặn hồi quy.

Chưa cập nhật tài liệu nào trong `docs/01..09` — task này không đổi quyết định nào.

## Câu hỏi mở

1. **Chặn: GitHub Actions không chạy.** Bốn job đều hỏng sau 3 giây với 0 bước. Nguyên văn GitHub: thanh toán gần đây hỏng, hoặc hạn mức chi tiêu cần nâng. Đây là cấp tài khoản, không phải repo, không phải mã. Ba lối đi:
   - Vào Billing & plans của tài khoản `hieudelfi`, sửa thanh toán hoặc nâng hạn mức. Repo private trên gói free có 2.000 phút Actions mỗi tháng.
   - Để repo public — Actions cho repo public không tính phút. Trái với luật "repo luôn private".
   - Bỏ CI trên GitHub, chạy checks bằng git hook ở máy. Mất cổng tự động, chỉ còn kỷ luật tay.
   Tôi không tự chọn được vì đây là quyết định ngân sách (CLAUDE.md §6).
2. Token `gh` hiện thiếu scope `user` nên tôi không đọc được số phút còn lại. Cần thì chạy `gh auth refresh -h github.com -s user` — bạn tự chạy, tôi không tự nâng quyền token.

## Người kiểm: tự kiểm  Ngày: 2026-09-24  Kết luận: **Chặn** — chờ quyết định về GitHub Actions
