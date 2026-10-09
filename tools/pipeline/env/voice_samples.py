"""Make the blind listening set for task P.4: five voices, twenty words, five sentences.

Run with the project environment:
    tools/pipeline/.venv/Scripts/python tools/pipeline/env/voice_samples.py

    ... voice_samples.py --page-only    rewrite rate.html only; the audio is left untouched

Output, all under content/pack/audio_test/voices/ (ignored by git):
    s001.opus ... s125.opus   levelled to -16 LUFS, names carry no voice
    rate.html                 the rating page, with the file list written in
    sheets/                   where the rater puts sheet_R1.csv, sheet_R2.csv, sheet_R3.csv
    _key/key.csv              which sample is which voice and text. Keep it away from the rater.
    _key/measures.csv         length and loudness per sample, sound string per text
    _key/wav/                 the raw recordings, named by voice

The order is fixed by a seed, so a second run gives the same names.
"""
import csv
import hashlib
import json
import random
import sys
import time
from pathlib import Path

from _paths import (CANDIDATE_VOICES, KEY_DIR, LEXICON_CSV, SAMPLE_WORDS, SENTENCES, VOICES_DIR,
                    WIND_NOUN_SOUNDS, WIND_VERB_SENTENCE, WIND_VERB_SOUNDS, setup)

setup()

from encode_opus import TARGET_LUFS, TOLERANCE, level_and_encode  # noqa: E402

SEED = 20261009
# TC-CT-02, docs/08-kiem-thu.md: length limits in ms.
LIMITS = {"word": (300, 4000), "sentence": (800, 8000)}
PAGE_TEMPLATE = Path(__file__).with_name("rate.html")
FILES_MARK = "/*SAMPLE_FILES*/[]"
SET_MARK = '/*SET_ID*/""'
SEXES = {"af_": "female", "am_": "male"}


def write_page(samples):
    """Copy the page next to the samples, with the file list and an id of this exact audio."""
    page = PAGE_TEMPLATE.read_text(encoding="utf-8")
    for mark in (FILES_MARK, SET_MARK):
        if mark not in page:
            sys.exit(f"{PAGE_TEMPLATE.name}: the marker {mark} is missing")
    digest = hashlib.sha256()
    for sample in samples:
        digest.update((VOICES_DIR / f"{sample}.opus").read_bytes())
    set_id = digest.hexdigest()[:16]
    names = [f"{sample}.opus" for sample in samples]
    page = page.replace(FILES_MARK, json.dumps(names)).replace(SET_MARK, json.dumps(set_id))
    (VOICES_DIR / "rate.html").write_text(page, encoding="utf-8")
    (VOICES_DIR / "sheets").mkdir(exist_ok=True)
    return set_id


def main():
    if "--page-only" in sys.argv:
        with open(KEY_DIR / "key.csv", encoding="utf-8", newline="") as f:
            samples = [row["sample"] for row in csv.DictReader(f)]
        print(f"rate.html rewritten for {len(samples)} samples, set id {write_page(samples)}")
        return
    from _kokoro import SAMPLE_RATE, make_pipeline, speak
    import soundfile as sf
    unknown = [v for v in CANDIDATE_VOICES if v[:3] not in SEXES]
    if unknown:
        sys.exit(f"cannot tell the sex of {unknown} from the name; add the prefix to SEXES")
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
        key_rows.append(dict(sample=sample, voice=take["voice"], sex=SEXES[take["voice"][:3]],
                             kind=take["kind"],
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

    write_page([row["sample"] for row in key_rows])

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
