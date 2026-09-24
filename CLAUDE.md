# CLAUDE.md — Hướng dẫn thường trực cho Claude Code

Dự án: **Ứng dụng học từ vựng tiếng Anh** (web React PWA + mobile Flutter, miễn phí, local-first).
Ngôn ngữ làm việc: tiếng Việt cho tài liệu, ghi chép và giao tiếp; tiếng Anh cho mã, tên biến, commit.

## 1. Nguồn sự thật — đọc trước khi làm bất kỳ task nào

| Tài liệu | Dùng khi |
| --- | --- |
| `docs/01-yeu-cau.md` | Mọi task: tra FR-xx, NFR, quyết định đã chốt (§8.3, §14), nguồn dữ liệu (§6), tuân thủ store (§10, §13) |
| `docs/07-kien-truc.md` | Task kỹ thuật: mô hình sự kiện §5.1, FSRS §5.2, dựng phiên §5.3, đồng bộ §5.4, pipeline §5.5, danh sách từ và quiz §5.6, cache/phiên §6, CSDL §7 |
| `docs/08-kiem-thu.md` | Trước khi đóng task: test đối chiếu TC-xx-nn, dữ liệu mock §2, checklist §8 |
| `docs/09-ke-hoach.md` | Chọn task, checklist bước, ước lượng, bằng chứng cần nộp; quy trình một task §2 |
| `docs/06-thiet-ke-ui-ux.md` | Task màn hình: behavior từng màn, quy ước tương tác |
| `docs/02..05` | Rà soát, bằng chứng nguồn, chiến lược động lực, khoa học ghi nhớ — tra khi cần lý do |

Mockup: https://claude.ai/artifact/BJJpsvciECNVUK4VocwWUq (15 màn). Tài liệu gốc (bản sống, có comment): xem `docs/README.md`.

## 2. Quy trình một task — bắt buộc

1. **Mở** `prompts/<phase>/<task-id>.md`. Đọc mục tài liệu được tham chiếu. Kiểm tra phụ thuộc đã Xong trong `records/TRACKING.md`.
2. **CỔNG A — bản kế hoạch (plan drop)**. Viết `records/drops/<task-id>-plan.md` từ `records/drops/TEMPLATE-plan.md`, đọc lại nguội (mục 7.3), đẩy lên yawasa (mục 7). Báo link. **DỪNG, chờ người duyệt.** Chưa duyệt thì chưa viết một dòng mã, chưa tải một tệp dữ liệu nào.
3. **Tạo bản ghi** `records/<task-id>.md` từ `records/TEMPLATE.md` ngay khi bắt đầu; ghi ngày bắt đầu và link plan drop.
4. **Làm theo checklist**; sau MỖI bước ghi một dòng "kết quả: <cái gì được tạo, ở đâu>" vào bản ghi. Không gộp nhiều bước thành một dòng.
5. **Kiểm tra**: chạy test đối chiếu (ID trong prompt). Ghi bảng Test | Cách chạy | Input | Output thật | Đạt? với số thật, không ghi "OK".
6. **Xác minh output trước khi đóng** (mục 3 dưới). Không đạt → ghi lý do, sửa, chạy lại; không đóng task.
7. **Bằng chứng**: link commit, đường dẫn file đầu ra, số đo. Cập nhật `records/TRACKING.md` (trạng thái, thực tế nđ, kết quả test).
8. **Tài liệu**: nếu task thay đổi một quyết định, sửa đúng mục trong `docs/` và ghi "đã cập nhật docs/xx §y" vào bản ghi.
9. **CỔNG B — bản kết quả (outcome drop)**. Viết `records/drops/<task-id>-outcome.md` từ `records/drops/TEMPLATE-outcome.md`, đẩy lên yawasa (mục 7). Báo link. **DỪNG, chờ nghiệm thu.**
10. Chỉ khi 1–9 xong mới báo "Xong". Nếu chỉ có một người, ghi "tự kiểm" và ngày.

## 3. Xác minh output — không đóng gói khi chưa qua

- **Dữ liệu** (CSV/SQLite/JSON): chạy `python tools/checks/verify_pack.py <đường dẫn>`; mọi bản ghi phải có `source` và `license` trong allowlist; số dòng khớp kỳ vọng; không trùng `item_id`; đồng tự khác âm tách dòng.
- **Audio**: duration trong ngưỡng, loudness −16 ±2 LUFS, mỗi từ có đủ 2 giọng; nghe kiểm ngẫu nhiên 5% và ghi lại danh sách đã nghe.
- **Timing/viseme**: mốc tăng đơn điệu, kết ≤ duration, viseme ∈ 0..11; so phoneme với CMUdict, mismatch ≤ 2% và có `mismatch.csv`.
- **Mã**: test vàng 100% (`golden/`), lint sạch, không thêm dependency ngoài `tools/checks/sdk-allowlist.md` khi chưa duyệt.
- **Màn hình**: chụp ảnh so với mockup, chạy TC E2E tương ứng, kiểm offline bằng chế độ máy bay.
- **Đóng gói** (`content/pack/*.sqlite` + manifest): chỉ đóng gói bản ghi `review_status = approved`; manifest có sha256 mọi tệp; `verify_pack.py` 10/10 (TC-CT-01→11).

## 4. Ranh giới — không làm

