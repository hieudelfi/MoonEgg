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

1. **Mở** `prompts/<phase>/<task-id>.md`. Đọc mục tài liệu được tham chiếu. Kiểm tra phụ thuộc đã Xong trong `records/TRACKING.md`. Phân loại Type / Level / Repro theo mục 7.1. Level `L3` → dừng, viết báo cáo, mở task riêng, không code.
2. **Cắt nhánh** `feature|fix|chore/<task-id>-<slug>` từ `main`. Không làm task trên `main`.
3. **CỔNG A** (mục 7.3). Viết `docs/tasks/<task-id>/Plan.md`, và `Flow.md` nếu không thuộc diện bỏ ở mục 7.2. Đọc lại nguội 4 câu. Đẩy lên yawasa. Báo link. **DỪNG, chờ duyệt.** Chưa duyệt thì chưa chạm vào mã, chưa tải tệp dữ liệu nào.
4. **Tạo bản ghi** `records/<task-id>.md` từ `records/TEMPLATE.md`; ghi ngày bắt đầu, nhánh, link Plan và Flow. Đổi trạng thái trong `records/TRACKING.md` thành "Đang làm".
5. **Làm theo checklist**; sau MỖI bước ghi một dòng "kết quả: <cái gì được tạo, ở đâu>" vào bản ghi. Không gộp nhiều bước thành một dòng. Kế hoạch đổi giữa chừng → sửa `Plan.md`, ghi vào Decisions log, đẩy lại `--update`, nói rõ chỗ đổi; không lặng lẽ đi hướng khác.
6. **Kiểm tra**: chạy test đối chiếu (ID trong prompt). Ghi bảng Test | Cách chạy | Input | Output thật | Đạt? với số thật, không ghi "OK".
7. **Xác minh output trước khi đóng** (mục 3 dưới). Không đạt → ghi lý do, sửa, chạy lại; không đóng task.
8. **Tài liệu**: nếu task thay đổi một quyết định, sửa đúng mục trong `docs/` và ghi "đã cập nhật docs/xx §y" vào bản ghi.
9. **CỔNG B** (mục 7.4). Viết `docs/tasks/<task-id>/Result.md`, đẩy lên yawasa. Dựng `docs/Delivery/<ngày>_<task-id>/`, quét bằng chứng tìm khoá và dữ liệu người thật. Trình bày câu lệnh commit dự định. Báo link. **DỪNG, chờ nghiệm thu.**
10. Được duyệt mới commit, gộp nhánh vào `main` bằng `gate.sh merge`, đẩy Delivery, cập nhật `records/TRACKING.md` (trạng thái, thực tế nđ, kết quả test, người kiểm, ngày). Chỉ khi 1–9 xong mới báo "Xong". Nếu chỉ có một người, ghi "tự kiểm" và ngày.

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
- Nhánh: chỉ `feature/`, `fix/`, `chore/` + `<task-id>-<slug>`, cắt từ `main`. Không có tiền tố khác.
- Commit: `<tag>(<task-id>): <việc>` với tag đúng ba giá trị: **`feature`** (thêm năng lực, gồm cả hạ tầng, pipeline, dữ liệu mới), **`bug`** (sửa lỗi), **`docs`** (tài liệu, luật, quy trình). Ví dụ `feature(P.1): add license scan job`. Một task nhiều commit được, mỗi commit build được.
- Bộ tag commit khác bộ tiền tố nhánh, cố ý. Ánh xạ: tag `bug` nằm trên nhánh `fix/`; tag `feature` nằm trên `feature/` nếu là năng lực người học thấy, trên `chore/` nếu là hạ tầng hay công cụ.
- Commit chỉ mang tên tác giả là chủ máy. Không `Co-Authored-By`, không dòng "Generated with", không ghi công công cụ ở commit, PR hay CHANGELOG.
- Không emoji ở bất cứ đâu: mã, commit, PR, tài liệu, drop.

## 6. Khi không chắc

Ghi câu hỏi vào mục "Câu hỏi mở" của bản ghi task và chọn phương án ít rủi ro nhất có ghi lý do; không dừng chờ trừ khi task có phụ thuộc chưa xong hoặc cần quyết định ngân sách/pháp lý.

## 7. Quy trình hai cổng — Plan, Flow, Result

Theo chuẩn chung của nhóm (Product Issue Workflow). Ba tệp cho mỗi task, cùng một thư mục:
`docs/tasks/<task-id>/Plan.md`, `Flow.md`, `Result.md`. Template ở `docs/tasks/_TEMPLATE_*.md`.

