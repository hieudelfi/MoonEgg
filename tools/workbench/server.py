"""Local server of the content workbench. Standard library only.

    python tools/workbench/server.py <working folder> --reviewer <short name>
           [--lexicon <csv>] [--audio <folder>] [--port 8765]

Listens on 127.0.0.1 only. Serves one page, a small JSON API, and files under content/ (audio,
pictures, the sheet of mouth shapes). Every rule lives in review.py; this file only carries
requests to it.
"""
import json
import mimetypes
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from review import CHECK_NAMES, MAX_GLOSS_WORDS, SENTENCE_WORDS, Refused, Review, count_words, licence_ok
from store import Stale, read_table

HOST = "127.0.0.1"
REPO = Path(__file__).resolve().parents[2]
STATIC = Path(__file__).resolve().parent / "static"
CONTENT = REPO / "content"
VOICES = (("f", "Nữ", "af_heart"), ("m", "Nam", "am_adam"))
mimetypes.add_type("audio/ogg", ".opus")
mimetypes.add_type("image/svg+xml", ".svg")


def slug(item_id):
    return "".join(c if c.isalnum() else "_" for c in item_id)


def safe_file(root, relative):
    """Resolve a requested path under root. Return None when it escapes root or is no file."""
    root = Path(root).resolve()
    target = (root / relative).resolve()
    if target != root and root not in target.parents:
        return None
    return target if target.is_file() else None


class Workbench:
    """State shared by all requests: the review object, the word list, a revision per word."""

    def __init__(self, folder, reviewer, lexicon, audio_dir):
        self.review = Review(folder, reviewer)
        _, self.lexicon = read_table(lexicon)
        self.by_id = {row["item_id"]: row for row in self.lexicon}
        self.audio_dir = Path(audio_dir)
        self.rev = {}
        self.lock = threading.Lock()

    def words(self, queue):
        out = []
        for row in self.lexicon:
            status = self.review.folder.word(row["item_id"])["review_status"]
            if queue == 2 and status != "needs_second":
                continue
            out.append(dict(item_id=row["item_id"], headword=row["headword"], pos=row["pos"],
                            status=status))
        return out

    def word(self, item_id):
        lex = self.by_id[item_id]
        folder, allow = self.review.folder, self.review.allow
        status = folder.word(item_id)

        def badge(record, licence="license", source="source"):
            return dict(source=record[source], license=record[licence],
                        allowed=licence_ok(record[licence], allow) and bool(record[source].strip()))

        audio = []
        for key, label, voice in VOICES:
            path = self.audio_dir / f"{slug(item_id)}__{voice}.opus"
            if path.is_file() and CONTENT in path.resolve().parents:
                audio.append(dict(label=label, url="/files/" + path.resolve().relative_to(CONTENT).as_posix()))
        return dict(
            item_id=item_id, rev=self.rev.get(item_id, 0), reviewer=self.review.reviewer,
            headword=lex["headword"], pos=lex["pos"], ipa=lex.get("ipa_us", ""),
            sounds=lex.get("viseme_seq", "").split(), status=status["review_status"],
            reject_reason=status["reject_reason"], word_reviewed_at=status["reviewed_at"],
            audio=audio, check_names=CHECK_NAMES,
            limits=dict(gloss=MAX_GLOSS_WORDS, sentence=list(SENTENCE_WORDS)),
            senses=[dict(id=r["sense_id"], definition=r["def_en_simple"], gloss=r["gloss_vi"],
                         chosen=r["chosen"] == "1", status=r["review_status"] or "pending",
                         note=r["note"], gloss_words=count_words(r["gloss_vi"]),
                         badge=badge(r), gloss_badge=badge(r, "gloss_license", "gloss_source"),
                         source_checked=bool(r["source_checked_at"]))
                    for r in sorted(folder.of_word("senses", item_id), key=lambda r: r["order"])],
            examples=[dict(id=r["example_id"], en=r["en"], vi=r["vi"], chosen=r["chosen"] == "1",
                           checks=(r["checks"] or "").ljust(len(CHECK_NAMES), "0"),
                           status=r["review_status"] or "pending", note=r["note"],
                           words=count_words(r["en"]), badge=badge(r),
                           source_checked=bool(r["source_checked_at"]))
                      for r in folder.of_word("examples", item_id)],
            images=[dict(id=r["image_id"], slot=r["slot"], url="/files/" + r["path"],
                         chosen=r["chosen"] == "1", status=r["review_status"] or "pending",
                         reject_reason=r["reject_reason"], badge=badge(r))
                    for r in sorted(folder.of_word("images", item_id), key=lambda r: r["slot"])],
        )

    def act(self, body):
        """Apply one action. Returns (HTTP status, payload)."""
        item_id, action = body.get("item_id", ""), body.get("action", "")
        if item_id not in self.by_id:
            return 404, dict(error="unknown word")
        with self.lock:
            if body.get("rev") != self.rev.get(item_id, 0):
                return 409, dict(error="Từ này vừa được lưu ở một thẻ khác. Hãy tải lại trang.")
            review = self.review
            try:
                if action == "choose":
                    review.set_chosen(body["table"], body["id"], body["chosen"])
                elif action == "check":
                    review.set_check(body["id"], int(body["index"]), body["value"])
                elif action == "tick_all":
                    review.tick_all(body["id"])
                elif action == "edit":
                    review.edit(body["table"], body["id"], body["fields"])
                elif action == "pick_image":
                    review.pick_image(item_id, body["slot"])
                elif action == "reject_images":
                    review.reject_images(item_id, body.get("reason", ""))
                elif action == "source_checked":
                    review.source_checked(body["table"], body["id"])
                elif action == "approve":
                    review.approve(item_id)
                elif action == "reject":
                    review.reject(item_id, body.get("reason", ""))
                elif action == "undo_reject":
                    review.undo_reject(item_id)
                else:
                    return 400, dict(error=f"unknown action {action!r}")
            except Refused as refused:
                return 422, dict(refused=refused.message, rule=refused.rule, word=self.word(item_id))
            except Stale as stale:
                return 409, dict(error=f"{stale}. Hãy khởi động lại xưởng.")
            except (KeyError, ValueError) as bad:
                return 400, dict(error=f"bad request: {bad}")
            self.rev[item_id] = self.rev.get(item_id, 0) + 1
            return 200, dict(word=self.word(item_id))


