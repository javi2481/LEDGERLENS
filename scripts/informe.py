#!/usr/bin/env python3
"""Write academic dossier HTML from accepted claims + gold evals. No RAGFlow."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from schemas.classify import classify_pdf
from schemas.corpus import SAMPLES
from schemas.dossier import render_dossier
from schemas.review import load_verdicts
from schemas.store import load_claims


def classified_samples(folder: Path | None = None) -> dict[str, str]:
    directory = folder or SAMPLES
    return {pdf.name: classify_pdf(pdf) for pdf in sorted(directory.glob("*.pdf"))}


def main() -> int:
    parser = argparse.ArgumentParser(description="Dossier HTML académico BYMA")
    parser.add_argument("--verdicts", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=ROOT / "outputs" / "dossier.html")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    claims, _cached = load_claims(force=args.refresh)
    verdicts = load_verdicts(args.verdicts)
    html = render_dossier(
        claims,
        verdicts=verdicts,
        classified=classified_samples(),
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
