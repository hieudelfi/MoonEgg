"""Test cho tools/pipeline/env/score.py (P.4): ghép bảng điểm với khoá, tính trung bình, chọn giọng.
Và test cho _kokoro.py và rate.html. Không import gói nặng nào, nên cổng chạy được bằng Python mặc định."""
import csv
import pathlib
import subprocess
import sys

ENV = pathlib.Path(__file__).resolve().parents[1] / "pipeline" / "env"
sys.path.insert(0, str(ENV))

from score import check_sheet, find_sheets, load, pick, summarise  # noqa: E402

KEY = {
    "s001": dict(sample="s001", voice="af_heart", sex="female", kind="word", text="hello"),
    "s002": dict(sample="s002", voice="af_bella", sex="female", kind="word", text="hello"),
    "s003": dict(sample="s003", voice="am_adam", sex="male", kind="word", text="hello"),
    "s004": dict(sample="s004", voice="am_michael", sex="male", kind="word", text="hello"),
    "s005": dict(sample="s005", voice="af_heart", sex="female", kind="sentence", text="Hi there."),
    "s006": dict(sample="s006", voice="am_adam", sex="male", kind="sentence", text="Hi there."),
}
FULL = {"s001": (5, 4), "s002": (3, 3), "s003": (2, 2), "s004": (4, 5), "s005": (5, 5), "s006": (3, 2)}


def sheet(scores, rater="R1"):
    """scores: {sample: (clarity, natural)}"""
    return [dict(rater=rater, order=str(i), sample=s, clarity=str(c), natural=str(n))
            for i, (s, (c, n)) in enumerate(scores.items(), 1)]


def write(path, rows, fields=("rater", "order", "sample", "clarity", "natural")):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)


def folder(tmp_path, sheets):
    """Dựng voices/_key/key.csv và các bảng trong voices/sheets/. sheets: {tên tệp: dòng}"""
    key_dir = tmp_path / "voices" / "_key"
    write(key_dir / "key.csv", list(KEY.values()), ("sample", "voice", "sex", "kind", "text"))
    for name, rows in sheets.items():
        write(tmp_path / "voices" / "sheets" / name, rows)
    return key_dir


def test_bang_du_dong_khong_co_ly_do_loai():
    assert check_sheet(sheet(FULL), KEY, "sheet_R1.csv", "R1") == []


def test_bang_thieu_dong_bi_loai():
    short = dict(list(FULL.items())[:4])
    assert check_sheet(sheet(short), KEY, "sheet_R1.csv") == ["sheet_R1.csv: 4 rows, needs 6"]


def test_diem_ngoai_thang_bi_loai():
    bad = dict(FULL, s003=(6, 2))
    assert any("clarity='6'" in r for r in check_sheet(sheet(bad), KEY, "x.csv"))


def test_mau_la_va_mau_trung_bi_loai():
    rows = sheet(FULL)
    rows[0]["sample"] = "s999"
    rows[1]["sample"] = "s003"
    reasons = " | ".join(check_sheet(rows, KEY, "x.csv"))
    assert "unknown samples ['s999']" in reasons and "scored twice" in reasons


def test_ma_phien_trong_tep_phai_khop_ten_tep():
    reasons = check_sheet(sheet(FULL, "R1"), KEY, "sheet_R2.csv", "R2")
    assert reasons == ["sheet_R2.csv: rater code inside is ['R1'], the file name says R2"]


def test_chi_ba_ten_tep_dung_duoc_tinh(tmp_path):
    key_dir = folder(tmp_path, {"sheet_R1.csv": sheet(FULL), "sheet_R1 (1).csv": sheet(FULL),
                                "sheet_R4.csv": sheet(FULL, "R4")})
    found, ignored = find_sheets(key_dir)
    assert list(found) == ["R1"] and sorted(ignored) == ["sheet_R1 (1).csv", "sheet_R4.csv"]


def test_bang_chep_lai_khong_duoc_tinh_la_mot_phien(tmp_path):
    key_dir = folder(tmp_path, {"sheet_R1.csv": sheet(FULL, "R1"), "sheet_R2.csv": sheet(FULL, "R2")})
    _, sheets, messages = load(key_dir)
    assert list(sheets) == ["R1"]
    assert any("every score equals R1" in m for m in messages)


def test_chua_du_ba_phien_thi_khong_in_gi_ve_giong(tmp_path):
    second = dict(FULL, s001=(4, 4))
    key_dir = folder(tmp_path, {"sheet_R1.csv": sheet(FULL, "R1"), "sheet_R2.csv": sheet(second, "R2")})
    done = subprocess.run([sys.executable, str(ENV / "score.py"), str(key_dir)],
                          capture_output=True, text=True, encoding="utf-8")
    assert done.returncode != 0
    assert "sheets: 2 complete of 3 needed" in done.stdout
    for voice in ("af_heart", "af_bella", "am_adam", "am_michael"):
        assert voice not in done.stdout + done.stderr
    assert not (key_dir / "scores.csv").exists()


