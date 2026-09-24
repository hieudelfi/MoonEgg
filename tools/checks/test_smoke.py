"""Test khói cho CI: verify_pack chạy được và dữ liệu test 30 từ không lỗi.
Thay cho một bộ test rỗng — pytest thoát mã 5 khi không tìm thấy test nào."""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "content" / "lexicon" / "lexicon_raw_test.csv"


def run_verify(*args):
    return subprocess.run(
        [sys.executable, str(ROOT / "tools" / "checks" / "verify_pack.py"), str(SAMPLE), *args],
        capture_output=True, text=True, encoding="utf-8",
    )


def test_du_lieu_mau_ton_tai():
    assert SAMPLE.is_file(), f"thiếu {SAMPLE}"


def test_verify_pack_khong_loi_tren_du_lieu_mau():
    r = run_verify()
    assert r.returncode == 0, f"exit {r.returncode}\n{r.stdout}\n{r.stderr}"
    assert "0 lỗi" in r.stdout, r.stdout


def test_verify_pack_in_duoc_tieng_viet():
    """Chặn hồi quy lỗi UnicodeEncodeError trên console cp1252."""
    r = run_verify()
    assert "UnicodeEncodeError" not in r.stderr, r.stderr
    assert "bản ghi" in r.stdout, r.stdout
