"""Check the aligner's output against CMUdict.

Run with any Python 3.11+ that has ffprobe on PATH:
    python tools/pipeline/env/check_textgrid.py

For each TextGrid: a tier named "phones" exists, times only go up, the last time is not after the
end of the audio, and the sounds equal the ARPAbet in content/lexicon/lexicon_raw_test.csv.
Writes mismatch.csv even when it is empty, so "no mismatch" is a file and not a silence.
"""
import csv
import json
import re
import subprocess
import sys

from _paths import ALIGNED_DIR, AUDIO_TEST, ITEM_IDS, LEXICON_CSV, WAV_DIR, setup

# Rounding in the TextGrid, in seconds. One audio sample at 24 kHz is far below this.
TIME_SLACK = 0.001


def parse_textgrid(text):
    """Return {tier name: [(start, end, label), ...]} from a Praat long-format TextGrid."""
    tiers, name = {}, None
    xmin = xmax = None
    for line in text.splitlines():
        line = line.strip()
        if found := re.match(r'name = "(.*)"', line):
            name = found.group(1)
            tiers[name] = []
            xmin = xmax = None
        elif name is None:
            continue
        elif found := re.match(r"xmin = (\S+)", line):
            xmin = float(found.group(1))
        elif found := re.match(r"xmax = (\S+)", line):
            xmax = float(found.group(1))
        elif found := re.match(r'text = "(.*)"', line):
            tiers[name].append((xmin, xmax, found.group(1)))
    return tiers


def strip_stress(phone):
    return phone.rstrip("012")


def check(tiers, expected_arpabet, duration_s):
    """Return a list of problems as (kind, detail). Empty means the file is clean."""
    if "phones" not in tiers:
        return [("no_phones_tier", "tiers: " + ", ".join(tiers) or "none")]
    problems = []
    intervals = tiers["phones"]
    previous_end = 0.0
    for start, end, label in intervals:
        if start < previous_end - TIME_SLACK or end <= start:
            problems.append(("time_not_rising", f"{label or 'silence'} {start}-{end}"))
        previous_end = end
    if intervals and intervals[-1][1] > duration_s + TIME_SLACK:
        problems.append(("ends_after_audio", f"{intervals[-1][1]} > {duration_s}"))
    aligned = [label for _, _, label in intervals if label]
    expected = expected_arpabet.split()
    if [strip_stress(p) for p in aligned] != [strip_stress(p) for p in expected]:
        problems.append(("sound_mismatch", " ".join(aligned)))
    elif aligned != expected:
        problems.append(("stress_only", " ".join(aligned)))
    return problems


def wav_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout
    return float(out.strip())


def main():
    setup()
    with open(LEXICON_CSV, encoding="utf-8", newline="") as f:
        arpabet = {row["item_id"]: row["arpabet"] for row in csv.DictReader(f)}
    grids = sorted(ALIGNED_DIR.glob("*.TextGrid"))
    if not grids:
        sys.exit(f"no TextGrid files in {ALIGNED_DIR}. Run align_sample.py first.")

    rows, mismatches, hard_failures = [], [], 0
    for grid in grids:
        word = grid.stem.split("__")[0]
        item_id = ITEM_IDS[word]
        expected = arpabet[item_id]
        tiers = parse_textgrid(grid.read_text(encoding="utf-8"))
        duration = wav_duration(WAV_DIR / (grid.stem + ".wav"))
        problems = check(tiers, expected, duration)
        phones = [(s, e, p) for s, e, p in tiers.get("phones", []) if p]
        aligned = " ".join(p for _, _, p in phones)
        kinds = [k for k, _ in problems]
        hard_failures += sum(1 for k in kinds if k != "stress_only")
        for kind, detail in problems:
            if kind in ("sound_mismatch", "stress_only"):
                mismatches.append(dict(file=grid.name, item_id=item_id, kind=kind,
                                       cmudict=expected, aligned=detail))
        rows.append(dict(file=grid.name, item_id=item_id, cmudict=expected, aligned=aligned,
                         first_sound_s=phones[0][0] if phones else None,
                         last_sound_s=phones[-1][1] if phones else None,
                         duration_s=round(duration, 3), problems=kinds))
        print(f"{grid.name:32} {aligned:28} cmudict {expected:28} "
              f"{'ok' if not kinds else ', '.join(kinds)}")

    with open(AUDIO_TEST / "mismatch.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "item_id", "kind", "cmudict", "aligned"])
        writer.writeheader()
        writer.writerows(mismatches)
    (AUDIO_TEST / "textgrid_report.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    clean_words = {r["item_id"] for r in rows} - {m["item_id"] for m in mismatches
                                                  if m["kind"] == "sound_mismatch"}
    print(f"{len(rows)} files, {len(clean_words)} of {len(ITEM_IDS)} words match CMUdict, "
          f"{len(mismatches)} rows in mismatch.csv, {hard_failures} hard failures")
    sys.exit(1 if hard_failures else 0)


if __name__ == "__main__":
    main()
