---
name: harness-prompt-upgrade
description: Review official OpenAI or Codex product updates and produce a prioritized list of candidate Harness HQ prompt upgrades. Use after the user updates Codex/OpenAI tooling and wants Codex to identify which new agent, app, automation, tool-use, model, or generated deck prompt-context capabilities might be worth reflecting in the harness, without applying changes until the user explicitly approves selected items.
---

# Harness Prompt Upgrade

## Overview

Use this skill to translate OpenAI/Codex product updates into a concrete review list for Harness HQ. Ground the work in official OpenAI sources first, then identify which prompt, policy, hook, skill, model, or generated deck prompt-context changes are worth considering. Do not edit files unless the user explicitly asks to apply selected items.

## Workflow

1. Read [references/openai-update-sources.md](references/openai-update-sources.md) and confirm which official update source is relevant.
2. Inspect the current repo context before proposing changes.
3. If working in Harness HQ:
   - Review `AGENTS.md`, `README.md`, `.codex/`, `scripts/`, `.harness/contracts/`, and `.harness/templates/service-repo/`.
   - Identify prompt policy, hooks, templates, docs, or model pins that might benefit from the update.
4. If working in a generated service repo:
   - Read `service.yaml`, `docs/product/product-spec.kr.md`, `docs/design/art-direction.kr.md`, `docs/design/ui-principles.kr.md`, `docs/design/browser-review.kr.md`, and `docs/prompting/prompt-context.kr.md`.
   - Treat `docs/prompting/prompt-context.kr.md` as the prompt-ready summary of the current deck.
5. Produce an upgrade candidate list before any implementation:
   - `candidate`: short name.
   - `source`: official source and date when available.
   - `why it matters`: concrete harness benefit.
   - `target files`: likely files or generated repo areas.
   - `scope`: HQ only, new generated repos, existing deck repos, or all.
   - `risk`: low, medium, or high.
   - `recommendation`: apply now, defer, reject, or needs user decision.
6. Stop after the candidate list unless the user explicitly asks to implement selected items.

## Upgrade Rules

- Use only official OpenAI sources for update claims.
- Distinguish between platform changes and repo-local prompt shaping.
- Only promote a new capability into the harness when it changes how the agent should work, not just because it exists.
- Keep prompt files concise and derived from source documents instead of duplicating large docs inline.
- When generated deck contents change, refresh the prompt-context file instead of hand-editing prompt summaries.
- If the user approves implementation and scripts, contracts, or `.codex` policy change in HQ, update docs and run `python3 scripts/validate_harness.py --mode all`.
- Do not create or update recurring automations unless the user explicitly asks for automation.

## Repo-Specific Outputs

- In HQ, likely targets include `.codex/`, `scripts/`, `.harness/contracts/`, `.harness/templates/service-repo/`, and linked docs.
- In generated repos, likely targets include `scripts/harness.py`, `docs/prompting/prompt-context.kr.md`, `AGENTS.md`, and prompt-facing docs referenced by the harness.

## Validation

- Candidate-list only: no validation command is required unless local inspection scripts were run.
- Harness HQ after approved implementation: `python3 scripts/validate_harness.py --mode all`
- Generated service repo:
  - `python3 scripts/harness.py pre-task`
  - `python3 scripts/harness.py ci`
