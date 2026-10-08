# task-lead — Kỹ năng toàn cục chạy một task với ba trợ thủ

Bắt đầu: 2026-10-08 (Plan và Cổng A duyệt cùng ngày)  Kết thúc: 2026-10-08  Công thực tế: chưa đo (ước: không có, task phát sinh từ Analysis)
Token: scout 1 (general-purpose thay thế): sonnet, 71.004 · scout 2 (evidence-scout): sonnet, 31.712 · reviewer Plan P.4: opus, 53.532 · reviewer test 5 lần 1: opus, 56.029 · reviewer test 5 lần 2: opus, 57.327 (tổng: 269.604; chưa tính phiên dẫn, công cụ không báo)
Type: INFRA  Level: L2  Repro (ISSUE): không áp dụng
Người kiểm: tự kiểm  Nhánh: `chore/task-lead-skill` (cắt từ `main` tại `852d94b`)
Plan: https://hub.yawasa.com/app/p/moonegg-task-lead-plan  Flow: bỏ — Type INFRA  Result: https://hub.yawasa.com/app/p/moonegg-task-lead-result
Delivery: `docs/Delivery/2026-10-08_task-lead/` · https://hub.yawasa.com/app/p/moonegg-task-lead-delivery
Tham chiếu: Analysis https://hub.yawasa.com/app/p/moonegg-an-agent-network (follow-up 1, 2, 5) · CLAUDE.md §2, §7
Phụ thuộc: Analysis AgentNetwork (Accepted 2026-10-08)

