# P.3 — Môi trường pipeline

Bắt đầu: 2026-10-08 (Plan và Cổng A duyệt cùng ngày)  Kết thúc: <ngày>  Công thực tế: <nđ> (ước: 1,5)
Type: INFRA  Level: L2  Repro (ISSUE): không áp dụng
Người kiểm: tự kiểm  Nhánh: `chore/p3-pipeline-env` (cắt từ `main` tại `4963232`)
Plan: https://hub.yawasa.com/app/p/moonegg-p3-plan  Flow: bỏ — Type INFRA, không có màn hình  Result: <link hub>
Delivery: `docs/Delivery/<ngày>_P.3/`
Tham chiếu: Kế hoạch §3P.1 P.3 · Kiến trúc §5.5 · Yêu cầu §8.3, §9.3 · ngưỡng của TC-CT-02, TC-CT-04
Phụ thuộc: P.1 (Xong 2026-09-24)

## Checklist
- [x] B1 Hai môi trường và bộ nhớ đệm trên D: (`.venv`, `.mfa`, `.cache`) — kết quả: `.venv` Python 3.12.14 với torch 2.14.1+cpu, kokoro 0.9.4, 1,2 GB, cài 4 phút 41 giây. Miniforge conda 26.7.2 ở `D:\tools\miniforge3`, 621 MB, không vào PATH. `.mfa` có MFA 3.4.2, 2,4 GB; Miniforge cộng MFA cài 3 phút 33 giây. `.cache` 1,9 GB. `.gitignore` thêm 2 dòng. Ổ C: 9,17 GB trước, 9,54 GB sau.
- [x] B2 Liệt kê giấy phép mọi gói đã cài, trước khi dùng — kết quả: `.venv` lúc mới cài 103 gói, 4 gói ngoài allowlist: `phonemizer-fork` và `cmudict` (GPL-3.0-or-later), `espeakng-loader` (không khai, bọc espeak-ng), `num2words` (LGPL). Đã gỡ cả bốn; còn 95 gói, 0 gói GPL/LGPL. `.mfa`: 204 gói conda, 28 gói họ GPL/LGPL không gỡ được. Xem quyết định bên dưới.
- [x] B3 `tts_sample.py`: 5 audio × 2 giọng tồn tại — kết quả: 10 WAV ở `content/pack/audio_test/wav/`, dài 1.225–1.550 ms, kèm 10 tệp `.lab`. Trung bình 0,686 giây mỗi từ lần đầu, 0,625 giây lần hai. Nạp model 38,59 giây lần đầu (có tải), 3,45 giây lần hai.
- [x] B4 `encode_opus.py`: 10 file Opus loudness −16 ±2 LUFS — kết quả: lần đầu dùng `loudnorm` 7/10 tệp trượt (−18,2 đến −20,0). Đổi sang đo + tăng âm + hãm đỉnh: 10/10 nằm trong −16,5 đến −16,0 LUFS, 20,9–24,8 kbps, 3.405–4.831 byte, trung bình 0,364 giây mỗi tệp.
- [x] B5 `align_sample.py`: TextGrid có tier phones — kết quả: 10/10 TextGrid ở `content/pack/audio_test/aligned/`, mỗi tệp hai tier `words` và `phones`. 89,1 giây cho 10 tệp; chạy lại 90,3 giây; 40 tệp 93,2 giây.
- [x] B6 `check_textgrid.py` + test trong `tools/checks/` — kết quả: 4/5 từ khớp CMUdict. `market` lệch ở cả hai giọng: CMUdict `M AA1 R K AH0 T`, MFA `M AA1 R K IH0 T`. `mismatch.csv` có 2 dòng. Mốc thời gian tăng đơn điệu và không vượt độ dài audio ở 10/10 tệp. 7 test mới trong `tools/checks/test_textgrid.py`, cả bộ `12 passed`.
- [x] B7 1 ảnh SD hoặc lý do — kết quả: không cài. Lý do ở `tools/pipeline/ENV.md` mục 7: không có GPU rời, card tích hợp 512 MB. Quyết định 3 của Cổng A.
- [ ] B8 `build_lexicon.py` chạy lại trong venv — kết quả: **chưa chạy, đang chặn.** Script cần gói `cmudict`, mã bọc mang giấy phép GPL-3.0. Chờ quyết định về giấy phép ở mục Câu hỏi mở.
- [x] B9 `ENV.md`, `requirements.txt`, dòng mới trong `sdk-allowlist.md` — kết quả: `tools/pipeline/ENV.md` 7 mục có bảng thời gian và ước cho cả bộ nội dung (khoảng 23 giờ máy); `requirements.txt` ghim 95 gói; `sdk-allowlist.md` thêm khối "Công cụ pipeline nội dung" 8 dòng.
- [ ] B10 Người review nghe 10 file, ghi nhận xét — kết quả:
- [ ] B11 Cổng B: Result.md + Delivery + quét bằng chứng — kết quả:

