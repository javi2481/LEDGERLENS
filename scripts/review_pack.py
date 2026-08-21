#!/usr/bin/env python3
"""Write HITL review HTML from kernel claims. No RAGFlow."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from schemas.review import load_verdicts, render_review_html
from schemas.store import load_claims


def main() -> int:
    parser = argparse.ArgumentParser(description="Paquete HTML de revisión HITL")
    parser.add_argument(
        "--verdicts",
        type=Path,
        default=None,
        help="JSON de veredictos (omitido = todo accept)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "outputs" / "review.html",
    )
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    claims, _cached = load_claims(force=args.refresh)
    verdicts = load_verdicts(args.verdicts)
    html = render_review_html(claims, verdicts=verdicts)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
