"""Test cho xưởng nội dung (task P.5): luật duyệt R1–R7, bảng trạng thái, lưu an toàn, máy chủ,
bản xuất, bộ kiểm tệp làm việc và báo cáo giây/từ. 44 test, đánh số T1–T13 theo
docs/tasks/P.5/Plan.md mục 7. Chỉ dùng thư viện chuẩn, nên cổng chạy được bằng Python mặc định."""
import http.client
import os
import pathlib
import sys
import threading

import pytest

BENCH = pathlib.Path(__file__).resolve().parents[1] / "workbench"
sys.path.insert(0, str(BENCH))

import check_files  # noqa: E402
import export  # noqa: E402
import report  # noqa: E402
import server  # noqa: E402
import store  # noqa: E402
from review import ALL_TICKED, NO_TICKS, Refused, Review  # noqa: E402

ALLOW = {"own", "self", "WordNet", "CC-BY-SA"}
LEX_HEADER = ["item_id", "headword", "pos", "ipa_us", "arpabet", "viseme_seq", "source", "license"]
GOOD = "We walk to the big market together."            # 7 từ
LONG = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen"


def row(table, **values):
    out = {c: "" for c in store.COLUMNS[table]}
    out.update(values)
    return out


def sense(item, n, gloss="nghĩa thử", **extra):
    return row("senses", sense_id=f"{item}/s{n}", item_id=item, order=str(n), def_en_simple=f"def {n}",
               gloss_vi=gloss, chosen="0", source="https://example.org/wn", license="WordNet",
               gloss_source="self", gloss_license="own", review_status="pending", **extra)


def example(item, n, en=GOOD, **extra):
    return row("examples", example_id=f"{item}/e{n}", sense_id=f"{item}/s1", item_id=item, en=en,
               vi="câu thử", checks=NO_TICKS, chosen="0", source="self", license="own",
               review_status="pending", **extra)


def image(item, n, **extra):
    return row("images", image_id=f"{item}/i{n}", item_id=item, slot=str(n), path=f"pack/x/{n}.svg",
               chosen="0", source="self", license="own", review_status="pending", **extra)


@pytest.fixture
def bench(tmp_path):
    """Một thư mục làm việc nhỏ: alpha có 4 nghĩa, 4 câu, 4 ảnh; beta có 1 nghĩa, 2 câu, không ảnh."""
    folder = tmp_path / "work"
    folder.mkdir()
    a, b = "w:alpha#1", "w:beta#1"
    store.write_table(folder / "senses.csv", store.COLUMNS["senses"],
                      [sense(a, n) for n in range(1, 5)] + [sense(b, 1)])
    store.write_table(folder / "examples.csv", store.COLUMNS["examples"],
                      [example(a, n) for n in range(1, 5)] + [example(b, 1), example(b, 2)])
    store.write_table(folder / "images.csv", store.COLUMNS["images"], [image(a, n) for n in range(1, 5)])
    lexicon = tmp_path / "lexicon.csv"
    store.write_table(lexicon, LEX_HEADER, [
        dict(item_id=a, headword="alpha", pos="n", ipa_us="/a/", arpabet="AE1", viseme_seq="aa",
             source="cmudict", license="BSD"),
        dict(item_id=b, headword="beta", pos="n", ipa_us="/b/", arpabet="B EY1", viseme_seq="PP E",
             source="cmudict", license="BSD")])
    ticks = iter(range(1, 100000))
    review = Review(store.Folder(folder), "tester", clock=lambda: f"2026-10-13T00:{next(ticks):05d}Z",
                    allow=ALLOW)
    review.a, review.b, review.lexicon = a, b, lexicon
    return review


def ready(review, item=None):
    """Đưa một từ tới chỗ bấm A là qua: 1 nghĩa, 2 câu đủ 5 mục, và ảnh số 1 nếu từ có ảnh."""
    item = item or review.a
    review.set_chosen("senses", f"{item}/s1", True)
    for n in (1, 2):
        review.set_chosen("examples", f"{item}/e{n}", True)
        review.tick_all(f"{item}/e{n}")
    if review.folder.of_word("images", item):
        review.pick_image(item, 1)


