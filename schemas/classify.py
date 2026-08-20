"""Filename → recipe. Domain plugins register via recipes/; this heuristic is generic."""

from __future__ import annotations

SKIP_SUBSTR = (
    "memoria",
    "comunicado",
    "presentacion",
    "presentación",
    "transcripcion",
    "transcripción",
)

UNKNOWN = "UNKNOWN"


def dedicated_financial_statement(name: str) -> bool:
    """Dedicated EEFF filing, not a memoria/comunicado/deck/transcript."""
    lower = name.lower()
    if not lower.endswith(".pdf"):
        return False
    if "eeff" not in lower:
        return False
    return not any(token in lower for token in SKIP_SUBSTR)


def dedicated_press_release(name: str) -> bool:
    lower = name.lower()
    if not lower.endswith(".pdf"):
        return False
    return "comunicado" in lower


def classify_filename(name: str, recipe_ids: tuple[str, ...] | None = None) -> str:
    """Return a recipe id or UNKNOWN. Finance is one plugin, not the kernel."""
    ids = recipe_ids
    if ids is None:
        from schemas.catalog import load_recipes

        ids = tuple(load_recipes())
    if dedicated_financial_statement(name) and "financial_statement" in ids:
        return "financial_statement"
    if dedicated_press_release(name) and "press_release" in ids:
        return "press_release"
    return UNKNOWN
