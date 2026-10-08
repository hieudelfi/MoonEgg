# task-lead — Kỹ năng toàn cục chạy một task với ba trợ thủ

Bắt đầu: 2026-10-08 (Plan và Cổng A duyệt cùng ngày)  Kết thúc: <ngày>  Công thực tế: chưa đo (ước: không có, task phát sinh từ Analysis)
Token: <trợ thủ: model, số> (tổng: <n>)
Type: INFRA  Level: L2  Repro (ISSUE): không áp dụng
Người kiểm: tự kiểm  Nhánh: `chore/task-lead-skill` (cắt từ `main` tại `852d94b`)
Plan: https://hub.yawasa.com/app/p/moonegg-task-lead-plan  Flow: bỏ — Type INFRA  Result: <link hub>
Delivery: `docs/Delivery/<ngày>_task-lead/`
Tham chiếu: Analysis https://hub.yawasa.com/app/p/moonegg-an-agent-network (follow-up 1, 2, 5) · CLAUDE.md §2, §7
Phụ thuộc: Analysis AgentNetwork (Accepted 2026-10-08)

## Checklist
- [ ] B1 Repo riêng tư `hieudelfi/claude-local` + script cài — kết quả:
- [ ] B2 `skills/task-lead/SKILL.md` — kết quả:
- [ ] B3 `agents/gate-reviewer.md` (Opus, chỉ đọc) — kết quả:
- [ ] B4 `agents/evidence-scout.md` (Sonnet, chỉ đọc) — kết quả:
- [ ] B5 Cài vào `~/.claude`, kiểm clone `yawasa-skills` vẫn sạch — kết quả:
- [ ] B6 `records/TEMPLATE.md` thêm dòng Token; `CLAUDE.md` §2 bước 1 thêm một câu — kết quả:
- [ ] B7 Chạy thử trên P.4 tới Cổng A: scout, Plan, reviewer — kết quả:
- [ ] B8 Test 5: reviewer bắt được giả định giấu cố ý — kết quả:
- [ ] B9 Cổng B: Result.md + Delivery + quét bằng chứng — kết quả:

## Kiểm tra
| Test | Cách chạy | Input | Output thật | Đạt? |
| --- | --- | --- | --- | --- |

## Xác minh output trước khi đóng (CLAUDE.md §3)
- [ ] `bash tools/checks/gate.sh full` sạch:

## Bằng chứng
- Commit/PR:
- File đầu ra:
- Ảnh/số đo:
- Delivery đã quét khoá/token/dữ liệu người thật:

## Giải thích
Bốn quyết định của Cổng A nằm trong Decisions log của `docs/tasks/task-lead/Plan.md`.

Quyết định trong lúc làm:

## Câu hỏi mở
- Chưa có.

## Người kiểm: tự kiểm  Ngày:   Kết luận: Xong / Làm lại (lý do)