## Kiểm tra
| Test | Cách chạy | Input | Output thật | Đạt? |
| --- | --- | --- | --- | --- |
| 1 10 bản ghi tồn tại | `.venv/Scripts/python tools/pipeline/env/tts_sample.py` | 5 từ × 2 giọng | 10 WAV 24 kHz; dài 1.400, 1.450, 1.550, 1.275, 1.375 ms (`af_heart`) và 1.425, 1.350, 1.550, 1.225, 1.325 ms (`am_michael`); ngưỡng 300–4.000 | Đạt |
| 2 Nén và đều âm lượng | `python tools/pipeline/env/encode_opus.py` | 10 WAV | 10 Opus; âm lượng −16,3 −16,4 −16,0 −16,3 −16,4 −16,5 −16,5 −16,3 −16,3 −16,5 LUFS; 20,9–24,8 kbps; exit 0 | Đạt |
| 3 Có mốc thời gian | `python tools/pipeline/env/align_sample.py` | 10 WAV + `.lab` | `10 of 10 files aligned in 89.1 s`, MFA 3.4.2 | Đạt |
| 4 Mốc hợp lý | `python tools/pipeline/env/check_textgrid.py` | 10 TextGrid | 0 tệp có `time_not_rising`, 0 tệp có `ends_after_audio` | Đạt |
| 5 Âm khớp CMUdict | cùng lệnh | 5 từ | 4/5 từ khớp; `market` lệch `AH0` thành `IH0`; `mismatch.csv` 2 dòng; exit 1 | Không đạt 5/5 — theo DoD: đã liệt kê và giải thích |
| 6 Trường hợp "wind" | cùng lệnh | `w:wind#1` | Kokoro đọc `/wˈɪnd/`, MFA căn `W IH1 N D`, khớp CMUdict ở cả hai giọng | Đạt |
| 7 `build_lexicon.py` chạy lại | — | — | chưa chạy, chặn vì giấy phép gói `cmudict` | |
| 8 Không rơi vào ổ C | `Get-PSDrive C` trước và sau | — | 9,17 GB trước khi cài, 9,54 GB sau; `Documents\MFA` 2 KB | Đạt |
| 9 Không có audio trong git | `git status --short` | — | không dòng nào là WAV, Opus, `.venv`, `.mfa`, `.cache` | Đạt |
| 10 Cổng vẫn xanh | `bash tools/checks/gate.sh full` | — | 4 mục Đạt, exit 0 | Đạt |
| 11 Nghe kiểm | người review nghe 10 tệp | — | chưa nghe | |
| 12 Giấy phép | `pip-licenses`, và trường `license` trong `conda-meta/*.json` | 95 + 204 gói | `.venv` 0 gói ngoài allowlist; `.mfa` 28 gói họ GPL/LGPL | Chờ quyết định |

## Xác minh output trước khi đóng (CLAUDE.md §3)
- [ ] `bash tools/checks/gate.sh full` sạch:
- [ ] Audio: duration trong ngưỡng, loudness −16 ±2 LUFS, đủ 2 giọng:
- [ ] Timing: mốc tăng đơn điệu, kết ≤ duration, có `mismatch.csv`:

## Bằng chứng
- Commit/PR:
- File đầu ra:
- Ảnh/số đo:
- Delivery đã quét khoá/token/dữ liệu người thật:

## Giải thích
Sáu quyết định của Cổng A nằm trong Decisions log của `docs/tasks/P.3/Plan.md`, không chép lại ở đây.

Quyết định trong lúc làm:
- 2026-10-08 — **Gỡ ba gói GPL/LGPL khỏi `.venv` và chèn module giả, thay vì chỉ "không dùng".**
  Kokoro `import` thẳng `misaki.espeak` ở đầu tệp (`kokoro/pipeline.py:5`), nên chỉ cần cài là mã GPL
  được nạp. `tts_sample.py` đặt hai module giả vào `sys.modules` trước khi nạp Kokoro. Kokoro đã có
  sẵn nhánh xử lý khi phần dự phòng không khởi động được (`pipeline.py:107-112`): từ ngoài từ điển
  bị bỏ qua. Đúng quyết định 4 của Cổng A. Hệ quả: văn bản có chữ số sẽ báo lỗi.
