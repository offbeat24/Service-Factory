# 구조 이유

## 구조 원칙

- 서비스 레포는 제품 코드와 제품 문서를 담고, 하네스 HQ는 생성과 정책을 담당한다.
- 큰 프롬프트 하나 대신 짧은 AGENTS.md와 상세 docs를 같이 쓴다.
- 검증은 텍스트 설명보다 evidence bundle과 run-report를 우선한다.

## 기본 스택

- 웹 앱 기본 방향: Next.js + TypeScript
- 배포 기본 방향: {{DEPLOY_PREFERENCE}}
- 데이터 기본 방향: Supabase/Postgres
- 인증 필요도: {{AUTH_NEED}}
- 스토리지 필요도: {{STORAGE_NEED}}

## 예외와 override

{{OVERRIDES_BULLETS}}

## Task {{INIT_TASK_ID}}

- 초기 생성 시점에는 기본 스택을 먼저 채택하고, override는 문서화 없이는 허용하지 않는다.

## Task {{BOOTSTRAP_TASK_ID}}

- 첫 구현은 기본 스택 가정을 깨지 않는 범위에서 시작한다.
- 구조 변경이 필요하면 이 문서에 사유와 기대효과를 함께 남긴다.

