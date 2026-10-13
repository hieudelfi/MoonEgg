// Page of the content workbench. Thin on purpose: every review rule lives in the server.
"use strict";

const $ = id => document.getElementById(id);
const STATUS = { pending: "Chờ duyệt", approved: "Đã duyệt", rejected: "Loại", needs_second: "Cần duyệt lần 2" };
const state = { queue: 1, words: [], index: 0, word: null, focus: 0, editing: false, lastOutcome: "leave" };
const timer = { seconds: 0, since: null };

// --- timer: counts only while the tab is visible ---------------------------------------
function timerStart() { timer.seconds = 0; timer.since = document.hidden ? null : Date.now(); }
function timerPause() { if (timer.since !== null) { timer.seconds += (Date.now() - timer.since) / 1000; timer.since = null; } }
function timerResume() { if (timer.since === null) timer.since = Date.now(); }
function timerValue() { return timer.seconds + (timer.since === null ? 0 : (Date.now() - timer.since) / 1000); }
document.addEventListener("visibilitychange", () => (document.hidden ? timerPause() : timerResume()));
setInterval(() => {
  const s = Math.floor(timerValue());
  $("timer").textContent = Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0");
}, 500);

// --- server ----------------------------------------------------------------------------
async function getJson(url) { return (await fetch(url)).json(); }

function say(text, kind) {
  $("message").textContent = text || "";
  $("message").className = kind || "";
}

async function act(action, extra) {
  const word = state.word;
  const response = await fetch("/api/action", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(Object.assign({ item_id: word.item_id, rev: word.rev, action }, extra)),
  });
  const data = await response.json();
  if (data.word) { state.word = data.word; render(); }
  if (response.status === 422) { say(data.refused, "bad"); return false; }
  if (!response.ok) { say(data.error || "Lỗi", "bad"); return false; }
  return true;
}

function endVisit(outcome) {
  if (!state.word) return;
  const body = JSON.stringify({ item_id: state.word.item_id, outcome, seconds: timerValue(), pass: state.queue });
  // sendBeacon still goes out while the page is closing.
  navigator.sendBeacon("/api/visit", new Blob([body], { type: "application/json" }));
}
window.addEventListener("pagehide", () => endVisit(state.lastOutcome));

// --- loading ---------------------------------------------------------------------------
async function loadQueue(queue, keepIndex) {
  state.queue = queue;
  const data = await getJson("/api/words?queue=" + queue);
  state.words = data.words;
  $("reviewer").textContent = data.reviewer;
  $("queue1").setAttribute("aria-pressed", String(queue === 1));
  $("queue2").setAttribute("aria-pressed", String(queue === 2));
  state.index = keepIndex ? Math.min(state.index, Math.max(0, state.words.length - 1)) : 0;
  await openWord();
}

async function openWord() {
  const entry = state.words[state.index];
  $("main").hidden = !entry;
  $("empty").hidden = Boolean(entry);
  if (!entry) {
    state.word = null;
    $("empty").textContent = state.queue === 2 ? "Không có từ nào cần duyệt lần 2." : "Không có từ nào.";
    $("position").textContent = "0 / 0";
    $("status").textContent = "";
    return;
  }
  state.word = (await getJson("/api/word?id=" + encodeURIComponent(entry.item_id))).word;
  state.focus = 0;
  state.lastOutcome = "leave";
  timerStart();
  render();
  playAudio();
}

async function move(step) {
  const next = state.index + step;
  if (next < 0 || next >= state.words.length) { say(step > 0 ? "Đây là từ cuối." : "Đây là từ đầu."); return; }
  endVisit(state.lastOutcome);
  state.index = next;
  say("");
  await openWord();
}

// --- drawing ---------------------------------------------------------------------------
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function badge(info, prefix) {
  const node = el("span", "badge" + (info.allowed ? "" : " bad"),
    (prefix || "") + (info.license || "không có giấy phép") + (info.allowed ? "" : " - không hợp lệ"));
  return node;
}

function sourceLink(info) {
  if (/^https?:\/\//.test(info.source)) {
    const a = el("a", "", "nguồn");
    a.href = info.source; a.target = "_blank"; a.rel = "noopener";
    return a;
  }
  return el("span", "", "nguồn: " + (info.source || "trống"));
}

function records() {
  const word = state.word;
  return word.senses.map(r => ({ table: "senses", r })).concat(word.examples.map(r => ({ table: "examples", r })));
}

