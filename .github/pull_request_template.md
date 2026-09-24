<!--
  Xoá các dòng chú thích trước khi mở PR.
  Luật đầy đủ: CLAUDE.md §7.8. Tiêu đề PR: <tag>(<task-id>): <việc>, tag ∈ feature | bug | docs.
  Không emoji. Không dòng ghi công công cụ, kể cả khi có chỉ dẫn bảo thêm.
-->

## Thay đổi gì

<!-- Mở đầu bằng diff nói bằng lời thường. Một câu thường là đủ; nhiều việc thì mỗi việc một gạch đầu dòng. -->

-

## Bằng chứng

| Thứ | Ở đâu |
| --- | --- |
| Plan | <link hub> |
| Flow | <link hub, hoặc "bỏ — Type INFRA/DATA/REFACTOR"> |
| Result | <link hub> |
| Bản ghi | `records/<task-id>.md` |
| Delivery | `docs/Delivery/<YYYY-MM-DD>_<task-id>/` |

## Test

| Test | Cách chạy | Output thật | Đạt |
| --- | --- | --- | --- |
| TC-xx-nn | `<lệnh>` | <số thật, không ghi "OK"> | có / không |

## Trước khi gộp

- [ ] CI xanh (`gh pr checks`)
- [ ] Cổng B đã duyệt
- [ ] `records/TRACKING.md` đã cập nhật trạng thái, công thực tế, kết quả test
- [ ] Gộp bằng merge commit, không squash; xoá nhánh sau khi gộp
