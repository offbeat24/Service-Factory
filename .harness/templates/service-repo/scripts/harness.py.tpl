#!/usr/bin/env python3
"""Task-bound validation and Codex hook logic for generated service repositories."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment-specific fallback
    raise SystemExit("PyYAML is required. Install it with `python3 -m pip install pyyaml`.") from exc


ROOT = Path(__file__).resolve().parents[1]

DANGEROUS_COMMANDS = [
    r"\brm\s+-rf\b",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+clean\s+-fd\b",
    r"\bdd\s+if=",
    r"\bmkfs\b",
]

RUN_REPORT_REQUIRED_FIELDS = [
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


class ValidationError(RuntimeError):
    pass


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def manifest() -> dict[str, Any]:
    return load_json(ROOT / "docs-manifest.json")


def branch_name() -> str | None:
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=str(ROOT),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except Exception:
        return None
    name = result.stdout.strip()
    return name or None


def infer_task_id(explicit: str | None) -> str:
    if explicit:
        return explicit

    rules = manifest()
    current_branch = branch_name()
    if current_branch:
        matched = re.match(rules["branch_pattern"], current_branch)
        if matched:
            return matched.group("task_id")

    active_dir = ROOT / "docs" / "exec-plans" / "active"
    active_files = sorted(path.stem for path in active_dir.glob("*.kr.md"))
    if len(active_files) == 1:
        return active_files[0]
    raise ValidationError("could not determine task_id; pass --task-id or use a task/<TASK-ID>-... branch")


def normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def changed_files(mode: str) -> list[str]:
    commands = {
        "pre-commit": ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        "ci": ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
        "pre-complete": ["git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD"],
        "codex-stop": ["git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD"],
    }
    command = commands.get(mode, ["git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD"])
    try:
        result = subprocess.run(
            command,
            cwd=str(ROOT),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except Exception:
        return []
    return [normalize_path(line.strip()) for line in result.stdout.splitlines() if line.strip()]


def is_exempt(path: str) -> bool:
    for prefix in manifest()["exempt_paths"]:
        if path == prefix or path.startswith(prefix):
            return True
    return False


def contains_placeholder(text: str, placeholder_tokens: list[str]) -> bool:
    for token in placeholder_tokens:
        if token in text:
            return True
    for line in text.splitlines():
        stripped = line.strip()
        if re.fullmatch(r"#+", stripped):
            return True
        if stripped in {"-", "*"}:
            return True
    return False


def require_file(path: Path) -> None:
    if not path.exists():
        raise ValidationError(f"required file is missing: {path.relative_to(ROOT)}")


def require_sections(path: Path, sections: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for section in sections:
        if section not in text:
            raise ValidationError(f"{path.relative_to(ROOT)} is missing section marker: {section}")
    if contains_placeholder(text, manifest()["placeholder_tokens"]):
        raise ValidationError(f"{path.relative_to(ROOT)} still contains placeholder text")


def require_marker(path: Path, marker: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker not in text:
        raise ValidationError(f"{path.relative_to(ROOT)} is missing task marker: {marker}")
    if contains_placeholder(text, manifest()["placeholder_tokens"]):
        raise ValidationError(f"{path.relative_to(ROOT)} still contains placeholder text")


def validate_required_docs() -> None:
    rules = manifest()
    for entry in rules["required_documents"]:
        path = ROOT / entry["path"]
        require_file(path)
        require_sections(path, entry["sections"])


def validate_service_yaml() -> None:
    payload = load_yaml(ROOT / "service.yaml")
    if not isinstance(payload, dict):
        raise ValidationError("service.yaml must be a YAML mapping")
    required = [
        "id",
        "name",
        "concept",
        "pages",
        "core_flows",
        "success_metrics",
        "provider",
    ]
    missing = [field for field in required if field not in payload]
    if missing:
        raise ValidationError(f"service.yaml missing required keys: {', '.join(missing)}")


def validate_task_pack(task_id: str) -> None:
    path = ROOT / "task-pack.json"
    require_file(path)
    payload = load_json(path)
    if payload.get("task_id") != task_id:
        raise ValidationError(f"task-pack.json task_id mismatch: expected {task_id}")


def validate_active_exec_plan(task_id: str) -> None:
    rules = manifest()["task_bound_documents"]
    path = ROOT / rules["active_exec_plan_path"].format(task_id=task_id)
    require_file(path)
    require_sections(path, rules["active_exec_plan_sections"])


def validate_run_report(task_id: str) -> None:
    rules = manifest()["task_bound_documents"]
    path = ROOT / rules["run_report_path"].format(task_id=task_id)
    require_file(path)
    payload = load_json(path)
    missing = [field for field in RUN_REPORT_REQUIRED_FIELDS if field not in payload]
    if missing:
        raise ValidationError(f"{path.relative_to(ROOT)} missing fields: {', '.join(missing)}")
    if payload["task_id"] != task_id:
        raise ValidationError(f"{path.relative_to(ROOT)} task_id mismatch: expected {task_id}")


def should_require_marker(changes: list[str], prefixes: list[str]) -> bool:
    if not changes:
        return False
    return any(any(path == prefix or path.startswith(prefix) for prefix in prefixes) for path in changes)


def validate_task_markers(task_id: str, mode: str) -> None:
    rules = manifest()["task_bound_documents"]
    build_journal = ROOT / "docs" / "build-journal.kr.md"
    require_marker(build_journal, rules["build_journal_marker"].format(task_id=task_id))
    validate_run_report(task_id)

    changes = [path for path in changed_files(mode) if not is_exempt(path)]
    if not changes:
        return

    if should_require_marker(changes, manifest()["why_required_prefixes"]):
        why_doc = ROOT / "docs" / "architecture" / "why.kr.md"
        require_marker(why_doc, rules["why_marker"].format(task_id=task_id))

    if should_require_marker(changes, manifest()["harness_feedback_prefixes"]):
        feedback_doc = ROOT / "docs" / "retrospectives" / "harness-feedback.kr.md"
        require_marker(feedback_doc, rules["harness_feedback_marker"].format(task_id=task_id))


def run_pre_task(task_id: str) -> None:
    validate_required_docs()
    validate_service_yaml()
    validate_task_pack(task_id)
    validate_active_exec_plan(task_id)


def run_pre_complete(task_id: str, mode: str) -> None:
    run_pre_task(task_id)
    validate_task_markers(task_id, mode)


def codex_session_start() -> int:
    try:
        task_id = infer_task_id(None)
    except ValidationError:
        task_id = "UNKNOWN"
    payload = {
        "continue": True,
        "systemMessage": f"Current task context: {task_id}. Keep work scoped and update task-bound docs before stopping.",
        "hookSpecificOutput": {
          "hookEventName": "SessionStart",
          "additionalContext": "Run python3 scripts/harness.py pre-task before edits and pre-complete before ending the task."
        }
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
                    "permissionDecisionReason": "This repository blocks dangerous shell commands by policy."
                }
            }
            print(json.dumps(payload))
            return 0
    return 0


def codex_stop() -> int:
    try:
        task_id = infer_task_id(None)
        run_pre_complete(task_id, "codex-stop")
    except ValidationError as exc:
        payload = {"decision": "block", "reason": str(exc)}
        print(json.dumps(payload))
        return 0
    print(json.dumps({"continue": True}))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode",
        choices=[
            "pre-task",
            "pre-complete",
            "pre-commit",
            "ci",
            "codex-session-start",
            "codex-pre-tool-use",
            "codex-stop",
        ],
    )
    parser.add_argument("--task-id", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "codex-session-start":
        return codex_session_start()
    if args.mode == "codex-pre-tool-use":
        return codex_pre_tool_use()
    if args.mode == "codex-stop":
        return codex_stop()

    task_id = infer_task_id(args.task_id)
    try:
        if args.mode == "pre-task":
            run_pre_task(task_id)
        elif args.mode == "pre-complete":
            run_pre_complete(task_id, "pre-complete")
        elif args.mode == "pre-commit":
            run_pre_complete(task_id, "pre-commit")
        elif args.mode == "ci":
            run_pre_complete(task_id, "ci")
    except ValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
