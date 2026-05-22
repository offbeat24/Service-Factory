# Harness HQ v4

Harness HQ는 Codex-first 서비스 팩토리의 본부 저장소다. 이 저장소에는 실제로 배포할 제품 앱을 넣지 않는다. 대신 서비스 레포를 반복 가능하게 생성하고 운영하기 위한 계약, 템플릿, Codex 정책, 검증 스크립트, 문서 규칙을 관리한다.

## 이 저장소가 담는 것

- `AGENTS.md`: 코딩 에이전트용 짧은 진입 문서
- `.codex/`: HQ 작업에 쓰는 Codex 기본 설정, 훅, 커스텀 에이전트 정의
- `skills/`: Harness 전용 업그레이드 워크플로에 쓰는 저장소 버전 관리형 Codex 스킬
- `.harness/contracts/`: `service.yaml`, `task-pack.json`, `run-report.json`, `docs-manifest.json`의 기계 판독 계약
- `.harness/templates/service-repo/`: 서비스 레포를 생성할 때 쓰는 기본 템플릿
- `scripts/`: HQ 생성 및 검증 스크립트
- `docs/`: 구조, evidence, 승인, 프롬프트 정책 같은 사람이 읽는 운영 문서
- `docs/operations/prompt-policy.kr.md`: 프롬프트, 도구, 검증, 인계, 메모리 운영 정책
- `examples/`: 샘플 서비스 스펙과 작업 산출물 예시
- `tests/`: 레포 생성 및 강제 규칙 회귀 테스트
- `.gitignore`: HQ 산출물과 OS 잡파일 정리 규칙

## 운영 모델

1. 새 머신에서 clone한 뒤 `python3 scripts/setup_hq.py`를 한 번 실행한다.
2. 먼저 `service.yaml`을 작성한다.
3. 이 HQ에서 형제 디렉터리 `deck/` 아래로 서비스 레포를 생성한다.
4. 활성 Codex 대화와 작업 디렉터리를 생성된 서비스 레포로 옮긴다. 제품 구현을 HQ 안에서 계속하지 않는다.
5. 생성된 서비스 레포에 git이 아직 없으면 `git init -b main`으로 초기화한다.
6. 생성된 서비스 레포에서 `feature/init` 같은 작업 브랜치를 만든다.
7. 레포 로컬 git hooks 경로를 `git config core.hooksPath .githooks`로 설정한다.
8. 필요하면 `git config commit.template .gitmessage.txt`로 커밋 템플릿도 켠다.
9. 생성된 레포에서 `python3 scripts/harness.py pre-task`를 실행한다.
10. 이후 제품 작업은 생성된 레포의 `AGENTS.md`, `.codex/`, `docs/`, hooks 규칙 안에서 진행한다.
11. 작업을 마치기 전 `python3 scripts/harness.py pre-complete`를 실행하거나, 같은 규칙을 hooks와 CI로 통과시킨다.

## 현재 기본값

- 런타임 표면: Codex CLI/App
- 제공자: OpenAI only
- 기본 리드 정책: `gpt-5.4`, medium reasoning
  - 일반 계획, 구현 조율, 보통 난도의 제품 작업에 사용한다.
- 계획/승격 정책: `gpt-5.5`, high reasoning
  - 초기 제품 방향, 아키텍처/데이터 경계, 인증/결제/보안, 복잡한 UX 계층, 큰 작업 분해, 실패 복구 계획, 계약/템플릿 정책 변경, 프롬프트/구조 감사, 최종 리뷰에 사용한다.
- 코딩 worker 정책: `gpt-5.3-codex`
  - 범위가 좁은 구현, 리팩터링, 버그 수정, 테스트 보강에 사용한다.
- 문서/evidence worker 정책: `gpt-5.4-mini`
  - 저위험 문서 작업, 요약, 산출물 정리에 사용한다.
- 장시간 작업 정책: `gpt-5.2`
  - 긴 감사, 마이그레이션, 오래 훑는 합성 작업에 사용한다.
- UI checker 정책: `gpt-5.5`
  - 스크린샷, DOM, 브라우저 콘솔, 플로우 evidence 점검에 사용한다.
- 프롬프트/구조 감사 정책: `gpt-5.5`, high reasoning
  - `AGENTS.md`, `.codex/`, `.harness/contracts/`, `.harness/templates/`, `scripts/`, `docs/operations/`를 함께 점검하는 작업은 비용 절감보다 판단 품질을 우선한다.
- 이미지 작업 정책: 최신 상위 모델 우선
  - 이미지 생성 초안, 이미지 해석, 시각 회귀 판단, 디자인 방향 비교처럼 이미지가 핵심 입력 또는 출력인 작업은 현재 최신 모델인 `gpt-5.5`를 우선 사용한다.
