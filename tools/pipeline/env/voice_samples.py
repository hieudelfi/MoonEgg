"""Make the blind listening set for task P.4: five voices, twenty words, five sentences.

Run with the project environment:
    tools/pipeline/.venv/Scripts/python tools/pipeline/env/voice_samples.py

Output, all under content/pack/audio_test/voices/ (ignored by git):
    s001.opus ... s125.opus   levelled to -16 LUFS, names carry no voice
    rate.html                 the rating page, with the file list written in
    _key/key.csv              which sample is which voice and text. Keep it away from the rater.
    _key/measures.csv         length and loudness per sample, sound string per text
    _key/wav/                 the raw recordings, named by voice

The order is fixed by a seed, so a second run gives the same names.
"""
import csv
import json
import random
import shutil
import sys
import time
from pathlib import Path

from _paths import (CANDIDATE_VOICES, KEY_DIR, LEXICON_CSV, SAMPLE_WORDS, SENTENCES, VOICES_DIR,
                    WIND_NOUN_SOUNDS, WIND_VERB_SENTENCE, WIND_VERB_SOUNDS, setup)

setup()

from _kokoro import SAMPLE_RATE, make_pipeline, speak  # noqa: E402
from encode_opus import TARGET_LUFS, TOLERANCE, level_and_encode  # noqa: E402

import soundfile as sf  # noqa: E402

SEED = 20261009
# TC-CT-02, docs/08-kiem-thu.md: length limits in ms.
LIMITS = {"word": (300, 4000), "sentence": (800, 8000)}
PAGE_TEMPLATE = Path(__file__).with_name("rate.html")
FILES_MARK = "/*SAMPLE_FILES*/[]"


def main():
    texts = [("word", w) for w in SAMPLE_WORDS] + [("sentence", s) for s in SENTENCES]
    with open(LEXICON_CSV, encoding="utf-8", newline="") as f:
        arpabet = {}
        for row in csv.DictReader(f):
            arpabet.setdefault(row["headword"], row["arpabet"])

    wav_dir = KEY_DIR / "wav"
    wav_dir.mkdir(parents=True, exist_ok=True)
    for stale in VOICES_DIR.glob("s*.opus"):
        stale.unlink()

    started = time.perf_counter()
    pipeline = make_pipeline(CANDIDATE_VOICES)
    load_s = time.perf_counter() - started

    takes, synth_s = [], 0.0
    for voice in CANDIDATE_VOICES:
        for index, (kind, text) in enumerate(texts, 1):
            t0 = time.perf_counter()
            audio, phonemes = speak(pipeline, text, voice)
            synth_s += time.perf_counter() - t0
            wav = wav_dir / f"{voice}__t{index:02d}.wav"
            sf.write(wav, audio.numpy(), SAMPLE_RATE, subtype="PCM_16")
            takes.append(dict(voice=voice, kind=kind, text=text, wav=wav, phonemes=phonemes))

    random.Random(SEED).shuffle(takes)
    key_rows, measure_rows, problems = [], [], []
    for number, take in enumerate(takes, 1):
        sample = f"s{number:03d}"
        result = level_and_encode(take["wav"], VOICES_DIR / f"{sample}.opus")
        low, high = LIMITS[take["kind"]]
        if not low <= result["duration_ms"] <= high:
            problems.append(f"{sample}: {result['duration_ms']} ms, outside {low}-{high}")
        if result["verdict"] != "ok":
            problems.append(f"{sample}: loudness {result['out_lufs']}, {result['verdict']}")
        sex = "female" if take["voice"].startswith("af_") else "male"
        key_rows.append(dict(sample=sample, voice=take["voice"], sex=sex, kind=take["kind"],
                             text=take["text"]))
        measure_rows.append(dict(sample=sample, voice=take["voice"], kind=take["kind"],
                                 text=take["text"], duration_ms=result["duration_ms"],
                                 raw_lufs=result["in_lufs"], out_lufs=result["out_lufs"],
                                 gain_db=result["gain_db"], phonemes=take["phonemes"],
                                 cmudict=arpabet.get(take["text"], "")))

    for name, rows in (("key.csv", key_rows), ("measures.csv", measure_rows)):
        with open(KEY_DIR / name, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    page = PAGE_TEMPLATE.read_text(encoding="utf-8")
    if FILES_MARK not in page:
        sys.exit(f"{PAGE_TEMPLATE.name}: the marker {FILES_MARK} is missing")
    names = [f"{row['sample']}.opus" for row in key_rows]
    (VOICES_DIR / "rate.html").write_text(page.replace(FILES_MARK, json.dumps(names)),
                                          encoding="utf-8")
    shutil.copy2(PAGE_TEMPLATE, KEY_DIR / "rate.template.html")

    per_voice = {v: sum(1 for r in key_rows if r["voice"] == v) for v in CANDIDATE_VOICES}
    print(f"voices loaded in {load_s:.1f} s; {len(takes)} takes, {synth_s / len(takes):.3f} s each")
    print("samples per voice:", per_voice)
    print(f"loudness target {TARGET_LUFS} +/- {TOLERANCE} LUFS; "
          f"measured {min(r['out_lufs'] for r in measure_rows)} to "
          f"{max(r['out_lufs'] for r in measure_rows)}")
    by_text = {r["text"]: r["phonemes"] for r in measure_rows}
    noun, verb = by_text["wind"], by_text[WIND_VERB_SENTENCE]
    print(f"wind alone:    /{noun}/  noun sound {WIND_NOUN_SOUNDS!r} present: "
          f"{WIND_NOUN_SOUNDS in noun}")
    print(f"wind as verb:  /{verb}/  verb sound {WIND_VERB_SOUNDS!r} present: "
          f"{WIND_VERB_SOUNDS in verb}")
    print(f"open {VOICES_DIR / 'rate.html'} to rate; keep {KEY_DIR.name}/ closed until done")
    if problems:
        sys.exit("\n".join(["problems:"] + problems))


if __name__ == "__main__":
    main()