## Checklist
- [x] B1 Repo riêng tư `hieudelfi/claude-local` + script cài — kết quả: tạo bằng `gh repo create --private`, `gh repo view` in `PRIVATE https://github.com/hieudelfi/claude-local`. Nằm ở `D:\Projects\claude-local`, commit đầu `579d46d`. `install.sh` chép skill và agent vào `~/.claude`, rồi in `git status` của clone `yawasa-skills`.
- [x] B2 `skills/task-lead/SKILL.md` — kết quả: 7 mục: luật nhường repo, bảng ai được làm gì, vị trí ba trợ thủ, ba mẫu brief (scout, builder, reviewer) đủ 5 phần, dòng token, các trường hợp từ chối, checklist của lead. Mô tả ghi rõ chỉ gọi bằng tên, không theo từ khoá.
- [x] B3 `agents/gate-reviewer.md` (Opus, chỉ đọc) — kết quả: `tools: Read, Grep, Glob`, `model: opus`. Bắt buộc 4 câu đọc nguội mỗi câu một dòng kèm `strong|weak`, bảng lỗi theo `File.ext:line`, và mục "LOOKED FOR, FOUND NONE" bắt buộc khi bảng lỗi trống.
- [x] B4 `agents/evidence-scout.md` (Sonnet, chỉ đọc) — kết quả: `tools: Read, Grep, Glob, Bash`, `model: sonnet`; Bash giới hạn bằng luật trong tệp ở các lệnh đọc. Đầu ra là bảng sự kiện và danh sách "Could not find".
- [x] B5 Cài vào `~/.claude`, kiểm clone `yawasa-skills` vẫn sạch — kết quả: `bash install.sh` chép 1 skill + 2 agent; `git status --short` trong clone in đúng một dòng `?? task-lead/`, không có tệp tracked nào đổi. Trùng tên với agent của 4 repo khác: 0 (`ls D:/Projects/*/.claude/agents | grep -cE "gate-reviewer|evidence-scout"` = 0). Gọi `Skill task-lead` ngay trong phiên này: `Unknown skill` — kỹ năng chỉ nạp khi mở phiên mới, test 1 và 2 chờ phiên sau.
- [x] B6 `records/TEMPLATE.md` thêm dòng Token; `CLAUDE.md` §2 bước 1 thêm một câu — kết quả: `git diff --stat`: `CLAUDE.md | 2 +-`, `records/TEMPLATE.md | 1 +`. Commit `feature(task-lead): add token line to the record template, name the skill in the task cycle`.
- [x] B7 Chạy thử trên P.4 tới Cổng A: scout, Plan, reviewer — kết quả: (1) Scout lần 1 chạy qua `general-purpose` + nội dung `evidence-scout.md` vì agent mới chưa nạp: 10 câu hỏi, trả lời 8, để trống 2 và ghi rõ ở "Could not find"; số dòng `docs/01` đếm từ cửa sổ `sed`, tự khai là chưa xác nhận, và sau đó đúng là lệch 1. Scout lần 2 chạy bằng agent `evidence-scout` thật (đã nạp giữa phiên): trả đủ, kể cả việc `import kokoro` hỏng khi thiếu `num2words`. (2) Lead viết `docs/tasks/P.4/Plan.md` từ hai bảng. (3) `gate-reviewer` (Opus) đọc nguội: 4 câu trả lời 1 strong / 3 weak, **15 lỗi** có `File:dòng`, mục "looked for, found none" 8 dòng. Lỗi nặng thật: ba số dòng lệch 1; Plan tự mâu thuẫn (`VOICES` đổi nhưng test 7 đòi tên tệp P.3 giữ nguyên); `mismatch.csv` bị `check_textgrid.py` ghi đè và không được commit; người chấm nghe WAV thô nên giọng to hơn thắng điểm "rõ ràng"; tên người chấm lọt vào Delivery; bảng điểm thiếu dòng không có luật; 10 dòng `docs/08` chỉ có 9 headword. Lead sửa cả 15, ghi Decisions log 2 và 3 của Plan P.4. Commit `c39988a`.
- [x] B8 Test 5: reviewer bắt được giả định giấu cố ý — kết quả: bản biến thể giấu việc 3/5 tệp giọng chưa có trên máy và ghi "Runs offline". **Lần 1: không đạt** — 16 lỗi khác (có 5 lỗi mới áp dụng được cho Plan thật) nhưng không nêu giả định bị giấu. Sửa `gate-reviewer.md`: thêm bước 3 "kiểm kê tài nguyên Plan cần rồi kiểm từng thứ" và bảng RESOURCES; cài lại; commit `4e548f2` ở claude-local. **Lần 2: đạt** — câu 4 nêu đúng "af_bella.pt, af_sarah.pt, am_adam.pt không có trong cache, dòng 96 nói offline", lỗi số 1 là chính nó; 18 lỗi. Agent lần 2 tự ghi mục RESOURCES "không có trong định nghĩa của tôi", tức định nghĩa sửa chưa nạp lại giữa phiên; bước đó đi qua brief. Xác nhận định nghĩa mới có tác dụng: chờ phiên mới.
- [x] B9 Cổng B: Result.md + Delivery + quét bằng chứng — kết quả: `docs/tasks/task-lead/Result.md` viết và đẩy hub. `docs/Delivery/2026-10-08_task-lead/` có `index.md`, `README.md`, 9 tệp bằng chứng; các báo cáo agent chép từ phiên vì tệp nhật ký agent rỗng (0 byte). Quét: 0 phát hiện. Cổng B duyệt 2026-10-08; Delivery đã đẩy hub, riêng tư; nhánh gộp vào `main` bằng `gate.sh merge`.

## Kiểm tra
| Test | Cách chạy | Input | Output thật | Đạt? |
| --- | --- | --- | --- | --- |
| 1 Kỹ năng nạp bằng tên | Skill tool `task-lead P.4` | — | lần 1 `Unknown skill`; sau khi harness liệt kê kỹ năng mới: `Launching skill: task-lead`, nội dung nạp đủ. Agent `evidence-scout`: lần 1 `not found`, sau đó gọi được | Đạt (nạp giữa phiên); phiên mới chưa thử |
| 2 Từ khoá không kích hoạt | gõ "feature: add X" ở phiên mới | — | chưa chạy | chưa đo |
| 3 Scout chỉ trả sự kiện | brief P.4 | 10 + 5 câu hỏi | 100% dòng có `File:dòng` hoặc lệnh; 2 câu để trống có ghi lý do; 3 số dòng tự khai "chưa xác nhận" và đúng là lệch 1 | Đạt |
| 4 Reviewer trả lời 4 câu | brief với Plan P.4 | Plan 209 dòng | 4 dòng, mỗi dòng `strong`/`weak` kèm lý do; bảng 15 lỗi; mục looked-for 8 dòng | Đạt |
| 5 Reviewer không gật đầu | bản biến thể giấu 1 giả định | — | lần 1 không nêu (16 lỗi khác); sửa định nghĩa; lần 2 nêu đúng ở câu 4 và lỗi số 1 | Đạt sau 1 lần sửa |
| 6 Trợ thủ không đẩy hub, không commit | đọc 3 brief trong SKILL.md | — | `grep -c "exp-publish\|git commit"` trong 3 brief = 0; builder brief ghi "Do not commit" | Đạt |
| 7 Clone sống sót | `git status --short` trong `~/.claude/skills` | — | đúng một dòng `?? task-lead/`, không tệp tracked nào đổi | Đạt |
| 8 Không trùng tên | `ls D:/Projects/*/.claude/agents` | 22 tệp ở 4 repo | 0 tệp tên `gate-reviewer.md` hay `evidence-scout.md` | Đạt |
| 9 Dòng token | `records/task-lead.md` dòng 4 | 5 lượt trợ thủ | 5 số thật từ công cụ, tổng 269.604; phiên dẫn ghi "công cụ không báo" | Đạt |
| 10 Cổng xanh | `bash tools/checks/gate.sh full` | — | 4 mục Đạt, exit 0 | Đạt |

