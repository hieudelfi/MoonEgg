# P.1 — Repo, CI, quét giấy phép

**Tham chiếu:** Kế hoạch §3P.1 P.1 · Kiến trúc §2 · Yêu cầu §13.2 · Test TC-CP-01/02

## Mục tiêu
Có repo với cấu trúc thư mục của kit, CI chạy được test rỗng cho Python/TS/Dart và chặn giấy phép ngoài allowlist.

## Cách làm
1. Khởi tạo git tại thư mục kit này (đã có sẵn cấu trúc). `git init`, commit đầu `P.1: init from kit`.
2. Tạo `web/` bằng Vite React TS (npm create vite), `mobile/` bằng `flutter create` (nếu Flutter đã cài; chưa cài thì tạo placeholder và ghi Câu hỏi mở).
3. GitHub Actions `.github/workflows/ci.yml`: job python (pytest tools/checks), job web (npm test — Vitest rỗng), job mobile (flutter test — bỏ qua nếu chưa có), job license: `npx license-checker --summary` + so với tools/checks/license-allowlist.txt; fail nếu có GPL/AGPL/SSPL/UNKNOWN.
4. Bảo vệ nhánh main (nếu dùng GitHub): yêu cầu CI xanh.

## Checklist (chép vào records/P.1.md, tick từng dòng kèm 'kết quả:')
- [ ] Cấu trúc thư mục đúng README
- [ ] CI chạy 4 job, xanh
- [ ] license job fail khi thêm thử một gói GPL rồi gỡ
- [ ] Nhánh main bảo vệ hoặc ghi lý do chưa

## Kiểm tra (test đối chiếu)
- TC-CP-01: npx license-checker --json → 0 gói ngoài allowlist
- TC-CP-02: mọi gói trong web/package.json ∈ tools/checks/sdk-allowlist.md

## Xác minh output trước khi đóng
- `python tools/checks/verify_pack.py content/lexicon/lexicon_raw_test.csv` chạy được trong CI
- Chạy `CLAUDE.md` §3 cho loại đầu ra; chưa qua → không đóng.

## Bằng chứng cần nộp
- Link repo/commit
- Ảnh CI xanh
- Output license-checker
