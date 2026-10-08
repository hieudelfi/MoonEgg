"""Level each sample to -16 LUFS and compress it to Opus at 24 kbps.

Run with any Python 3.11+ that has ffmpeg and ffprobe on PATH:
    python tools/pipeline/env/encode_opus.py

Per file: measure the loudness, add the missing gain, hold the peaks with a limiter, encode, then
measure the Opus file itself. A target that was asked for is not proof of what came out, so the
gain is corrected from the measured result until it lands.

Why not ffmpeg's loudnorm alone: a single spoken word has tall peaks and little body. On the first
run loudnorm needed +8 dB, had room for +4 dB before the peak ceiling, and left 7 of 10 files
between -18 and -20 LUFS. Gain plus a limiter reaches the target; the limiter only touches peaks.
"""
import json
import re
import subprocess
import sys
import time

from _paths import AUDIO_TEST, OPUS_DIR, WAV_DIR, setup

setup()

TARGET_LUFS = -16.0
TOLERANCE = 2.0
PEAK_CEILING_DB = -1.5
# Close enough to stop correcting. Tighter than TOLERANCE so no file sits on the edge.
SETTLE = 0.5
MAX_TRIES = 4
BITRATE = "24k"
# EBU R128 gates on 400 ms blocks. Below that there is nothing to measure.
MIN_MEASURABLE_MS = 400


def run(args):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration,bit_rate",
               "-of", "json", str(path)]).stdout
    fmt = json.loads(out)["format"]
    return round(float(fmt["duration"]) * 1000), round(int(fmt["bit_rate"]) / 1000, 1)


def measure(path):
    """Integrated loudness of a finished file, read from ffmpeg's ebur128 summary."""
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128",
               "-f", "null", "-"]).stderr
    found = re.findall(r"I:\s+(-?\d+(?:\.\d+)?) LUFS", err)
    return float(found[-1]) if found else None


def main():
    wavs = sorted(WAV_DIR.glob("*.wav"))
    if not wavs:
        sys.exit(f"no WAV files in {WAV_DIR}. Run tts_sample.py first.")
    OPUS_DIR.mkdir(parents=True, exist_ok=True)
    rows, failed = [], 0
    ceiling = 10 ** (PEAK_CEILING_DB / 20)
    for wav in wavs:
        t0 = time.perf_counter()
        in_lufs = measure(wav)
        if in_lufs is None:
            sys.exit(f"{wav.name}: ffmpeg could not measure the input")
        out = OPUS_DIR / (wav.stem + ".opus")
        gain, lufs, tries = TARGET_LUFS - in_lufs, None, 0
        while tries < MAX_TRIES:
            tries += 1
            chain = (f"volume={gain:.2f}dB,"
                     f"alimiter=limit={ceiling:.4f}:level=false:attack=1:release=50")
            done = run(["ffmpeg", "-hide_banner", "-nostats", "-y", "-i", str(wav), "-af", chain,
                        "-ar", "48000", "-ac", "1", "-c:a", "libopus", "-b:a", BITRATE, str(out)])
            if done.returncode != 0:
                sys.exit(f"{wav.name}: ffmpeg failed\n{done.stderr[-400:]}")
            lufs = measure(out)
            if lufs is None or abs(lufs - TARGET_LUFS) <= SETTLE:
                break
            gain += TARGET_LUFS - lufs
        seconds = time.perf_counter() - t0
        duration_ms, kbps = probe(out)
        if duration_ms < MIN_MEASURABLE_MS:
            lufs = None
        if lufs is None:
            verdict = "too short to measure"
            failed += 1
        elif abs(lufs - TARGET_LUFS) <= TOLERANCE:
            verdict = "ok"
        else:
            verdict = "outside target"
            failed += 1
        rows.append(dict(file=out.name, in_lufs=in_lufs, out_lufs=lufs, gain_db=round(gain, 2),
                         tries=tries, duration_ms=duration_ms, kbps=kbps, bytes=out.stat().st_size,
                         encode_s=round(seconds, 3), verdict=verdict))
        shown = "  n/a" if lufs is None else f"{lufs:6.1f}"
        print(f"{out.name:29} in {in_lufs:6.1f}  gain {gain:+5.1f} dB  out {shown} LUFS"
              f"  {duration_ms:5d} ms  {kbps:5.1f} kbps  {out.stat().st_size:5d} B"
              f"  {tries} tries  {seconds:5.2f} s  {verdict}")
    (AUDIO_TEST / "opus_report.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    mean = sum(r["encode_s"] for r in rows) / len(rows)
    print(f"{len(rows)} files, mean {mean:.3f} s per file, {failed} outside the target")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
