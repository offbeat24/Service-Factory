#!/usr/bin/env python3
"""Prepare Harness HQ for first use on a new machine."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def default_deck_root() -> Path:
    override = os.environ.get("HARNESS_DECK_ROOT")
    if override:
        return Path(override).expanduser()
    return ROOT.parent / "deck"


def ensure_pyyaml() -> None:
    try:
        import yaml  # noqa: F401
    except ImportError as exc:  # pragma: no cover - environment-specific fallback
        raise SystemExit(
            "PyYAML is required. Install it with `python3 -m pip install pyyaml`, "
            "then rerun `python3 scripts/setup_hq.py`."
        ) from exc


def run_validation() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_harness.py"), "--mode", "all"],
        check=True,
        cwd=str(ROOT),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--deck-root",
        type=Path,
        default=default_deck_root(),
        help="Directory where generated service repositories should live",
    )
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="Create local directories without running HQ validation",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    deck_root = args.deck_root.expanduser().resolve()

    deck_root.mkdir(parents=True, exist_ok=True)
    ensure_pyyaml()

    if not args.skip_validate:
        run_validation()

    print(f"HQ root: {ROOT}")
    print(f"Deck root: {deck_root}")
    print("Next: python3 scripts/generate_service_repo.py --spec examples/service.yaml")
    print("After generation: switch Codex to the generated repo and continue product work there, not in HQ.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
