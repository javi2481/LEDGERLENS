"""Layer 2: lexical query understanding + identity lookup. No embeddings."""

from __future__ import annotations

from dataclasses import dataclass

from schemas.claim import (
    SCOPE_CONSOLIDADO,
    SCOPE_CONTROLANTE,
    Claim,
    Route,
)
from schemas.extract import fold

PERIOD_1T26 = "2026-03-31"
PERIOD_2T26 = "2026-06-30"


@dataclass(frozen=True)
class Intent:
    route: Route
    scope: str | None
    period: str | None
    compare: bool
    abstain_reason: str | None = None


@dataclass(frozen=True)
class LookupResult:
    route: Route
    claims: tuple[Claim, ...]
    abstain_reason: str | None
    compare: bool


def understand(question: str) -> Intent:
    q = fold(question)
    if any(token in q for token in ("ypf",)) and any(
        token in q for token in ("precio", "cierre", "3 de enero", "3 enero")
    ):
        return Intent("abstain", None, None, False, "off_corpus")
    if "memoria" in q and any(token in q for token in ("resultado", "neto", "eeff", "pl")):
        return Intent("abstain", None, None, False, "recipe_no_extract")
    if "comunicado" in q and any(token in q for token in ("resultado neto", "consolidado", "controlante")):
        return Intent("abstain", None, None, False, "recipe_no_extract")
    if any(token in q for token in ("contrato", "clausula", "cláusula")):
        return Intent("abstain", None, None, False, "recipe_no_extract")
    narrative_hits = (
        "crecimiento de ingresos",
        "explica",
        "politica contable",
        "highlights",
        "presentacion de resultados",
        "hechos relevantes",
        "webcast",
        "conference call",
        "slides",
    )
    if any(token in q for token in narrative_hits) and "resultado neto" not in q:
        return Intent("narrative", None, None, False, None)

    compare = any(
        token in q
        for token in ("compar", " vs ", "versus", "mayor", "diferencia", "ambos periodos", "ambos períodos")
    )
    period: str | None = None
    has_1t = any(
        token in q
        for token in ("1t26", "1t 26", "marzo", "2026-03-31", "31 de marzo", "primer trimestre")
    )
    has_2t = any(
        token in q
        for token in ("2t26", "2t 26", "junio", "2026-06-30", "30 de junio", "segundo trimestre")
    )
    if has_1t and not has_2t:
        period = PERIOD_1T26
    elif has_2t and not has_1t:
        period = PERIOD_2T26
    elif has_1t and has_2t:
        compare = True
        period = None

    negated_parent = any(
        phrase in q
        for phrase in (
            "no el atribuible",
            "no atribuible",
            "no la controlante",
            "no el controlante",
            "no controlante",
        )
    )
    controlante = (
        "controlante" in q or "atribuible" in q or "propietarios" in q
    ) and not negated_parent
    identity_ask = any(
        token in q
        for token in (
            "resultado neto",
            "neto del",
            "del periodo",
            "del período",
            "trimestre",
            "consolidado",
            "eeff",
            "1t26",
            "2t26",
            "sintesis",
            "síntesis",
        )
    )
    if controlante:
        return Intent("identity", SCOPE_CONTROLANTE, period, compare, None)
    if identity_ask or compare:
        return Intent("identity", SCOPE_CONSOLIDADO, period, compare, None)
    return Intent("abstain", None, None, False, "unresolved_identity")


def lookup(question: str, claims: tuple[Claim, ...] | list[Claim]) -> LookupResult:
    intent = understand(question)
    store = tuple(claims)
    if intent.route == "narrative":
        return LookupResult("narrative", (), None, False)
    if intent.route == "abstain":
        return LookupResult("abstain", (), intent.abstain_reason, False)

    scoped = tuple(c for c in store if c.scope == intent.scope)
    if intent.period:
        scoped = tuple(c for c in scoped if c.period == intent.period)
    if not scoped:
        return LookupResult("abstain", (), "no_matching_claim", False)
    periods = {c.period for c in scoped}
    if intent.compare:
        by_period: dict[str, Claim] = {}
        for claim in scoped:
            by_period.setdefault(claim.period, claim)
        ordered = tuple(by_period[k] for k in sorted(by_period))
        if len(ordered) < 2:
            return LookupResult("abstain", (), "incomplete_comparison", False)
        return LookupResult("identity", ordered, None, True)
    if intent.period is None and len(periods) > 1:
        return LookupResult("abstain", (), "ambiguous_period", False)
    return LookupResult("identity", (scoped[0],), None, False)
