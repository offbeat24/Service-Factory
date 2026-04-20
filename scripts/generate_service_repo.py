#!/usr/bin/env python3
"""Generate a Codex-first service repository from a service.yaml spec."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment-specific fallback
    raise SystemExit("PyYAML is required. Install it with `python3 -m pip install pyyaml`.") from exc


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / ".harness" / "templates" / "service-repo"
CONTRACTS_ROOT = ROOT / ".harness" / "contracts"

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

BOOTSTRAP_TASK_ID = "BOOTSTRAP-001"
INIT_TASK_ID = "INIT-000"
LEAD_MODEL = "gpt-5.1-codex"
WORKER_MODEL = "gpt-5.1-codex-mini"


def default_output_root() -> Path:
    override = os.environ.get("HARNESS_DECK_ROOT")
    if override:
        return Path(override).expanduser()
    return ROOT.parent / "deck"


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def dump_yaml(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=True)


def ensure_service_spec(spec: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_SERVICE_FIELDS if field not in spec]
    if missing:
        raise SystemExit(f"service spec is missing required fields: {', '.join(missing)}")

    if not re.fullmatch(r"[a-z0-9-]+", str(spec["id"])):
        raise SystemExit("service spec id must match ^[a-z0-9-]+$")

    for list_field in ["target_users", "pages", "core_flows", "data_entities", "success_metrics"]:
        value = spec.get(list_field)
        if not isinstance(value, list) or not value:
            raise SystemExit(f"{list_field} must be a non-empty list")

    if spec["provider"] != "openai":
        raise SystemExit("v1 only supports provider=openai")

    if not isinstance(spec["branding"], dict):
        raise SystemExit("branding must be a mapping")
    if not isinstance(spec["overrides"], dict):
        raise SystemExit("overrides must be a mapping")


def flatten_item(item: Any) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        parts = []
        for key, value in item.items():
            if isinstance(value, list):
                rendered = ", ".join(flatten_item(entry) for entry in value)
            elif isinstance(value, dict):
                rendered = ", ".join(f"{sub_key}={sub_value}" for sub_key, sub_value in value.items())
            else:
                rendered = str(value)
            parts.append(f"{key}: {rendered}")
        return "; ".join(parts)
    return str(item)


def render_bullets(items: list[Any]) -> str:
    return "\n".join(f"- {flatten_item(item)}" for item in items)


def render_kv_bullets(mapping: dict[str, Any]) -> str:
    if not mapping:
        return "- 없음. 기본 정책을 그대로 사용한다."
    lines = []
    for key, value in mapping.items():
        if isinstance(value, list):
            rendered = ", ".join(flatten_item(entry) for entry in value)
        elif isinstance(value, dict):
            rendered = ", ".join(f"{sub_key}={sub_value}" for sub_key, sub_value in value.items())
        else:
            rendered = str(value)
        lines.append(f"- {key}: {rendered}")
    return "\n".join(lines)


def render_branding(mapping: dict[str, Any]) -> str:
    if not mapping:
        return "- 브랜드 속성은 후속 작업에서 보강한다."
    return "\n".join(f"- {key}: {flatten_item(value)}" for key, value in mapping.items())


def render_context(spec: dict[str, Any], source_spec: Path) -> dict[str, str]:
    today = date.today().isoformat()
    return {
        "SERVICE_ID": str(spec["id"]),
        "SERVICE_NAME": str(spec["name"]),
        "CONCEPT": str(spec["concept"]),
        "PROBLEM": str(spec["problem"]),
        "TARGET_USERS_BULLETS": render_bullets(spec["target_users"]),
        "PAGES_BULLETS": render_bullets(spec["pages"]),
        "CORE_FLOWS_BULLETS": render_bullets(spec["core_flows"]),
        "DATA_ENTITIES_BULLETS": render_bullets(spec["data_entities"]),
        "SUCCESS_METRICS_BULLETS": render_bullets(spec["success_metrics"]),
        "BRANDING_BULLETS": render_branding(spec["branding"]),
        "OVERRIDES_BULLETS": render_kv_bullets(spec["overrides"]),
        "MONETIZATION": str(spec["monetization"]),
        "AUTH_NEED": str(spec["auth_need"]),
        "STORAGE_NEED": str(spec["storage_need"]),
        "DEPLOY_PREFERENCE": str(spec["deploy_preference"]),
        "DOMAIN_PREFERENCE": str(spec["domain_preference"]),
        "PROVIDER": str(spec["provider"]),
        "TODAY": today,
        "BOOTSTRAP_TASK_ID": BOOTSTRAP_TASK_ID,
        "INIT_TASK_ID": INIT_TASK_ID,
        "SOURCE_SPEC_PATH": str(source_spec),
        "SERVICE_SPEC_JSON": json.dumps(spec, ensure_ascii=False, indent=2),
        "INITIAL_TASK_PACK_JSON": json.dumps(
            {
                "task_id": BOOTSTRAP_TASK_ID,
                "goal": f"{spec['name']} 서비스의 첫 구현 루프를 시작한다.",
                "scope": [
                    "서비스 레포의 기본 문서와 실행 환경을 검토한다.",
                    "핵심 플로우 1개를 구현하기 위한 세부 실행 계획을 만든다.",
                    "기본 검증 명령과 evidence 수집 경로를 점검한다.",
                ],
                "constraints": [
                    "AGENTS.md는 짧게 유지한다.",
                    "큰 프롬프트 대신 현재 작업에 필요한 문서만 읽는다.",
                    "문서 없는 구현은 완료로 간주하지 않는다.",
                ],
                "must_read": [
                    "AGENTS.md",
                    f"docs/exec-plans/active/{BOOTSTRAP_TASK_ID}.kr.md",
                    "docs/product/product-spec.kr.md",
                    "docs/architecture/why.kr.md",
                ],
                "acceptance_criteria": [
                    "active exec plan이 최신 상태다.",
                    "핵심 플로우 구현 범위와 검증 방법이 분명하다.",
                    "evidence 저장 경로가 준비되어 있다.",
                ],
                "verification_commands": [
                    "python3 scripts/harness.py pre-task",
                    "python3 scripts/harness.py ci",
                ],
                "docs_required": [
                    f"docs/exec-plans/active/{BOOTSTRAP_TASK_ID}.kr.md",
                    "docs/build-journal.kr.md",
                    "docs/architecture/why.kr.md",
                    "docs/retrospectives/harness-feedback.kr.md",
                ],
                "approval_required": False,
            },
            ensure_ascii=False,
            indent=2,
        ),
        "INIT_RUN_REPORT_JSON": json.dumps(
            {
                "task_id": INIT_TASK_ID,
                "provider": spec["provider"],
                "lead_model": LEAD_MODEL,
                "worker_models": [WORKER_MODEL],
                "changed_scope": [
                    "AGENTS.md",
                    ".codex/",
                    "docs/",
                    "scripts/",
                    "docs-manifest.json",
                ],
                "verification_results": [
                    {
                        "name": "scaffold_generation",
                        "status": "passed",
                        "details": "Harness HQ generated the initial service repository layout."
                    }
                ],
                "evidence_paths": [],
                "failures": [],
                "handoff_notes": [
                    "The next human or agent should create a task branch named task/BOOTSTRAP-001-...",
                    "Run python3 scripts/harness.py pre-task before editing product code."
                ],
                "next_actions": [
                    "Review product-spec.kr.md and refine the first implementation slice.",
                    "Create evidence-producing commands once the app scaffold exists."
                ]
            },
            ensure_ascii=False,
            indent=2,
        ),
    }


def render_text(template: str, context: dict[str, str]) -> str:
    rendered = template
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def copy_templates(destination: Path, context: dict[str, str]) -> None:
    for source in sorted(TEMPLATE_ROOT.rglob("*")):
        relative = source.relative_to(TEMPLATE_ROOT)
        target_name = relative.name[:-4] if relative.name.endswith(".tpl") else relative.name
        target = destination / relative.parent / target_name
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        text = source.read_text(encoding="utf-8")
        target.write_text(render_text(text, context), encoding="utf-8")

        if target.name in {"pre-commit", "harness.py", "generate_claude_shim.py"}:
            mode = target.stat().st_mode
            target.chmod(mode | 0o111)


def sync_docs_manifest(destination: Path) -> None:
    manifest_src = CONTRACTS_ROOT / "docs-manifest.json"
    manifest_dst = destination / "docs-manifest.json"
    manifest_dst.write_text(manifest_src.read_text(encoding="utf-8"), encoding="utf-8")


def sync_service_yaml(spec_path: Path, destination: Path, spec: dict[str, Any]) -> None:
    try:
        raw = spec_path.read_text(encoding="utf-8")
    except OSError:
        dump_yaml(destination / "service.yaml", spec)
        return

    # Preserve the user's file when possible.
    if raw.strip():
        (destination / "service.yaml").write_text(raw, encoding="utf-8")
    else:
        dump_yaml(destination / "service.yaml", spec)


def generate(spec_path: Path, output_root: Path, force: bool) -> Path:
    spec = load_yaml(spec_path)
    if not isinstance(spec, dict):
        raise SystemExit("service spec must be a YAML mapping")

    ensure_service_spec(spec)
    destination = output_root / str(spec["id"])
    if destination.exists():
        if not force:
            raise SystemExit(f"destination already exists: {destination}")
        shutil.rmtree(destination)

    destination.mkdir(parents=True, exist_ok=True)
    context = render_context(spec, spec_path)
    copy_templates(destination, context)
    sync_docs_manifest(destination)
    sync_service_yaml(spec_path, destination, spec)
    return destination


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path, help="Path to service.yaml")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=default_output_root(),
        help=(
            "Directory where the generated service repository will be created "
            f"(default: {default_output_root()})"
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing generated repo with the same service id",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    destination = generate(args.spec.resolve(), args.output_root.resolve(), args.force)
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
