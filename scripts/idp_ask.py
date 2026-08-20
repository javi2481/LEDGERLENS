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

from schemas.corpus import extract_claims_from_dir
from schemas.lookup import lookup


def main() -> int:
    parser = argparse.ArgumentParser(description="Identity lookup over docs/archivos_muestra/")
    parser.add_argument("question", nargs="+", help="Pregunta en español")
    args = parser.parse_args()
    question = " ".join(args.question)
    claims = extract_claims_from_dir()
    result = lookup(question, claims)
    payload = {
        "route": result.route,
        "compare": result.compare,
        "abstain_reason": result.abstain_reason,
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