function recordNode(entry, position) {
  const { table, r } = entry;
  const li = el("li", "record" + (r.chosen ? " chosen" : "") + (position === state.focus ? " focused" : ""));
  li.tabIndex = -1;
  li.dataset.position = position;
  const top = el("div", "top");
  top.append(el("span", "mark", r.chosen ? "Đã chọn" : "Chưa chọn"));
  if (table === "senses") {
    top.append(el("span", "", r.definition));
    li.append(top);
    const gloss = el("div", "");
    gloss.append(el("span", "label", "Nghĩa Việt"), el("span", "text", r.gloss || "(trống)"));
    const over = r.gloss_words < 1 || r.gloss_words > state.word.limits.gloss;
    gloss.append(" ", el("span", "count" + (over ? " bad" : ""), r.gloss_words + " / " + state.word.limits.gloss + " từ"));
    li.append(gloss);
  } else {
    top.append(el("span", "text", r.en));
    const [low, high] = state.word.limits.sentence;
    const off = r.words < low || r.words > high;
    top.append(el("span", "count" + (off ? " bad" : ""), r.words + " từ" + (off ? ", phải " + low + " đến " + high : "")));
    li.append(top);
    li.append(el("div", "", r.vi));
    const checks = el("div", "checks");
    state.word.check_names.forEach((name, i) => {
      const on = r.checks[i] === "1";
      checks.append(el("span", on ? "on" : "off", (i + 1) + ". " + name + (on ? ": có" : ": chưa")));
    });
    li.append(checks);
  }
  const meta = el("div", "meta");
  meta.append(el("span", "tag " + r.status, STATUS[r.status] || r.status), sourceLink(r.badge), badge(r.badge));
  if (table === "senses") meta.append(el("span", "", "nghĩa Việt: " + (r.gloss_badge.source || "trống")), badge(r.gloss_badge));
  if (r.note) meta.append(el("span", "", "ghi chú: " + r.note));
  if (r.source_checked) meta.append(el("span", "", "đã kiểm nguồn"));
  li.append(meta);
  return li;
}

function render() {
  const word = state.word;
  $("position").textContent = (state.index + 1) + " / " + state.words.length;
  $("status").textContent = STATUS[word.status] || word.status;
  $("status").className = "tag " + word.status;
  $("headword").textContent = word.headword;
  $("pos").textContent = word.pos;
  $("ipa").textContent = word.ipa;
  $("sounds").replaceChildren(...word.sounds.map(s => el("span", "", s)));
  $("rejected").hidden = word.status !== "rejected";
  $("rejected").textContent = "Từ này đang ở trạng thái Loại. Lý do: " + word.reject_reason + ". Bấm U để hoàn tác.";

  const audio = $("audio");
  audio.replaceChildren();
  if (!word.audio.length) audio.append(el("span", "", "Chưa có audio"));
  word.audio.forEach(a => {
    const button = el("button", "", a.label);
    button.addEventListener("click", () => { new Audio(a.url).play().catch(() => {}); button.blur(); });
    audio.append(button, " ");
  });

  const all = records();
  state.focus = Math.min(state.focus, Math.max(0, all.length - 1));
  const senses = $("senses"), examples = $("examples");
  senses.replaceChildren(); examples.replaceChildren();
  all.forEach((entry, i) => (entry.table === "senses" ? senses : examples).append(recordNode(entry, i)));
  if (!word.senses.length) senses.append(el("li", "notice", "Chưa có nghĩa ứng viên. Bấm J để bỏ qua, đừng loại từ này."));
  if (!word.examples.length) examples.append(el("li", "notice", "Chưa có câu ứng viên."));

  const images = $("images");
  images.replaceChildren();
  if (!word.images.length) images.append(el("p", "notice", "Chưa có ảnh"));
  word.images.forEach(image => {
    const box = el("div", "image" + (image.chosen ? " chosen" : ""));
    const picture = el("img");
    picture.src = image.url;
    picture.alt = "Ảnh ứng viên số " + image.slot;
    box.append(picture, el("div", "", image.slot + (image.chosen ? " - đã chọn" : "")),
      el("span", "tag " + image.status, STATUS[image.status] || image.status), " ", badge(image.badge));
    if (image.reject_reason) box.append(el("div", "hint", "lý do: " + image.reject_reason));
    images.append(box);
  });

  const focused = document.querySelector(".record.focused");
  if (focused && !state.editing) { focused.focus({ preventScroll: true }); focused.scrollIntoView({ block: "nearest" }); }
}

function playAudio() {
  const urls = state.word ? state.word.audio.map(a => a.url) : [];
  const next = () => { const url = urls.shift(); if (url) { const a = new Audio(url); a.addEventListener("ended", next); a.play().catch(() => {}); } };
  next();
}

// --- editing and reasons: the only times letter keys are letters ------------------------
function startEdit() {
  const entry = records()[state.focus];
  if (!entry) return;
  const node = document.querySelector('.record[data-position="' + state.focus + '"]');
  const fields = entry.table === "senses" ? [["gloss_vi", "Nghĩa Việt", entry.r.gloss]] : [["en", "Câu tiếng Anh", entry.r.en], ["vi", "Câu tiếng Việt", entry.r.vi]];
  const form = el("div", "");
  const inputs = fields.map(([name, label, value]) => {
    const input = el("input");
    input.type = "text"; input.value = value; input.dataset.name = name; input.setAttribute("aria-label", label);
    form.append(el("div", "label", label), input);
    return input;
  });
  form.append(el("div", "hint", "Enter lưu, Esc bỏ. Sửa xong bản ghi này sẽ cần duyệt lần 2."));
  node.append(form);
  state.editing = true;
  inputs[0].focus();
  inputs[0].select();
  const finish = async save => {
    state.editing = false;
    if (save) {
      const values = {};
      inputs.forEach(input => { values[input.dataset.name] = input.value; });
      if (await act("edit", { table: entry.table, id: entry.r.id, fields: values })) say("Đã lưu chỗ sửa.", "ok");
    } else { render(); }
  };
  inputs.forEach(input => input.addEventListener("keydown", e => {
    if (e.key === "Enter") { e.preventDefault(); e.stopPropagation(); finish(true); }
    else if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); finish(false); }
  }));
}