def make_handler(bench):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send(self, status, payload=None, content_type="application/json; charset=utf-8", raw=None):
            data = raw if raw is not None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def send_file(self, path):
            if path is None:
                return self.send(404, dict(error="not found"))
            kind = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            if kind.startswith("text/") or kind in ("application/javascript", "image/svg+xml"):
                kind += "; charset=utf-8"
            self.send(200, raw=path.read_bytes(), content_type=kind)

        def do_GET(self):
            url = urlparse(self.path)
            query = parse_qs(url.query)
            path = unquote(url.path)
            if path == "/":
                return self.send_file(safe_file(STATIC, "index.html"))
            if path.startswith("/static/"):
                return self.send_file(safe_file(STATIC, path[len("/static/"):]))
            if path.startswith("/files/"):
                return self.send_file(safe_file(CONTENT, path[len("/files/"):]))
            if path == "/api/words":
                return self.send(200, dict(words=bench.words(int(query.get("queue", ["1"])[0])),
                                           reviewer=bench.review.reviewer))
            if path == "/api/word":
                item_id = query.get("id", [""])[0]
                if item_id not in bench.by_id:
                    return self.send(404, dict(error="unknown word"))
                return self.send(200, dict(word=bench.word(item_id)))
            self.send(404, dict(error="not found"))

        def do_POST(self):
            length = int(self.headers.get("Content-Length") or 0)
            try:
                body = json.loads(self.rfile.read(length) or b"{}")
            except ValueError:
                return self.send(400, dict(error="bad JSON"))
            if self.path == "/api/action":
                return self.send(*bench.act(body))
            if self.path == "/api/visit":
                if body.get("item_id") in bench.by_id:
                    with bench.lock:
                        bench.review.log_visit(body["item_id"], body.get("outcome", "leave"),
                                               body.get("seconds", 0), body.get("pass", 1))
                return self.send(200, dict(ok=True))
            self.send(404, dict(error="not found"))

    return Handler


def option(argv, name, default):
    return argv[argv.index(name) + 1] if name in argv else default


def main(argv):
    if not argv or argv[0].startswith("--") or "--reviewer" not in argv:
        sys.exit(__doc__)
    bench = Workbench(argv[0], option(argv, "--reviewer", ""),
                      option(argv, "--lexicon", CONTENT / "lexicon" / "lexicon_raw_test.csv"),
                      option(argv, "--audio", CONTENT / "pack" / "audio_test" / "workbench"))
    port = int(option(argv, "--port", "8765"))
    server = ThreadingHTTPServer((HOST, port), make_handler(bench))
    print(f"workbench: http://{HOST}:{port}/  folder {argv[0]}  reviewer {bench.review.reviewer}  "
          f"{len(bench.lexicon)} words. Ctrl+C stops it.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("stopped")


if __name__ == "__main__":
    main(sys.argv[1:])
