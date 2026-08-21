"""Retrieval pilot metrics. Ranked {doc, page} vs gold. No RAGFlow."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

Hit = tuple[str, int]


def as_hit(row: dict) -> Hit | None:
    doc = row.get("doc")
    page = row.get("page")
    if not isinstance(doc, str) or not isinstance(page, int):
        return None
    return (doc, page)


def gold_set(relevant: Iterable[dict]) -> set[Hit]:
    out: set[Hit] = set()
    for row in relevant:
        hit = as_hit(row)
        if hit is not None:
            out.add(hit)
    return out


def ranked_hits(rows: Sequence[dict]) -> list[Hit]:
    out: list[Hit] = []
    seen: set[Hit] = set()
    for row in rows:
        hit = as_hit(row)
        if hit is None or hit in seen:
            continue
        seen.add(hit)
        out.append(hit)
    return out


def first_gold_rank(ranked: Sequence[Hit], gold: set[Hit]) -> int | None:
    for idx, hit in enumerate(ranked, start=1):
        if hit in gold:
            return idx
    return None


def recall_at_k(ranked: Sequence[Hit], gold: set[Hit], k: int) -> float:
    if not gold:
        return 0.0
    return 1.0 if first_gold_rank(ranked[:k], gold) is not None else 0.0


def mrr(ranked: Sequence[Hit], gold: set[Hit]) -> float:
    rank = first_gold_rank(ranked, gold)
    if rank is None:
        return 0.0
    return 1.0 / rank


def mean(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def score_case(ranked_rows: Sequence[dict], relevant: Iterable[dict], *, k5: int = 5, k10: int = 10) -> dict:
    ranked = ranked_hits(ranked_rows)
    gold = gold_set(relevant)
    return {
        "recall@5": recall_at_k(ranked, gold, k5),
        "recall@10": recall_at_k(ranked, gold, k10),
        "mrr": mrr(ranked, gold),
    }


def summarize_arm(case_scores: Sequence[dict]) -> dict:
    return {
        "recall@5": round(mean([row["recall@5"] for row in case_scores]), 4),
        "recall@10": round(mean([row["recall@10"] for row in case_scores]), 4),
        "mrr": round(mean([row["mrr"] for row in case_scores]), 4),
        "n": len(case_scores),
    }
