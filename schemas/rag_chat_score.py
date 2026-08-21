"""Score rag_chat_v1 dumps. Identity exact-match; abstain; citation docs. No RAGFlow."""

from __future__ import annotations

from collections.abc import Sequence

EMPTY_HINTS = (
    "no hay evidencia",
    "no invento",
    "no cuento con",
)


def _digits(text: str) -> str:
    return "".join(ch for ch in text if ch.isdigit())


def cited_ok(cited: Sequence[str], expected_docs: Sequence[str]) -> bool:
    if not expected_docs:
        return True
    have = {name.casefold() for name in cited}
    return any(doc.casefold() in have for doc in expected_docs)


def looks_abstained(answer: str, flagged: bool) -> bool:
    if flagged:
        return True
    blob = " ".join(answer.casefold().split())
    return any(hint in blob for hint in EMPTY_HINTS)


def score_chat_case(case: dict, run: dict) -> dict:
    partition = str(case.get("partition") or "")
    answer = str(run.get("answer") or "")
    cited = [str(x) for x in (run.get("cited_docs") or [])]
    abstained = looks_abstained(answer, bool(run.get("abstained")))
    expected_docs = [str(x) for x in (case.get("expected_docs") or [])]
    expected_value = case.get("expected_value")
    forbid = [str(x) for x in (case.get("forbid_values") or [])]
    want_abstain = bool(case.get("expected_abstain"))
    compact = answer.replace(".", "").replace(",", "").replace(" ", "")
    digit_blob = _digits(answer)

    retrieval = cited_ok(cited, expected_docs)
    citation = retrieval and not any("hechos_eeff" in name.casefold() for name in cited)
    leaked = any(val and (val in compact or val in digit_blob) for val in forbid)

    if want_abstain:
        return {
            "retrieval": 1.0,
            "answer": 1.0 if abstained and not leaked else 0.0,
            "citation": 1.0,
            "abstention": 1.0 if abstained and not leaked else 0.0,
        }

    if partition == "narrative":
        ok = (not abstained) and not leaked and retrieval
        return {
            "retrieval": 1.0 if retrieval else 0.0,
            "answer": 1.0 if ok else 0.0,
            "citation": 1.0 if citation else 0.0,
            "abstention": 1.0,
        }

    value_ok = expected_value is None or str(expected_value) in compact or str(expected_value) in digit_blob
    ok = value_ok and not leaked and not abstained
    if partition == "comparison":
        retrieval = all(cited_ok(cited, [doc]) for doc in expected_docs) if expected_docs else True
        citation = retrieval
    return {
        "retrieval": 1.0 if retrieval else 0.0,
        "answer": 1.0 if ok else 0.0,
        "citation": 1.0 if citation else 0.0,
        "abstention": 1.0 if not abstained else 0.0,
    }


def summarize_chat(scores: Sequence[dict]) -> dict:
    if not scores:
        return {"retrieval": 0.0, "answer": 0.0, "citation": 0.0, "abstention": 0.0, "n": 0}
    n = len(scores)
    return {
        "retrieval": round(sum(s["retrieval"] for s in scores) / n, 4),
        "answer": round(sum(s["answer"] for s in scores) / n, 4),
        "citation": round(sum(s["citation"] for s in scores) / n, 4),
        "abstention": round(sum(s["abstention"] for s in scores) / n, 4),
        "n": n,
    }
