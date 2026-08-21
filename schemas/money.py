"""ARS amounts as printed in BYMA filings (thousands dots). Not an entity."""

from __future__ import annotations

from typing import Any


def digits_ars(value: Any) -> str | None:
    """Keep digits only. 21.262.335 → 21262335. None stays None."""
    if value is None:
        return None
    text = str(value).strip().replace(" ", "")
    if not text:
        return None
    if text.count(".") >= 1 and "," not in text:
        parts = text.split(".")
        if all(p.isdigit() for p in parts) and all(len(p) == 3 for p in parts[1:]):
            return "".join(parts)
    digits = "".join(ch for ch in text if ch.isdigit())
    return digits or None


def format_display_ars(value: Any) -> str:
    """21262335 → 21.262.335. Keeps a leading minus."""
    text = str(value).strip()
    sign = ""
    if text.startswith("-"):
        sign = "-"
        text = text[1:]
    digits = "".join(ch for ch in text if ch.isdigit())
    if not digits:
        return str(value)
    parts: list[str] = []
    while digits:
        parts.append(digits[-3:])
        digits = digits[:-3]
    return sign + ".".join(reversed(parts))


def signed_ars(value: Any) -> str | None:
    """Parentheses mean negative. (14.950.948) → -14950948."""
    if value is None:
        return None
    text = str(value).strip().replace(" ", "")
    if not text:
        return None
    negative = text.startswith("(") and text.endswith(")")
    inner = text[1:-1] if negative else text
    digits = digits_ars(inner)
    if not digits:
        return None
    return f"-{digits}" if negative else digits
