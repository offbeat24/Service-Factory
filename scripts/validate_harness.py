#!/usr/bin/env python3
"""Validate Harness HQ contracts, templates, and examples."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment-specific fallback
    raise SystemExit("PyYAML is required. Install it with `python3 -m pip install pyyaml`.") from exc


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS_ROOT = ROOT / ".harness" / "contracts"
TEMPLATE_ROOT = ROOT / ".harness" / "templates" / "service-repo"
EXAMPLES_ROOT = ROOT / "examples"
EXPECTED_LEAD_MODEL = "gpt-5.4"
EXPECTED_REVIEW_MODEL = "gpt-5.5"
EXPECTED_PLANNER_MODEL = "gpt-5.5"
EXPECTED_DOC_MODEL = "gpt-5.4-mini"
EXPECTED_CODING_WORKER_MODEL = "gpt-5.3-codex"
EXPECTED_LONG_RUNNER_MODEL = "gpt-5.2"
EXPECTED_UI_CHECKER_MODEL = "gpt-5.4"
EXPECTED_WORKER_MODELS = [
    EXPECTED_DOC_MODEL,
    EXPECTED_CODING_WORKER_MODEL,
    EXPECTED_LONG_RUNNER_MODEL,
]
REQUIRED_BRANDING_FIELDS = [
    "tone",
    "visual_direction",
    "keywords",
]
REQUIRED_TASK_PACK_READS = [
    "docs/design/art-direction.kr.md",
    "docs/design/ui-principles.kr.md",
    "docs/design/browser-review.kr.md",
    "docs/prompting/prompt-context.kr.md",
]
REQUIRED_TEMPLATES = [
    "AGENTS.md.tpl",
    "README.md.tpl",
    ".gitignore.tpl",
    ".nvmrc.tpl",
    ".node-version.tpl",
    ".gitmessage.txt.tpl",
    ".codex/config.toml.tpl",
    ".codex/hooks.json.tpl",
    ".codex/agents/architecture-planner.toml.tpl",
    ".codex/agents/reviewer.toml.tpl",
    ".codex/agents/ui-checker.toml.tpl",
    ".codex/agents/doc-gardener.toml.tpl",
    ".codex/agents/implementation-worker.toml.tpl",
    ".codex/agents/long-runner.toml.tpl",
    ".github/workflows/harness.yml.tpl",
    ".githooks/pre-commit.tpl",
    ".githooks/commit-msg.tpl",
    "scripts/harness.py.tpl",
    "scripts/generate_claude_shim.py.tpl",
    "docs/product/product-spec.kr.md.tpl",
    "docs/design/art-direction.kr.md.tpl",
    "docs/design/browser-review.kr.md.tpl",
    "docs/design/ui-principles.kr.md.tpl",
    "docs/prompting/prompt-context.kr.md.tpl",
    "docs/exec-plans/active/BOOTSTRAP-001.kr.md.tpl",
    "docs/exec-plans/completed/INIT-000.kr.md.tpl",
    "docs/build-journal.kr.md.tpl",
    "docs/architecture/why.kr.md.tpl",
    "docs/retrospectives/harness-feedback.kr.md.tpl",
    "docs/public/case-study.en.md.tpl",
    "artifacts/run-reports/INIT-000.json.tpl",
    "task-pack.json.tpl",
]

REQUIRED_SERVICE_FIELDS = [
    "id",
    "name",
    "concept",
    "target_users",
    "problem",
    "pages",
    "core_flows",
    "data_entities",
    "branding",
    "monetization",
    "auth_need",
    "storage_need",
    "deploy_preference",
    "domain_preference",
    "provider",
    "overrides",
    "success_metrics",
]

DANGEROUS_COMMANDS = [
    r"\brm\s+-rf\b",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+clean\s+-fd\b",
    r"\bdd\s+if=",
    r"\bmkfs\b",
]
DISALLOWED_REPO_FILES = [
    ".DS_Store",
    "docs/.DS_Store",
]


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8") as handle:
        return handle.read()


def toml_int_value(path: Path, section: str, key: str) -> int | None:
    current_section: str | None = None
    for raw_line in read_text(path).splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        section_match = re.fullmatch(r"\[(.+)\]", stripped)
        if section_match:
            current_section = section_match.group(1).strip()
            continue
        if current_section != section:
            continue
        value_match = re.fullmatch(rf"{re.escape(key)}\s*=\s*(-?\d+)", stripped)
        if value_match:
            return int(value_match.group(1))
    return None


def toml_string_value(path: Path, section: str | None, key: str) -> str | None:
    current_section: str | None = None
    for raw_line in read_text(path).splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        section_match = re.fullmatch(r"\[(.+)\]", stripped)
        if section_match:
            current_section = section_match.group(1).strip()
            continue
        if current_section != section:
            continue
        value_match = re.fullmatch(rf'{re.escape(key)}\s*=\s*"([^"]+)"', stripped)
        if value_match:
            return value_match.group(1)
    return None


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate_service_spec(path: Path) -> None:
    payload = load_yaml(path)
    ensure(isinstance(payload, dict), "example service.yaml must be a mapping")
    missing = [field for field in REQUIRED_SERVICE_FIELDS if field not in payload]
    ensure(not missing, f"example service.yaml missing fields: {', '.join(missing)}")
    ensure(str(payload["provider"]) == "openai", "example service.yaml must use provider=openai")
    branding = payload.get("branding")
    ensure(isinstance(branding, dict), "example service.yaml branding must be a mapping")
    branding_missing = [field for field in REQUIRED_BRANDING_FIELDS if field not in branding]
    ensure(not branding_missing, f"example service.yaml branding missing fields: {', '.join(branding_missing)}")
    ensure(
        isinstance(branding["keywords"], list) and bool(branding["keywords"]),
        "example service.yaml branding.keywords must be a non-empty list",
    )
    for field in ["references", "anti_references", "layout_principles", "component_rules"]:
        value = branding.get(field)
        ensure(value is None or isinstance(value, list), f"example service.yaml branding.{field} must be a list")
    for field in ["palette", "typography", "motion", "imagery"]:
        value = branding.get(field)
        ensure(value is None or isinstance(value, dict), f"example service.yaml branding.{field} must be a mapping")


def validate_task_pack(path: Path) -> None:
    payload = load_json(path)
    required = [
        "task_id",
        "goal",
        "scope",
        "constraints",
        "must_read",
        "acceptance_criteria",
        "verification_commands",
        "docs_required",
        "approval_required",
    ]
    missing = [field for field in required if field not in payload]
    ensure(not missing, f"example task-pack.json missing fields: {', '.join(missing)}")
    ensure(isinstance(payload["must_read"], list), "example task-pack.json must_read must be a list")
    ensure(isinstance(payload["docs_required"], list), "example task-pack.json docs_required must be a list")
    for path_str in REQUIRED_TASK_PACK_READS:
        ensure(path_str in payload["must_read"], f"example task-pack.json must_read missing {path_str}")
        ensure(path_str in payload["docs_required"], f"example task-pack.json docs_required missing {path_str}")


def validate_run_report(path: Path) -> None:
    payload = load_json(path)
    required = [
        "task_id",
        "provider",
        "lead_model",
        "worker_models",
        "changed_scope",
        "verification_results",
        "evidence_paths",
        "failures",
        "handoff_notes",
        "next_actions",
    ]
    missing = [field for field in required if field not in payload]
    ensure(not missing, f"example run-report.json missing fields: {', '.join(missing)}")
    ensure(payload["lead_model"] == EXPECTED_LEAD_MODEL, "example run-report.json lead_model does not match HQ policy")
    ensure(
        payload["worker_models"] == EXPECTED_WORKER_MODELS,
        "example run-report.json worker_models do not match HQ policy",
    )


def validate_contracts() -> None:
    for contract_name in [
        "service.schema.json",
        "task-pack.schema.json",
        "run-report.schema.json",
        "docs-manifest.json",
    ]:
        load_json(CONTRACTS_ROOT / contract_name)


def validate_templates() -> None:
    missing = [path for path in REQUIRED_TEMPLATES if not (TEMPLATE_ROOT / path).exists()]
    ensure(not missing, f"template files are missing: {', '.join(missing)}")
    validate_codex_policy_files()
    validate_repo_hygiene()


def validate_codex_policy_files() -> None:
    hq_config = ROOT / ".codex" / "config.toml"
    template_config = TEMPLATE_ROOT / ".codex" / "config.toml.tpl"
    template_agents = TEMPLATE_ROOT / "AGENTS.md.tpl"
    hq_architecture_planner = ROOT / ".codex" / "agents" / "architecture-planner.toml"
    hq_reviewer = ROOT / ".codex" / "agents" / "reviewer.toml"
    hq_doc_gardener = ROOT / ".codex" / "agents" / "doc-gardener.toml"
    hq_ui_checker = ROOT / ".codex" / "agents" / "ui-checker.toml"
    hq_implementation_worker = ROOT / ".codex" / "agents" / "implementation-worker.toml"
    hq_long_runner = ROOT / ".codex" / "agents" / "long-runner.toml"
    template_architecture_planner = TEMPLATE_ROOT / ".codex" / "agents" / "architecture-planner.toml.tpl"
    template_reviewer = TEMPLATE_ROOT / ".codex" / "agents" / "reviewer.toml.tpl"
    template_doc_gardener = TEMPLATE_ROOT / ".codex" / "agents" / "doc-gardener.toml.tpl"
    template_ui_checker = TEMPLATE_ROOT / ".codex" / "agents" / "ui-checker.toml.tpl"
    template_implementation_worker = TEMPLATE_ROOT / ".codex" / "agents" / "implementation-worker.toml.tpl"
    template_long_runner = TEMPLATE_ROOT / ".codex" / "agents" / "long-runner.toml.tpl"

    hq_depth = toml_int_value(hq_config, "agents", "max_depth")
    template_depth = toml_int_value(template_config, "agents", "max_depth")
    hq_model = toml_string_value(hq_config, None, "model")
    hq_review_model = toml_string_value(hq_config, None, "review_model")
    template_model = toml_string_value(template_config, None, "model")
    template_review_model = toml_string_value(template_config, None, "review_model")

    ensure(hq_depth is not None, "HQ .codex/config.toml must define [agents].max_depth")
    ensure(hq_depth >= 1, "HQ .codex/config.toml must set agents.max_depth >= 1")
    ensure(template_depth is not None, "service template .codex/config.toml.tpl must define [agents].max_depth")
    ensure(template_depth >= 1, "service template .codex/config.toml.tpl must set agents.max_depth >= 1")
    ensure(hq_model == EXPECTED_LEAD_MODEL, "HQ .codex/config.toml model does not match HQ policy")
    ensure(hq_review_model == EXPECTED_REVIEW_MODEL, "HQ .codex/config.toml review_model does not match HQ policy")
    ensure(template_model == EXPECTED_LEAD_MODEL, "service template .codex/config.toml.tpl model does not match HQ policy")
    ensure(
        template_review_model == EXPECTED_REVIEW_MODEL,
        "service template .codex/config.toml.tpl review_model does not match HQ policy",
    )
    ensure(
        toml_string_value(hq_architecture_planner, None, "model") == EXPECTED_PLANNER_MODEL,
        "HQ architecture_planner agent model does not match planning escalation policy",
    )
    ensure(
        toml_string_value(template_architecture_planner, None, "model") == EXPECTED_PLANNER_MODEL,
        "service template architecture_planner agent model does not match planning escalation policy",
    )
    ensure(
        toml_string_value(hq_reviewer, None, "model") == EXPECTED_REVIEW_MODEL,
        "HQ reviewer agent model does not match HQ policy",
    )
    ensure(
        toml_string_value(template_reviewer, None, "model") == EXPECTED_REVIEW_MODEL,
        "service template reviewer agent model does not match HQ policy",
    )
    ensure(
        toml_string_value(hq_doc_gardener, None, "model") == EXPECTED_DOC_MODEL,
        "HQ doc_gardener agent model does not match HQ policy",
    )
    ensure(
        toml_string_value(hq_ui_checker, None, "model") == EXPECTED_UI_CHECKER_MODEL,
        "HQ ui_checker agent model does not match design/development model policy",
    )
    ensure(
        toml_string_value(hq_implementation_worker, None, "model") == EXPECTED_CODING_WORKER_MODEL,
        "HQ implementation_worker agent model does not match coding worker policy",
    )
    ensure(
        toml_string_value(hq_long_runner, None, "model") == EXPECTED_LONG_RUNNER_MODEL,
        "HQ long_runner agent model does not match long-running work policy",
    )
    ensure(
        toml_string_value(template_doc_gardener, None, "model") == EXPECTED_DOC_MODEL,
        "service template doc_gardener agent model does not match HQ policy",
    )
    ensure(
        toml_string_value(template_ui_checker, None, "model") == EXPECTED_UI_CHECKER_MODEL,
        "service template ui_checker agent model does not match design/development model policy",
    )
    ensure(
        toml_string_value(template_implementation_worker, None, "model") == EXPECTED_CODING_WORKER_MODEL,
        "service template implementation_worker agent model does not match coding worker policy",
    )
    ensure(
        toml_string_value(template_long_runner, None, "model") == EXPECTED_LONG_RUNNER_MODEL,
        "service template long_runner agent model does not match long-running work policy",
    )

    agents_text = read_text(template_agents)
    ensure(
        "Codex must not spawn nested workers in this repo." in agents_text,
        "service template AGENTS.md.tpl must keep the nested-worker policy statement",
    )
    for agent_name in ["architecture_planner", "implementation_worker", "long_runner", "ui_checker", "doc_gardener"]:
        ensure(
            agent_name in agents_text,
            f"service template AGENTS.md.tpl must mention {agent_name} model routing",
        )


def validate_repo_hygiene() -> None:
    ensure((ROOT / ".gitignore").exists(), "HQ repo must include a .gitignore")
    gitignore_text = read_text(ROOT / ".gitignore")
    for token in [".DS_Store", "__pycache__/", "*.pyc", "node_modules/", ".next/"]:
        ensure(token in gitignore_text, f"HQ .gitignore must include {token}")

    template_gitignore = TEMPLATE_ROOT / ".gitignore.tpl"
    template_gitignore_text = read_text(template_gitignore)
    for token in [".DS_Store", "__pycache__/", "*.pyc", "node_modules/", ".next/", "*.tsbuildinfo"]:
        ensure(token in template_gitignore_text, f"service template .gitignore.tpl must include {token}")

    lingering = [path for path in DISALLOWED_REPO_FILES if (ROOT / path).exists()]
    ensure(not lingering, f"remove disallowed repo files: {', '.join(lingering)}")
    ensure((ROOT / "scripts" / "setup_hq.py").exists(), "HQ repo must include scripts/setup_hq.py")
    ensure((TEMPLATE_ROOT / ".nvmrc.tpl").exists(), "service template must include .nvmrc.tpl")
    ensure((TEMPLATE_ROOT / ".node-version.tpl").exists(), "service template must include .node-version.tpl")


def validate_examples() -> None:
    validate_service_spec(EXAMPLES_ROOT / "service.yaml")
    validate_task_pack(EXAMPLES_ROOT / "task-pack.json")
    validate_run_report(EXAMPLES_ROOT / "run-report.json")


def validate_dry_run_generation() -> None:
    generator = ROOT / "scripts" / "generate_service_repo.py"
    with tempfile.TemporaryDirectory(prefix="harness-hq-") as tmpdir:
        destination = Path(tmpdir) / "output"
        subprocess.run(
            [
                sys.executable,
                str(generator),
                "--spec",
                str(EXAMPLES_ROOT / "service.yaml"),
                "--output-root",
                str(destination),
            ],
            check=True,
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        generated = destination / "focus-sprint"
        ensure((generated / "AGENTS.md").exists(), "generated AGENTS.md missing")
        ensure((generated / ".gitignore").exists(), "generated .gitignore missing")
        ensure((generated / ".nvmrc").exists(), "generated .nvmrc missing")
        ensure((generated / ".node-version").exists(), "generated .node-version missing")
        ensure((generated / ".gitmessage.txt").exists(), "generated .gitmessage.txt missing")
        ensure((generated / ".codex" / "config.toml").exists(), "generated config.toml missing")
        ensure((generated / ".codex" / "hooks.json").exists(), "generated hooks.json missing")
        for agent_file in [
            "architecture-planner.toml",
            "reviewer.toml",
            "ui-checker.toml",
            "doc-gardener.toml",
            "implementation-worker.toml",
            "long-runner.toml",
        ]:
            ensure((generated / ".codex" / "agents" / agent_file).exists(), f"generated agent file missing: {agent_file}")
        ensure((generated / ".githooks" / "commit-msg").exists(), "generated commit-msg hook missing")
        ensure((generated / "service.yaml").exists(), "generated service.yaml missing")
        ensure((generated / "docs-manifest.json").exists(), "generated docs-manifest.json missing")
        ensure((generated / "docs" / "design" / "art-direction.kr.md").exists(), "generated art-direction doc missing")
        ensure((generated / "docs" / "design" / "browser-review.kr.md").exists(), "generated browser-review doc missing")
        ensure((generated / "docs" / "design" / "ui-principles.kr.md").exists(), "generated ui-principles doc missing")
        ensure((generated / "docs" / "prompting" / "prompt-context.kr.md").exists(), "generated prompt-context doc missing")
        generated_depth = toml_int_value(generated / ".codex" / "config.toml", "agents", "max_depth")
        ensure(generated_depth is not None, "generated config.toml must define [agents].max_depth")
        ensure(generated_depth >= 1, "generated config.toml must set agents.max_depth >= 1")
        ensure(
            toml_string_value(generated / ".codex" / "config.toml", None, "model") == EXPECTED_LEAD_MODEL,
            "generated config.toml model does not match HQ policy",
        )
        ensure(
            toml_string_value(generated / ".codex" / "config.toml", None, "review_model") == EXPECTED_REVIEW_MODEL,
            "generated config.toml review_model does not match HQ policy",
        )


def codex_session_start() -> int:
    payload = {
        "continue": True,
        "systemMessage": (
            "Harness HQ controls contracts, templates, and guardrails. "
            "Keep product code out of this repo. "
            "If this machine has not been prepared yet, run `python3 scripts/setup_hq.py` first. "
            "After generating a service repo from service.yaml, move the active work to that generated repo."
        ),
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": (
                "On a new machine, run `python3 scripts/setup_hq.py` before other HQ work. "
                "Before large changes, read AGENTS.md and the docs linked from it. "
                "If scripts, contracts, or .codex policy change, update docs and run python3 scripts/validate_harness.py --mode all. "
                "Once a service repo is generated, continue the implementation conversation there instead of staying in HQ."
            ),
        },
    }
    print(json.dumps(payload))
    return 0


def codex_pre_tool_use() -> int:
    hook_input = json.load(sys.stdin)
    command = hook_input.get("tool_input", {}).get("command", "")
    for pattern in DANGEROUS_COMMANDS:
        if re.search(pattern, command):
            payload = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "Harness HQ blocks dangerous shell commands by policy.",
                }
            }
            print(json.dumps(payload))
            return 0
    return 0


def root_changed_files() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD"],
            check=True,
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except Exception:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def codex_stop() -> int:
    changed = root_changed_files()
    watch_prefixes = (".codex/", ".harness/contracts/", "scripts/")
    docs_touched = any(path in {"AGENTS.md", "README.md"} or path.startswith("docs/") for path in changed)
    if any(path.startswith(watch_prefixes) for path in changed) and not docs_touched:
        payload = {
            "decision": "block",
            "reason": (
                "Scripts, contracts, or Codex policy changed without doc updates. "
                "Update AGENTS.md, README.md, or docs/* before stopping."
            ),
        }
        print(json.dumps(payload))
        return 0
    print(json.dumps({"continue": True}))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=[
            "all",
            "contracts",
            "templates",
            "examples",
            "dry-run",
            "codex-session-start",
            "codex-pre-tool-use",
            "codex-stop",
        ],
        default="all",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.mode == "contracts":
        validate_contracts()
        return 0
    if args.mode == "templates":
        validate_templates()
        return 0
    if args.mode == "examples":
        validate_examples()
        return 0
    if args.mode == "dry-run":
        validate_dry_run_generation()
        return 0
    if args.mode == "codex-session-start":
        return codex_session_start()
    if args.mode == "codex-pre-tool-use":
        return codex_pre_tool_use()
    if args.mode == "codex-stop":
        return codex_stop()

    validate_contracts()
    validate_templates()
    validate_examples()
    validate_dry_run_generation()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
