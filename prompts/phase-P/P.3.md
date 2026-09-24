# P.3 — Môi trường pipeline

**Tham chiếu:** Kế hoạch §3P.1 P.3 · Kiến trúc §5.5

## Mục tiêu
Máy chạy được Kokoro, MFA, ffmpeg, Stable Diffusion; đo thời gian/từ để lập lịch.

## Cách làm
1. Python venv `tools/pipeline/.venv`; `pip install cmudict nltk kokoro soundfile misaki` (+ `torch` theo GPU/CPU). `python -m nltk.downloader wordnet`.
2. Kokoro: sinh audio cho hello, market, reluctant, think, wind với 2 giọng (af_heart, am_michael tạm) → `content/pack/audio_test/`. Ghi thời gian mỗi từ.
3. ffmpeg: chuyển WAV → Opus 24 kbps; chuẩn hoá `loudnorm I=-16`.
4. MFA: `conda install -c conda-forge montreal-forced-aligner` (hoặc pip); tải `english_us_arpa` (dictionary + acoustic); căn 5 file → TextGrid.
5. Stable Diffusion (tuỳ máy): Automatic1111 hoặc ComfyUI; sinh 1 ảnh thử với prompt trong Yêu cầu §9.3. Không GPU → ghi Câu hỏi mở và dùng dịch vụ miễn phí ở P.5 sau.
6. Ghi `tools/pipeline/ENV.md`: phiên bản, lệnh cài, thời gian đo.

## Checklist (chép vào records/P.3.md, tick từng dòng kèm 'kết quả:')
- [ ] 5 audio × 2 giọng tồn tại, nghe được
- [ ] 5 file Opus loudness −16 ±2 LUFS (ffmpeg loudnorm print)
- [ ] 5 TextGrid có tier phones
- [ ] 1 ảnh SD hoặc lý do
- [ ] ENV.md có bảng thời gian

## Kiểm tra (test đối chiếu)
- Kiểm tay: nghe 10 file, ghi nhận xét
- Mở 1 TextGrid, đối chiếu phone với ARPAbet CMUdict của từ đó

## Xác minh output trước khi đóng
- `python tools/pipeline/build_lexicon.py` chạy lại không lỗi trong venv
- Chạy `CLAUDE.md` §3 cho loại đầu ra; chưa qua → không đóng.

## Bằng chứng cần nộp
- Thư mục audio_test
- TextGrid
- ENV.md