def test_du_ba_phien_thi_neu_ten_va_ghi_scores(tmp_path):
    second, third = dict(FULL, s001=(4, 4)), dict(FULL, s002=(4, 3))
    key_dir = folder(tmp_path, {"sheet_R1.csv": sheet(FULL, "R1"), "sheet_R2.csv": sheet(second, "R2"),
                                "sheet_R3.csv": sheet(third, "R3")})
    done = subprocess.run([sys.executable, str(ENV / "score.py"), str(key_dir)],
                          capture_output=True, text=True, encoding="utf-8")
    assert done.returncode == 0, done.stdout + done.stderr
    assert "female  af_heart" in done.stdout and "male    am_michael" in done.stdout
    assert len((key_dir / "scores.csv").read_text(encoding="utf-8").splitlines()) == 1 + 18


def test_trung_binh_theo_giong():
    summary = summarise(KEY, {"R1": sheet(FULL)})
    heart = summary["af_heart"]
    assert heart["count"] == 2 and heart["clarity"] == 5.0 and heart["natural"] == 4.5
    assert heart["total"] == 9.5 and heart["sex"] == "female"
    assert summary["am_adam"]["total"] == 4.5


def test_gioi_lay_tu_khoa_khong_doan_tu_ten():
    key = {s: dict(k, sex="male" if k["voice"] == "af_bella" else k["sex"]) for s, k in KEY.items()}
    assert summarise(key, {"R1": sheet(FULL)})["af_bella"]["sex"] == "male"


def test_chon_mot_nu_mot_nam():
    winners = pick(summarise(KEY, {"R1": sheet(FULL)}))
    assert winners["female"]["voice"] == "af_heart" and winners["male"]["voice"] == "am_michael"
    assert winners["female"]["tied"] == [] and winners["female"]["weak"] is False
    assert winners["female"]["unsteady"] is False


def test_hoa_diem_duoc_bao():
    tie = dict(FULL, s004=(2, 2), s003=(2, 2), s006=(2, 2))
    winners = pick(summarise(KEY, {"R1": sheet(tie)}))
    assert sorted(winners["male"]["tied"]) == ["am_adam", "am_michael"]


def test_giong_tot_nhat_van_yeu_duoc_bao():
    weak = dict(FULL, s004=(2, 5), s003=(1, 1), s006=(1, 1))
    assert pick(summarise(KEY, {"R1": sheet(weak)}))["male"]["weak"] is True


def test_do_lech_giua_cac_phien():
    second = dict(FULL, s001=(3, 2), s005=(3, 3))
    summary = summarise(KEY, {"R1": sheet(FULL), "R2": sheet(second, "R2")})
    assert summary["af_heart"]["count"] == 4
    assert summary["af_heart"]["spread"] == 9.5 - 5.5


def test_dan_dau_khong_on_dinh_duoc_bao():
    """af_heart thắng tổng nhưng thua af_bella ở phiên R2: phải báo, không in như thắng rõ."""
    second = dict(FULL, s001=(3, 3), s005=(3, 3), s002=(4, 4))
    winners = pick(summarise(KEY, {"R1": sheet(FULL), "R2": sheet(second, "R2")}))
    female = winners["female"]
    assert female["voice"] == "af_heart" and female["unsteady"] is True
    assert female["led"] == ["R1"] and female["sittings"] == 2


def test_module_gia_co_mat_truoc_khi_nap_kokoro():
    """Thiếu hai module giả thì `import kokoro` hỏng vì num2words và espeak đã bị gỡ có chủ đích.
    Kiểm bằng mã nguồn, không import, để không chèn module giả vào tiến trình pytest của cổng."""
    source = (ENV / "_kokoro.py").read_text(encoding="utf-8")
    assert source.index('_stub("num2words"') < source.index("from kokoro import")
    assert source.index('_stub("misaki.espeak"') < source.index("from kokoro import")


def test_trang_cham_khong_lo_ten_giong():
    page = (ENV / "rate.html").read_text(encoding="utf-8")
    for voice in ("af_heart", "af_bella", "af_sarah", "am_michael", "am_adam", "key.csv", "_key"):
        assert voice not in page
    assert "/*SAMPLE_FILES*/[]" in page and '/*SET_ID*/""' in page


def test_trang_cham_bo_qua_phim_giu():
    """Phím số bị giữ từng tự điền cả hai điểm bằng cùng một số (P.4, phiên R3)."""
    page = (ENV / "rate.html").read_text(encoding="utf-8")
    assert "e.repeat" in page
