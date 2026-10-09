"""Test cho tools/pipeline/env/score.py (P.4): ghép bảng điểm với khoá, tính trung bình, chọn giọng.
Và một test cho _kokoro.py: hai module giả phải có mặt trước khi Kokoro được nạp.
Không import gói nặng nào, nên cổng chạy được bằng Python mặc định."""
import pathlib
import sys

ENV = pathlib.Path(__file__).resolve().parents[1] / "pipeline" / "env"
sys.path.insert(0, str(ENV))

from score import check_sheet, pick, summarise  # noqa: E402

KEY = {
    "s001": dict(sample="s001", voice="af_heart", sex="female", kind="word", text="hello"),
    "s002": dict(sample="s002", voice="af_bella", sex="female", kind="word", text="hello"),
    "s003": dict(sample="s003", voice="am_adam", sex="male", kind="word", text="hello"),
    "s004": dict(sample="s004", voice="am_michael", sex="male", kind="word", text="hello"),
    "s005": dict(sample="s005", voice="af_heart", sex="female", kind="sentence", text="Hi there."),
    "s006": dict(sample="s006", voice="am_adam", sex="male", kind="sentence", text="Hi there."),
}


def sheet(scores):
    """scores: {sample: (clarity, natural)}"""
    return [dict(rater="R1", order=str(i), sample=s, clarity=str(c), natural=str(n))
            for i, (s, (c, n)) in enumerate(scores.items(), 1)]


FULL = {"s001": (5, 4), "s002": (3, 3), "s003": (2, 2), "s004": (4, 5), "s005": (5, 5), "s006": (3, 2)}


def test_bang_du_dong_khong_co_ly_do_loai():
    assert check_sheet(sheet(FULL), KEY, "sheet_R1.csv") == []


def test_bang_thieu_dong_bi_loai():
    short = dict(list(FULL.items())[:4])
    reasons = check_sheet(sheet(short), KEY, "sheet_R1.csv")
    assert reasons == ["sheet_R1.csv: 4 rows, needs 6"]


def test_diem_ngoai_thang_bi_loai():
    bad = dict(FULL, s003=(6, 2))
    assert any("clarity='6'" in r for r in check_sheet(sheet(bad), KEY, "x.csv"))


def test_mau_la_va_mau_trung_bi_loai():
    rows = sheet(FULL)
    rows[0]["sample"] = "s999"
    rows[1]["sample"] = "s003"
    reasons = " | ".join(check_sheet(rows, KEY, "x.csv"))
    assert "unknown samples ['s999']" in reasons and "scored twice" in reasons


def test_trung_binh_theo_giong():
    summary = summarise(KEY, {"R1": sheet(FULL)})
    heart = summary["af_heart"]
    assert heart["count"] == 2 and heart["clarity"] == 5.0 and heart["natural"] == 4.5
    assert heart["total"] == 9.5 and heart["sex"] == "female"
    assert summary["am_adam"]["total"] == 4.5


def test_chon_mot_nu_mot_nam():
    winners = pick(summarise(KEY, {"R1": sheet(FULL)}))
    assert winners["female"]["voice"] == "af_heart" and winners["male"]["voice"] == "am_michael"
    assert winners["female"]["tied"] == [] and winners["female"]["weak"] is False


def test_hoa_diem_duoc_bao():
    tie = dict(FULL, s004=(2, 2), s003=(2, 2), s006=(2, 2))
    winners = pick(summarise(KEY, {"R1": sheet(tie)}))
    assert sorted(winners["male"]["tied"]) == ["am_adam", "am_michael"]


def test_giong_tot_nhat_van_yeu_duoc_bao():
    weak = dict(FULL, s004=(2, 5), s003=(1, 1), s006=(1, 1))
    assert pick(summarise(KEY, {"R1": sheet(weak)}))["male"]["weak"] is True


def test_do_lech_giua_cac_phien():
    second = dict(FULL, s001=(3, 2), s005=(3, 3))
    summary = summarise(KEY, {"R1": sheet(FULL), "R2": sheet(second)})
    assert summary["af_heart"]["count"] == 4
    assert summary["af_heart"]["spread"] == 9.5 - 5.5


def test_module_gia_co_mat_truoc_khi_nap_kokoro():
    """Thiếu hai module giả thì `import kokoro` hỏng vì num2words và espeak đã bị gỡ có chủ đích."""
    import _kokoro  # noqa: F401
    assert "misaki.espeak" in sys.modules and "num2words" in sys.modules
    source = (ENV / "_kokoro.py").read_text(encoding="utf-8")
    assert source.index('_stub("num2words"') < source.index("from kokoro import")


def test_trang_cham_khong_lo_ten_giong():
    page = (ENV / "rate.html").read_text(encoding="utf-8")
    for voice in ("af_heart", "af_bella", "af_sarah", "am_michael", "am_adam", "key.csv"):
        assert voice not in page
    assert "/*SAMPLE_FILES*/[]" in page
