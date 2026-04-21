# Harness HQ 구조

## 목적

이 저장소는 실제 서비스를 담는 앱 레포가 아니라, 서비스 레포를 반복 생성하기 위한 하네스 본부다. 여기서 관리하는 것은 서비스 자체가 아니라 서비스 제작 시스템이다.

## 핵심 경계

- `AGENTS.md`: 짧은 진입 문서
- `.codex/`: HQ 작업에 적용되는 Codex 정책
- `.harness/contracts/`: 기계가 읽는 계약
- `.harness/templates/service-repo/`: 생성되는 서비스 레포의 초기 구조
- `scripts/`: 생성, 검증, shim 생성 같은 운영 스크립트
- `docs/`: 사람이 읽는 운영 문서
- `.gitignore`: HQ 작업 중 생기는 OS/빌드 잡파일 차단
- `../deck/`: HQ가 생성한 서비스 레포들이 쌓이는 형제 디렉터리

## 디자인 문서 원칙

- 제품 스펙 하나에 디자인 의도를 몰아넣지 않는다.
- 생성 서비스 레포에는 `docs/design/art-direction.kr.md`, `docs/design/ui-principles.kr.md`, `docs/design/browser-review.kr.md`를 함께 넣는다.
- 생성 서비스 레포에는 런타임 기준을 명확히 하기 위해 `.nvmrc`와 `.node-version`도 함께 넣는다.
- 디자인 품질 판단은 감상평 대신 reference, anti-pattern, screenshot evidence, spacing/type hierarchy 메모로 남긴다.
- 브라우저에서 실제 화면과 핵심 플로우를 보고 수정하는 루프를 기본 절차로 취급한다.

## Codex 설정 원칙

- Codex 설정은 HQ와 서비스 템플릿에서 함께 관리하고 함께 검증해야 한다.
- 모델 핀은 Codex CLI/App 기준과 맞아야 하며, HQ와 서비스 템플릿이 같은 Codex 전용 모델군을 써야 한다.
- 서비스 템플릿은 현재 Codex 런타임 제약에 맞춰 `agents.max_depth = 1`을 사용한다.
- 생성 서비스 레포의 기본 앱 런타임은 `Node 20.19.6 LTS`, 기본 웹 스택은 `Next.js 16.x LTS line + React 19.x stable line + TypeScript`로 고정한다.
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