| Tệp | Trả lời câu gì | Cho ai | Viết lúc nào |
| --- | --- | --- | --- |
| `Plan.md` | Làm thế nào | người review kỹ thuật | Cổng A, trước khi chạm vào bất cứ thứ gì |
| `Flow.md` | Người học thấy gì đổi | người review sản phẩm, người test | Cổng A, cùng lượt với Plan |
| `Result.md` | Đã ra cái gì | người đọc hub | ngay khi test đạt, trước cổng commit |
| `records/<task-id>.md` | Từng bước chạy ra số gì | người đang làm | trong lúc làm |

Bản ghi giữ số thô; ba tệp kia giữ phần đọc hiểu được, mỗi tệp gọn một màn hình.
**Ba nguyên tắc cứng:** (1) chưa qua Cổng A thì không chạm vào mã hay dữ liệu; chưa qua Cổng B thì
không commit, không cập nhật TRACKING; (2) thứ người review duyệt phải là tệp trên đĩa, không phải
đoạn chat; (3) Definition of Done viết trước khi làm, không sửa cho vừa cái đã làm.

**7.1 Phân loại — ghi vào đầu Plan.md**

- **Type**: `INFRA` (P.1–P.3) · `DATA` (P.7–P.10, 1.2–1.7, 5.1–5.4) · `FEATURE` (màn hình, lõi học)
  · `ISSUE` (sửa lỗi) · `REFACTOR` (không đổi hành vi).
- **Level theo rủi ro, không theo số tệp**: `L1` một chỗ bề mặt (một màu, một chữ, một khoảng cách)
  · `L2` có nhánh logic · `L3` chạm hạ tầng dùng chung, đổi hợp đồng dữ liệu hoặc trải nhiều luồng.
  **L3 là báo cáo, không code** — mở task riêng.
- **L1 tự lên L2** nếu dính một trong bốn điều: chạm quá 1 tệp, thêm/bớt một nhánh `if`/`switch`,
  đổi dữ liệu lưu lại, hoặc đổi hành vi ở màn khác.
- **Repro (chỉ ISSUE)**: `Confirmed` tự tái hiện được · `Trace-confirmed` có stack trace và mã
  chứng minh, phải kèm cách ép lỗi ở §7 của Plan · `Unconfirmed` thì **dừng**, hỏi tối đa 3 câu,
  không đoán.

**7.2 Khi nào được bỏ Flow.md**

Chỉ với `INFRA`, `DATA`, và `REFACTOR` không đổi hành vi. Vài thay đổi hành vi cố ý thì gộp vào
`Plan.md` §5 theo cột Situation | Before | After. **Không bao giờ bỏ Flow.md cho FEATURE, hay cho
ISSUE có đổi màn hình** — nửa người học nhìn thấy chính là phần cần review nhất ở đó.

**7.3 Cổng A**

1. Viết `Plan.md` (và `Flow.md` nếu không thuộc diện bỏ). Bằng chứng về mã và dữ liệu phải lấy từ
   lệnh grep chạy hôm nay kèm `File.ext:dòng`, không lấy từ trí nhớ.
2. Đọc lại nguội, 4 câu: bản này nói mục tiêu hay chỉ liệt kê việc? người không ngồi cùng có hiểu
   không? giả định đã ghi ra hay đang giấu? điều nhỏ nhất có thể hỏng mà chưa nhắc là gì?
   **Khi `Reviewer: self`: viết xong không đọc lại ngay.** Chờ ít nhất 15 phút hoặc làm việc khác
   rồi mới đọc. Đọc ngay thì chỉ đang nhớ lại lý do mình vừa viết, không phải đang review.
3. Đẩy `Plan.md` lên yawasa. Có `Flow.md` thì đẩy thành một drop riêng.
4. Báo: tóm tắt, đường dẫn tệp, link hub, câu hỏi mở. **DỪNG.** Chờ người review.

**Vòng sửa khi chưa được duyệt:** sửa cho `Plan.md` và `Flow.md` khớp nhau, không để tệp này nói A
tệp kia nói B. Ghi dòng quyết định kèm ngày vào khối "Decisions log" ở đầu `Plan.md`, không xoá
dòng cũ. Đẩy lại kèm `--update` để giữ nguyên link. Vẫn chưa được code.

**7.4 Cổng B**

1. Test đạt → viết `Result.md`, đẩy lên hub ngay (trong đó không có tệp bằng chứng nên không phải
   quét gì).
