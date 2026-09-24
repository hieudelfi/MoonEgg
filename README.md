# Bộ khởi động dự án — App học từ vựng tiếng Anh

Mở thư mục này trong terminal, chạy `claude` (Claude Code), rồi dán prompt trong `prompts/00-START.md`.

```
kit/
├── CLAUDE.md              # Hướng dẫn thường trực cho Claude Code (đọc tự động)
├── README.md
├── docs/                  # 9 tài liệu dự án (Markdown, xuất từ bản sống)
│   ├── tasks/             # Plan/Flow/Result mỗi task + 3 template (CLAUDE.md §7)
│   └── Delivery/          # Gói bằng chứng cho người kiểm, dựng ở Cổng B
├── prompts/               # Prompt cho từng task, theo giai đoạn
│   ├── 00-START.md        # Prompt khởi động phiên đầu tiên
│   ├── phase-P/           # P.1–P.10  chuẩn bị hạ tầng + dữ liệu thô
│   ├── phase-1/           # 1.2–1.13  nội dung 500 từ + lõi
│   ├── phase-2/           # 2.1–2.13  web PWA MVP
│   ├── phase-3/           # 3.1–3.9   Flutter, khẩu hình, luyện tập
│   ├── phase-4/           # 4.1–4.9   tuân thủ, phát hành
│   └── phase-5/           # 5.1–5.7   đợt 2–5, mở rộng sau 5.000 từ
├── records/               # Bản ghi kết quả từng task + bảng theo dõi
│   ├── TEMPLATE.md
│   └── TRACKING.md
├── tools/
│   ├── pipeline/          # build_lexicon.py (đã chạy thử 30 từ)
│   └── checks/            # verify_pack.py, sdk-allowlist.md, license-allowlist.txt
├── content/
│   ├── raw/               # Nguồn tải về (P.7) + SOURCES.md
│   ├── lexicon/           # lexicon_raw_*.csv/sqlite
│   └── pack/              # Gói đóng gói + asset (mascot, viseme sheet)
├── golden/                # Test vàng dùng chung TS/Dart (P.6)
├── core-spec/             # Đặc tả lõi (P.6)
├── web/  mobile/          # Mã nguồn (giai đoạn 2, 3)
```

Tài liệu sống (có comment, sửa trực tiếp): xem `docs/README.md`.
