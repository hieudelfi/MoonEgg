"""Speak the five sample words with two voices and time each one.

Run with the project environment:
    tools/pipeline/.venv/Scripts/python tools/pipeline/env/tts_sample.py

Output: content/pack/audio_test/wav/<word>__<voice>.wav, a .lab file with the word next to each
(the aligner reads it), and tts_timing.json. One speed only: slow playback is done in the app.
"""
import json
import sys
import time
import types

from _paths import AUDIO_TEST, VOICES, WAV_DIR, WORDS, setup, stem

setup()


def _stub(name, **attrs):
    module = types.ModuleType(name)
    module.__dict__.update(attrs)
    sys.modules[name] = module


class _NoFallback:
    def __init__(self, *args, **kwargs):
        raise RuntimeError("the espeak fallback is left out on purpose")


def _no_numbers(*args, **kwargs):
    raise RuntimeError("num2words is left out on purpose; spell numbers out in the text")


# Kokoro imports two things this project does not install: the espeak-ng fallback (GPL-3.0) and
# num2words (LGPL). Neither licence is on tools/checks/license-allowlist.txt. Kokoro already
# handles a fallback that fails to start, so a word outside its dictionary is skipped, not guessed.
_stub("misaki.espeak", EspeakFallback=_NoFallback, EspeakG2P=_NoFallback)
_stub("num2words", num2words=_no_numbers)

import soundfile as sf  # noqa: E402
import torch  # noqa: E402
from kokoro import KPipeline  # noqa: E402

SAMPLE_RATE = 24000


def main():
    WAV_DIR.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M", device="cpu")
    for voice in VOICES:
        pipeline.load_voice(voice)
    load_s = time.perf_counter() - started

    rows = []
    for voice in VOICES:
        for word in WORDS:
            t0 = time.perf_counter()
            results = list(pipeline(word, voice=voice, speed=1.0))
            audio = torch.cat([r.audio for r in results if r.audio is not None])
            seconds = time.perf_counter() - t0
            phonemes = " ".join(r.phonemes for r in results)
            if not phonemes.strip() or audio.numel() == 0:
                sys.exit(f"{word}: Kokoro produced no sound. The word is outside its dictionary.")
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
