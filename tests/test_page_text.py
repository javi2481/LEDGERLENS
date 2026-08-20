"""pdftotext argv is a list; never a shell string built from the filename."""

from __future__ import annotations

from pathlib import Path

from schemas.page_text import pdftotext_argv


def test_pdftotext_argv_is_list_not_shell_string() -> None:
    pdf = Path("/tmp/evil; rm -rf /; BYMA_-_EEFF.pdf")
    cmd = pdftotext_argv(pdf, 4)
    assert isinstance(cmd, list)
    assert cmd[0] == "pdftotext"
    assert "-layout" in cmd
    assert "-f" in cmd and "-l" in cmd
    assert "4" in cmd
    assert str(pdf) in cmd
    assert all(isinstance(part, str) for part in cmd)
    assert cmd[cmd.index(str(pdf))] == str(pdf)