def status(review, table, record_id):
    return review.folder.find(table, record_id)["review_status"]


def refused_rule(review, item):
    with pytest.raises(Refused) as caught:
        review.approve(item)
    return caught.value.rule


# --- T1: luật R1 đến R7 -------------------------------------------------------------------

def test_t1_r1_khong_chon_nghia_nao(bench):
    ready(bench)
    bench.set_chosen("senses", "w:alpha#1/s1", False)
    assert refused_rule(bench, bench.a) == "R1"


def test_t1_r2_nghia_viet_chin_tu(bench):
    ready(bench)
    bench.folder.find("senses", "w:alpha#1/s1")["gloss_vi"] = "một hai ba bốn năm sáu bảy tám chín"
    assert refused_rule(bench, bench.a) == "R2"


def test_t1_r3_chi_mot_cau(bench):
    ready(bench)
    bench.set_chosen("examples", "w:alpha#1/e2", False)
    assert refused_rule(bench, bench.a) == "R3"


def test_t1_r4_cau_muoi_bon_tu(bench):
    ready(bench)
    bench.folder.find("examples", "w:alpha#1/e1")["en"] = LONG
    assert refused_rule(bench, bench.a) == "R4"


def test_t1_r5_thieu_mot_muc_kiem(bench):
    ready(bench)
    bench.set_check("w:alpha#1/e2", 3, False)
    assert refused_rule(bench, bench.a) == "R5"


def test_t1_r6_giay_phep_ngoai_danh_sach(bench):
    ready(bench)
    bench.folder.find("examples", "w:alpha#1/e1")["license"] = "GPL-3.0"
    assert refused_rule(bench, bench.a) == "R6"


def test_t1_r7_co_anh_ma_khong_chon(bench):
    ready(bench)
    for img in bench.folder.of_word("images", bench.a):
        img["chosen"] = "0"
    assert refused_rule(bench, bench.a) == "R7"


def test_t1_du_luat_thi_qua_va_tu_choi_khong_doi_trang_thai(bench):
    ready(bench)
    bench.set_chosen("examples", "w:alpha#1/e2", False)
    assert refused_rule(bench, bench.a) == "R3"
    assert bench.folder.word(bench.a)["review_status"] == "pending"
    assert bench.folder.find("examples", "w:alpha#1/e1")["chosen"] == "1"     # lựa chọn vẫn còn
    bench.set_chosen("examples", "w:alpha#1/e2", True)
    assert bench.approve(bench.a) == "approved"


# --- T2: A ghi gì -------------------------------------------------------------------------

def test_t2_duoc_chon_khong_sua_thanh_approved(bench):
    ready(bench)
    bench.approve(bench.a)
    assert status(bench, "senses", "w:alpha#1/s1") == "approved"
    assert status(bench, "examples", "w:alpha#1/e2") == "approved"
    assert status(bench, "images", "w:alpha#1/i1") == "approved"


def test_t2_duoc_chon_da_sua_van_needs_second(bench):
    ready(bench)
    bench.edit("senses", "w:alpha#1/s1", dict(gloss_vi="nghĩa đã sửa"))
    bench.approve(bench.a)
    assert status(bench, "senses", "w:alpha#1/s1") == "needs_second"


def test_t2_khong_duoc_chon_thanh_rejected(bench):
    ready(bench)
    bench.approve(bench.a)
    assert status(bench, "senses", "w:alpha#1/s2") == "rejected"
    assert status(bench, "examples", "w:alpha#1/e3") == "rejected"
    assert status(bench, "images", "w:alpha#1/i2") == "rejected"


def test_t2_tu_thanh_approved_khi_khong_co_gi_bi_sua(bench):
    ready(bench)
    assert bench.approve(bench.a) == "approved"
    word = bench.folder.word(bench.a)
    assert word["reviewed_by"] == "tester" and word["reviewed_at"] and not word["second_by"]


def test_t2_tu_thanh_needs_second_khi_co_ban_ghi_bi_sua(bench):
    ready(bench)
    bench.edit("examples", "w:alpha#1/e1", dict(en="We walk to the old market together."))
    bench.tick_all("w:alpha#1/e1")
    assert bench.approve(bench.a) == "needs_second"
    assert status(bench, "examples", "w:alpha#1/e2") == "approved"


