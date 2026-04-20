#!/bin/sh
set -eu

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
python3 "$ROOT_DIR/scripts/harness.py" pre-commit

