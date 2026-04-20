# {{BOOTSTRAP_TASK_ID}} 실행 계획

## 목표

`{{SERVICE_NAME}}`의 첫 구현 루프를 시작하기 전에 현재 스펙, 기본 스택, 문서 구조, 검증 구조를 정렬한다.

## 범위

- 서비스 레포 초기 구조 확인
- 핵심 플로우 중 첫 구현 대상 선정
- evidence 수집 방식과 검증 명령 확인

## 제약

- 기본 provider는 `{{PROVIDER}}`다.
- AGENTS.md는 짧게 유지한다.
- 문서 없는 구현은 완료로 간주하지 않는다.

## 수용 기준

- product spec과 architecture why가 현재 방향을 설명한다.
- 첫 구현 범위가 분명하다.
- evidence 저장 위치와 run-report 위치가 준비되어 있다.

## 읽을 문서

- `AGENTS.md`
- `docs/product/product-spec.kr.md`
- `docs/architecture/why.kr.md`
- `docs/build-journal.kr.md`

## 예상 변경

- 앱 스캐폴드 또는 첫 핵심 기능 구현
- 검증 명령 보강
- task evidence 수집 규칙 고도화

## 검증 방법

- `python3 scripts/harness.py pre-task`
- `python3 scripts/harness.py ci`