## Xác minh output trước khi đóng (CLAUDE.md §3)
- [x] `bash tools/checks/gate.sh full` sạch: 2026-10-08, 4 mục Đạt, nguyên văn ở `docs/Delivery/2026-10-08_task-lead/evidence/test10-gate-full.txt`

## Bằng chứng
- Commit/PR: không mở PR. MoonEgg: `0ba70b0` plan, `37c956e` template + CLAUDE.md, `c39988a` Plan P.4, cộng commit bản ghi. claude-local: `579d46d`, `4e548f2`.
- File đầu ra: `D:\Projects\claude-local/{skills/task-lead/SKILL.md, agents/gate-reviewer.md, agents/evidence-scout.md, install.sh, README.md}`; bản chép ở `~/.claude/skills/task-lead/` và `~/.claude/agents/`; `docs/tasks/P.4/Plan.md`.
- Ảnh/số đo: `docs/Delivery/2026-10-08_task-lead/evidence/`, 9 tệp.
- Delivery đã quét khoá/token/dữ liệu người thật: 2026-10-08, 0 phát hiện.

## Giải thích
Bốn quyết định của Cổng A nằm trong Decisions log của `docs/tasks/task-lead/Plan.md`.

Quyết định trong lúc làm:
- 2026-10-08 — **Scout lần 1 chạy bằng agent thay thế.** `evidence-scout` chưa được nạp khi gọi lần đầu (`Agent type not found`), nên chạy `general-purpose` (sonnet) với nguyên văn định nghĩa dán vào brief. Khi harness nạp agent mới giữa phiên, scout lần 2 chạy bằng agent thật. Cả hai đều ghi trong bằng chứng.
- 2026-10-08 — **Plan P.4 nằm trên nhánh task-lead**, theo quyết định 3 của Cổng A. Reviewer coi đó là lỗi (CLAUDE.md §7.8); giữ nguyên vì chủ dự án đã duyệt, và ghi rõ ở đầu Plan P.4.
- 2026-10-08 — **Sửa định nghĩa reviewer ngay trong task** sau khi test 5 lần 1 không đạt. Thêm bước kiểm kê tài nguyên. Đây là sửa deliverable của chính task này, không phải đổi kế hoạch, nên không cần vòng Cổng A mới.
- 2026-10-08 — **Tệp nhật ký của agent rỗng (0 byte)** ở thư mục `tasks/`, nên bằng chứng là bản chép từ phiên, có ghi rõ chỗ nào nguyên văn chỗ nào tóm tắt.
- 2026-10-08 — **Ba lần review Opus tốn 167 nghìn token cho một Plan 209 dòng.** Đắt hơn ước "2 đến 3 lần một phiên" trong Analysis; số này là dữ liệu đầu tiên cho follow-up 5 của Analysis.

## Câu hỏi mở
- Chưa có.

## Người kiểm: tự kiểm  Ngày: 2026-10-08  Kết luận: **Xong** — 9/10 phép thử Đạt, test 2 chưa đo (cần phiên mới); Cổng B duyệt. Việc còn nợ ở phiên mới: test 2, và chạy lại test 5 không nhắc bước kiểm kê trong brief.
