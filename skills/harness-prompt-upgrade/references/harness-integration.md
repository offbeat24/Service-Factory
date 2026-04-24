# Harness Integration Notes

Use these repo anchors when listing or applying prompt upgrades.

## Harness HQ

- `AGENTS.md`: short operating map
- `README.md`: operator-facing workflow and defaults
- `.codex/config.toml` and `.codex/hooks.json`: prompt-adjacent runtime policy
- `scripts/validate_harness.py`: HQ enforcement
- `.harness/contracts/docs-manifest.json`: required generated docs
- `.harness/templates/service-repo/`: generated repo defaults

## Generated Service Repo

- `service.yaml`: structured service intent and brand inputs
- `docs/product/product-spec.kr.md`: product scope
- `docs/design/art-direction.kr.md`: visual direction
- `docs/design/ui-principles.kr.md`: UI rules
- `docs/design/browser-review.kr.md`: browser review loop
- `docs/prompting/prompt-context.kr.md`: prompt-ready deck summary
- `scripts/harness.py`: auto-sync and enforcement entrypoint

## Preferred Review Pattern

1. List candidate changes first.
2. Identify the exact source documents, structured inputs, scripts, or hooks each candidate would touch.
3. Wait for the user to choose which candidates to implement.
4. After approval, update only the selected targets.