# --- T3: một lần sửa ----------------------------------------------------------------------

def test_t3_sua_cau_thanh_needs_second_va_xoa_nam_dau_tick(bench):
    ready(bench)
    assert bench.folder.find("examples", "w:alpha#1/e1")["checks"] == ALL_TICKED
    bench.edit("examples", "w:alpha#1/e1", dict(en="We walk to the new market together."))
    record = bench.folder.find("examples", "w:alpha#1/e1")
    assert record["review_status"] == "needs_second" and record["checks"] == NO_TICKS
    assert record["en"] == "We walk to the new market together."


def test_t3_sua_xong_tu_van_pending_va_da_luu_xuong_dia(bench):
    bench.edit("senses", "w:alpha#1/s1", dict(gloss_vi="đã sửa"))
    assert bench.folder.word(bench.a)["review_status"] == "pending"
    reloaded = store.Folder(bench.folder.path)
    assert reloaded.find("senses", "w:alpha#1/s1")["gloss_vi"] == "đã sửa"


# --- T4: duyệt lần 2 ----------------------------------------------------------------------

def test_t4_duyet_lan_hai_duyet_ca_ban_ghi_va_tu(bench):
    ready(bench)
    bench.edit("senses", "w:alpha#1/s1", dict(gloss_vi="nghĩa đã sửa"))
    assert bench.approve(bench.a) == "needs_second"
    assert bench.queue_of(bench.a) == 2
    assert bench.approve(bench.a) == "approved"
    record, word = bench.folder.find("senses", "w:alpha#1/s1"), bench.folder.word(bench.a)
    assert record["review_status"] == "approved" and record["second_by"] == "tester"
    assert word["second_by"] == "tester" and word["second_at"]


def test_t4_sua_lai_trong_lan_hai_thi_van_o_hang_doi(bench):
    ready(bench)
    bench.edit("senses", "w:alpha#1/s1", dict(gloss_vi="sửa lần một"))
    bench.approve(bench.a)
    bench.edit("senses", "w:alpha#1/s1", dict(gloss_vi="sửa lần hai"))
    assert bench.approve(bench.a) == "needs_second"
    assert status(bench, "senses", "w:alpha#1/s1") == "needs_second"
    assert bench.approve(bench.a) == "approved"                 # lượt kế không sửa nữa thì qua


# --- T5: loại từ và hoàn tác --------------------------------------------------------------

def test_t5_x_chi_dung_vao_tu(bench):
    ready(bench)
    with pytest.raises(Refused):
        bench.reject(bench.a, "  ")
    bench.reject(bench.a, "từ hiếm")
    word = bench.folder.word(bench.a)
    assert word["review_status"] == "rejected" and word["reject_reason"] == "từ hiếm"
    assert bench.folder.find("senses", "w:alpha#1/s1")["chosen"] == "1"
    assert {r["review_status"] for r in bench.folder.of_word("examples", bench.a)} == {"pending"}


def test_t5_u_dua_tu_ve_pending(bench):
    bench.reject(bench.a, "nhầm tay")
    bench.undo_reject(bench.a)
    word = bench.folder.word(bench.a)
    assert word["review_status"] == "pending" and word["reject_reason"] == ""
    with pytest.raises(Refused):
        bench.undo_reject(bench.a)


# --- T6: mở lại từ đã duyệt ---------------------------------------------------------------

def test_t6_doi_lua_chon_o_tu_da_duyet_thi_tu_ve_pending(bench):
    ready(bench)
    bench.approve(bench.a)
    bench.set_chosen("examples", "w:alpha#1/e3", True)
    assert bench.folder.word(bench.a)["review_status"] == "pending"
    assert status(bench, "examples", "w:alpha#1/e3") == "pending"
    assert status(bench, "examples", "w:alpha#1/e1") == "approved"      # bản ghi không đổi giữ nguyên
    log = store.read_table(bench.folder.file("review_log"))[1]
    assert [r["action"] for r in log if r["item_id"] == bench.a][-2:] == ["approved", "reopen"]


