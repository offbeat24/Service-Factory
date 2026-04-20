from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_service_repo.py"
SETUP = ROOT / "scripts" / "setup_hq.py"
VALIDATOR = ROOT / "scripts" / "validate_harness.py"
EXAMPLE_SPEC = ROOT / "examples" / "service.yaml"


def run(command: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd),
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


class HarnessHQTests(unittest.TestCase):
    def test_validate_hq_all(self) -> None:
        run([sys.executable, str(VALIDATOR), "--mode", "all"], ROOT)

    def test_generate_service_repo_creates_expected_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-generate-") as tmpdir:
            output_root = Path(tmpdir) / "out"
            run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--spec",
                    str(EXAMPLE_SPEC),
                    "--output-root",
                    str(output_root),
                ],
                ROOT,
            )
            repo = output_root / "focus-sprint"
            self.assertTrue((repo / "AGENTS.md").exists())
            self.assertTrue((repo / ".gitignore").exists())
            self.assertTrue((repo / ".codex" / "config.toml").exists())
            self.assertTrue((repo / ".codex" / "hooks.json").exists())
            self.assertTrue((repo / "docs-manifest.json").exists())
            self.assertTrue((repo / "docs" / "product" / "product-spec.kr.md").exists())
            self.assertTrue((repo / "scripts" / "harness.py").exists())
            config_text = (repo / ".codex" / "config.toml").read_text(encoding="utf-8")
            self.assertIn('model = "gpt-5.4"', config_text)
            self.assertIn('review_model = "gpt-5.4"', config_text)
            self.assertIn("max_depth = 1", config_text)

    def test_setup_hq_creates_requested_deck_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-setup-") as tmpdir:
            deck_root = Path(tmpdir) / "deck"
            run(
                [
                    sys.executable,
                    str(SETUP),
                    "--deck-root",
                    str(deck_root),
                    "--skip-validate",
                ],
                ROOT,
            )
            self.assertTrue(deck_root.exists())
            self.assertTrue(deck_root.is_dir())

    def test_generated_repo_gates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-repo-") as tmpdir:
            output_root = Path(tmpdir) / "out"
            run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--spec",
                    str(EXAMPLE_SPEC),
                    "--output-root",
                    str(output_root),
                ],
                ROOT,
            )
            repo = output_root / "focus-sprint"
            self._init_git_repo(repo)

            run([sys.executable, "scripts/harness.py", "pre-task"], repo)

            failed = run(
                [sys.executable, "scripts/harness.py", "pre-complete"],
                repo,
                check=False,
            )
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("required file is missing: artifacts/run-reports/BOOTSTRAP-001.json", failed.stderr)

            report_path = repo / "artifacts" / "run-reports" / "BOOTSTRAP-001.json"
            report_path.write_text(
                json.dumps(
                    {
                        "task_id": "BOOTSTRAP-001",
                        "provider": "openai",
                        "lead_model": "gpt-5.4",
                        "worker_models": ["gpt-5.4-mini"],
                        "changed_scope": ["docs/product/product-spec.kr.md"],
                        "verification_results": [{"name": "pre-complete", "status": "passed"}],
                        "evidence_paths": [],
                        "failures": [],
                        "handoff_notes": ["Bootstrap notes are recorded."],
                        "next_actions": ["Start the first implementation slice."]
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            run([sys.executable, "scripts/harness.py", "pre-complete"], repo)

    def _init_git_repo(self, repo: Path) -> None:
        run(["git", "init", "-b", "main"], repo)
        run(["git", "config", "user.name", "Harness HQ"], repo)
        run(["git", "config", "user.email", "harness@example.com"], repo)
        run(["git", "add", "."], repo)
        run(["git", "commit", "-m", "initial scaffold"], repo)
        run(["git", "checkout", "-b", "task/BOOTSTRAP-001-init"], repo)


if __name__ == "__main__":
    unittest.main()
