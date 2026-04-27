# 프롬프트 컨텍스트

## 문서 목적

- 이 문서는 `service.yaml`과 핵심 설계 문서를 프롬프트 친화적인 요약으로 압축한다.
- 상세한 판단 근거는 원문 문서를 우선으로 보고, 이 문서는 세션 시작과 검증 시점에 빠르게 맥락을 회복하는 용도로 사용한다.

## 서비스 핵심

- 서비스 이름: {{SERVICE_NAME}}
- 서비스 ID: {{SERVICE_ID}}
- 컨셉: {{CONCEPT}}
- 문제 정의: {{PROBLEM}}
- 타깃 사용자:
{{TARGET_USERS_BULLETS}}
- 핵심 페이지:
{{PAGES_BULLETS}}
- 핵심 플로우:
{{CORE_FLOWS_BULLETS}}
- 성공 지표:
{{SUCCESS_METRICS_BULLETS}}

## 디자인/UX 기준

- 톤: {{DESIGN_TONE}}
- 비주얼 방향: {{DESIGN_VISUAL_DIRECTION}}
- 키워드:
{{DESIGN_KEYWORDS_BULLETS}}
- 컬러 토큰:
{{DESIGN_PALETTE_BULLETS}}
- 타이포그래피:
{{DESIGN_TYPOGRAPHY_BULLETS}}
- 레이아웃 원칙:
{{DESIGN_LAYOUT_PRINCIPLES_BULLETS}}
- 컴포넌트 규칙:
{{DESIGN_COMPONENT_RULES_BULLETS}}
- 모션:
{{DESIGN_MOTION_BULLETS}}

## 디자인 구현 규칙

- 기본 구현 폰트는 국문 Pretendard, 영문 Inter로 고정한다.
- 테마상 다른 글꼴이 필요할 때만 예외를 허용하고 art direction에 이유와 적용 범위를 남긴다.
- 웹 디자인은 구현 전에 Codex가 이미지 기반 비주얼 초안을 먼저 생성한다.
- 필요한 경우 생성 이미지를 실제 UI 자산으로 활용하고, 브라우저 리뷰에서 초안과 구현 결과를 대조한다.

## Deck 문서 반영 메모

### product-spec

- `docs/product/product-spec.kr.md`를 서비스 범위의 기준 문서로 사용한다.

### design

- `docs/design/art-direction.kr.md`, `docs/design/ui-principles.kr.md`, `docs/design/browser-review.kr.md`를 함께 읽고 UI 판단에 반영한다.

### architecture

- 구조나 정책 관련 변경은 `docs/architecture/why.kr.md`와 `AGENTS.md` 기준을 따른다.

## 작업 컨텍스트

- 기본 task id: `{{BOOTSTRAP_TASK_ID}}`
- 현재 작업은 브랜치와 active exec plan 기준으로 좁혀서 해석한다.
- 세부 실행 범위는 `docs/exec-plans/active/{{BOOTSTRAP_TASK_ID}}.kr.md`와 `task-pack.json`을 함께 본다.

## 프롬프트 적용 규칙

- 최신 근거 순서: `AGENTS.md` -> `service.yaml` -> `docs/prompting/prompt-context.kr.md` -> 상세 설계 문서
- 디자인 추정이 필요하면 디자인 문서와 브라우저 리뷰 기준을 먼저 확인한다.
- deck 내부 문서와 충돌하는 오래된 기억이나 일반론보다 현재 repo 문서를 우선한다.
