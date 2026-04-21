#!/usr/bin/env python3
"""Generate a minimal CLAUDE.md shim from AGENTS.md and selected docs."""

from __future__ import annotations

import argparse
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def build_shim(repo_root: Path) -> str:
    agents = read_text(repo_root / "AGENTS.md")
    why = read_text(repo_root / "docs" / "architecture" / "why.kr.md")
    product = read_text(repo_root / "docs" / "product" / "product-spec.kr.md")
    art_direction = read_text(repo_root / "docs" / "design" / "art-direction.kr.md")
    ui_principles = read_text(repo_root / "docs" / "design" / "ui-principles.kr.md")
    browser_review = read_text(repo_root / "docs" / "design" / "browser-review.kr.md")
    return "\n\n".join(
        [
            "# CLAUDE.md",
            "This file is generated from the canonical AGENTS.md and selected repo docs.",
            agents,
            "## Imported Architecture Notes",
            why,
            "## Imported Product Notes",
            product,
            "## Imported Art Direction",
            art_direction,
            "## Imported UI Principles",
            ui_principles,
            "## Imported Browser Review Checklist",
            browser_review,
        ]
    ) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    output = args.output.resolve() if args.output else repo_root / "CLAUDE.md"
    output.write_text(build_shim(repo_root), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
