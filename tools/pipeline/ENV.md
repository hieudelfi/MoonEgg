# ENV — môi trường pipeline nội dung

Đo và cài ngày 2026-10-08, task P.3. Máy: Ryzen 7 5800U (8 nhân, 16 luồng), RAM 31,3 GB, card AMD
Radeon tích hợp 512 MB, không có GPU rời. Windows 11. Mọi số dưới đây là số đo thật trên máy này;
chỗ nào là ước tính thì ghi rõ "ước".

## 1. Có gì, ở đâu

| Thứ | Phiên bản | Nằm ở | Dung lượng |
| --- | --- | --- | --- |
| Python cho giọng đọc | 3.12.14 (do `uv` cài sẵn) | `tools/pipeline/.venv` | 1,2 GB |
| torch | 2.14.1+cpu | trong `.venv` | |
| Kokoro | 0.9.4, model `hexgrad/Kokoro-82M` | trong `.venv`, model ở `.cache/hf` | |
| misaki | 0.9.4 | trong `.venv` | |
| spaCy + `en_core_web_sm` | 3.8.16 + 3.8.0 | trong `.venv` | |
| soundfile, nltk | 0.14.0, 3.10.3 | trong `.venv` | |
| Miniforge (conda) | conda 26.7.2 | `D:\tools\miniforge3`, không vào PATH | 621 MB |
| Montreal Forced Aligner | 3.4.2 (Python 3.13.16, kalpy 0.10.5, kaldi 5.5.1172) | `tools/pipeline/.mfa` | 2,4 GB |
| Model MFA | `english_us_arpa`, từ điển + acoustic | `.cache/mfa/pretrained_models` | |
| ffmpeg, ffprobe | 9.0.2 full build (gyan.dev), có libopus | cài sẵn qua winget | |
| Bộ nhớ đệm | pip, model, conda, tệp tạm | `tools/pipeline/.cache` | 1,9 GB |

Tổng trên ổ D: khoảng 6,1 GB. Ổ C: trước khi cài trống 9,17 GB, sau khi xong 9,54 GB — không mất gì.
Thứ duy nhất rơi vào ổ C là `Documents\MFA\global_config.yaml`, 2 KB, do MFA tự tạo lúc cài.

`.venv`, `.mfa`, `.cache` đều bị git bỏ qua. `requirements.txt` và tệp này thì được theo dõi.

## 2. Lệnh cài, theo đúng thứ tự đã chạy

Chạy trong Git Bash, đứng ở gốc repo. Ba biến đầu giữ mọi thứ khỏi ổ C; thiếu chúng thì pip, model
và tệp tạm sẽ rơi vào hồ sơ người dùng.

```bash
P="$(pwd -W)/tools/pipeline"
export PIP_CACHE_DIR="$P/.cache/pip" HF_HOME="$P/.cache/hf" TMP="$P/.cache/tmp" TEMP="$P/.cache/tmp"
export CONDA_PKGS_DIRS="$P/.cache/conda-pkgs"
mkdir -p "$P/.cache/tmp"

# 2.1 Môi trường giọng đọc. `py -3.12` KHÔNG khởi động được bản 3.12 của uv, phải gọi đủ tên.
py -V:Astral/CPython3.12.14 -m venv tools/pipeline/.venv
PY=tools/pipeline/.venv/Scripts/python
$PY -m pip install --upgrade pip
$PY -m pip install torch --index-url https://download.pytorch.org/whl/cpu
$PY -m pip install kokoro soundfile nltk cmudict
$PY -m pip uninstall -y phonemizer-fork espeakng-loader num2words   # xem mục 4
$PY -m spacy download en_core_web_sm

# 2.2 Miniforge, cài im lặng, không đăng ký Python, không sửa PATH
curl -sL -o "$P/.cache/dl/Miniforge3.exe" \
  https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe
# trong PowerShell:
#   Start-Process -Wait "<P>\.cache\dl\Miniforge3.exe" `
#     -ArgumentList '/InstallationType=JustMe','/RegisterPython=0','/AddToPath=0','/S','/D=D:\tools\miniforge3'

