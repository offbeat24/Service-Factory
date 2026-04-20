# AGENTS.md

## Project Overview

`{{SERVICE_NAME}}` is a generated service repository managed by Harness HQ. Build the product here. Keep the work scoped to the current task branch and keep documentation in sync with the implementation.

## Setup Commands

- Enable git hook enforcement once per clone: `git config core.hooksPath .githooks`
- Pre-task gate: `python3 scripts/harness.py pre-task`
- Pre-complete gate: `python3 scripts/harness.py pre-complete`
- CI-equivalent gate: `python3 scripts/harness.py ci`
- Generate Claude shim if needed: `python3 scripts/generate_claude_shim.py`

## Repo Map

- Product spec: `docs/product/product-spec.kr.md`
- Active execution plan: `docs/exec-plans/active/{{BOOTSTRAP_TASK_ID}}.kr.md`
- Build journal: `docs/build-journal.kr.md`
- Architecture why: `docs/architecture/why.kr.md`
- Harness feedback: `docs/retrospectives/harness-feedback.kr.md`
- Public case study: `docs/public/case-study.en.md`
- Evidence: `artifacts/evidence/<task-id>/`
- Run reports: `artifacts/run-reports/`

## Task Flow

1. Create or switch to a branch like `task/{{BOOTSTRAP_TASK_ID}}-init`.
2. Run `python3 scripts/harness.py pre-task`.
3. Read the active exec plan and product spec before editing code.
4. Keep work inside the current task scope.
5. Before stopping, run `python3 scripts/harness.py pre-complete`.

## Codex Policy

- Codex must not spawn nested workers in this repo.
- The generated `.codex/config.toml` keeps `agents.max_depth = 1` because current Codex requires depth >= 1 for the root agent to run.
- Use focused workers only when the parent explicitly asks for them.
- Do not treat hooks as a full safety boundary. Keep human approval for production, billing, data deletion, DB migration, secrets, and infra mutation.

## Documentation Rules

- `AGENTS.md` stays short; detailed reasoning belongs in `docs/`.
- Do not leave `TODO`, `TBD`, or empty headings in required docs.
- Code or config changes must map back to the current `task_id`.
