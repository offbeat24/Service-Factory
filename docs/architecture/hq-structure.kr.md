# Harness HQ 구조

## 목적

이 저장소는 실제 서비스를 담는 앱 레포가 아니라, 서비스 레포를 반복 생성하기 위한 하네스 본부다. 여기서 관리하는 것은 서비스 자체가 아니라 서비스 제작 시스템이다.

## 핵심 경계

- `AGENTS.md`: 짧은 진입 문서
- `.codex/`: HQ 작업에 적용되는 Codex 정책
- `skills/`: HQ와 생성 레포에 적용할 수 있는 저장소 버전 관리형 Codex 스킬
- `.harness/contracts/`: 기계가 읽는 계약
- `.harness/templates/service-repo/`: 생성되는 서비스 레포의 초기 구조
- `scripts/`: 생성, 검증, shim 생성 같은 운영 스크립트
- `docs/`: 사람이 읽는 운영 문서
- `docs/operations/model-routing.kr.md`: 작업 단계별 Codex 모델 배치 기준
- `docs/operations/prompt-policy.kr.md`: 프롬프트, 도구, 검증, 인계, 메모리 운영 기준
- `.gitignore`: HQ 작업 중 생기는 OS/빌드 잡파일 차단
- `../deck/`: HQ가 생성한 서비스 레포들이 쌓이는 형제 디렉터리

## 디자인 문서 원칙

- 제품 스펙 하나에 디자인 의도를 몰아넣지 않는다.
- 생성 서비스 레포 루트에는 `DESIGN.md`를 두고, 에이전트가 가장 먼저 읽는 압축된 디자인 명세로 사용한다.
- 생성 서비스 레포에는 `docs/design/art-direction.kr.md`, `docs/design/ui-principles.kr.md`, `docs/design/browser-review.kr.md`를 함께 넣는다.
- 생성 서비스 레포에는 `docs/design/design-reference-selection.kr.md`를 함께 넣고, 서비스 컨셉에 맞춰 `oh-my-design`와 `getdesign.md`에서 DESIGN.md 후보를 먼저 추린 뒤 선택 근거와 적용 축을 기록한다.
- 생성 서비스 레포에는 first-pass UI 품질을 위해 `docs/design/ui-intent-brief.kr.md`, `docs/design/layout-exploration.kr.md`, `docs/design/visual-concepts.kr.md`도 함께 넣는다.
- 생성 서비스 레포에는 UI 수정 요청을 구조화하기 위한 `docs/design/ui-edit-brief.kr.md` 기본 문서를 함께 넣는다.
- 생성 서비스 레포에는 `docs/prompting/prompt-context.kr.md`를 두고, `service.yaml`과 deck 문서에서 자동으로 다시 만든다.
- 생성 서비스 레포에는 UI 수정 프롬프트를 좁은 범위로 고정하기 위한 `docs/prompting/ui-edit-prompt-template.kr.md` 기본 템플릿을 함께 넣는다.
- 생성 서비스 레포에는 새 화면, 랜딩, 대시보드 같은 작업에서 2개 방향 비교와 thesis 고정을 요구하는 `docs/prompting/ui-foundation-prompt-template.kr.md` 기본 템플릿도 함께 넣는다.
- 생성 서비스 레포에는 런타임 기준을 명확히 하기 위해 `.nvmrc`와 `.node-version`도 함께 넣는다.
- 생성 서비스 레포에는 브랜치/커밋 규칙을 바로 쓸 수 있도록 `.gitmessage.txt`와 필요한 git hook도 함께 넣는다.
- 생성 서비스 레포의 기본 구현 폰트는 국문 Pretendard, 영문 Inter로 고정하고, 테마 적합성이 명확한 예외만 art direction에 근거를 남겨 허용한다.
- 웹 디자인은 구현 전에 Codex가 이미지 기반 비주얼 초안을 먼저 만들고, 필요한 경우 그 이미지를 실제 구현 자산으로 활용한다.
- 디자인 품질 판단은 감상평 대신 reference, anti-pattern, screenshot evidence, spacing/type hierarchy 메모로 남긴다.
- 브라우저에서 실제 화면과 핵심 플로우를 보고 수정하는 루프를 기본 절차로 취급한다.
- 중요한 UI 작업은 코드 전에 brief, structural exploration, visual concepts, concept images를 먼저 고정하고, 브라우저 리뷰는 fidelity 판정에 사용한다.
- 초기 디자인 설정과 실질적인 DESIGN.md 변경은 두 제공처 후보 비교를 먼저 거치며, 변경 후에는 `service.yaml`, `DESIGN.md`, art direction, prompt context가 같은 선택 결과를 가리켜야 한다.
- UI 수정 통제는 긴 프롬프트 한 번보다 문서화된 수정 범위, 금지 패턴, 브라우저 비교 evidence로 다룬다.

