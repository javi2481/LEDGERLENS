#!/usr/bin/env python3
"""Cover-page orientation probe. Exit 0 and skip without Paddle. Not identity OCR."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from schemas.corpus import SAMPLES
from schemas.preprocess import probe_directory, report_json


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sonda de orientación (PP-LCNet_x1_0_doc_ori). Skip sin Paddle."
    )
    parser.add_argument("--dir", type=Path, default=SAMPLES)
    args = parser.parse_args()
    payload = probe_directory(args.dir)
    sys.stdout.write(report_json(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
