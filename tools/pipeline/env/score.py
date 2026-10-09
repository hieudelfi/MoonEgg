"""Turn the rating sheets of task P.4 into one female and one male voice.

Run with any Python 3.11+:
    python tools/pipeline/env/score.py

Reads _key/key.csv and exactly sheet_R1.csv, sheet_R2.csv, sheet_R3.csv, looked for in sheets/
next to the rating page, then in _key/, then beside the page. Nothing about any voice is printed
or written until all three sheets are complete: an early look would end the blind test.

The three sheets are three sittings of one listener. They show how steady that listener is, not
whether other people agree.
"""
import csv
import re
import sys
from pathlib import Path

RATERS = ("R1", "R2", "R3")
SHEET_NAME = re.compile(r"^sheet_(R[1-3])\.csv$")
# Below this mean on either score, the best voice of a sex is not good enough to pick.
MIN_ACCEPTABLE = 3.0
# A sitting where most rows carry the same number twice may come from a held key.
SAME_SCORE_SHARE = 0.7


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def check_sheet(rows, key, name, rater=None):
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
    if rater is not None:
        inside = sorted({r.get("rater", "") for r in rows})
        if inside != [rater]:
            reasons.append(f"{name}: rater code inside is {inside}, the file name says {rater}")
    for r in rows:
        for field in ("clarity", "natural"):
            if r.get(field) not in ("1", "2", "3", "4", "5"):
                reasons.append(f"{name}: {r.get('sample')} has {field}={r.get(field)!r}")
                break
    return reasons


def scores_of(rows):
    return {r["sample"]: (r["clarity"], r["natural"]) for r in rows}


def find_sheets(key_dir):
    """Return ({rater: path}, [ignored file names]). Only the three exact names count."""
    found, ignored = {}, []
    for folder in (key_dir.parent / "sheets", key_dir, key_dir.parent):
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("sheet_*.csv")):
            match = SHEET_NAME.match(path.name)
            if not match:
                ignored.append(path.name)
            elif match.group(1) in found:
                ignored.append(f"{path.name} in {folder.name}/ (already found elsewhere)")
            else:
                found[match.group(1)] = path
    return found, ignored


def summarise(key, sheets):
    """Per voice: count, mean of each score, their sum, the sum per sitting, and its spread."""
    out = {}
    for voice in sorted({k["voice"] for k in key.values()}):
        clarity, natural, per_sheet = [], [], {}
        for rater, rows in sheets.items():
            mine = [r for r in rows if key[r["sample"]]["voice"] == voice]
            c = [int(r["clarity"]) for r in mine]
            n = [int(r["natural"]) for r in mine]
            clarity += c
            natural += n
            if mine:
                per_sheet[rater] = sum(c) / len(c) + sum(n) / len(n)
        count = len(clarity)
        mean_c = sum(clarity) / count if count else 0.0
        mean_n = sum(natural) / count if count else 0.0
        sex = next(k["sex"] for k in key.values() if k["voice"] == voice)
        totals = list(per_sheet.values())
        out[voice] = dict(sex=sex, count=count, clarity=mean_c, natural=mean_n,
                          total=mean_c + mean_n, per_sheet=per_sheet,
                          spread=max(totals) - min(totals) if totals else 0.0)
    return out


def pick(summary):
    """Per sex: the winner, ties, weakness, and how steady the lead is across sittings."""
    winners = {}
    for sex in sorted({s["sex"] for s in summary.values()}):
        ranked = sorted(((v, s) for v, s in summary.items() if s["sex"] == sex),
                        key=lambda item: -item[1]["total"])
        best_voice, best = ranked[0]
        tied = [v for v, s in ranked if abs(s["total"] - best["total"]) < 1e-9]
        margin = best["total"] - ranked[1][1]["total"] if len(ranked) > 1 else None
        led = [rater for rater in best["per_sheet"]
               if all(best["per_sheet"][rater] >= s["per_sheet"].get(rater, 0.0) for _, s in ranked)]
        # A sitting that scores everything lower widens the spread without changing the order,
        # so the spread alone is not a sign of doubt. Losing a sitting is.
        unsteady = len(led) < len(best["per_sheet"])
        winners[sex] = dict(voice=best_voice, tied=tied if len(tied) > 1 else [],
                            weak=best["clarity"] < MIN_ACCEPTABLE or best["natural"] < MIN_ACCEPTABLE,
                            margin=margin, led=led, sittings=len(best["per_sheet"]),
                            unsteady=unsteady and len(tied) < 2)
    return winners


