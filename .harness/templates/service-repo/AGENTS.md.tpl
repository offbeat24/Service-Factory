# AGENTS.md

## Project Overview

`{{SERVICE_NAME}}` is a generated service repository managed by Harness HQ. Build the product here. Keep the work scoped to the current task branch and keep documentation in sync with the implementation.

## Setup Commands

- Node runtime baseline: `{{DEFAULT_NODE_LABEL}}`
- Enable git hook enforcement once per clone: `git config core.hooksPath .githooks`
- Enable the commit template once per clone: `git config commit.template .gitmessage.txt`
- Pre-task gate: `python3 scripts/harness.py pre-task`
- Pre-complete gate: `python3 scripts/harness.py pre-complete`
- CI-equivalent gate: `python3 scripts/harness.py ci`
- Generate Claude shim if needed: `python3 scripts/generate_claude_shim.py`

## Repo Map

- Product spec: `docs/product/product-spec.kr.md`
- Art direction: `docs/design/art-direction.kr.md`
- UI principles: `docs/design/ui-principles.kr.md`
- Browser review checklist: `docs/design/browser-review.kr.md`
- Prompt context: `docs/prompting/prompt-context.kr.md`
- Active execution plan: `docs/exec-plans/active/{{BOOTSTRAP_TASK_ID}}.kr.md`
- Build journal: `docs/build-journal.kr.md`
- Architecture why: `docs/architecture/why.kr.md`
- Harness feedback: `docs/retrospectives/harness-feedback.kr.md`
- Public case study: `docs/public/case-study.en.md`
- Evidence: `artifacts/evidence/<task-id>/`
- Run reports: `artifacts/run-reports/`

## Task Flow

1. If this repo was just generated from HQ, move the active Codex conversation here before product work starts.
2. Use Node `{{DEFAULT_NODE_VERSION}}` before npm commands.
3. Keep the main branch name as `main` and initialize with `git init -b main` if needed.
4. Create or switch to a branch like `feature/{{BOOTSTRAP_TASK_ID}}-init`.
5. Run `python3 scripts/harness.py pre-task`.
6. Read the active exec plan, product spec, prompt context, art direction, UI principles, and browser review checklist before editing code.
7. Keep work inside the current task scope.
8. Use `<type>: <subject>` commit messages with the repo commit template and commit-msg hook.
9. Before stopping, run `python3 scripts/harness.py pre-complete`.

## Codex Policy

- Codex must not spawn nested workers in this repo.
- The generated `.codex/config.toml` keeps `agents.max_depth = 1` because current Codex requires depth >= 1 for the root agent to run.
- Use focused workers only when the parent explicitly asks for them.
- Do not treat hooks as a full safety boundary. Keep human approval for production, billing, data deletion, DB migration, secrets, and infra mutation.

## Documentation Rules

- `AGENTS.md` stays short; detailed reasoning belongs in `docs/`.
- Do not leave `TODO`, `TBD`, or empty headings in required docs.
- Code or config changes must map back to the current `task_id`.
- Design work must update the design docs before the UI is treated as complete.
- `docs/prompting/prompt-context.kr.md` is generated context. Update source docs and rerun the harness instead of hand-maintaining summaries.
- Polished UI or flow work is not complete until the browser review checklist has been executed and evidence has been recorded.
