"""Chặn hồi quy lỗi UnicodeEncodeError của build_lexicon.py trên Windows (P.3).
Script cần cmudict và nltk, cổng không có hai gói đó, nên test đọc mã nguồn chứ không chạy script."""
import pathlib
import re

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "pipeline" / "build_lexicon.py"
SOURCE = SCRIPT.read_text(encoding="utf-8")


def test_moi_lenh_open_deu_khai_ma_hoa():
    calls = re.findall(r"\bopen\([^)]*\)", SOURCE)
    assert calls, "không tìm thấy lệnh open() nào, test này cần xem lại"
    thieu = [c for c in calls if "encoding=" not in c]
    assert not thieu, f"open() thiếu encoding: {thieu}"


def test_stdout_duoc_dat_utf8():
    assert "sys.stdout.reconfigure(encoding='utf-8')" in SOURCE
