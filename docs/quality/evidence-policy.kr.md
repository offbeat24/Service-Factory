# Evidence 정책

## 기본 원칙

평가는 텍스트의 모양이 아니라 같은 수용 기준과 evidence bundle을 통과하는지로 판단한다.

## Day 1 기본 증거

- 핵심 플로우 실행 결과
- 스크린샷
- DOM snapshot 또는 HTML excerpt
- 브라우저 console 오류 기록
- network 실패 기록
- 서버 로그 excerpt

## 저장 위치

생성된 서비스 레포는 `artifacts/evidence/<task-id>/` 아래에 증거를 저장한다.

## 승격 조건

아래 조건 중 하나라도 만족하면 메트릭과 트레이스를 추가한다.

- 외부 포트폴리오에 공개
- 커스텀 서브도메인 연결
- 실사용자 유입 또는 수익화 시작

