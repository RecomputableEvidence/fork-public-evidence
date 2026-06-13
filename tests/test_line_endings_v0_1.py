from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_line_endings.py"
NORMALIZER = ROOT / "tools" / "normalize_line_endings.py"


def run_command(*args: str | Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(arg) for arg in args],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_checker_accepts_lf_file(tmp_path: Path) -> None:
    sample = tmp_path / "sample.md"
    sample.write_bytes(b"# Title\n\nBody\n")

    result = run_command(sys.executable, CHECKER, sample)

    assert result.returncode == 0, result.stderr
    assert "LINE_ENDING_PASS" in result.stdout


def test_checker_rejects_crlf_file(tmp_path: Path) -> None:
    sample = tmp_path / "sample.md"
    sample.write_bytes(b"# Title\r\n\r\nBody\r\n")

    result = run_command(sys.executable, CHECKER, sample)

    assert result.returncode != 0
    assert "LINE_ENDING_DEFECT" in result.stderr
    assert "CRLF" in result.stderr


def test_normalizer_converts_crlf_to_lf(tmp_path: Path) -> None:
    sample = tmp_path / "sample.json"
    sample.write_bytes(b"{\r\n  \"ok\": true\r\n}\r\n")

    normalize_result = run_command(sys.executable, NORMALIZER, sample)

    assert normalize_result.returncode == 0, normalize_result.stderr
    assert b"\r\n" not in sample.read_bytes()
    assert b"\r" not in sample.read_bytes()

    check_result = run_command(sys.executable, CHECKER, sample)

    assert check_result.returncode == 0, check_result.stderr
    assert "LINE_ENDING_PASS" in check_result.stdout


def test_repository_governed_text_artifacts_use_lf() -> None:
    result = run_command(sys.executable, CHECKER)

    assert result.returncode == 0, result.stderr
    assert "LINE_ENDING_PASS" in result.stdout