# --- T7: ảnh ------------------------------------------------------------------------------

def test_t7_chon_mot_anh(bench):
    bench.pick_image(bench.a, 3)
    assert [i["chosen"] for i in bench.folder.of_word("images", bench.a)] == ["0", "0", "1", "0"]
    with pytest.raises(Refused):
        bench.pick_image(bench.a, 7)


def test_t7_bam_khong_phai_co_ly_do_va_qua_duoc_r7(bench):
    ready(bench)
    with pytest.raises(Refused):
        bench.reject_images(bench.a, "")
    bench.reject_images(bench.a, "không ảnh nào đúng nghĩa")
    images = bench.folder.of_word("images", bench.a)
    assert {i["review_status"] for i in images} == {"rejected"}
    assert {i["reject_reason"] for i in images} == {"không ảnh nào đúng nghĩa"}
    assert bench.approve(bench.a) == "approved"


def test_t7_tu_khong_co_anh_van_duyet_duoc(bench):
    ready(bench, bench.b)
    assert bench.approve(bench.b) == "approved"


# --- T8: lưu tệp --------------------------------------------------------------------------

def test_t8_hong_giua_chung_thi_tep_cu_con_nguyen(bench, monkeypatch):
    path = bench.folder.file("senses")
    before = path.read_bytes()

    def boom(*args):
        raise OSError("mất điện")
    monkeypatch.setattr(os, "replace", boom)
    bench.folder.find("senses", "w:alpha#1/s1")["gloss_vi"] = "đang ghi dở"
    with pytest.raises(OSError):
        bench.folder.save("senses")
    assert path.read_bytes() == before


def test_t8_tep_doi_tren_dia_thi_tu_choi_ghi(bench):
    path = bench.folder.file("senses")
    path.write_bytes(path.read_bytes() + b"\n")
    with pytest.raises(store.Stale):
        bench.set_chosen("senses", "w:alpha#1/s1", True)


def test_t8_cot_la_duoc_giu_dung_cho(tmp_path):
    folder = tmp_path / "w"
    folder.mkdir()
    header = ["sense_id", "cot_la", "item_id"] + [c for c in store.COLUMNS["senses"] if c not in ("sense_id", "item_id")]
    store.write_table(folder / "senses.csv", header, [dict(sense(  "w:a#1", 1), cot_la="giữ tôi")])
    loaded = store.Folder(folder)
    loaded.find("senses", "w:a#1/s1")["chosen"] = "1"
    loaded.save("senses")
    new_header, rows = store.read_table(folder / "senses.csv")
    assert new_header[:3] == ["sense_id", "cot_la", "item_id"] and rows[0]["cot_la"] == "giữ tôi"


def test_t8_xuong_dong_lf_va_dong_khong_dung_toi_giu_nguyen_tung_byte(bench):
    path = bench.folder.file("examples")
    before = path.read_bytes().split(b"\n")
    bench.set_chosen("examples", "w:alpha#1/e2", True)
    after = path.read_bytes()
    assert b"\r" not in after
    lines = after.split(b"\n")
    changed = [i for i, (x, y) in enumerate(zip(before, lines)) if x != y]
    assert len(lines) == len(before) and changed == [2]          # dòng 0 là tiêu đề, e2 là dòng 2


# --- T9: máy chủ --------------------------------------------------------------------------

@pytest.fixture
def running(bench, tmp_path):
    app = server.Workbench(bench.folder.path, "tester", bench.lexicon, tmp_path / "audio")
    httpd = server.ThreadingHTTPServer((server.HOST, 0), server.make_handler(app))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield httpd
    httpd.shutdown()
    httpd.server_close()


def fetch(httpd, path):
    conn = http.client.HTTPConnection(*httpd.server_address, timeout=5)
    conn.request("GET", path)
    response = conn.getresponse()
    body = response.read()
    conn.close()
    return response.status, body


def test_t9_duong_dan_ra_ngoai_repo_bi_tu_choi(running):
    assert server.safe_file(server.CONTENT, "../CLAUDE.md") is None
    for path in ("/files/../CLAUDE.md", "/files/..%2F..%2FCLAUDE.md", "/static/../server.py"):
        assert fetch(running, path)[0] == 404
    assert fetch(running, "/static/app.js")[0] == 200


