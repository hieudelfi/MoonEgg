"""Turn the rating sheets of task P.4 into one female and one male voice.

Run with any Python 3.11+:
    python tools/pipeline/env/score.py

Reads _key/key.csv and sheet_R1.csv, sheet_R2.csv, sheet_R3.csv (from _key/ or the folder above
it). Names the winners only when all three sheets are complete. The three sheets are three
sittings of one listener: they show how steady that listener is, not whether others agree.
"""
import csv
import sys
from pathlib import Path

SHEETS_NEEDED = 3
# Below this mean on either score, the best voice of a sex is not good enough to pick.
MIN_ACCEPTABLE = 3.0


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def check_sheet(rows, key, name):
    """Return a list of reasons this sheet cannot be used. Empty means it is complete."""
    reasons = []
    samples = [r.get("sample", "") for r in rows]
    if len(rows) != len(key):
        reasons.append(f"{name}: {len(rows)} rows, needs {len(key)}")
    if len(set(samples)) != len(samples):
        reasons.append(f"{name}: a sample is scored twice")
    unknown = sorted(set(samples) - set(key))
    if unknown:
        reasons.append(f"{name}: unknown samples {unknown[:3]}")
    for r in rows:
        for field in ("clarity", "natural"):
            if r.get(field) not in ("1", "2", "3", "4", "5"):
                reasons.append(f"{name}: {r.get('sample')} has {field}={r.get(field)!r}")
                break
    return reasons


def summarise(key, sheets):
    """Per voice: count, mean of each score, their sum, and the spread between sheets."""
    out = {}
    for voice in sorted({k["voice"] for k in key.values()}):
        clarity, natural, per_sheet = [], [], []
        for rows in sheets.values():
            mine = [r for r in rows if key[r["sample"]]["voice"] == voice]
            c = [int(r["clarity"]) for r in mine]
            n = [int(r["natural"]) for r in mine]
            clarity += c
            natural += n
            if mine:
                per_sheet.append(sum(c) / len(c) + sum(n) / len(n))
        count = len(clarity)
        mean_c = sum(clarity) / count if count else 0.0
        mean_n = sum(natural) / count if count else 0.0
        out[voice] = dict(sex="female" if voice.startswith("af_") else "male", count=count,
                          clarity=mean_c, natural=mean_n, total=mean_c + mean_n,
                          spread=max(per_sheet) - min(per_sheet) if per_sheet else 0.0)
    return out


def pick(summary):
    """Per sex: the winning voice, whether it is tied, and whether it is too weak to accept."""
    winners = {}
    for sex in ("female", "male"):
        ranked = sorted(((v, s) for v, s in summary.items() if s["sex"] == sex),
                        key=lambda item: -item[1]["total"])
        if not ranked:
            continue
        best_voice, best = ranked[0]
        tied = [v for v, s in ranked if abs(s["total"] - best["total"]) < 1e-9]
        winners[sex] = dict(voice=best_voice, tied=tied if len(tied) > 1 else [],
                            weak=best["clarity"] < MIN_ACCEPTABLE or best["natural"] < MIN_ACCEPTABLE)
    return winners


def find_sheets(key_dir):
    found = {}
    for folder in (key_dir, key_dir.parent):
        for path in sorted(folder.glob("sheet_R*.csv")):
            found.setdefault(path.stem.removeprefix("sheet_"), path)
    return found


def main():
    from _paths import KEY_DIR
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    key_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else KEY_DIR
    key = {r["sample"]: r for r in read_csv(key_dir / "key.csv")}
    paths = find_sheets(key_dir)
    sheets, reasons = {}, []
    for rater, path in paths.items():
        rows = read_csv(path)
        bad = check_sheet(rows, key, path.name)
        reasons += bad
        if not bad:
            sheets[rater] = rows

    print(f"sheets: {len(sheets)} complete of {SHEETS_NEEDED} needed "
          f"({', '.join(sheets) or 'none'}); one listener, {len(sheets)} sitting(s)")
    for reason in reasons:
        print("not counted -", reason)

    measures = key_dir / "measures.csv"
    if measures.exists():
        print("\nmeasured, not scored (words only)")
        print(f"{'voice':12} {'mean ms':>8} {'raw LUFS':>9}")
        rows = [r for r in read_csv(measures) if r["kind"] == "word"]
        for voice in sorted({r["voice"] for r in rows}):
            mine = [r for r in rows if r["voice"] == voice]
            print(f"{voice:12} {sum(int(r['duration_ms']) for r in mine) / len(mine):8.0f} "
                  f"{sum(float(r['raw_lufs']) for r in mine) / len(mine):9.1f}")

    if not sheets:
        sys.exit("\nno complete sheet yet. Winners are not named.")
    summary = summarise(key, sheets)
    print("\nscores")
    print(f"{'voice':12} {'sex':7} {'rows':>4} {'clarity':>8} {'natural':>8} {'sum':>6} {'spread':>7}")
    for voice, s in sorted(summary.items(), key=lambda item: (item[1]["sex"], -item[1]["total"])):
        print(f"{voice:12} {s['sex']:7} {s['count']:4d} {s['clarity']:8.2f} {s['natural']:8.2f} "
              f"{s['total']:6.2f} {s['spread']:7.2f}")

    with open(key_dir / "scores.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rater", "order", "sample", "voice", "sex", "kind", "text", "clarity", "natural"])
        for rater, rows in sheets.items():
            for r in rows:
                k = key[r["sample"]]
                writer.writerow([rater, r.get("order", ""), r["sample"], k["voice"], k["sex"],
                                 k["kind"], k["text"], r["clarity"], r["natural"]])

    if len(sheets) < SHEETS_NEEDED:
        sys.exit(f"\n{len(sheets)} of {SHEETS_NEEDED} sheets. Winners are not named yet.")
    print("\nchosen")
    for sex, w in pick(summary).items():
        note = ""
        if w["tied"]:
            note += f"  TIE between {', '.join(w['tied'])}: decide by ear"
        if w["weak"]:
            note += f"  BELOW {MIN_ACCEPTABLE} on one score: consider the backup voice set"
        print(f"{sex:7} {w['voice']}{note}")


if __name__ == "__main__":
    main()
