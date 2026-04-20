# 하네스 피드백

## 하네스 관찰

- 문서 hard gate가 활성화되어 있어 계획 없는 구현을 줄일 수 있다.
- task-bound evidence 구조가 있어 검증 결과를 축적하기 쉽다.

## 유지할 것

- AGENTS.md는 짧게 유지하고 상세 내용은 docs로 내리는 구조
- task_id 기반 문서와 run-report 연결

## 바꿀 것

- 앱 코드가 생기면 evidence 수집 명령을 실제 스택에 맞게 더 구체화한다.

## Task {{INIT_TASK_ID}}

- 초기 생성 단계에서는 문서와 검증 구조를 우선 깔아두는 방식이 유효했다.

## Task {{BOOTSTRAP_TASK_ID}}

- 첫 구현 루프에서는 어떤 검증이 자동화로 승격될지 기록한다.
- 반복되는 실수는 문서가 아니라 hook, script, CI 규칙으로 승격한다.

