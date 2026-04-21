# Harness HQ v4

Harness HQ is the control plane for a Codex-first service factory. This repository does not hold the product apps you want to ship. It holds the repeatable system that creates them: contracts, templates, Codex policies, validation scripts, and documentation rules.

## What this repo contains

- `AGENTS.md`: short map for coding agents
- `.codex/`: Codex runtime defaults, hooks, and custom agent definitions for HQ work
- `.harness/contracts/`: machine-readable contracts for `service.yaml`, `task-pack.json`, `run-report.json`, and `docs-manifest.json`
- `.harness/templates/service-repo/`: the template used to create each service repository
- `scripts/`: HQ generation and validation tooling
- `docs/`: human-readable policy docs for structure, evidence, and approvals
- `examples/`: a working sample spec and sample task artifacts
- `tests/`: regression tests for repo generation and enforcement
- `.gitignore`: workspace hygiene rules for HQ artifacts and OS noise

## Operating model

1. Run `python3 scripts/setup_hq.py` once after cloning on a new machine.
2. Write a `service.yaml` first.
3. Generate a service repository from this HQ into the sibling `deck/` directory.
4. Switch the active Codex conversation and workspace to the generated repo. Do not keep implementing the product inside HQ.
5. Keep the default integration branch name as `main`.
6. Create a work branch in the generated repo such as `feature/BOOTSTRAP-001-init`.
7. Set the repo-local git hooks path with `git config core.hooksPath .githooks`.
8. Optionally enable the commit template with `git config commit.template .gitmessage.txt`.
9. Run the generated repo's `scripts/harness.py pre-task`.
10. Let Codex work inside the generated repo with `AGENTS.md`, `.codex/`, docs, and hooks enabled.
11. Before ending work, run `scripts/harness.py pre-complete` or rely on hooks plus CI to enforce the same rules.

## Current defaults

- Runtime: Codex CLI/App
- Provider: OpenAI only
- Lead/review model policy: `gpt-5.4`
- Supporting worker policy: `gpt-5.4-mini`
- Generated service repos use `agents.max_depth = 1` so the root agent can run under current Codex while nested workers remain disallowed by repo policy.
- Default runtime policy for generated repos: `Node 20.19.6 LTS`
- Default product stack policy for generated repos: `Next.js 16.x LTS line + React 19.x stable line + TypeScript`, `Vercel`, `Supabase/Postgres`
- Default integration branch name for generated repos: `main`
- Default work branch prefixes for generated repos: `feature/`, `bugfix/`, `hotfix/`, `experiment/`, `wip/` with task id in the branch name
- Generated service repos include a commit message template and commit-msg hook for `<type>: <subject>` style messages.
- Generated service repos include `.nvmrc` and `.node-version` pinned to the HQ runtime default.
- Generated service repos include design docs for art direction and UI principles.
- Generated service repos include a browser-review checklist for design and functional iteration in the running app.
- Documentation policy: Korean for internal operating docs, English for public case studies

## Example commands

Prepare HQ on a new machine:

```bash
python3 scripts/setup_hq.py
```

Generate a new service repository:

```bash
python3 scripts/generate_service_repo.py \
  --spec examples/service.yaml
```

By default, generated services are created under `../deck/<service-id>` relative to this HQ repo.
Set `HARNESS_DECK_ROOT` if you want a different generated-services directory on a given machine.

Validate the HQ itself:

```bash
python3 scripts/validate_harness.py --mode all
python3 -m unittest tests.test_harness_hq
```

## Notes

- This repo intentionally keeps Claude compatibility as a future adapter. `AGENTS.md` is canonical. Generated repos include a `generate_claude_shim.py` utility so the compatibility layer can be added without dual-authoring docs by hand.
- Agents opening HQ for the first time on a machine should treat `python3 scripts/setup_hq.py` as the first setup step.
- Hooks are experimental in Codex. This repo uses them as guardrails, then backs them up with explicit scripts and CI.
- Codex model availability differs by surface and release. Revalidate the model pins in `.codex/` when you upgrade the Codex client.
- The Python tooling expects `PyYAML`. Install it with `python3 -m pip install pyyaml` if it is not already present in your environment.
