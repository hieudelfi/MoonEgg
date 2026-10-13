"""Seconds per word, from the review log of a working folder.

    python tools/workbench/report.py <working folder> [--lexicon <csv>]

The log holds one row per visit to a word. A word's time is the sum of its visits. Only words
with a decision (approved, needs_second or rejected) are counted in the averages. Seconds per
sentence are not measured: the timer runs per word.
"""
import collections
import statistics
import sys
from pathlib import Path

from store import Folder, read_table

DEFAULT_LEXICON = Path(__file__).resolve().parents[2] / "content" / "lexicon" / "lexicon_raw_test.csv"
TARGET_SECONDS = 180
LONG_VISIT_SECONDS = 15 * 60
DECISIONS = ("approved", "needs_second", "rejected")


def summarise(log_rows, word_status, lexicon_ids, senses_by_word):
    """Return a dict with the numbers the report prints."""
    seconds = collections.defaultdict(float)
    for row in log_rows:
        if row["action"] == "visit" and row["seconds"]:
            seconds[row["item_id"]] += float(row["seconds"])
    decided = [i for i in lexicon_ids if word_status.get(i) in DECISIONS]
    timed = [seconds[i] for i in decided if seconds[i] > 0]
    return dict(
        decided=len(decided),
        by_status=collections.Counter(word_status.get(i, "pending") for i in lexicon_ids),
        timed=len(timed),
        mean=statistics.mean(timed) if timed else None,
        median=statistics.median(timed) if timed else None,
        slowest=max(((seconds[i], i) for i in decided), default=None),
        long_words=sorted(i for i in decided if seconds[i] > LONG_VISIT_SECONDS),
        waiting=sorted(i for i in lexicon_ids
                       if word_status.get(i, "pending") == "pending" and not senses_by_word.get(i)),
    )


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
    _, log_rows = read_table(folder.file("review_log"))
    status = {row["item_id"]: row["review_status"] for row in folder.rows["word_review"]}
    senses = collections.Counter(row["item_id"] for row in folder.rows["senses"])
    s = summarise(log_rows, status, [row["item_id"] for row in lexicon_rows], senses)
    print(f"words: {len(lexicon_rows)} | " + ", ".join(f"{k} {v}" for k, v in sorted(s["by_status"].items())))
    print(f"words with a decision: {s['decided']} (timed: {s['timed']})")
    if s["timed"]:
        print(f"seconds per word: mean {s['mean']:.1f}, median {s['median']:.1f}, "
              f"slowest {s['slowest'][0]:.1f} ({s['slowest'][1]})")
        print(f"target from the plan: {TARGET_SECONDS} seconds per word. "
              f"Measured mean is {s['mean'] / TARGET_SECONDS:.0%} of it.")
    else:
        print("seconds per word: no timed visit yet")
    print(f"over 15 minutes: {s['long_words'] or 'none'}")
    print(f"waiting for candidates (no meaning to choose): {s['waiting'] or 'none'}")
    print("seconds per sentence: not measured, the timer runs per word")


if __name__ == "__main__":
    main(sys.argv[1:])
