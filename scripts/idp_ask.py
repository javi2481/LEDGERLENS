#!/usr/bin/env python3
"""Ask an identity question against sample EEFF. No RAGFlow, no embeddings."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from schemas.lookup import lookup
from schemas.store import load_claims


def main() -> int:
    parser = argparse.ArgumentParser(description="Identity lookup over docs/archivos_muestra/")
    parser.add_argument("question", nargs="+", help="Pregunta en español")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Reextraer desde fixtures/mineru y reescribir outputs/claims.json",
    )
    args = parser.parse_args()
    question = " ".join(args.question)
    claims, cached = load_claims(force=args.refresh)
    result = lookup(question, claims)
    payload = {
        "route": result.route,
        "compare": result.compare,
        "abstain_reason": result.abstain_reason,
        "store": "hit" if cached else "miss",
        "claims": [
            {
                "identity_key": row.identity_key,
                "value": row.value,
                "period": row.period,
                "source_page": row.source_page,
                "source_text": row.source_text,
            }
            for row in result.claims
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
