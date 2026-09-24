"""TC-CP-01/02: cổng giấy phép phải chặn gói ngoài allowlist.
Fixture offline nên test chạy được cả khi không có mạng."""
import pathlib
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECKER = ROOT / "tools" / "checks" / "check_licenses.mjs"
GPL_CASE = ROOT / "tools" / "checks" / "fixtures" / "gpl-case"


def run(target):
    return subprocess.run(
        ["node", str(CHECKER), str(target)],
        capture_output=True, text=True, encoding="utf-8", cwd=ROOT,
        shell=False,
    )


def test_co_node():
    assert shutil.which("node"), "cần node để chạy cổng giấy phép"


def test_goi_gpl_bi_chan():
    r = run(GPL_CASE)
    assert r.returncode == 1, f"cổng không chặn GPL: exit {r.returncode}\n{r.stdout}"
    assert "GPL-3.0 ngoài allowlist" in r.stdout, r.stdout
