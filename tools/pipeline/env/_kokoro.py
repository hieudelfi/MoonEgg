"""Kokoro, loaded the way this project allows it.

Kokoro imports two things this project does not install: the espeak-ng fallback (GPL-3.0) and
num2words (LGPL). Neither licence is on tools/checks/license-allowlist.txt. Importing this module
puts two stand-ins in their place, so Kokoro itself must be imported only through make_pipeline().
Kokoro already handles a fallback that fails to start: a word outside its dictionary is skipped,
not guessed. Text with digits raises, so numbers must be spelled out.
"""
import sys
import types

SAMPLE_RATE = 24000
REPO_ID = "hexgrad/Kokoro-82M"


def _stub(name, **attrs):
    module = types.ModuleType(name)
    module.__dict__.update(attrs)
    sys.modules[name] = module


class _NoFallback:
    def __init__(self, *args, **kwargs):
        raise RuntimeError("the espeak fallback is left out on purpose")


def _no_numbers(*args, **kwargs):
    raise RuntimeError("num2words is left out on purpose; spell numbers out in the text")


_stub("misaki.espeak", EspeakFallback=_NoFallback, EspeakG2P=_NoFallback)
_stub("num2words", num2words=_no_numbers)


def make_pipeline(voices):
    """American English pipeline on the processor, with the given voices loaded."""
    from kokoro import KPipeline
    pipeline = KPipeline(lang_code="a", repo_id=REPO_ID, device="cpu")
    for voice in voices:
        pipeline.load_voice(voice)
    return pipeline


def speak(pipeline, text, voice):
    """Return (audio tensor, phoneme string) for one text. Exits when Kokoro skips the text."""
    import torch
    # Kokoro drops a word it does not know and keeps going. Catch it before any sound is made.
    _, tokens = pipeline.g2p(text)
    lost = [t.text for t in tokens if t.phonemes is None and t.text.strip().isalpha()]
    if lost:
        sys.exit(f"{text!r}: Kokoro has no sounds for {lost}. Swap the word or spell it out.")
    results = list(pipeline(text, voice=voice, speed=1.0))
    chunks = [r.audio for r in results if r.audio is not None]
    phonemes = " ".join(r.phonemes for r in results)
    if not phonemes.strip() or not chunks:
        sys.exit(f"{text!r}: Kokoro produced no sound. A word is outside its dictionary.")
    return torch.cat(chunks), phonemes