def test_t9_chi_nghe_o_may_nay_va_tra_danh_sach_tu(running):
    assert server.HOST == "127.0.0.1" and running.server_address[0] == "127.0.0.1"
    status_code, body = fetch(running, "/api/words?queue=1")
    assert status_code == 200 and body.count(b'"item_id"') == 2


# --- T10: bản xuất ------------------------------------------------------------------------

def lexicon_rows(review):
    return store.read_table(review.lexicon)[1]


def test_t10_nghia_viet_noi_theo_thu_tu(bench):
    ready(bench)
    bench.set_chosen("senses", "w:alpha#1/s2", True)
    bench.folder.find("senses", "w:alpha#1/s2")["gloss_vi"] = "nghĩa hai"
    bench.approve(bench.a)
    rows, _ = export.build(bench.folder, lexicon_rows(bench))
    assert rows[0]["gloss_vi"] == "nghĩa thử; nghĩa hai" and rows[0]["n_senses"] == "2"


def test_t10_dem_cau_va_chi_lay_tu_da_duyet(bench):
    ready(bench)
    bench.set_chosen("examples", "w:alpha#1/e3", True)
    bench.tick_all("w:alpha#1/e3")
    bench.approve(bench.a)
    rows, _ = export.build(bench.folder, lexicon_rows(bench))
    assert [r["item_id"] for r in rows] == [bench.a]
    assert rows[0]["n_examples"] == "3" and rows[0]["review_status"] == "approved"


def test_t10_duong_dan_anh_va_danh_sach_tu_khong_anh(bench):
    ready(bench)
    ready(bench, bench.b)
    bench.approve(bench.a)
    bench.approve(bench.b)
    rows, no_image = export.build(bench.folder, lexicon_rows(bench))
    assert rows[0]["image_asset"] == "pack/x/1.svg" and rows[1]["image_asset"] == ""
    assert no_image == [bench.b]


def test_t10_tu_choi_ban_nhap_khi_khong_phai_thu(bench):
    ready(bench)
    bench.folder.find("examples", "w:alpha#1/e1")["note"] = "draft"
    bench.approve(bench.a)
    with pytest.raises(export.DraftsFound):
        export.build(bench.folder, lexicon_rows(bench))
    assert len(export.build(bench.folder, lexicon_rows(bench), trial=True)[0]) == 1
    with pytest.raises(SystemExit):
        export.main([str(bench.folder.path), "--lexicon", str(bench.lexicon)])
    assert not (bench.folder.path / "lexicon_reviewed.csv").exists()


def test_t10_che_do_thu_ghi_tep_ten_rieng_trong_thu_muc_lam_viec(bench):
    ready(bench)
    bench.folder.find("examples", "w:alpha#1/e1")["note"] = "draft"
    bench.approve(bench.a)
    export.main([str(bench.folder.path), "--lexicon", str(bench.lexicon), "--trial"])
    out = bench.folder.path / "lexicon_reviewed_trial.csv"
    header, rows = store.read_table(out)
    assert header[:len(LEX_HEADER)] == LEX_HEADER and header[-7:] == export.EXTRA
    assert len(rows) == 1 and not (bench.folder.path / "lexicon_reviewed.csv").exists()


# --- T11: bộ kiểm tệp làm việc ------------------------------------------------------------

def errors_of(review, **kwargs):
    return check_files.check(review.folder, lexicon_rows(review), ALLOW, **kwargs)[0]


def test_t11_trung_ma(bench):
    assert errors_of(bench) == []
    bench.folder.rows["senses"].append(dict(bench.folder.find("senses", "w:alpha#1/s1")))
    assert any("duplicate id w:alpha#1/s1" in e for e in errors_of(bench))


