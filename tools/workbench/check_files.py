"""Data check for the working files of the content workbench.

    python tools/workbench/check_files.py <working folder> [--lexicon <csv>] [--for-pack]

tools/checks/verify_pack.py reads word rows only, so the three record files need their own check:
unique IDs, links that resolve, valid statuses, source and licence on every record, and no word
approved on too little. With --for-pack any record marked note=draft is an error as well.
Exits 1 when there is an error.
"""
import collections
import sys
from pathlib import Path

from review import CHECK_NAMES, licence_ok, load_allowlist
from store import ID_COLUMN, STATUSES, Folder, read_table

DEFAULT_LEXICON = Path(__file__).resolve().parents[2] / "content" / "lexicon" / "lexicon_raw_test.csv"


def check(folder, lexicon_rows, allow, for_pack=False):
    """Return (errors, counts of statuses per table)."""
    errors, counts = [], {}
    words = {row["item_id"] for row in lexicon_rows}
    sense_ids = {row["sense_id"] for row in folder.rows["senses"]}
    for table in ("senses", "examples", "images"):
        key = ID_COLUMN[table]
        seen = collections.Counter(row[key] for row in folder.rows[table])
        errors += [f"{table}: duplicate id {i}" for i, n in seen.items() if n > 1]
        counts[table] = collections.Counter(row["review_status"] or "pending"
                                            for row in folder.rows[table])
        for row in folder.rows[table]:
            name = f"{table} {row[key]}"
            if row["item_id"] not in words:
                errors.append(f"{name}: item_id {row['item_id']!r} is not in the lexicon")
            if (row["review_status"] or "pending") not in STATUSES:
                errors.append(f"{name}: status {row['review_status']!r} is not valid")
            if not row["source"].strip():
                errors.append(f"{name}: source is empty")
            if not licence_ok(row["license"], allow):
                errors.append(f"{name}: licence {row['license']!r} is not on the allowlist")
            if for_pack and row["note"] == "draft":
                errors.append(f"{name}: a draft cannot be packed")
        if table == "senses":
            for row in folder.rows[table]:
                if row["gloss_vi"].strip() and (not row["gloss_source"].strip()
                                                or not licence_ok(row["gloss_license"], allow)):
                    errors.append(f"senses {row['sense_id']}: the Vietnamese meaning has no "
                                  f"source or an unlisted licence")
        if table == "examples":
            for row in folder.rows[table]:
                if row["sense_id"] and row["sense_id"] not in sense_ids:
                    errors.append(f"examples {row['example_id']}: sense_id {row['sense_id']!r} "
                                  f"does not exist")
                checks = row["checks"]
                if checks and (len(checks) != len(CHECK_NAMES) or set(checks) - {"0", "1"}):
                    errors.append(f"examples {row['example_id']}: checks {checks!r} is not "
                                  f"{len(CHECK_NAMES)} bits")
    counts["words"] = collections.Counter(row["review_status"] or "pending"
                                          for row in folder.rows["word_review"])
    for row in folder.rows["word_review"]:
        item_id = row["item_id"]
        if item_id not in words:
            errors.append(f"word_review {item_id}: not in the lexicon")
        if row["review_status"] == "approved":
            senses = [r for r in folder.of_word("senses", item_id) if r["review_status"] == "approved"]
            examples = [r for r in folder.of_word("examples", item_id) if r["review_status"] == "approved"]
            if len(senses) < 1 or len(examples) < 2:
                errors.append(f"word_review {item_id}: approved with {len(senses)} approved "
                              f"meanings and {len(examples)} approved sentences")
    return errors, counts


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    lexicon = Path(argv[argv.index("--lexicon") + 1]) if "--lexicon" in argv else DEFAULT_LEXICON
    args = [a for a in args if Path(a) != lexicon]
    folder = Folder(args[0])
    _, lexicon_rows = read_table(lexicon)
    errors, counts = check(folder, lexicon_rows, load_allowlist(), "--for-pack" in argv)
    for table, by_status in counts.items():
        shown = ", ".join(f"{status} {by_status.get(status, 0)}" for status in STATUSES)
        print(f"{table:9} {sum(by_status.values()):4d} rows: {shown}")
    for error in errors[:40]:
        print("ERROR", error)
    if len(errors) > 40:
        print(f"... and {len(errors) - 40} more")
    print(f"{len(errors)} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
