"""Build the trial working folder for the content workbench: 30 test words, everything pending.

    python tools/workbench/seed_trial.py [<working folder>]      default: content/pack/trial

Meanings come from the WordNet definitions already in the test lexicon. The Vietnamese meanings
and the sentences are drafts from tools/workbench/trial_drafts.json, marked note=draft. Four plain
SVG pictures are drawn for five words, so the image keys have something to act on. Nothing here
may be packed: export.py and check_files.py --for-pack refuse drafts.

The folder is rebuilt from scratch. It refuses to run when the folder already holds review work.
"""
import json
import sys
from pathlib import Path

from store import COLUMNS, read_table, write_table

REPO = Path(__file__).resolve().parents[2]
CONTENT = REPO / "content"
LEXICON = CONTENT / "lexicon" / "lexicon_raw_test.csv"
DRAFTS = Path(__file__).with_name("trial_drafts.json")
WORDNET = "https://wordnet.princeton.edu/"
WITH_IMAGES = ["w:market#1", "w:umbrella#1", "w:kettle#1", "w:egg#1", "w:rain#1"]
COLOURS = ["#f4b860", "#7cc4ff", "#c4f47c", "#c8a4ff"]


def slug(item_id):
    return "".join(c if c.isalnum() else "_" for c in item_id)


def picture(word, slot, colour):
    """A placeholder, not an illustration: a coloured card with the word and the slot number."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" role="img" '
            f'aria-label="placeholder {slot} for {word}">\n'
            f'<rect width="240" height="240" fill="{colour}"/>\n'
            f'<circle cx="{60 + 40 * slot}" cy="{70 + 20 * slot}" r="{28 + 4 * slot}" fill="#ffffff" opacity="0.7"/>\n'
            f'<text x="120" y="190" font-family="sans-serif" font-size="26" text-anchor="middle" '
            f'fill="#1d2433">{word} {slot}</text>\n</svg>\n')


def row(table, **values):
    out = {column: "" for column in COLUMNS[table]}
    out.update(values)
    return out


def build(folder):
    _, lexicon = read_table(LEXICON)
    drafts = json.loads(DRAFTS.read_text(encoding="utf-8"))
    senses, examples, images = [], [], []
    for word in lexicon:
        item_id, draft = word["item_id"], drafts[word["item_id"]]
        definitions = [d.strip() for d in word["wn_defs"].split("|") if d.strip()]
        for n, definition in enumerate(definitions, 1):
            gloss = draft["gloss"][n - 1] if n <= len(draft["gloss"]) else ""
            senses.append(row("senses", sense_id=f"{item_id}/s{n}", item_id=item_id, order=str(n),
                              def_en_simple=definition, gloss_vi=gloss, chosen="0",
                              source=WORDNET, license="WordNet",
                              gloss_source="self" if gloss else "", gloss_license="own" if gloss else "",
                              review_status="pending", note="draft" if gloss else ""))
        first_sense = f"{item_id}/s1" if definitions else ""
        for n, (en, vi) in enumerate(draft["examples"], 1):
            examples.append(row("examples", example_id=f"{item_id}/e{n}", sense_id=first_sense,
                                item_id=item_id, en=en, vi=vi, difficulty="1", checks="00000",
                                chosen="0", source="self", license="own", review_status="pending",
                                note="draft"))
        if item_id in WITH_IMAGES:
            for slot in range(1, 5):
                path = folder / "images" / f"{slug(item_id)}_{slot}.svg"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(picture(word["headword"], slot, COLOURS[slot - 1]),
                                encoding="utf-8", newline="\n")
                images.append(row("images", image_id=f"{item_id}/i{slot}", item_id=item_id,
                                  slot=str(slot), path=path.relative_to(CONTENT).as_posix(),
                                  chosen="0", source="self", license="own",
                                  review_status="pending", note="draft"))
    return dict(senses=senses, examples=examples, images=images, word_review=[])


def main(argv):
    folder = Path(argv[0]) if argv else CONTENT / "pack" / "trial"
    folder = folder.resolve()
    if CONTENT.resolve() not in folder.parents:
        sys.exit(f"{folder} is not under {CONTENT}: the workbench serves pictures from content/ only")
    _, done = read_table(folder / "word_review.csv")
    if done:
        sys.exit(f"{folder} already holds review work ({len(done)} words). Delete word_review.csv "
                 f"to rebuild on purpose.")
    folder.mkdir(parents=True, exist_ok=True)
    tables = build(folder)
    for name, rows in tables.items():
        write_table(folder / f"{name}.csv", COLUMNS[name], rows)
    (folder / "README.md").write_text(
        "# Thư mục thử của xưởng nội dung\n\n"
        "Dữ liệu ở đây là **bản nháp** do phiên dựng task P.5 viết ra để thử công cụ: nghĩa Việt, câu ví dụ\n"
        "và ảnh giữ chỗ đều mang `note=draft`. **Không được đóng gói.** `export.py` và\n"
        "`check_files.py --for-pack` từ chối bản nháp. Dựng lại bằng `python tools/workbench/seed_trial.py`.\n",
        encoding="utf-8", newline="\n")
    print(f"{folder}: {len(tables['senses'])} meanings, {len(tables['examples'])} sentences, "
          f"{len(tables['images'])} pictures, all pending")


if __name__ == "__main__":
    main(sys.argv[1:])
