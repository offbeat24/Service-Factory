#!/usr/bin/env python3
"""Generate a Codex-first service repository from a service.yaml spec."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
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
LEAD_MODEL = "gpt-5.4"
WORKER_MODELS = ["gpt-5.4-mini", "gpt-5.3-codex", "gpt-5.2"]
DEFAULT_NODE_VERSION = "20.19.6"
DEFAULT_NODE_LABEL = "Node 20.19.6 LTS"
DEFAULT_NEXT_LINE = "Next.js 16.x LTS line"
DEFAULT_REACT_LINE = "React 19.x stable line"
DEFAULT_WEB_STACK = "Next.js 16.x LTS line + React 19.x stable line + TypeScript"


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
    required_branding_fields = ["tone", "visual_direction", "keywords"]
    missing_branding = [field for field in required_branding_fields if field not in spec["branding"]]
    if missing_branding:
        raise SystemExit(f"branding is missing required fields: {', '.join(missing_branding)}")
    if not isinstance(spec["branding"]["keywords"], list) or not spec["branding"]["keywords"]:
        raise SystemExit("branding.keywords must be a non-empty list")
    for field in ["references", "anti_references", "layout_principles", "component_rules"]:
        value = spec["branding"].get(field)
        if value is not None and not isinstance(value, list):
            raise SystemExit(f"branding.{field} must be a list when provided")
    for field in ["palette", "typography", "motion", "imagery"]:
        value = spec["branding"].get(field)
        if value is not None and not isinstance(value, dict):
            raise SystemExit(f"branding.{field} must be a mapping when provided")
    if not isinstance(spec["overrides"], dict):
        raise SystemExit("overrides must be a mapping")


def flatten_item(item: Any) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, list):
        return ", ".join(flatten_item(entry) for entry in item)
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
    summary_keys = ["tone", "visual_direction", "keywords"]
    lines = []
    for key in summary_keys:
        if key in mapping:
            lines.append(f"- {key}: {flatten_item(mapping[key])}")
    return "\n".join(lines) if lines else "- 브랜드 속성은 후속 작업에서 보강한다."


def render_list_or_default(items: Any, default: str) -> str:
    if isinstance(items, list) and items:
        return "\n".join(f"- {flatten_item(item)}" for item in items)
    return f"- {default}"


def render_mapping_or_default(mapping: Any, default: str) -> str:
    if isinstance(mapping, dict) and mapping:
        return "\n".join(f"- {key}: {flatten_item(value)}" for key, value in mapping.items())
    return f"- {default}"


def render_context(spec: dict[str, Any], source_spec: Path) -> dict[str, str]:
    today = date.today().isoformat()
    branding = spec["branding"]
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
        "BRANDING_BULLETS": render_branding(branding),
        "DESIGN_TONE": str(branding.get("tone", "명시 필요")),
        "DESIGN_VISUAL_DIRECTION": str(branding.get("visual_direction", "명시 필요")),
        "DESIGN_KEYWORDS_BULLETS": render_list_or_default(branding.get("keywords"), "핵심 키워드를 추가한다."),
        "DESIGN_REFERENCES_BULLETS": render_list_or_default(
            branding.get("references"),
            "참고 레퍼런스를 최소 3개까지 보강한다.",
        ),
        "DESIGN_ANTI_REFERENCES_BULLETS": render_list_or_default(
            branding.get("anti_references"),
            "피해야 할 디자인 패턴을 문서화한다.",
        ),
        "DESIGN_PALETTE_BULLETS": render_mapping_or_default(
            branding.get("palette"),
            "primary, accent, background, text 기준 색을 추가한다.",
        ),
        "DESIGN_TYPOGRAPHY_BULLETS": render_mapping_or_default(
            branding.get("typography"),
            "헤드라인/본문 타이포 기준을 추가한다.",
        ),
        "DESIGN_MOTION_BULLETS": render_mapping_or_default(
            branding.get("motion"),
            "모션 강도와 허용 범위를 추가한다.",
        ),
        "DESIGN_IMAGERY_BULLETS": render_mapping_or_default(
            branding.get("imagery"),
            "이미지 또는 일러스트 방향을 추가한다.",
        ),
        "DESIGN_LAYOUT_PRINCIPLES_BULLETS": render_list_or_default(
            branding.get("layout_principles"),
            "레이아웃 원칙을 최소 3개 정의한다.",
        ),
        "DESIGN_COMPONENT_RULES_BULLETS": render_list_or_default(
            branding.get("component_rules"),
            "버튼, 카드, 폼에 대한 규칙을 정의한다.",
        ),
        "OVERRIDES_BULLETS": render_kv_bullets(spec["overrides"]),
        "MONETIZATION": str(spec["monetization"]),
        "AUTH_NEED": str(spec["auth_need"]),
        "STORAGE_NEED": str(spec["storage_need"]),
        "DEPLOY_PREFERENCE": str(spec["deploy_preference"]),
        "DOMAIN_PREFERENCE": str(spec["domain_preference"]),
        "PROVIDER": str(spec["provider"]),
        "DEFAULT_NODE_VERSION": DEFAULT_NODE_VERSION,
        "DEFAULT_NODE_LABEL": DEFAULT_NODE_LABEL,
        "DEFAULT_NEXT_LINE": DEFAULT_NEXT_LINE,
        "DEFAULT_REACT_LINE": DEFAULT_REACT_LINE,
        "DEFAULT_WEB_STACK": DEFAULT_WEB_STACK,
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
                    "디자인 입력과 art direction, UI principles를 정렬한다.",
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
                    "docs/prompting/prompt-context.kr.md",
                    "docs/design/art-direction.kr.md",
                    "docs/design/ui-principles.kr.md",
                    "docs/design/browser-review.kr.md",
                    "docs/architecture/why.kr.md",
                ],
                "acceptance_criteria": [
                    "active exec plan이 최신 상태다.",
                    "디자인 기준 문서가 첫 화면의 톤, 계층, 금지 패턴을 설명한다.",
                    "browser review checklist가 디자인과 기능 점검 순서를 설명한다.",
                    "핵심 플로우 구현 범위와 검증 방법이 분명하다.",
                    "evidence 저장 경로가 준비되어 있다.",
                ],
                "verification_commands": [
                    "python3 scripts/harness.py pre-task",
                    "python3 scripts/harness.py ci",
                ],
                "docs_required": [
                    f"docs/exec-plans/active/{BOOTSTRAP_TASK_ID}.kr.md",
                    "docs/prompting/prompt-context.kr.md",
                    "docs/design/art-direction.kr.md",
                    "docs/design/ui-principles.kr.md",
                    "docs/design/browser-review.kr.md",
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
                "worker_models": WORKER_MODELS,
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
                    "The next human or agent should keep `main` as the integration branch and create a work branch such as feature/BOOTSTRAP-001-....",
                    "Set git hooks with `git config core.hooksPath .githooks` and optionally `git config commit.template .gitmessage.txt` before editing product code.",
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

        if target.name in {"pre-commit", "commit-msg", "harness.py", "generate_claude_shim.py"}:
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
    print("Next: switch Codex to the generated repo and continue product implementation there.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