- 상세 모델 라우팅 정책: `docs/operations/model-routing.kr.md`
- 상세 프롬프트 정책: `docs/operations/prompt-policy.kr.md`
- 생성 서비스 레포는 `agents.max_depth = 1`을 사용한다.
  - 현재 Codex 제약에서 루트 에이전트를 실행 가능하게 유지하면서, repo 정책상 중첩 worker는 계속 금지한다.
- 생성 서비스 레포 기본 앱 런타임: `Node 20.19.6 LTS`
- 생성 서비스 레포 기본 웹 스택: `Next.js 16.x LTS line + React 19.x stable line + TypeScript`, `Vercel`, `Supabase/Postgres`
- 생성 서비스 레포 기본 통합 브랜치: `main`
- 생성 서비스 레포 기본 작업 브랜치 접두사: `feature/`, `bugfix/`, `hotfix/`, `experiment/`, `wip/`
  - 브랜치 이름에는 task id를 넣지 않는다. task id는 active exec plan, `task-pack.json`, run report에서 관리한다.
  - 브랜치명에서 task id를 추론하지 않으므로 active exec plan은 기본적으로 하나만 유지한다.
- 생성 서비스 레포는 `<type>: <subject>` 형식의 커밋 메시지를 위한 템플릿과 `commit-msg` hook을 포함한다.
- 생성 서비스 레포는 HQ 런타임 기본값에 맞춘 `.nvmrc`, `.node-version`을 포함한다.
- 생성 서비스 레포는 art direction, UI principles, browser review 문서를 포함한다.
- 생성 서비스 레포는 UI 수정 요청을 좁게 고정하기 위한 `docs/design/ui-edit-brief.kr.md` 기본 문서를 포함한다.
- 생성 서비스 레포는 `docs/prompting/prompt-context.kr.md`를 포함한다.
  - 이 문서는 `service.yaml`과 deck 문서에서 다시 생성하는 프롬프트 친화 요약이다.
- 생성 서비스 레포는 좁은 UI 수정 작업을 위한 `docs/prompting/ui-edit-prompt-template.kr.md` 기본 템플릿을 포함한다.
- 생성 서비스 레포는 실행 중인 앱을 기준으로 디자인/기능 반복을 검증하기 위한 browser-review 체크리스트를 포함한다.
- 문서 언어 정책: 내부 운영 문서는 한국어, 공개 case study는 영어

## 프롬프트 운영 원칙

- 프롬프트는 한 번의 지시문이 아니라 작업 환경 전체다.
- repo 문서, 구조화된 산출물, 도구 선택, 검증 루프, 인계 규칙까지 함께 설계한다.
- 기본 작업 순서는 `observe -> plan -> execute -> verify -> record`다.
- 코드만이 산출물이 아니다.
  - 필요하면 테스트, 문서, evidence, run report, 리뷰 메모까지 함께 남긴다.
- 장기 기억은 채팅이 아니라 버전 관리되는 파일과 문서에 둔다.
- 시점 민감한 사실은 웹이나 공식 도구로 확인하고, repo 내부 정책은 외부 일반론보다 우선한다.
- 프롬프트/구조 감사는 `gpt-5.5`로 수행하고, 결과는 문서와 검증 스크립트에 반영한다.
- 이미지가 핵심 입력 또는 출력인 작업은 비용 절감보다 판단 품질을 우선해 최신 상위 모델로 처리한다.

## 예시 명령

새 머신에서 HQ 준비:

```bash
python3 scripts/setup_hq.py
```

새 서비스 레포 생성:

```bash
python3 scripts/generate_service_repo.py \
  --spec examples/service.yaml
```

기본 생성 위치는 이 HQ 저장소 기준 `../deck/<service-id>`다. 머신별로 다른 생성 루트를 쓰고 싶으면 `HARNESS_DECK_ROOT`를 설정한다.

HQ 자체 검증:

```bash
python3 scripts/validate_harness.py --mode all
python3 -m unittest tests.test_harness_hq
```

## 참고

- 이 저장소는 미래 어댑터로서 Claude 호환도 유지한다. 기준 문서는 `AGENTS.md`이며, 생성 레포에는 수동 중복 작성 없이 호환 레이어를 추가할 수 있도록 `generate_claude_shim.py`를 포함한다.
- 새 머신에서 처음 HQ를 열면 `python3 scripts/setup_hq.py`를 첫 단계로 취급한다.
- Codex hooks는 아직 실험적이다. 이 저장소는 hooks를 1차 가드레일로 쓰고, 명시적 스크립트와 CI로 다시 강제한다.
- Codex 모델 가용성은 사용 표면과 릴리스에 따라 달라질 수 있다. Codex 클라이언트를 올리면 `.codex/`의 모델 핀을 다시 확인한다.
- Python 도구는 `PyYAML`을 요구한다. 환경에 없다면 `python3 -m pip install pyyaml`로 설치한다.
