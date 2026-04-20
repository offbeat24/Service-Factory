name: harness

on:
  push:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install Python requirements
        run: python3 -m pip install pyyaml
      - name: Validate service harness
        run: python3 scripts/harness.py ci
