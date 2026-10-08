"""Test cho tools/pipeline/env/check_textgrid.py: phần đọc TextGrid và so phone với CMUdict.
Không import gói nặng nào, nên cổng chạy được bằng Python mặc định."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "pipeline" / "env"))

from check_textgrid import check, parse_textgrid  # noqa: E402


def textgrid(phones, end=1.375):
    """Dựng một TextGrid dạng dài của Praat, hai tier, giống tệp MFA ghi ra."""
    def tier(name, intervals):
        lines = [f'    item [1]:\n        class = "IntervalTier" \n        name = "{name}" \n'
                 f"        xmin = 0 \n        xmax = {end} \n"
                 f"        intervals: size = {len(intervals)} \n"]
        for i, (start, stop, text) in enumerate(intervals, 1):
            lines.append(f"        intervals [{i}]:\n            xmin = {start} \n"
                         f'            xmax = {stop} \n            text = "{text}" \n')
        return "".join(lines)
    head = f'File type = "ooTextFile"\nObject class = "TextGrid"\n\nxmin = 0 \nxmax = {end} \n'
    return head + tier("words", [(0.0, end, "wind")]) + tier("phones", phones)


WIND = [(0.0, 0.37, ""), (0.37, 0.47, "W"), (0.47, 0.61, "IH1"), (0.61, 0.71, "N"),
        (0.71, 0.88, "D"), (0.88, 1.375, "")]


def test_doc_duoc_hai_tier():
    tiers = parse_textgrid(textgrid(WIND))
    assert list(tiers) == ["words", "phones"]
    assert tiers["phones"][2] == (0.47, 0.61, "IH1")


def test_tep_sach_khong_co_loi():
    assert check(parse_textgrid(textgrid(WIND)), "W IH1 N D", 1.375) == []


def test_thieu_tier_phones():
    tiers = {"words": [(0.0, 1.0, "wind")]}
    assert [k for k, _ in check(tiers, "W IH1 N D", 1.0)] == ["no_phones_tier"]


def test_moc_thoi_gian_di_lui():
    bad = [(0.0, 0.37, ""), (0.37, 0.61, "W"), (0.47, 0.61, "IH1"), (0.61, 0.71, "N"),
           (0.71, 0.88, "D")]
    assert "time_not_rising" in [k for k, _ in check(parse_textgrid(textgrid(bad)), "W IH1 N D", 1.375)]


def test_moc_cuoi_vuot_do_dai_audio():
    kinds = [k for k, _ in check(parse_textgrid(textgrid(WIND)), "W IH1 N D", 1.2)]
    assert kinds == ["ends_after_audio"]


def test_dong_tu_khac_am_bi_bat():
    """wind (danh từ) phải là IH, không phải AY của động từ."""
    verb = [(0.37, 0.47, "W"), (0.47, 0.61, "AY1"), (0.61, 0.71, "N"), (0.71, 0.88, "D")]
    problems = check(parse_textgrid(textgrid(verb)), "W IH1 N D", 1.375)
    assert problems == [("sound_mismatch", "W AY1 N D")]


def test_chi_lech_dau_trong_am_duoc_tach_rieng():
    flat = [(0.37, 0.47, "W"), (0.47, 0.61, "IH0"), (0.61, 0.71, "N"), (0.71, 0.88, "D")]
    problems = check(parse_textgrid(textgrid(flat)), "W IH1 N D", 1.375)
    assert problems == [("stress_only", "W IH0 N D")]
