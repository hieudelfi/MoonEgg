"""Speak the five sample words with two voices and time each one.

Run with the project environment:
    tools/pipeline/.venv/Scripts/python tools/pipeline/env/tts_sample.py

Output: content/pack/audio_test/wav/<word>__<voice>.wav, a .lab file with the word next to each
(the aligner reads it), and tts_timing.json. One speed only: slow playback is done in the app.
"""
import json
import time

from _paths import AUDIO_TEST, VOICES, WAV_DIR, WORDS, setup, stem

setup()

from _kokoro import SAMPLE_RATE, make_pipeline, speak  # noqa: E402

import soundfile as sf  # noqa: E402
import torch  # noqa: E402


def main():
    WAV_DIR.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    pipeline = make_pipeline(VOICES)
    load_s = time.perf_counter() - started

    rows = []
    for voice in VOICES:
        for word in WORDS:
            t0 = time.perf_counter()
            audio, phonemes = speak(pipeline, word, voice)
            seconds = time.perf_counter() - t0
            out = WAV_DIR / f"{stem(word, voice)}.wav"
            sf.write(out, audio.numpy(), SAMPLE_RATE, subtype="PCM_16")
            out.with_suffix(".lab").write_text(word + "\n", encoding="utf-8")
            duration_ms = round(audio.numel() / SAMPLE_RATE * 1000)
            rows.append(dict(word=word, voice=voice, file=out.name, phonemes=phonemes,
                             duration_ms=duration_ms, synth_s=round(seconds, 3)))
            print(f"{out.name:28} {duration_ms:5d} ms  synth {seconds:6.3f} s  /{phonemes}/")

    report = dict(model_load_s=round(load_s, 3), torch=torch.__version__,
                  threads=torch.get_num_threads(), files=rows)
    (AUDIO_TEST / "tts_timing.json").write_text(json.dumps(report, indent=2, ensure_ascii=False),
                                                encoding="utf-8")
    mean = sum(r["synth_s"] for r in rows) / len(rows)
    print(f"model and voices loaded in {load_s:.2f} s, paid once per run")
    print(f"{len(rows)} files, mean {mean:.3f} s per word")


if __name__ == "__main__":
    main()