## Codex 설정 원칙

- Codex 설정은 HQ와 서비스 템플릿에서 함께 관리하고 함께 검증해야 한다.
- 모델 핀은 Codex CLI/App 기준과 맞아야 하며, HQ와 서비스 템플릿이 같은 Codex 전용 모델군을 써야 한다.
- 기본 루트 작업은 `gpt-5.4`로 시작한다.
- `gpt-5.5`는 초기 제품 방향, 아키텍처/데이터 경계, 인증/결제/보안, 복잡한 UX 계층, 큰 작업 분해, 반복 실패 후 복구 계획, 계약/템플릿 정책 변경, 프롬프트/구조 감사, 최종 리뷰에 승격한다.
- 프롬프트/구조 감사는 `AGENTS.md`, `.codex/`, 계약, 템플릿, 스크립트, 정책 문서를 함께 판단하는 작업으로 보고 `gpt-5.5`를 강제한다.
- 반복 구현은 `gpt-5.3-codex`, 문서와 evidence 정리는 `gpt-5.4-mini`, 긴 감사와 마이그레이션은 `gpt-5.2`에 배정한다.
- 이미지 생성 초안, 이미지 해석, 스크린샷 기반 시각 판단은 최신 상위 모델로 처리한다. 현재 기본 핀은 `gpt-5.5`다.
- 서비스 템플릿은 현재 Codex 런타임 제약에 맞춰 `agents.max_depth = 1`을 사용한다.
- 생성 서비스 레포의 기본 앱 런타임은 `Node 20.19.6 LTS`, 기본 웹 스택은 `Next.js 16.x LTS line + React 19.x stable line + TypeScript`로 고정한다.
- 생성 서비스 레포의 기본 메인 브랜치 이름은 `main`이고, 작업 브랜치는 `feature/init` 같은 접두사 기반 규칙을 따른다. task id는 브랜치명이 아니라 active exec plan, `task-pack.json`, run report에서 관리하므로 active exec plan은 기본적으로 하나만 유지한다.
- 위 값은 루트 에이전트를 실행 가능하게 두기 위한 최소값이다. 중첩 worker 금지 정책은 `AGENTS.md` 문구로 계속 유지한다.

## 새 머신 준비

- HQ를 clone한 뒤에는 `python3 scripts/setup_hq.py`를 한 번 실행한다.
- 이 명령은 형제 디렉터리 `deck/`를 만들고, HQ 검증이 가능한 상태인지 점검한다.
- `HARNESS_DECK_ROOT`를 주면 머신별 생성 루트를 다른 위치로 바꿀 수 있다.

## 왜 이렇게 나눴는가

- 서비스 레포와 HQ를 분리해야 100개 서비스가 생겨도 공통 규칙을 한 곳에서 개선할 수 있다.
- 생성 결과를 `COL` 바깥 형제 디렉터리인 `deck/`에 두면 HQ와 서비스 작업 공간이 섞이지 않는다.
- `service.yaml` 작성과 생성은 HQ에서 하지만, 실제 제품 대화와 구현은 생성된 서비스 레포로 바로 이동해야 경계가 흐려지지 않는다.
- 서비스 레포가 독립 저장소여야 브랜드, 도메인, 배포, 권한을 서비스별로 다르게 운영할 수 있다.
- 하네스 규칙은 문서만으로 유지하지 않고, 템플릿과 검증 스크립트에 반영해야 실제로 반복 가능해진다.