2. Dựng `docs/Delivery/<YYYY-MM-DD>_<task-id>/` cho người kiểm: bằng chứng, log, ảnh, mẫu audio.
   **Quét `evidence/` tìm token, khoá, số máy, dữ liệu người thật TRƯỚC khi đẩy** — bản delivery là
   HTML đóng băng, đẩy rồi không rút lại được.
3. Trình bày câu lệnh commit dự định và ghi chú cho bản ghi. **DỪNG.** Chờ duyệt.
4. Được duyệt mới đẩy Delivery, commit, cập nhật `records/<task-id>.md` và `records/TRACKING.md`.
5. **Chạy cổng, gộp vào `main` tại máy, xoá nhánh** (mục 7.8). Nhánh chưa gộp thì task chưa đóng; không sang task kế tiếp khi nhánh còn mở.

**7.5 Hub của dự án**

- Trang dự án: https://hub.yawasa.com/app/projects/moonegg
- Mọi lần đẩy kèm **ba** cờ, không thiếu cờ nào:
  `--project "moonegg" --no-share-project --visibility private`
  - `--project` nối bản đẩy vào trang dự án. Thiếu nó thì bản đẩy rơi vào thư mục nháp
    `Unpublished` chỉ mình thấy, trang dự án trống.
  - `--no-share-project` **bắt buộc**. Mặc định của `--project` là chia sẻ bản đẩy cho mọi thành
    viên của project (hub tự gắn audience của project vào drop). Không truyền cờ này thì script
    không gửi trường `share_with_project` và hub áp mặc định chia sẻ của nó.
  - `--visibility private` chốt lại quyền xem. Hub tự lật visibility sang `shared` khi có bất kỳ
    nhóm hay audience nào được gắn, nên phải nói rõ.
- **Mặc định của dự án này là riêng tư, chỉ chủ sở hữu.** Muốn ai đó xem thì chia sẻ tay trên giao
  diện hub, từng bản một, có chủ đích. Không bao giờ để mặc định của công cụ quyết định việc này.
- API của hub **không có endpoint đọc trạng thái chia sẻ**. Chỉ `/api/upload`, `/api/drop/<slug>/md`
  và `/api/drop/<slug>/prompt`. Nghĩa là không tự kiểm được bằng lệnh: sau khi đẩy phải **mở giao
  diện hub nhìn bằng mắt**, cả vị trí project lẫn quyền xem.
- **Không dùng `--folder` thay cho `--project`**: `--folder` là thư mục trong thư viện cá nhân.
  Đẩy nhầm cờ thì hub vẫn báo thành công nhưng trang dự án không có gì.
- Cờ `--project` có từ bản exp-publish 19/09/2026. Script báo `unknown option` → chạy skill
  `update-yawasa`.
- Slug: `moonegg-<task-id>-plan` · `-flow` · `-result`, task-id bỏ dấu chấm (`P.1` → `p1`,
  `1.13` → `1-13`).
- Tag: luôn có `moonegg`, cộng `plan`/`flow`/`result`, cộng phase và task-id.

```bash
bash ~/.claude/skills/exp-publish/scripts/exp-publish.sh \
  docs/tasks/<task-id>/Plan.md \
  --slug "moonegg-<task-id>-plan" \
  --title "MoonEgg <task-id> - <ten task> - plan" \
  --tags "moonegg,plan,<phase>,<task-id>" \
  --project "moonegg" --no-share-project --visibility private
```

Flow và Result đổi `plan` thành `flow` / `result` ở cả ba chỗ. Sửa một drop đã đẩy: thêm `--update`
để giữ nguyên link; không có cờ đó hub tạo slug mới `-2` và link đã đưa cho người review trỏ vào
bản cũ.

`--title` chỉ dùng ASCII và gạch ngang thường; dấu tiếng Việt và gạch dài làm hỏng mã hoá khi đẩy
từ Windows.

Đẩy xong phải **mở trang dự án kiểm bằng mắt**: API của hub không cho đọc bản đẩy đang nằm ở
project nào, nên "upload thành công" chưa chứng minh nó về đúng chỗ.

**7.8 Vòng làm việc với git — một task, một nhánh, cổng chạy ở máy**

Cổng kiểm tra chạy **trên máy này**, không chờ GitHub. Đầy đủ mất khoảng 5 giây, thay vì vài phút
đợi runner. GitHub chỉ còn là nơi chứa mã.

