"""Pure retrieval metrics: no HTTP, no RAGFlow."""

from schemas.retrieval_metrics import recall_at_k, mrr, score_case, summarize_arm
from schemas.rag_chat_score import score_chat_case, summarize_chat

EEFF = "BYMA_-_EEFF_31-03-2026_VF.pdf"
GOLD = [{"doc": EEFF, "page": 4}]


def test_chunk_to_hit_reads_positions() -> None:
    from schemas.ragflow_http import chunk_to_hit

    hit = chunk_to_hit(
        {
            "document_keyword": "BYMA_-_EEFF_31-03-2026_VF.pdf",
            "positions": [[4, 0, 0, 0]],
        }
    )
    assert hit == {"doc": "BYMA_-_EEFF_31-03-2026_VF.pdf", "page": 4}
    ranked = [(EEFF, 1), (EEFF, 4), ("other.pdf", 2)]
    gold = {(EEFF, 4)}
    assert recall_at_k(ranked, gold, 1) == 0.0
    assert recall_at_k(ranked, gold, 5) == 1.0
    assert mrr(ranked, gold) == 0.5


def test_score_case_from_dicts() -> None:
    ranked = [{"doc": EEFF, "page": 4}, {"doc": "press.pdf", "page": 2}]
    scores = score_case(ranked, GOLD)
    assert scores["recall@5"] == 1.0
    assert scores["recall@10"] == 1.0
    assert scores["mrr"] == 1.0


def test_summarize_arm() -> None:
    rows = [
        {"recall@5": 1.0, "recall@10": 1.0, "mrr": 1.0},
        {"recall@5": 0.0, "recall@10": 1.0, "mrr": 0.5},
    ]
    out = summarize_arm(rows)
    assert out["n"] == 2
    assert out["recall@5"] == 0.5
    assert out["recall@10"] == 1.0
    assert out["mrr"] == 0.75


def test_identity_chat_score() -> None:
    case = {
        "partition": "identity",
        "expected_value": "21262335",
        "expected_docs": [EEFF],
        "forbid_values": ["21259769"],
        "expected_abstain": False,
    }
    ok = score_chat_case(case, {"answer": "El neto es 21.262.335", "cited_docs": [EEFF]})
    assert ok["answer"] == 1.0
    assert ok["citation"] == 1.0
    bad = score_chat_case(case, {"answer": "21259769", "cited_docs": [EEFF]})
    assert bad["answer"] == 0.0


def test_abstain_chat_score() -> None:
    case = {
        "partition": "abstention",
        "expected_value": None,
        "expected_docs": [],
        "forbid_values": ["21262335"],
        "expected_abstain": True,
    }
    ok = score_chat_case(
        case,
        {"answer": "No hay evidencia suficiente en los documentos indexados para responder. No invento datos.", "cited_docs": [], "abstained": False},
    )
    assert ok["abstention"] == 1.0
    leak = score_chat_case(case, {"answer": "21262335", "cited_docs": []})
    assert leak["abstention"] == 0.0


def test_summarize_chat() -> None:
    scores = [
        {"retrieval": 1.0, "answer": 1.0, "citation": 1.0, "abstention": 1.0},
        {"retrieval": 0.0, "answer": 0.0, "citation": 0.0, "abstention": 1.0},
    ]
    out = summarize_chat(scores)
    assert out["n"] == 2
    assert out["retrieval"] == 0.5
    assert out["abstention"] == 1.0