- Không tải video/audio từ YouTube hay bất kỳ nguồn không có giấy phép mở; nguồn cho phép: NGSL, NAWL, CMUdict, Wiktionary/kaikki, Tatoeba, WordNet, Wikimedia Commons/Lingua Libre, Kokoro/Piper TTS, MFA, tự tạo.
- Không dùng Oxford 3000/5000 (bản quyền OUP).
- Không sinh file audio tốc độ chậm riêng (chậm bằng playbackRate).
- Không thêm SDK analytics/quảng cáo bên thứ ba.
- Không lưu ghi âm giọng người học lên máy chủ.
- Không bịa số liệu vào bản ghi task; thiếu thì ghi "chưa đo".
- Không sửa `golden/*.json` trừ khi task nói rõ và có review.

## 5. Quy ước kỹ thuật

- Python 3.11+, `tools/pipeline/`; pytest trong `tools/checks/`.
- Web: React + TypeScript + Vite, Dexie, ts-fsrs. Mobile: Flutter, drift, port FSRS trong `mobile/core_dart/`.
- `item_id` tự nhiên: `w:<headword>#<n>`, `p:<topic>#<n>`, `s:<ipa>`.
- Sự kiện: ULID, append-only, enum trong `docs/07-kien-truc.md` §5.1.
- Commit: `<task-id>: <việc>`; một task có thể nhiều commit, mỗi commit build được.

## 6. Khi không chắc

Ghi câu hỏi vào mục "Câu hỏi mở" của bản ghi task và chọn phương án ít rủi ro nhất có ghi lý do; không dừng chờ trừ khi task có phụ thuộc chưa xong hoặc cần quyết định ngân sách/pháp lý.

## 7. Đẩy bản kế hoạch và bản kết quả lên yawasa

Mỗi task để lại hai vết công khai trên hub, ngoài bản ghi trong repo. Ba thứ khác nhau, không thay nhau được:

| Thứ | Ở đâu | Cho ai đọc | Viết lúc nào |
| --- | --- | --- | --- |
| `records/<task-id>.md` | repo | người đang làm task | trong lúc làm, từng bước |
| plan drop | hub | người duyệt | trước khi làm bước đầu tiên |
| outcome drop | hub | người duyệt | sau khi test và xác minh đã đạt |

Bản ghi giữ số đo thô và từng dòng "kết quả"; hai drop giữ phần đọc hiểu được, mỗi bản gọn trong một màn hình.

**7.1 Địa chỉ hub của dự án**

- Trang dự án: https://hub.yawasa.com/app/projects/moonegg
- Mọi lần đẩy kèm `--project "moonegg"`. Đây là cờ nối bản đẩy vào **project**; thiếu nó bản đẩy rơi vào thư mục nháp `Unpublished` chỉ mình thấy, và không hiện ở trang dự án
- Đừng dùng `--folder` thay cho `--project`: `--folder` là thư mục trong thư viện cá nhân, khác hẳn project — đẩy nhầm cờ thì hub vẫn báo thành công nhưng trang dự án trống
- Cờ `--project` có từ exp-publish bản 19/09/2026. Nếu script báo `unknown option`, chạy skill `update-yawasa` để kéo bản mới
- Slug: `moonegg-<task-id>-plan` và `moonegg-<task-id>-outcome`, task-id bỏ dấu chấm (`P.1` → `p1`, `1.13` → `1-13`)
- Tag: luôn có `moonegg`, cộng `plan`/`outcome`, cộng phase (`phase-p`, `phase-1`…) và task-id

**7.2 Lệnh đẩy**

```bash
bash ~/.claude/skills/exp-publish/scripts/exp-publish.sh \
  records/drops/<task-id>-plan.md \
  --slug "moonegg-<task-id>-plan" \
  --title "MoonEgg <task-id> - <ten task> - plan" \
  --tags "moonegg,plan,<phase>,<task-id>" \
  --project "moonegg"
```

Outcome đổi `plan` thành `outcome` ở cả ba chỗ. Đẩy xong phải **mở trang dự án kiểm bằng mắt**: API của hub không cho đọc bản đẩy nằm ở project nào, nên "upload thành công" chưa chứng minh nó về đúng chỗ. Sửa một drop đã đẩy: thêm `--update` để giữ nguyên link (hub tự lưu bản cũ vào lịch sử). Không có `--update` thì hub tạo slug mới `-2`, link cũ vẫn trỏ bản cũ — tránh.

`--title` chỉ dùng ASCII và gạch ngang thường; dấu tiếng Việt và gạch dài làm hỏng mã hoá khi đẩy từ Windows.

**7.3 Đọc lại nguội trước khi đẩy plan drop**

Đọc bản kế hoạch như người chưa dự cuộc trò chuyện, trả lời 4 câu:

1. Bản này nói mục tiêu, hay chỉ liệt kê việc?
2. Người không ngồi cùng có hiểu không?
3. Giả định đã ghi ra, hay đang giấu?
4. Điều nhỏ nhất có thể hỏng mà chưa nhắc tới là gì?

Câu nào yếu thì sửa rồi đọc lại. Chỉ đẩy khi qua cả 4.

**7.4 Ngôn ngữ**

Hai drop viết bằng tiếng Anh mức B1/B2 (chuẩn chung của nhóm cho mọi thứ đưa lên hub); `docs/` và `records/` giữ tiếng Việt. Tên màn hình, tên nút, `item_id`, tên tệp giữ nguyên văn.

**7.5 Khi nào bỏ qua**

- Task L1 sửa một chỗ bề mặt (một màu, một chữ, một khoảng cách): bỏ plan drop, vẫn viết outcome drop nếu một phiên gom từ 2 sửa trở lên.
- Hỏi đáp, đọc mã, dò lỗi mà không tạo ra gì: không drop nào cả.
- Không chắc thì làm đủ hai drop.
