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
            self.assertTrue((repo / ".nvmrc").exists())
            self.assertTrue((repo / ".node-version").exists())
            self.assertTrue((repo / ".gitmessage.txt").exists())
            self.assertTrue((repo / ".codex" / "config.toml").exists())
            self.assertTrue((repo / ".codex" / "hooks.json").exists())
            self.assertTrue((repo / ".codex" / "agents" / "architecture-planner.toml").exists())
            self.assertTrue((repo / ".codex" / "agents" / "implementation-worker.toml").exists())
            self.assertTrue((repo / ".codex" / "agents" / "long-runner.toml").exists())
            self.assertTrue((repo / ".githooks" / "commit-msg").exists())
            self.assertTrue((repo / "docs-manifest.json").exists())
            self.assertTrue((repo / "docs" / "product" / "product-spec.kr.md").exists())
            self.assertTrue((repo / "docs" / "design" / "art-direction.kr.md").exists())
            self.assertTrue((repo / "docs" / "design" / "browser-review.kr.md").exists())
            self.assertTrue((repo / "docs" / "design" / "ui-principles.kr.md").exists())
            self.assertTrue((repo / "docs" / "prompting" / "prompt-context.kr.md").exists())
            self.assertTrue((repo / "scripts" / "harness.py").exists())
            config_text = (repo / ".codex" / "config.toml").read_text(encoding="utf-8")
            self.assertIn('model = "gpt-5.4"', config_text)
            self.assertIn('review_model = "gpt-5.5"', config_text)
            self.assertIn("max_depth = 1", config_text)
            planner_text = (repo / ".codex" / "agents" / "architecture-planner.toml").read_text(encoding="utf-8")
            self.assertIn('model = "gpt-5.5"', planner_text)
            worker_text = (repo / ".codex" / "agents" / "implementation-worker.toml").read_text(encoding="utf-8")
            self.assertIn('model = "gpt-5.3-codex"', worker_text)
            self.assertEqual((repo / ".nvmrc").read_text(encoding="utf-8").strip(), "20.19.6")
            self.assertEqual((repo / ".node-version").read_text(encoding="utf-8").strip(), "20.19.6")
            art_direction_text = (repo / "docs" / "design" / "art-direction.kr.md").read_text(encoding="utf-8")
            self.assertIn("Linear landing page clarity", art_direction_text)
            browser_review_text = (repo / "docs" / "design" / "browser-review.kr.md").read_text(encoding="utf-8")
            self.assertIn("Codex browser 또는 Computer Use", browser_review_text)
            self.assertIn("기능 리뷰", browser_review_text)
            product_spec_text = (repo / "docs" / "product" / "product-spec.kr.md").read_text(encoding="utf-8")
            self.assertIn("keywords: calm, sharp, execution", product_spec_text)
            readme_text = (repo / "README.md").read_text(encoding="utf-8")
            self.assertIn("Node 20.19.6 LTS", readme_text)
            self.assertIn("Switch Codex to this generated repo", readme_text)
            self.assertIn("feature/BOOTSTRAP-001-init", readme_text)
            self.assertIn("git config commit.template .gitmessage.txt", readme_text)
            prompt_context_text = (repo / "docs" / "prompting" / "prompt-context.kr.md").read_text(encoding="utf-8")
            self.assertIn("서비스 이름: Focus Sprint", prompt_context_text)
            self.assertIn("톤: sharp and disciplined", prompt_context_text)

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
                        "worker_models": ["gpt-5.4-mini", "gpt-5.3-codex", "gpt-5.2"],
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

    def test_generated_repo_syncs_prompt_context_from_service_yaml(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-prompt-context-") as tmpdir:
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
            service_yaml = (repo / "service.yaml").read_text(encoding="utf-8")
            service_yaml = service_yaml.replace("  tone: sharp and disciplined\n", "  tone: precise and calm\n")
            (repo / "service.yaml").write_text(service_yaml, encoding="utf-8")
            run([sys.executable, "scripts/harness.py", "sync-prompt-context", "--task-id", "BOOTSTRAP-001"], repo)
            prompt_context_text = (repo / "docs" / "prompting" / "prompt-context.kr.md").read_text(encoding="utf-8")
            self.assertIn("톤: precise and calm", prompt_context_text)

    def test_generated_repo_rejects_incomplete_branding(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-branding-") as tmpdir:
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
            broken = (repo / "service.yaml").read_text(encoding="utf-8").replace("  tone: sharp and disciplined\n", "")
            (repo / "service.yaml").write_text(broken, encoding="utf-8")
            failed = run([sys.executable, "scripts/harness.py", "pre-task"], repo, check=False)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("branding missing required keys: tone", failed.stderr)

    def test_generated_repo_rejects_missing_top_level_service_field(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-service-fields-") as tmpdir:
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
            broken = (repo / "service.yaml").read_text(encoding="utf-8").replace(
                "problem: Users collect many ideas but fail to turn them into a clear sprint plan, daily execution loop, and evidence-backed review ritual.\n",
                "",
            )
            (repo / "service.yaml").write_text(broken, encoding="utf-8")
            failed = run([sys.executable, "scripts/harness.py", "pre-task"], repo, check=False)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("service.yaml missing required keys: problem", failed.stderr)

    def test_generated_repo_rejects_task_pack_missing_design_docs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-task-pack-") as tmpdir:
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
            payload = json.loads((repo / "task-pack.json").read_text(encoding="utf-8"))
            payload["must_read"] = [entry for entry in payload["must_read"] if "docs/design/" not in entry]
            payload["docs_required"] = [entry for entry in payload["docs_required"] if "docs/design/" not in entry]
            (repo / "task-pack.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            failed = run([sys.executable, "scripts/harness.py", "pre-task"], repo, check=False)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("task-pack.json must_read missing required doc: docs/design/art-direction.kr.md", failed.stderr)

    def test_generated_repo_rejects_task_pack_missing_browser_review_doc(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-browser-review-") as tmpdir:
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
            payload = json.loads((repo / "task-pack.json").read_text(encoding="utf-8"))
            payload["must_read"] = [entry for entry in payload["must_read"] if entry != "docs/design/browser-review.kr.md"]
            payload["docs_required"] = [entry for entry in payload["docs_required"] if entry != "docs/design/browser-review.kr.md"]
            (repo / "task-pack.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            failed = run([sys.executable, "scripts/harness.py", "pre-task"], repo, check=False)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("task-pack.json must_read missing required doc: docs/design/browser-review.kr.md", failed.stderr)

    def _init_git_repo(self, repo: Path) -> None:
        run(["git", "init", "-b", "main"], repo)
        run(["git", "config", "user.name", "Harness HQ"], repo)
        run(["git", "config", "user.email", "harness@example.com"], repo)
        run(["git", "add", "."], repo)
        run(["git", "commit", "-m", "chore: Initial scaffold"], repo)
        run(["git", "checkout", "-b", "feature/BOOTSTRAP-001-init"], repo)


if __name__ == "__main__":
    unittest.main()