- 2026-10-08 — **Gói `cmudict` trên PyPI là GPL-3.0-or-later.** Chỉ phần mã bọc; dữ liệu CMUdict
  bên trong vẫn là BSD. Đề bài P.3 yêu cầu `pip install cmudict` và `build_lexicon.py:1` nhập nó.
  Đã gỡ, chưa dùng cho việc gì của task. Thú thật một lần gọi: tôi đã `import cmudict` đúng một lần
  để so nó với bản CMUdict của NLTK trước khi gỡ.
- 2026-10-08 — **Không đổi lặng lẽ sang CMUdict của NLTK.** NLTK (Apache-2.0) có sẵn một bản
  CMUdict, nhưng là bản cũ hơn: 123.455 mục so với 126.052. Trên 29 từ của tệp mẫu, 1 từ khác:
  `exhausted` có thêm một cách đọc và thứ tự cách đọc đổi. Đổi nguồn sẽ đổi dữ liệu đã theo dõi,
  nên đó không phải việc của task này.
- 2026-10-08 — **Bỏ `loudnorm`, dùng đo + tăng âm + hãm đỉnh.** Đề bài ghi `loudnorm I=-16`. Chạy
  đúng như vậy thì 7/10 tệp nằm ngoài ngưỡng. Đo cho thấy lý do: `reluctant__am_michael` có âm lượng
  −24,08 LUFS và đỉnh −5,88 dB, cần +8 dB mà trần đỉnh −1,5 dB chỉ cho +4,4 dB. `encode_opus.py`
  giờ tăng âm bằng `volume`, hãm đỉnh bằng `alimiter`, đo lại chính tệp Opus và sửa tới khi lệch dưới
  0,5 LU. Đây là lệch khỏi Plan §4.3, đã ghi vào Decisions log của Plan. Giọng `am_michael` cần tới
  +12 dB, tức bị hãm đỉnh nhiều hơn — cần tai người xác nhận không méo.
- 2026-10-08 — **Không sửa từ điển MFA cho khớp CMUdict trong task này.** Lệch ở `market` là do
  từ điển `english_us_arpa` của MFA ghi nguyên âm không nhấn khác CMUdict. Cách xử hợp lý là đưa
  cho MFA từ điển dựng từ CMUdict, nhưng đó là thiết kế của pipeline thật, thuộc P.10. Ở đây chỉ ghi
  nhận và để lại `mismatch.csv`.
- 2026-10-08 — **Đo MFA ở hai cỡ lô.** Một điểm đo 10 tệp cho ra 8,9 giây mỗi tệp, con số đó sai
  lệch hoàn toàn nếu đem nhân lên. Đo thêm 40 tệp: 93,2 giây. Suy ra khoảng 89 giây khởi động và
  khoảng 0,1 giây mỗi tệp.
- 2026-10-08 — **`tools/checks/__pycache__/` có tệp `.pyc` đang được git theo dõi từ P.1.** Test
  mới sinh thêm một tệp `.pyc` chưa theo dõi. Không thêm nó vào commit; không dọn các tệp cũ vì
  ngoài phạm vi task.

## Câu hỏi mở
- **Luật giấy phép cho công cụ chỉ chạy lúc dựng.** `license-allowlist.txt` không có GPL hay LGPL.
  Nhưng `ffmpeg` cài sẵn trên máy đã là bản GPL, và môi trường MFA kéo theo 28 gói họ GPL/LGPL không
  gỡ được. Cả hai đều do tài liệu dự án yêu cầu dùng. `docs/01` dòng 650 đã nói Kokoro, MFA, SD
  "chỉ dùng lúc build, không trong app, không vào SBOM app". Đề xuất: ghi rõ thành luật rằng
  allowlist áp cho thứ đi vào app và vào gói nội dung; công cụ trên máy dựng thì liệt kê ở `ENV.md`
  và `sdk-allowlist.md` nhưng không bị chặn. Nếu chấp nhận, cài lại `cmudict` và chạy B8. Đây là
  quyết định pháp lý, chờ người review.

## Người kiểm: tự kiểm  Ngày:   Kết luận: Xong / Làm lại (lý do)
