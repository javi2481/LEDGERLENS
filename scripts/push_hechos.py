#!/usr/bin/env python3
"""Alias: inject kernel claims into RAGFlow. Prefer scripts/push_claims.py."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from push_claims import main

if __name__ == "__main__":
    raise SystemExit(main())
