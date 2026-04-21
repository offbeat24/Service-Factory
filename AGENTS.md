# AGENTS.md

## Project Overview

Harness HQ is the control repo for a Codex-first service factory. It does not host real product apps. It owns the contracts, templates, scripts, and guardrails used to create per-service repositories.

## Setup Commands

- Prepare HQ on a new machine: `python3 scripts/setup_hq.py`
- Validate HQ contracts and examples: `python3 scripts/validate_harness.py --mode all`
- Generate a service repository from a spec: `python3 scripts/generate_service_repo.py --spec examples/service.yaml`
- Run HQ tests: `python3 -m unittest tests.test_harness_hq`

## Architecture Map

- Repo policy and operator guide: [README.md](README.md)
- HQ structure and boundaries: [docs/architecture/hq-structure.kr.md](docs/architecture/hq-structure.kr.md)
- Evidence policy: [docs/quality/evidence-policy.kr.md](docs/quality/evidence-policy.kr.md)
- Approval matrix: [docs/security/approval-matrix.kr.md](docs/security/approval-matrix.kr.md)
- Machine contracts: `.harness/contracts/`
- Service repo template: `.harness/templates/service-repo/`

## Working Rules

- On a newly cloned machine, run `python3 scripts/setup_hq.py` before generation, validation, or policy changes.
- Keep `AGENTS.md` short. Put detailed rules in linked docs.
- Treat `.harness/contracts/` as the source of truth for repo generation and validation.
- Do not add product-specific code here. Product code belongs in generated service repositories.
- After generating a service repository from `service.yaml`, move the active Codex work to that generated repo and keep product implementation there.
- Update docs when you change scripts, contracts, Codex config, or repo policy.
- Run `python3 scripts/validate_harness.py --mode all` before closing substantial HQ changes.

## Security And Approval

- Dangerous shell actions, destructive file removal, infra mutation, billing, and production deployment require approval.
- Hooks are only a guardrail. They do not replace human review or CI.
