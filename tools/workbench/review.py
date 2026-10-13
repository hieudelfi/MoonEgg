"""Review rules of the content workbench. No HTTP here, so the tests run it directly.

The model, as approved in docs/tasks/P.5/Plan.md section 4.3:
- Choosing a record, ticking a check and picking an image are saved at once. Statuses stay.
- An edit is saved at once and puts the record in needs_second. A sentence loses its five ticks.
- Approve checks rules R1 to R7 on the chosen records, then decides the statuses.
- Reject touches the word only, and can be undone.
"""
from datetime import datetime, timezone
from pathlib import Path

from store import Folder

CHECK_NAMES = ["Đúng ngữ pháp", "Tự nhiên", "Không nhạy cảm", "Nghĩa Việt khớp", "Đúng dạng từ"]
ALL_TICKED = "1" * len(CHECK_NAMES)
NO_TICKS = "0" * len(CHECK_NAMES)
MAX_GLOSS_WORDS = 8
SENTENCE_WORDS = (6, 12)
ALLOWLIST = Path(__file__).resolve().parents[1] / "checks" / "license-allowlist.txt"
EDITABLE = {"senses": ("gloss_vi",), "examples": ("en", "vi")}


class Refused(Exception):
    """A rule failed. Nothing about any status was changed."""

    def __init__(self, rule, message):
        super().__init__(message)
        self.rule, self.message = rule, message


def load_allowlist(path=ALLOWLIST):
    return {line.strip() for line in open(path, encoding="utf-8") if line.strip()}


def licence_ok(value, allow):
    """A licence cell may list several licences, split by ';' or ','. All must be allowed."""
    parts = [p.strip() for p in value.replace(",", ";").split(";") if p.strip()]
    return bool(parts) and all(p in allow for p in parts)


