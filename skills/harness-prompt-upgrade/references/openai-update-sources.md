# Official OpenAI Update Sources

Use official OpenAI sources only when deciding whether a new capability belongs in Harness HQ or a generated service repo.

## Priority Order

1. OpenAI product or release posts on `openai.com`
2. Official OpenAI docs or changelog pages linked from those posts
3. OpenAI Help Center release notes when product behavior or availability needs confirmation

## Relevant Source Types

- Codex product posts:
  - `https://openai.com/index/introducing-codex/`
  - `https://openai.com/index/introducing-the-codex-app/`
  - `https://openai.com/index/introducing-upgrades-to-codex/`
  - `https://openai.com/index/codex-for-almost-everything/`
- Model release notes:
  - `https://help.openai.com/en/articles/9624314-model-release-notes`

## What To Extract

- New agent capabilities that change how work can be delegated or automated
- New app or tool integrations that materially improve repo workflows
- Changes to model availability or behavior that should alter model pins, worker policy, or prompt wording
- New automation or memory features that justify prompt-context regeneration or recurring review flows

## What Not To Do

- Do not treat third-party blog summaries as authoritative.
- Do not add prompt rules for speculative or preview behavior unless the official source makes the limitation clear.
- Do not change Harness HQ just because a feature sounds useful; connect it to a concrete repo workflow.

