"""Write the reviewed word list that tools/checks/verify_pack.py --strict reads.

    python tools/workbench/export.py <working folder> [--lexicon <csv>] [--trial]

One row per approved word, written inside the working folder as lexicon_reviewed.csv. Approved
records marked note=draft are seed text and must never reach a pack: the export refuses them.
With --trial it accepts them and writes lexicon_reviewed_trial.csv instead.
"""
import sys
from pathlib import Path

from store import Folder, read_table, write_table

DEFAULT_LEXICON = Path(__file__).resolve().parents[2] / "content" / "lexicon" / "lexicon_raw_test.csv"
EXTRA = ["gloss_vi", "n_senses", "n_examples", "image_asset", "review_status", "reviewed_by",
         "reviewed_at"]


class DraftsFound(Exception):
    pass


def approved_of(folder, table, item_id):
    rows = [r for r in folder.of_word(table, item_id) if r["review_status"] == "approved"]
    return sorted(rows, key=lambda r: (r.get("order") or r.get("slot") or "", r[next(iter(r))]))


def build(folder, lexicon_rows, trial=False):
    """Return (rows, words without an image). Raises DraftsFound outside a trial."""
    rows, no_image, drafts = [], [], []
    for word in lexicon_rows:
        item_id = word["item_id"]
        status = folder.word(item_id)
        if status["review_status"] != "approved":
            continue
        senses = approved_of(folder, "senses", item_id)
        examples = approved_of(folder, "examples", item_id)
        images = approved_of(folder, "images", item_id)
        drafts += [r[k] for r, k in [(s, "sense_id") for s in senses]
                   + [(e, "example_id") for e in examples] + [(i, "image_id") for i in images]
                   if r["note"] == "draft"]
        if not images:
            no_image.append(item_id)
        rows.append({**word,
                     "gloss_vi": "; ".join(s["gloss_vi"] for s in senses),
                     "n_senses": str(len(senses)),
                     "n_examples": str(len(examples)),
                     "image_asset": images[0]["path"] if images else "",
                     "review_status": "approved",
                     "reviewed_by": status["reviewed_by"],
                     "reviewed_at": status["second_at"] or status["reviewed_at"]})
    if drafts and not trial:
        raise DraftsFound(f"{len(drafts)} approved records are drafts, for example {drafts[:3]}. "
                          f"Drafts are trial text. Use --trial, or review real candidates.")
    return rows, no_image


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    trial = "--trial" in argv
    lexicon = Path(argv[argv.index("--lexicon") + 1]) if "--lexicon" in argv else DEFAULT_LEXICON
    args = [a for a in args if Path(a) != lexicon]
    folder = Folder(args[0])
    header, lexicon_rows = read_table(lexicon)
    try:
        rows, no_image = build(folder, lexicon_rows, trial)
    except DraftsFound as problem:
        sys.exit(f"refused: {problem}")
    out = folder.path / ("lexicon_reviewed_trial.csv" if trial else "lexicon_reviewed.csv")
    write_table(out, header + EXTRA, rows)
    print(f"{len(rows)} approved words written to {out}")
    print(f"no image: {len(no_image)} words {no_image[:10]}{' ...' if len(no_image) > 10 else ''}")


if __name__ == "__main__":
    main(sys.argv[1:])