def load(key_dir):
    """Return (key, complete sheets, messages). A sheet with any problem is left out."""
    key = {r["sample"]: r for r in read_csv(key_dir / "key.csv")}
    paths, ignored = find_sheets(key_dir)
    messages = [f"ignored - {name}: only sheet_R1.csv, sheet_R2.csv, sheet_R3.csv count"
                for name in ignored]
    sheets = {}
    for rater in RATERS:
        if rater not in paths:
            continue
        rows = read_csv(paths[rater])
        problems = check_sheet(rows, key, paths[rater].name, rater)
        twin = next((other for other, kept in sheets.items()
                     if not problems and scores_of(kept) == scores_of(rows)), None)
        if twin:
            problems.append(f"{paths[rater].name}: every score equals {twin}; a copy, not a sitting")
        messages += [f"not counted - {p}" for p in problems]
        if not problems:
            sheets[rater] = rows
    return key, sheets, messages


def main():
    from _paths import KEY_DIR
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    key_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else KEY_DIR
    key, sheets, messages = load(key_dir)

    print(f"sheets: {len(sheets)} complete of {len(RATERS)} needed "
          f"({', '.join(sheets) or 'none'}); one listener, {len(sheets)} sitting(s)")
    for message in messages:
        print(message)
    if len(sheets) < len(RATERS):
        sys.exit("\nNothing about the voices is shown before all three sittings are in.")

    for rater, rows in sheets.items():
        same = sum(1 for r in rows if r["clarity"] == r["natural"])
        if same / len(rows) > SAME_SCORE_SHARE:
            print(f"note - {rater}: {same} of {len(rows)} rows have the same number for both "
                  f"scores. Check that this sitting was not scored with a held or doubled key.")

    measures = key_dir / "measures.csv"
    if measures.exists():
        print("\nmeasured, not scored (words only)")
        print(f"{'voice':12} {'mean ms':>8} {'raw LUFS':>9} {'limiter dB':>11}")
        rows = [r for r in read_csv(measures) if r["kind"] == "word"]
        for voice in sorted({r["voice"] for r in rows}):
            mine = [r for r in rows if r["voice"] == voice]
            raw = sum(float(r["raw_lufs"]) for r in mine) / len(mine)
            # Gain beyond plain levelling: what the limiter took off the peaks and had to give back.
            extra = sum(float(r["gain_db"]) - (float(r["out_lufs"]) - float(r["raw_lufs"]))
                        for r in mine) / len(mine)
            print(f"{voice:12} {sum(int(r['duration_ms']) for r in mine) / len(mine):8.0f} "
                  f"{raw:9.1f} {extra:11.1f}")

    summary = summarise(key, sheets)
    print("\nscores")
    head = "  ".join(f"{r:>5}" for r in sheets)
    print(f"{'voice':12} {'sex':7} {'rows':>4} {'clarity':>8} {'natural':>8} {'sum':>6} {'spread':>7}  {head}")
    for voice, s in sorted(summary.items(), key=lambda item: (item[1]["sex"], -item[1]["total"])):
        per = "  ".join(f"{s['per_sheet'][r]:5.2f}" for r in sheets)
        print(f"{voice:12} {s['sex']:7} {s['count']:4d} {s['clarity']:8.2f} {s['natural']:8.2f} "
              f"{s['total']:6.2f} {s['spread']:7.2f}  {per}")

    with open(key_dir / "scores.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rater", "order", "sample", "voice", "sex", "kind", "text", "clarity", "natural"])
        for rater, rows in sheets.items():
            for r in rows:
                k = key[r["sample"]]
                writer.writerow([rater, r.get("order", ""), r["sample"], k["voice"], k["sex"],
                                 k["kind"], k["text"], r["clarity"], r["natural"]])

    print("\nchosen")
    for sex, w in pick(summary).items():
        note = ""
        if w["tied"]:
            note += f"  TIE between {', '.join(w['tied'])}: decide by ear"
        if w["unsteady"]:
            note += (f"  UNSTEADY: leads in {len(w['led'])} of {w['sittings']} sittings, "
                     f"overall margin {w['margin']:.2f}: confirm by ear")
        elif w["margin"] is not None:
            note += f"  leads in every sitting, margin {w['margin']:.2f}"
        if w["weak"]:
            note += f"  BELOW {MIN_ACCEPTABLE} on one score: consider the backup voice set"
        print(f"{sex:7} {w['voice']}{note}")


if __name__ == "__main__":
    main()