| Lúc nào | Việc |
| --- | --- |
| Trước khi bắt đầu | `git switch main && git pull`, cắt nhánh `feature/`, `fix/` hoặc `chore/` + `<task-id>-<slug>` |
| Mỗi commit | Hook `pre-commit` tự chạy cổng mức `quick`. Hỏng thì commit bị từ chối |
| Mỗi push | Hook `pre-push` tự chạy cổng mức `full` |
| Sau khi Cổng B được duyệt | `gate.sh merge <nhánh>`: pull, gộp, chạy cổng, hỏng thì tự gỡ merge ra, đạt thì đẩy lên |

```bash
# bắt đầu task
git switch main && git pull && git switch -c chore/<task-id>-<slug>

# chạy cổng bằng tay bất cứ lúc nào
bash tools/checks/gate.sh quick     # ~2 giây
bash tools/checks/gate.sh full      # ~5 giây

# kết thúc task, sau khi Cổng B được duyệt
bash ~/.config/devgate/gate.sh merge chore/<task-id>-<slug>
git branch -d chore/<task-id>-<slug> && git push origin --delete chore/<task-id>-<slug>
```

**Luật**

- **Không mở pull request.** Gộp ngay tại máy sau khi cổng đạt, rồi đẩy `main` lên. Người review
  đọc Plan và Result trên hub, không đọc diff trên GitHub.
- Cổng đạt mới gộp. `gate.sh merge` tự lo: hỏng thì nó `reset --hard` về trước khi gộp, `main` trở
  lại nguyên trạng và nhánh còn nguyên. Không bao giờ gộp tay khi cổng đang đỏ.
- Gộp bằng `--no-ff`, giữ lại từng commit: bản ghi task trỏ tới chúng làm bằng chứng.
- Xoá nhánh ngay khi gộp xong, cả ở máy lẫn trên remote.
- Một task chưa gộp thì chưa đóng, và chưa mở task kế tiếp.
- `.github/workflows/ci.yml` giữ lại nhưng chỉ chạy khi bấm tay (`workflow_dispatch`). Hai lý do:
  Actions của tài khoản đang bị chặn thanh toán, và cổng ở máy nhanh hơn. Ngày nào cần CI đám mây
  trở lại thì đổi `on:` là đủ.

**Cổng chung của máy này**

`~/.config/devgate/` là cổng dùng chung cho mọi repo trên máy, không riêng MoonEgg.

- `git config --global core.hooksPath` trỏ vào `~/.config/devgate/hooks`, nên **mọi repo** đều đi
  qua nó. Repo nào không có tệp cổng riêng thì nó bỏ qua im lặng, không cản trở gì.
- Repo tham gia bằng cách có `.devgate.sh` ở gốc, hoặc `tools/checks/gate.sh`. MoonEgg dùng cách
  thứ hai. Tệp đó nhận `quick` hoặc `full` làm tham số và trả mã khác 0 khi hỏng.
- Hook riêng trong `.git/hooks/` của từng repo vẫn được gọi sau cổng, nên đặt hooksPath toàn cục
  không nuốt mất hook sẵn có.
- `bash ~/.config/devgate/gate.sh doctor` in ra cấu hình đang áp dụng.
- Bỏ cổng cho một lần commit: `git commit --no-verify`. Dùng khi thật cần, và ghi lý do vào bản ghi
  task — bỏ qua im lặng là tự xoá cổng duy nhất còn lại.

**7.6 Ngôn ngữ**

`Plan.md`, `Flow.md`, `Result.md` viết tiếng Anh mức B1/B2: câu ngắn dưới 20 từ, từ thông dụng, câu
chủ động, mỗi câu một ý, viết tắt thì giải nghĩa lần đầu. Sơ đồ mang nội dung chính, chữ dưới sơ đồ
chỉ một hai dòng. `docs/01..09`, `records/` và trao đổi trong phiên giữ tiếng Việt. Tên màn hình và
nhãn nút ghi đúng như người học thấy, in đậm; không có tên lớp hay tên hàm trong `Flow.md` và
`Result.md`.

**7.7 Khi nào bỏ bớt**

- Task `L1` đúng nghĩa (một chỗ bề mặt, không chạm logic): bỏ Cổng A, vẫn viết `Result.md` nếu một
  phiên gom từ 2 sửa trở lên.
- Hỏi đáp, đọc mã, dò lỗi mà không tạo ra gì: không tệp nào cả.
- Không chắc thì làm đủ hai cổng.
