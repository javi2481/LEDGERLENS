"""Kernel claims → RAGFlow ficha text. No HTTP."""

from __future__ import annotations

from schemas.claim import (
    METRIC_ATRIBUIBLE,
    METRIC_NETO,
    SCOPE_CONSOLIDADO,
    SCOPE_CONTROLANTE,
    Claim,
    identity_key,
)
from schemas.inject import (
    MARKER,
    MARKER_GRAPH,
    eeff_chunk,
    is_inject_chunk,
    prompt_lines,
    upsert_idp_prompt,
)
from schemas.money import format_display_ars


def _claim(period: str, scope: str, metric: str, value: str, page: int = 4) -> Claim:
    return Claim(
        identity_key=identity_key("BYMA", period, scope, metric),
        value=value,
        period=period,
        source_page=page,
        source_text=metric,
        issuer="BYMA",
        scope=scope,
        metric=metric,
    )


def test_format_display_ars() -> None:
    assert format_display_ars("21262335") == "21.262.335"
    assert format_display_ars("-14950948") == "-14.950.948"


def test_eeff_chunk_uses_idp_marker() -> None:
    claims = (
        _claim("2026-03-31", SCOPE_CONSOLIDADO, METRIC_NETO, "21262335"),
        _claim("2026-03-31", SCOPE_CONTROLANTE, METRIC_ATRIBUIBLE, "21259769"),
    )
    built = eeff_chunk(claims, "2026-03-31")
    assert built is not None
    content, _keywords, _questions = built
    assert MARKER in content
    assert "21.262.335" in content
    assert "21.259.769" in content
    assert "hechos_eeff.md" not in content
    assert MARKER in content


def test_upsert_replaces_graph_block() -> None:
    old = "--- Fichas Graph (LedgerLens) ---\nOLD\n--- Fin fichas Graph ---\n{knowledge}"
    text = upsert_idp_prompt(old, "NEW RULES")
    assert "OLD" not in text
    assert "Fichas IDP" in text
    assert "{knowledge}" in text


def test_is_inject_chunk_sees_graph_and_idp() -> None:
    assert is_inject_chunk(f"{MARKER} hello")
    assert is_inject_chunk(f"{MARKER_GRAPH} hello")
    assert not is_inject_chunk("plain chunk")


def test_prompt_lists_all_scopes() -> None:
    claims = (
        _claim("2026-03-31", SCOPE_CONSOLIDADO, METRIC_NETO, "21262335"),
        _claim("2026-03-31", "comunicado", "press_as_of_date", "2026-05-08", 1),
    )
    blob = prompt_lines(claims)
    assert "comunicado|press_as_of_date" in blob
    assert "2026-05-08" in blob
