"""Speak the test words with the two chosen voices, for the workbench trial.

Run with the pipeline environment, from the repo root:
    tools/pipeline/.venv/Scripts/python tools/workbench/make_trial_audio.py

Output: content/pack/audio_test/workbench/<item>__<voice>.opus, levelled to -16 LUFS. Ignored by git.
This is a prop for the trial, not content: task P.10 makes the real audio.

One item is left out on purpose. "wind" alone is always read as the noun, so there is no single-word
recording of the verb w:wind#2 yet. The workbench shows it as a word without audio.
"""
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "pipeline" / "env"))

from _paths import AUDIO_TEST, CACHE, LEXICON_CSV, setup  # noqa: E402

setup()

from _kokoro import SAMPLE_RATE, make_pipeline, speak  # noqa: E402
from encode_opus import level_and_encode  # noqa: E402

import soundfile as sf  # noqa: E402

VOICES = ["af_heart", "am_adam"]
NO_SINGLE_WORD_READING = {"w:wind#2"}
OUT = AUDIO_TEST / "workbench"
# TC-CT-02, docs/08-kiem-thu.md: a word is 300 to 4,000 ms long.
LIMITS = (300, 4000)


def slug(item_id):
    return "".join(c if c.isalnum() else "_" for c in item_id)


def main():
    with open(LEXICON_CSV, encoding="utf-8", newline="") as f:
        words = [(r["item_id"], r["headword"]) for r in csv.DictReader(f)
                 if r["item_id"] not in NO_SINGLE_WORD_READING]
    OUT.mkdir(parents=True, exist_ok=True)
    scratch = CACHE / "tmp" / "workbench_wav"
    scratch.mkdir(parents=True, exist_ok=True)
    pipeline = make_pipeline(VOICES)
    problems, lufs = [], []
    for item_id, headword in words:
        for voice in VOICES:
            audio, _ = speak(pipeline, headword, voice)
            wav = scratch / f"{slug(item_id)}__{voice}.wav"
            sf.write(wav, audio.numpy(), SAMPLE_RATE, subtype="PCM_16")
            result = level_and_encode(wav, OUT / f"{slug(item_id)}__{voice}.opus")
            lufs.append(result["out_lufs"])
            if result["verdict"] != "ok":
                problems.append(f"{result['file']}: loudness {result['out_lufs']}, {result['verdict']}")
            if not LIMITS[0] <= result["duration_ms"] <= LIMITS[1]:
                problems.append(f"{result['file']}: {result['duration_ms']} ms, outside {LIMITS}")
    print(f"{len(words)} items x {len(VOICES)} voices = {len(words) * len(VOICES)} files in {OUT}")
    print(f"loudness {min(lufs)} to {max(lufs)} LUFS; left out on purpose: {sorted(NO_SINGLE_WORD_READING)}")
    if problems:
        sys.exit("\n".join(["problems:"] + problems))


if __name__ == "__main__":
    main()