def test_t11_tu_khong_co_trong_lexicon_va_sense_id_khong_ton_tai(bench):
    bench.folder.find("senses", "w:beta#1/s1")["item_id"] = "w:ghost#1"
    bench.folder.find("examples", "w:beta#1/e1")["sense_id"] = "w:beta#1/s9"
    found = " | ".join(errors_of(bench))
    assert "item_id 'w:ghost#1' is not in the lexicon" in found and "sense_id 'w:beta#1/s9' does not exist" in found


def test_t11_trang_thai_va_checks_sai(bench):
    bench.folder.find("senses", "w:alpha#1/s1")["review_status"] = "done"
    bench.folder.find("examples", "w:alpha#1/e1")["checks"] = "1x1"
    found = " | ".join(errors_of(bench))
    assert "status 'done' is not valid" in found and "checks '1x1' is not 5 bits" in found


def test_t11_thieu_nguon_hoac_giay_phep(bench):
    bench.folder.find("examples", "w:alpha#1/e1")["source"] = ""
    bench.folder.find("images", "w:alpha#1/i1")["license"] = "GPL-3.0"
    bench.folder.find("senses", "w:alpha#1/s1")["gloss_license"] = ""
    found = " | ".join(errors_of(bench))
    assert "examples w:alpha#1/e1: source is empty" in found
    assert "images w:alpha#1/i1: licence 'GPL-3.0' is not on the allowlist" in found
    assert "senses w:alpha#1/s1: the Vietnamese meaning has no source" in found


def test_t11_tu_approved_ma_thieu_cau_da_duyet(bench):
    ready(bench)
    bench.approve(bench.a)
    assert errors_of(bench) == []
    bench.folder.find("examples", "w:alpha#1/e2")["review_status"] = "rejected"
    assert any("approved with 1 approved meanings and 1 approved sentences" in e for e in errors_of(bench))


def test_t11_ban_nhap_chi_la_loi_khi_dong_goi(bench):
    bench.folder.find("examples", "w:alpha#1/e1")["note"] = "draft"
    assert errors_of(bench) == []
    assert errors_of(bench, for_pack=True) == ["examples w:alpha#1/e1: a draft cannot be packed"]


# --- T12: báo cáo -------------------------------------------------------------------------

def test_t12_cong_cac_lan_ghe_cua_mot_tu(bench):
    ready(bench)
    bench.log_visit(bench.a, "leave", 40.0, 1)
    bench.approve(bench.a)
    bench.log_visit(bench.a, "approved", 20.5, 1)
    bench.log_visit(bench.b, "leave", 999, 1)                  # beta chưa có quyết định: không tính
    log = store.read_table(bench.folder.file("review_log"))[1]
    states = {r["item_id"]: r["review_status"] for r in bench.folder.rows["word_review"]}
    s = report.summarise(log, states, [bench.a, bench.b], {bench.a: 4, bench.b: 1})
    assert s["decided"] == 1 and s["timed"] == 1 and s["mean"] == 60.5 and s["slowest"] == (60.5, bench.a)


def test_t12_tu_qua_muoi_lam_phut_va_tu_cho_ung_vien(bench):
    bench.reject(bench.a, "thử")
    bench.log_visit(bench.a, "rejected", 16 * 60, 1)
    log = store.read_table(bench.folder.file("review_log"))[1]
    states = {r["item_id"]: r["review_status"] for r in bench.folder.rows["word_review"]}
    s = report.summarise(log, states, [bench.a, bench.b, "w:empty#1"], {bench.a: 4, bench.b: 1})
    assert s["long_words"] == [bench.a] and s["waiting"] == ["w:empty#1"]


# --- T13: trang ---------------------------------------------------------------------------

def test_t13_phim_giu_chi_tinh_mot_lan():
    page = (BENCH / "static" / "app.js").read_text(encoding="utf-8")
    handler = page[page.index('document.addEventListener("keydown"'):]
    assert handler.index("if (e.repeat) return;") < handler.index('if (key === "j")')


def test_t13_dang_mo_o_chu_thi_phim_khong_duyet_khong_loai():
    page = (BENCH / "static" / "app.js").read_text(encoding="utf-8")
    handler = page[page.index('document.addEventListener("keydown"'):]
    assert handler.index("if (state.editing") < handler.index('if (key === "a")')
    assert "state.editing = true" in page and "window.prompt" not in page
