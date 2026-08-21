"""Cover text → recipe. Filename is not the porter."""

from __future__ import annotations

from pathlib import Path

from schemas.parse_artifact import ParseArtifact, fold, load_parse

UNKNOWN = "UNKNOWN"

COVER_SKIP = (
    "memoria",
    "presentacion de resultados",
    "presentación de resultados",
    "transcripcion",
    "transcripción",
    "preguntas y respuestas",
)


def _recipe_ids(recipe_ids: tuple[str, ...] | None) -> tuple[str, ...]:
    if recipe_ids is not None:
        return recipe_ids
    from schemas.catalog import load_recipes

    return tuple(load_recipes())


def classify_text(text: str, recipe_ids: tuple[str, ...] | None = None) -> str:
    """Return a recipe id or UNKNOWN from parse cover text."""
    ids = _recipe_ids(recipe_ids)
    cover = fold(text)
    if any(token in cover for token in COVER_SKIP):
        return UNKNOWN
    if "press_release" in ids and (
        "comunicado de prensa" in cover or "anuncia resultados" in cover
    ):
        return "press_release"
    if "financial_statement" in ids and "estados financieros" in cover:
        return "financial_statement"
    return UNKNOWN


def classify_pdf(pdf: Path, recipe_ids: tuple[str, ...] | None = None) -> str:
    artifact = load_parse(pdf)
    if artifact is None:
        return UNKNOWN
    return classify_text(artifact.cover, recipe_ids)


def classify_artifact(artifact: ParseArtifact, recipe_ids: tuple[str, ...] | None = None) -> str:
    return classify_text(artifact.cover, recipe_ids)


# Kept for tests that still name the old porter; delegates to content when a parse exists.
def classify_filename(name: str, recipe_ids: tuple[str, ...] | None = None) -> str:
    from schemas.corpus import SAMPLES

    pdf = SAMPLES / name
    if pdf.is_file() and load_parse(pdf) is not None:
        return classify_pdf(pdf, recipe_ids)
    return UNKNOWN


def dedicated_financial_statement(name: str) -> bool:
    return classify_filename(name) == "financial_statement"