# 2.3 MFA, một môi trường riêng nằm trong repo
/d/tools/miniforge3/Scripts/conda.exe create -y -p "$P/.mfa" -c conda-forge montreal-forced-aligner
```

Thời gian cài thật: bước 2.1 mất 4 phút 41 giây; bước 2.2 và 2.3 cộng lại 3 phút 33 giây.
Tệp cài Miniforge đã tải: 148.256.480 byte, sha256 `71cf9519…fccbaab`.

Cài lại đúng phiên bản đã đo: `$PY -m pip install -r tools/pipeline/requirements.txt`, rồi chạy lại
dòng `pip uninstall` ở trên.

**Không gọi thẳng `mfa.exe`.** Nó cần các thư mục của môi trường conda trên PATH, thiếu thì báo
`cannot load library 'libsndfile.dll'`. `align_sample.py` tự đặt PATH; chạy tay thì dùng
`conda run -p tools/pipeline/.mfa mfa ...`.

## 3. Chạy

```bash
PY=tools/pipeline/.venv/Scripts/python
$PY tools/pipeline/env/tts_sample.py        # 10 WAV + .lab  -> content/pack/audio_test/wav/
python tools/pipeline/env/encode_opus.py    # 10 Opus        -> content/pack/audio_test/opus/
python tools/pipeline/env/align_sample.py   # 10 TextGrid    -> content/pack/audio_test/aligned/
python tools/pipeline/env/check_textgrid.py # so với CMUdict -> mismatch.csv
```

Hai script sinh giọng, `tts_sample.py` và `voice_samples.py` (task P.4), cần `.venv`. Các script còn lại chạy bằng Python 3.11 trở lên bất kỳ.
Mọi script sinh giọng nạp Kokoro qua `tools/pipeline/env/_kokoro.py`, không `import kokoro` trực tiếp.
Chạy lại lần nữa thì ghi đè đúng 10 tệp cũ, không sinh tệp trùng.

## 4. Giấy phép — đọc trước khi cài thêm gì

Model và dữ liệu đều nằm trong `tools/checks/license-allowlist.txt`: Kokoro-82M Apache-2.0,
`en_core_web_sm` MIT, model MFA `english_us_arpa` CC-BY-4.0.

Luật áp dụng nằm ở `CLAUDE.md` mục 5, chốt ngày 2026-10-08: thứ đi vào app và gói nội dung phải
nằm trong allowlist; công cụ chỉ chạy trên máy dựng thì được dùng kể cả khi mang GPL, miễn là được
liệt kê ở đây, không bị chép vào repo hay sản phẩm, và script nào `import` thẳng thư viện GPL thì
được nêu tên.

`.venv`: 96 gói. Ba gói bị gỡ, một gói GPL được giữ lại có chủ đích:

| Gói | Giấy phép | Ai kéo vào | Xử lý |
| --- | --- | --- | --- |
| `phonemizer-fork` 3.3.2 | GPL-3.0-or-later | kokoro → misaki | gỡ; `_kokoro.py` chèn module giả |
| `espeakng-loader` 0.2.4 | không khai, bọc espeak-ng GPL-3.0 | kokoro → misaki | gỡ; như trên |
| `num2words` 0.5.14 | LGPL | misaki | gỡ; chèn hàm giả |
| `cmudict` 1.1.3 | GPL-3.0-or-later (mã bọc; dữ liệu CMUdict bên trong là BSD) | đề bài P.3, `build_lexicon.py:1` | cài; chỉ `build_lexicon.py` dùng |

Hệ quả phải nhớ:
- Từ nằm ngoài từ điển của Kokoro **không được đoán âm**. Kokoro tự nó sẽ lặng lẽ bỏ từ đó và đọc tiếp; `_kokoro.py` hỏi trước bộ đổi chữ thành âm và dừng, nêu tên từ, kể cả khi từ nằm giữa câu.
  thông báo rõ khi gặp. Năm từ thử đều có trong từ điển.
- Văn bản có **chữ số** sẽ làm Kokoro báo lỗi. Câu ví dụ phải viết số bằng chữ.
- **`tools/pipeline/build_lexicon.py` là script duy nhất `import` thẳng một thư viện GPL** (`cmudict`).
  Script này không được phát hành ra ngoài repo riêng tư. Dữ liệu nó tạo ra không vướng: nội dung
  CMUdict là BSD, và tệp CSV ghi `source` và `license` theo dữ liệu gốc.
- Đường ít rủi ro hơn cho P.8: đọc thẳng tệp dữ liệu CMUdict (BSD) mà P.7 tải về, bỏ hẳn mã bọc GPL.
  Bản CMUdict đi kèm NLTK không thay được ngay: nó cũ hơn (123.455 mục so với 126.052), và trên 29
  từ mẫu đã có 1 từ khác (`exhausted`).

`.mfa` thì khác: 204 gói conda, trong đó **28 gói họ GPL/LGPL** đi kèm MFA mà không gỡ được, ví dụ
`ffmpeg` 8.1.2 và `sox` 14.4.2 (GPL-2.0), `libsndfile` (LGPL), `libgcc` (GPL kèm ngoại lệ GCC). Bản
`ffmpeg` cài sẵn trên máy cũng dựng với `--enable-gpl`. Tất cả là chương trình chạy lúc dựng nội dung,
không có dòng mã nào đi vào app hay vào tệp audio.

## 5. Thời gian đo được

Năm từ (hello, market, reluctant, think, wind) × hai giọng tạm (`af_heart`, `am_michael`) = 10 tệp.

| Bước | Trả một lần | Mỗi tệp | Ghi chú |
| --- | --- | --- | --- |
| Kokoro nạp model + 2 giọng | 3,45 giây (lần đầu 38,59 giây vì tải model) | | mỗi lần chạy trả một lần |
| Kokoro sinh một từ | | 0,625–0,686 giây (trung bình hai lần chạy) | 8 luồng CPU; audio dài 1,2–1,6 giây |
| ffmpeg: đo, tăng âm, hãm đỉnh, nén Opus | | 0,364 giây | 1 đến 4 vòng mỗi tệp |
| MFA tải model | 23,7 giây | | mỗi máy trả một lần |
| MFA căn 10 tệp | 89,1 và 90,3 giây (hai lần chạy) | | |
| MFA căn 40 tệp | 93,2 giây | | cùng 10 tệp nhân bốn |
| MFA suy ra | khoảng 89 giây khởi động | khoảng 0,1 giây | từ hai điểm đo 10 và 40 tệp |

Tệp ra: WAV 24 kHz 16 bit, dài 1.225–1.550 ms. Opus 20,9–24,8 kbps, 3,4–4,8 KB mỗi tệp,
âm lượng đo lại trên chính tệp Opus từ −16,5 đến −16,0 LUFS.

### Ước cho cả bộ nội dung

Ước, không phải đo. Nhân thẳng từ số đo trên 10 tệp nên sai số lớn; P.10 chạy 30 từ sẽ cho số tốt hơn.

| Khối lượng | Phép tính | Ước |
| --- | --- | --- |
| 5.000 từ × 2 giọng, Kokoro | 10.000 × 0,65 giây | 1,8 giờ |
| 15.000 câu × 2 giọng, Kokoro | 30.000 × 1,9 giây; giả định câu dài 4 giây, máy sinh nhanh gấp 2,1 lần thời gian thực | 16 giờ |
| 40.000 tệp, ffmpeg | 40.000 × 0,364 giây | 4 giờ |
| 40.000 tệp, MFA | 40.000 × 0,1 giây, chưa tính khởi động mỗi lô | 1,1 giờ |
| **Tổng** | | **khoảng 23 giờ máy** |

Khớp với con số "máy chạy 1–2 ngày" ở `docs/01-yeu-cau.md` dòng 401, nên chưa phải sửa lịch ở
`docs/09`. Độ dài câu 4 giây là giả định **chưa đo**. MFA có phí khởi động 89 giây mỗi lần gọi, nên
phải căn theo lô lớn, không gọi từng từ.

## 6. Ba điều rút ra cho task sau

1. **`loudnorm` của ffmpeg không đủ cho từ đơn.** Từ đơn có đỉnh cao, thân mỏng: cần tăng khoảng
   8 dB nhưng đỉnh chỉ còn chỗ cho 4 dB. Lần chạy đầu 7 trên 10 tệp nằm ở −18 đến −20 LUFS.
   `encode_opus.py` vì thế đo, tăng âm, hãm đỉnh ở −1,5 dB bằng `alimiter`, rồi đo lại tệp ra và
   sửa cho tới khi lệch dưới 0,5 LU. Giọng `am_michael` cần tăng tới +12 dB — nghe kiểm xem có méo không.
2. **Từ điển của MFA không trùng CMUdict.** `market`: CMUdict ghi `M AA1 R K AH0 T`, MFA căn ra
   `M AA1 R K IH0 T`. Bốn từ còn lại khớp hoàn toàn. Lệch một nguyên âm không nhấn ở 1 trên 5 từ là
   quá xa ngưỡng 98% của TC-CT-04. Hướng xử cho P.10: đưa cho MFA một từ điển dựng từ chính CMUdict,
   khi đó phone căn ra trùng CMUdict theo cấu trúc. Chưa thử ở task này.
3. **"wind" ra đúng âm danh từ** `/wˈɪnd/` ở cả hai giọng khi đọc riêng một từ. Chưa có cách ép âm
   động từ `/waɪnd/` cho `w:wind#2`; P.10 cần một cách, ví dụ đưa thẳng chuỗi phoneme cho Kokoro.

## 7. Stable Diffusion — không cài ở máy này

Máy không có GPU rời; card tích hợp chỉ có 512 MB. Chạy bằng CPU mất nhiều phút mỗi ảnh và thêm vài
GB cài đặt, mà P.5 sẽ không dùng kết quả đó. Quyết định ở Cổng A ngày 2026-10-08: bỏ, P.5 dùng dịch
vụ miễn phí có sẵn. Prompt gốc nằm ở `docs/01-yeu-cau.md` §9.3.
