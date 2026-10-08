"""Shared setup for the pipeline environment scripts.

Every cache lives under tools/pipeline/.cache on the project drive. Drive C: is nearly full on the
build machine, so nothing here may fall back to a default location in the user profile.
"""
import os
import shutil
import sys
from pathlib import Path

PIPELINE = Path(__file__).resolve().parents[1]
ROOT = PIPELINE.parents[1]
CACHE = PIPELINE / ".cache"
AUDIO_TEST = ROOT / "content" / "pack" / "audio_test"
WAV_DIR = AUDIO_TEST / "wav"
OPUS_DIR = AUDIO_TEST / "opus"
ALIGNED_DIR = AUDIO_TEST / "aligned"
LEXICON_CSV = ROOT / "content" / "lexicon" / "lexicon_raw_test.csv"

WORDS = ["hello", "market", "reluctant", "think", "wind"]
# Temporary pair. Task P.4 picks the final two voices.
VOICES = ["af_heart", "am_michael"]
# "wind" has two sounds. The sample is the noun.
ITEM_IDS = {"hello": "w:hello#1", "market": "w:market#1", "reluctant": "w:reluctant#1",
            "think": "w:think#1", "wind": "w:wind#1"}

MIN_FREE_C_GB = 5.0


def setup():
    """Point every cache at the project drive and refuse to run when C: is too full."""
    for name, sub in (("HF_HOME", "hf"), ("PIP_CACHE_DIR", "pip"), ("MFA_ROOT_DIR", "mfa"),
                      ("NLTK_DATA", "nltk"), ("TMP", "tmp"), ("TEMP", "tmp")):
        path = CACHE / sub
        path.mkdir(parents=True, exist_ok=True)
        os.environ[name] = str(path)
    if os.name == "nt":
        free_gb = shutil.disk_usage("C:\\").free / 1024 ** 3
        if free_gb < MIN_FREE_C_GB:
            sys.exit(f"C: has {free_gb:.1f} GB free, below {MIN_FREE_C_GB} GB. Stopping.")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def stem(word, voice):
    return f"{word}__{voice}"