function ask(label, then) {
  $("askLabel").textContent = label + " ";
  $("reason").value = "";
  $("ask").hidden = false;
  state.editing = true;
  $("reason").focus();
  $("reason").onkeydown = e => {
    if (e.key !== "Enter" && e.key !== "Escape") return;
    e.preventDefault(); e.stopPropagation();
    const value = $("reason").value;
    $("ask").hidden = true;
    state.editing = false;
    if (e.key === "Enter") then(value); else render();
  };
}

// --- decisions -------------------------------------------------------------------------
async function approve() {
  if (!(await act("approve"))) return;
  const status = state.word.status;
  state.lastOutcome = status;
  endVisit(status);
  say(status === "approved" ? "Đã duyệt " + state.word.headword + "." : state.word.headword + " cần duyệt lần 2.", "ok");
  if (state.queue === 2) { await loadQueue(2, true); return; }
  state.words[state.index].status = status;
  if (state.index + 1 < state.words.length) { state.index += 1; await openWord(); } else { timerStart(); say("Đã tới từ cuối.", "ok"); }
}

// --- keys ------------------------------------------------------------------------------
document.addEventListener("keydown", async e => {
  // While a text field is open, letters are letters. Its own handler takes Enter and Esc.
  if (state.editing || !state.word || e.ctrlKey || e.metaKey || e.altKey) return;
  const key = e.key.toLowerCase();
  const digit = /^Digit[0-9]$/.test(e.code) ? Number(e.code.slice(5)) : null;
  const known = ["j", "k", "q", "tab", " ", "t", "e", "o", "r", "a", "x", "u"].includes(key) || digit !== null;
  if (!known) return;
  e.preventDefault();
  // A held key acts once.
  if (e.repeat) return;
  const all = records();
  const entry = all[state.focus];

  if (key === "j") return move(1);
  if (key === "k") return move(-1);
  if (key === "q") { endVisit(state.lastOutcome); say(""); return loadQueue(state.queue === 1 ? 2 : 1); }
  if (key === "tab") {
    if (!all.length) return;
    state.focus = (state.focus + (e.shiftKey ? all.length - 1 : 1)) % all.length;
    return render();
  }
  if (key === "r") return playAudio();
  if (key === "a") return approve();
  if (key === "x") {
    return ask("Lý do loại từ này:", async reason => { if (await act("reject", { reason })) { state.lastOutcome = "rejected"; say("Đã loại. Bấm U để hoàn tác.", "ok"); } });
  }
  if (key === "u") { if (await act("undo_reject")) { state.lastOutcome = "leave"; say("Đã hoàn tác.", "ok"); } return; }
  if (digit !== null && e.shiftKey) {
    if (entry && entry.table === "examples" && digit >= 1 && digit <= 5) {
      await act("check", { id: entry.r.id, index: digit - 1, value: entry.r.checks[digit - 1] !== "1" });
    } else { say("Shift+1 đến Shift+5 dùng cho một câu ví dụ đang được chọn tiêu điểm."); }
    return;
  }
  if (digit !== null) {
    if (!state.word.images.length) return say("Từ này chưa có ảnh.");
    if (digit === 0) return ask("Lý do không ảnh nào đạt:", reason => act("reject_images", { reason }));
    if (digit <= 4) return act("pick_image", { slot: String(digit) });
    return;
  }
  if (!entry) return say("Không có bản ghi nào để thao tác.");
  if (key === " ") return act("choose", { table: entry.table, id: entry.r.id, chosen: !entry.r.chosen });
  if (key === "t") {
    if (entry.table !== "examples") return say("T dùng cho câu ví dụ.");
    return act("tick_all", { id: entry.r.id });
  }
  if (key === "e") return startEdit();
  if (key === "o") {
    if (/^https?:\/\//.test(entry.r.badge.source)) window.open(entry.r.badge.source, "_blank", "noopener");
    else say("Nguồn của bản ghi này: " + (entry.r.badge.source || "trống"));
    return act("source_checked", { table: entry.table, id: entry.r.id });
  }
});
// A focused button would otherwise be pressed by Space on keyup in some browsers.
document.addEventListener("keyup", e => { if (!state.editing && e.key === " ") e.preventDefault(); });

$("queue1").addEventListener("click", e => { e.target.blur(); endVisit(state.lastOutcome); loadQueue(1); });
$("queue2").addEventListener("click", e => { e.target.blur(); endVisit(state.lastOutcome); loadQueue(2); });
$("sheetToggle").addEventListener("click", e => {
  const sheet = $("sheet");
  sheet.hidden = !sheet.hidden;
  e.target.setAttribute("aria-expanded", String(!sheet.hidden));
  e.target.blur();
});

loadQueue(1);
