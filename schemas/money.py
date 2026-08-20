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
