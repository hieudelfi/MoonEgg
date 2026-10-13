"""Working files of the content workbench: read them, keep them in memory, save them safely.

One working folder holds senses.csv, examples.csv, images.csv, word_review.csv and review_log.csv.
The shape is written down in docs/07-kien-truc.md section 5.5.

A save writes a temporary file and renames it over the old one, so a crash cannot leave half a
file. Files are UTF-8 with LF line ends and minimal quoting: a save changes only the rows that
really changed, which keeps git diffs readable. Columns this code does not know are kept in place.
"""
import csv
import io
import os
from pathlib import Path

REVIEW_FIELDS = ["review_status", "reviewed_by", "reviewed_at", "second_by", "second_at",
                 "source_checked_by", "source_checked_at"]
COLUMNS = {
    "senses": ["sense_id", "item_id", "order", "def_en_simple", "gloss_vi", "collocations_json",
               "chosen", "source", "license", "gloss_source", "gloss_license", *REVIEW_FIELDS, "note"],
    "examples": ["example_id", "sense_id", "item_id", "en", "vi", "difficulty", "audio_asset_f",
                 "audio_asset_m", "checks", "chosen", "source", "license", *REVIEW_FIELDS, "note"],
    "images": ["image_id", "item_id", "slot", "path", "chosen", "reject_reason", "source",
               "license", *REVIEW_FIELDS, "note"],
    "word_review": ["item_id", "review_status", "reviewed_by", "reviewed_at", "second_by",
                    "second_at", "reject_reason"],
    "review_log": ["at", "reviewer", "pass", "item_id", "action", "target", "seconds"],
}
ID_COLUMN = {"senses": "sense_id", "examples": "example_id", "images": "image_id",
             "word_review": "item_id"}
STATUSES = ("pending", "approved", "rejected", "needs_second")


class Stale(Exception):
    """The file on disk changed since this process last read or wrote it."""


def to_text(header, rows):
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=header, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def read_table(path):
    """Return (header, rows). A missing file is an empty table with no header."""
    path = Path(path)
    if not path.exists():
        return [], []
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = [{k: (v or "") for k, v in row.items() if k is not None} for row in reader]
        return list(reader.fieldnames or []), rows


def write_table(path, header, rows):
    """Write through a temporary file in the same folder, then rename over the target."""
    path = Path(path)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(to_text(header, rows))
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def stamp(path):
    path = Path(path)
    if not path.exists():
        return None
    info = path.stat()
    return (info.st_size, info.st_mtime_ns)


class Folder:
    """The tables of one working folder, loaded once and saved one table at a time."""

    def __init__(self, path):
        self.path = Path(path)
        self.header, self.rows, self._stamp = {}, {}, {}
        for name in ("senses", "examples", "images", "word_review"):
            self.load(name)

    def file(self, name):
        return self.path / f"{name}.csv"

    def load(self, name):
        header, rows = read_table(self.file(name))
        # Known columns first appear in their documented order only for a new file.
        self.header[name] = header or list(COLUMNS[name])
        for column in COLUMNS[name]:
            if column not in self.header[name]:
                self.header[name].append(column)
        for row in rows:
            for column in self.header[name]:
                row.setdefault(column, "")
        self.rows[name] = rows
        self._stamp[name] = stamp(self.file(name))

    def save(self, name):
        if stamp(self.file(name)) != self._stamp[name]:
            raise Stale(f"{name}.csv changed on disk since it was read")
        write_table(self.file(name), self.header[name], self.rows[name])
        self._stamp[name] = stamp(self.file(name))

    def of_word(self, name, item_id):
        return [row for row in self.rows[name] if row["item_id"] == item_id]

    def find(self, name, record_id):
        column = ID_COLUMN[name]
        for row in self.rows[name]:
            if row[column] == record_id:
                return row
        raise KeyError(f"{name}: no record {record_id!r}")

    def word(self, item_id):
        """The status row of a word, created as pending when it does not exist yet."""
        for row in self.rows["word_review"]:
            if row["item_id"] == item_id:
                return row
        row = {column: "" for column in self.header["word_review"]}
        row.update(item_id=item_id, review_status="pending")
        self.rows["word_review"].append(row)
        return row

    def append_log(self, entry):
        """The log is append only: one line is added, nothing is rewritten."""
        path = self.file("review_log")
        header = COLUMNS["review_log"]
        new = not path.exists()
        with open(path, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
            if new:
                writer.writeheader()
            writer.writerow({column: entry.get(column, "") for column in header})