def count_words(text):
    return len(text.split())


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Review:
    def __init__(self, folder, reviewer, clock=now_utc, allow=None):
        self.folder = folder if isinstance(folder, Folder) else Folder(folder)
        self.reviewer = reviewer
        self.clock = clock
        self.allow = allow if allow is not None else load_allowlist()

    # --- small helpers -------------------------------------------------------------------

    def _log(self, item_id, action, target="", seconds="", pass_=""):
        self.folder.append_log(dict(at=self.clock(), reviewer=self.reviewer, item_id=item_id,
                                    action=action, target=target, seconds=seconds,
                                    **{"pass": pass_}))

    def _reopen(self, item_id, record=None):
        """A change on a decided word puts the word, and the changed record, back to pending."""
        word = self.folder.word(item_id)
        if word["review_status"] in ("approved", "rejected"):
            word["review_status"] = "pending"
            self.folder.save("word_review")
            self._log(item_id, "reopen")
        if record is not None and record["review_status"] in ("approved", "rejected"):
            record["review_status"] = "pending"

    def queue_of(self, item_id):
        return 2 if self.folder.word(item_id)["review_status"] == "needs_second" else 1

    # --- saved at once, statuses stay ----------------------------------------------------

    def set_chosen(self, table, record_id, chosen):
        record = self.folder.find(table, record_id)
        self._reopen(record["item_id"], record)
        record["chosen"] = "1" if chosen else "0"
        self.folder.save(table)

    def set_check(self, example_id, index, value):
        record = self.folder.find("examples", example_id)
        self._reopen(record["item_id"], record)
        checks = list((record["checks"] or NO_TICKS).ljust(len(CHECK_NAMES), "0"))
        checks[index] = "1" if value else "0"
        record["checks"] = "".join(checks)
        self.folder.save("examples")

    def tick_all(self, example_id):
        record = self.folder.find("examples", example_id)
        self._reopen(record["item_id"], record)
        record["checks"] = ALL_TICKED
        self.folder.save("examples")

    def pick_image(self, item_id, slot):
        images = self.folder.of_word("images", item_id)
        if str(slot) not in {image["slot"] for image in images}:
            raise Refused("R7", f"Không có ảnh số {slot}")
        self._reopen(item_id)
        for image in images:
            image["chosen"] = "1" if image["slot"] == str(slot) else "0"
            image["reject_reason"] = ""
            image["review_status"] = "pending"
        self.folder.save("images")

    def reject_images(self, item_id, reason):
        if not reason.strip():
            raise Refused("R7", "Cần ghi lý do loại cả bốn ảnh")
        images = self.folder.of_word("images", item_id)
        self._reopen(item_id)
        for image in images:
            image.update(chosen="0", reject_reason=reason.strip(), review_status="rejected",
                         reviewed_by=self.reviewer, reviewed_at=self.clock())
        self.folder.save("images")
        self._log(item_id, "reject_images", reason.strip())

    def source_checked(self, table, record_id):
        record = self.folder.find(table, record_id)
        record["source_checked_by"], record["source_checked_at"] = self.reviewer, self.clock()
        self.folder.save(table)

    # --- an edit -------------------------------------------------------------------------

    def edit(self, table, record_id, fields):
        record = self.folder.find(table, record_id)
        changed = {k: v.strip() for k, v in fields.items()
                   if k in EDITABLE[table] and v.strip() != record[k]}
        if not changed:
            return False
        self._reopen(record["item_id"])
        record.update(changed)
        record.update(review_status="needs_second", reviewed_by=self.reviewer,
                      reviewed_at=self.clock(), second_by="", second_at="")
        if table == "examples":
            # The ticks were given to the old text. They do not carry over.
            record["checks"] = NO_TICKS
        self.folder.save(table)
        self._log(record["item_id"], "edit", record_id)
        return True

    # --- approve -------------------------------------------------------------------------

    def check_rules(self, item_id):
        """Raise Refused for the first of R1 to R7 that fails. Change nothing."""
        senses = [r for r in self.folder.of_word("senses", item_id) if r["chosen"] == "1"]
        examples = [r for r in self.folder.of_word("examples", item_id) if r["chosen"] == "1"]
        images = self.folder.of_word("images", item_id)
        if not 1 <= len(senses) <= 3:
            raise Refused("R1", "Cần chọn 1 đến 3 nghĩa")
        for sense in senses:
            if not 1 <= count_words(sense["gloss_vi"]) <= MAX_GLOSS_WORDS:
                raise Refused("R2", f"Nghĩa Việt tối đa {MAX_GLOSS_WORDS} từ, và không để trống")
        if not 2 <= len(examples) <= 3:
            raise Refused("R3", "Cần 2 đến 3 câu")
        for example in examples:
            if not SENTENCE_WORDS[0] <= count_words(example["en"]) <= SENTENCE_WORDS[1]:
                raise Refused("R4", "Câu phải dài 6 đến 12 từ")
        for example in examples:
            if example["checks"] != ALL_TICKED:
                raise Refused("R5", "Mỗi câu được chọn phải đủ 5 mục kiểm")
        picked = [image for image in images if image["chosen"] == "1"]
        for record in senses + examples + picked:
            if not record["source"].strip() or not licence_ok(record["license"], self.allow):
                raise Refused("R6", "Giấy phép không hợp lệ")
        for sense in senses:
            if not sense["gloss_source"].strip() or not licence_ok(sense["gloss_license"], self.allow):
                raise Refused("R6", "Giấy phép không hợp lệ")
        if images and not picked:
            all_rejected = all(i["review_status"] == "rejected" and i["reject_reason"].strip()
                               for i in images)
            if not all_rejected:
                raise Refused("R7", "Chọn ảnh 1 đến 4 hoặc bấm 0")

    def approve(self, item_id):
        """Decide the statuses of a word and its records. Returns the word's new status."""
        self.check_rules(item_id)
        word = self.folder.word(item_id)
        second = word["review_status"] == "needs_second"
        first_decision_at = word["reviewed_at"]
        now = self.clock()
        still_waiting = False
        for table in ("senses", "examples"):
            for record in self.folder.of_word(table, item_id):
                if record["chosen"] != "1":
                    record["review_status"] = "rejected"
                elif record["review_status"] == "needs_second":
                    # In the second pass an edit made before the first decision is confirmed now.
                    # An edit made after it has not been seen by a second pass yet.
                    if second and record["reviewed_at"] <= first_decision_at:
                        record.update(review_status="approved", second_by=self.reviewer, second_at=now)
                    else:
                        still_waiting = True
                elif record["review_status"] != "approved":
                    record.update(review_status="approved", reviewed_by=self.reviewer, reviewed_at=now)
            self.folder.save(table)
        images = self.folder.of_word("images", item_id)
        if any(image["chosen"] == "1" for image in images):
            for image in images:
                if image["chosen"] == "1":
                    image.update(review_status="approved", reviewed_by=self.reviewer, reviewed_at=now)
                else:
                    image["review_status"] = "rejected"
            self.folder.save("images")
        if still_waiting:
            word.update(review_status="needs_second", reviewed_by=self.reviewer, reviewed_at=now,
                        second_by="", second_at="")
        elif second:
            word.update(review_status="approved", second_by=self.reviewer, second_at=now)
        else:
            word.update(review_status="approved", reviewed_by=self.reviewer, reviewed_at=now)
        word["reject_reason"] = ""
        self.folder.save("word_review")
        self._log(item_id, word["review_status"], pass_=2 if second else 1)
        return word["review_status"]

    # --- reject the word, and undo -------------------------------------------------------

    def reject(self, item_id, reason):
        if not reason.strip():
            raise Refused("X", "Cần ghi lý do loại từ")
        word = self.folder.word(item_id)
        word.update(review_status="rejected", reviewed_by=self.reviewer, reviewed_at=self.clock(),
                    reject_reason=reason.strip())
        self.folder.save("word_review")
        self._log(item_id, "reject", reason.strip())

    def undo_reject(self, item_id):
        word = self.folder.word(item_id)
        if word["review_status"] != "rejected":
            raise Refused("U", "Từ này không ở trạng thái Loại")
        word.update(review_status="pending", reject_reason="")
        self.folder.save("word_review")
        self._log(item_id, "undo_reject")

    # --- the timer -----------------------------------------------------------------------

    def log_visit(self, item_id, outcome, seconds, pass_):
        """One row per visit to a word. The report adds up the visits of a word."""
        self._log(item_id, "visit", outcome, f"{max(0.0, float(seconds)):.1f}", pass_)
