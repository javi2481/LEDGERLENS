"""Preprocess orientation: skip without Paddle; argv list; no fixture writes."""

from __future__ import annotations

from pathlib import Path

from schemas.preprocess import SKIP_NO_PADDLE, pdftoppm_cmd, probe_directory


def test_skip_without_paddle(monkeypatch, tmp_path: Path) -> None:
    import schemas.preprocess as preprocess

    monkeypatch.setattr(preprocess, "paddle_available", lambda: False)
    pdfs = tmp_path / "pdfs"
    pdfs.mkdir()
    (pdfs / "a.pdf").write_bytes(b"%PDF-1.4\n")
    payload = probe_directory(pdfs)
    assert payload["skipped"] is True
    assert payload["reason"] == SKIP_NO_PADDLE
    assert payload["rows"] == []


def test_pdftoppm_is_argv_list(tmp_path: Path) -> None:
    pdf = tmp_path / "a.pdf"
    dest = tmp_path / "cover"
    cmd = pdftoppm_cmd(pdf, dest)
    assert cmd[0] == "pdftoppm"
    assert all(isinstance(part, str) for part in cmd)
    root = Path(__file__).resolve().parents[1]
    probe = (root / "scripts" / "preprocess_probe.py").read_text(encoding="utf-8")
    schema = (root / "schemas" / "preprocess.py").read_text(encoding="utf-8")
    assert "shell=True" not in probe
    assert "shell=True" not in schema
    assert "subprocess.run(pdftoppm_cmd" in schema


def test_probe_does_not_write_fixtures(monkeypatch, tmp_path: Path) -> None:
    import schemas.preprocess as preprocess

    monkeypatch.setattr(preprocess, "paddle_available", lambda: False)
    root = Path(__file__).resolve().parents[1]
    fixtures = root / "fixtures" / "mineru"
    before = (
        {p.name: p.stat().st_mtime_ns for p in fixtures.glob("*.md")}
        if fixtures.is_dir()
        else {}
    )
    probe_directory(tmp_path)
    after = (
        {p.name: p.stat().st_mtime_ns for p in fixtures.glob("*.md")}
        if fixtures.is_dir()
        else {}
    )
    assert after == before


def test_preprocess_not_in_requirements_dev() -> None:
    root = Path(__file__).resolve().parents[1]
    text = (root / "requirements-dev.txt").read_text(encoding="utf-8").lower()
    assert "paddle" not in text
    assert "paddlex" not in text
    assert "paddleocr" not in text
