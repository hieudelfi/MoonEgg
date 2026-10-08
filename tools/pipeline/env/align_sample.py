"""Find when each sound starts in the sample recordings, with Montreal Forced Aligner (MFA).

Run with any Python 3.11+; MFA itself runs from its own conda environment in tools/pipeline/.mfa:
    python tools/pipeline/env/align_sample.py

Output: content/pack/audio_test/aligned/<word>__<voice>.TextGrid and align_timing.json.
The aligner reads the WAV files, not the Opus files: compression must not move the timings.
"""
import json
import os
import shutil
import subprocess
import sys
import time

from _paths import ALIGNED_DIR, AUDIO_TEST, CACHE, PIPELINE, VOICES, WAV_DIR, setup

setup()

MFA_ENV = PIPELINE / ".mfa"
MODEL = "english_us_arpa"


def mfa_environment():
    """The MFA program needs its own folders on PATH, the way 'conda activate' would set them."""
    env = dict(os.environ)
    parts = [MFA_ENV, MFA_ENV / "Library" / "mingw-w64" / "bin", MFA_ENV / "Library" / "usr" / "bin",
             MFA_ENV / "Library" / "bin", MFA_ENV / "Scripts", MFA_ENV / "bin"]
    env["PATH"] = os.pathsep.join(str(p) for p in parts) + os.pathsep + env["PATH"]
    env["CONDA_PREFIX"] = str(MFA_ENV)
    env["PYTHONUTF8"] = "1"
    return env


def mfa(env, *args):
    exe = MFA_ENV / "Scripts" / "mfa.exe" if os.name == "nt" else MFA_ENV / "bin" / "mfa"
    done = subprocess.run([str(exe), *args], env=env, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    if done.returncode != 0:
        sys.exit(f"mfa {' '.join(args[:3])} failed\n{(done.stdout + done.stderr)[-1500:]}")
    return done.stdout + done.stderr


def main():
    if not MFA_ENV.exists():
        sys.exit(f"{MFA_ENV} is missing. See tools/pipeline/ENV.md for the install command.")
    wavs = sorted(WAV_DIR.glob("*.wav"))
    if not wavs:
        sys.exit(f"no WAV files in {WAV_DIR}. Run tts_sample.py first.")
    env = mfa_environment()
    version = mfa(env, "version").strip().splitlines()[-1]

    t0 = time.perf_counter()
    mfa(env, "model", "download", "dictionary", MODEL)
    mfa(env, "model", "download", "acoustic", MODEL)
    download_s = time.perf_counter() - t0

    # One folder per voice: MFA treats each folder as one speaker.
    corpus = CACHE / "tmp" / "align_corpus"
    out = CACHE / "tmp" / "align_out"
    for folder in (corpus, out):
        shutil.rmtree(folder, ignore_errors=True)
    for voice in VOICES:
        (corpus / voice).mkdir(parents=True)
    for wav in wavs:
        voice = wav.stem.split("__")[1]
        shutil.copy2(wav, corpus / voice / wav.name)
        shutil.copy2(wav.with_suffix(".lab"), corpus / voice / (wav.stem + ".lab"))

    t0 = time.perf_counter()
    mfa(env, "align", "--clean", "--quiet", str(corpus), MODEL, MODEL, str(out))
    align_s = time.perf_counter() - t0

    shutil.rmtree(ALIGNED_DIR, ignore_errors=True)
    ALIGNED_DIR.mkdir(parents=True)
    grids = sorted(out.rglob("*.TextGrid"))
    for grid in grids:
        shutil.copy2(grid, ALIGNED_DIR / grid.name)
    missing = sorted({w.stem for w in wavs} - {g.stem for g in grids})

    report = dict(mfa_version=version, model=MODEL, files=len(wavs), textgrids=len(grids),
                  missing=missing, model_download_s=round(download_s, 2),
                  align_total_s=round(align_s, 2), align_per_file_s=round(align_s / len(wavs), 3))
    (AUDIO_TEST / "align_timing.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"MFA {version}, model {MODEL}")
    print(f"models ready in {download_s:.1f} s, paid once per machine")
    print(f"{len(grids)} of {len(wavs)} files aligned in {align_s:.1f} s, "
          f"{align_s / len(wavs):.2f} s per file including start-up")
    if missing:
        sys.exit("not aligned: " + ", ".join(missing))


if __name__ == "__main__":
    main()
