# 모델 라우팅 정책

## 목적

토큰 사용량을 줄이기 위해 모든 작업을 최고 모델에 맡기지 않는다. 기본 루트 작업은 균형형 모델에서 시작하고, 판단 난도가 높거나 실패 비용이 큰 단계만 상위 모델로 승격한다.

## 모델별 강점

- `gpt-5.5`: 가장 높은 판단 품질이 필요한 초기 제품/아키텍처 계획, 데이터 경계, 인증/결제/보안, 복잡한 UX 계층, 큰 작업 분해, 실패 복구 계획, 계약/템플릿 정책 변경, 최종 리뷰에 사용한다.
- `gpt-5.5`: 이미지 생성 초안, 이미지 해석, 시각 회귀 판단, 디자인 reference 비교처럼 이미지가 핵심 입력 또는 출력인 작업의 기본 모델로도 사용한다.
- `gpt-5.4`: 일반적인 계획, 구현 조율, UI evidence 검토, 사용성 판단에 쓰는 기본 리드 모델이다. 품질과 비용 균형을 우선한다.
- `gpt-5.3-codex`: 코드 편집, 테스트 보강, 버그 수정, 국소 리팩터링처럼 범위가 선명한 구현 작업에 사용한다.
- `gpt-5.4-mini`: 문서 정리, run report 초안, evidence 목록화, 단순 검색 요약처럼 실패 비용이 낮은 작업에 사용한다.
- `gpt-5.2`: 긴 감사, 대규모 마이그레이션 계획, 여러 파일을 오래 훑어야 하는 합성 작업에 사용한다. 최종 결정은 필요하면 `gpt-5.5`로 승격한다.

## 단계별 기본 배치

- 요청 해석과 기본 실행 계획: `gpt-5.4`, medium reasoning
- 초기 제품 framing, 핵심 사용자/수익화/권한 경계 결정: `architecture_planner` `gpt-5.5`, high reasoning
- 서비스 아키텍처, 데이터 모델, API 경계, 저장소/배포 전략 결정: `architecture_planner` `gpt-5.5`, high reasoning
- 인증, 결제, 개인정보, 보안, 승인 매트릭스가 얽힌 계획: `architecture_planner` `gpt-5.5`, high reasoning
- 복잡한 첫 화면 UX 계층, 정보 구조, 전환 흐름 결정: `architecture_planner` `gpt-5.5`, high reasoning
- 여러 패키지나 템플릿을 건드리는 큰 작업 분해: `architecture_planner` `gpt-5.5`, high reasoning
- HQ 또는 서비스 레포의 일반 구현: `gpt-5.4`가 조율하고, 분리 가능한 코드 작업은 `implementation_worker` `gpt-5.3-codex`에 맡긴다.
- 테스트 실패 수정과 좁은 버그 수정: `gpt-5.3-codex`, medium reasoning
- 두 번 이상 실패한 디버깅의 원인 재분석과 복구 계획: `architecture_planner` `gpt-5.5`, high reasoning
- 문서 동기화, 빌드 저널, run report, evidence 정리: `gpt-5.4-mini`, medium reasoning
- 장시간 작업 인계 문서 정리와 상태 요약: `gpt-5.4-mini`, medium reasoning
- 이미지 생성 초안, 이미지 해석, 디자인 레퍼런스 비교: `gpt-5.5`, high reasoning
- 브라우저 스크린샷, DOM, console, network evidence 점검: `ui_checker` `gpt-5.5`, high reasoning
- 생성 결과의 결함 위주 최종 점검과 evaluator 성격 리뷰: `reviewer` `gpt-5.5`, high reasoning
- 대규모 코드베이스 조사, 마이그레이션 후보 정리, 긴 비교 분석: `long_runner` `gpt-5.2`, medium reasoning
- 계약, 템플릿, 훅, 생성 스크립트, Codex 정책 변경 전후 판단: `architecture_planner` 또는 `reviewer` `gpt-5.5`, high reasoning
- 최종 코드 리뷰, 보안/승인 경계, 데이터 삭제/배포/과금 같은 고위험 판단: `reviewer` 또는 review model `gpt-5.5`, high reasoning

## 승격 기준

아래 중 하나에 해당하면 `gpt-5.5`로 승격한다.

- 보안, 시크릿, 결제, 데이터 삭제, DB 마이그레이션, 운영 배포가 걸린다.
- 여러 계약, 템플릿, 훅, 생성 스크립트를 동시에 바꿔야 한다.
- 초기 기획 결과가 데이터 모델, 권한 체계, 수익화, 배포 구조를 바꾼다.
- UI 방향이 핵심 전환율, onboarding, 결제 흐름, 사용자 신뢰에 직접 영향을 준다.
- 이미지가 핵심 입력 또는 출력이어서 시각 판단 품질이 직접 결과를 좌우한다.
- 같은 버그 수정이 두 번 이상 실패했거나 원인 가설이 갈린다.
- 테스트는 통과하지만 설계상 회귀 가능성이 크다.
- 모델이 서로 다른 결론을 내거나 근거가 약하다.

## 절감 기준

아래 작업은 상위 모델을 쓰지 않는다.

- 단순 문서 포맷 정리
- 이미 결정된 정책의 반복 반영
- run report 또는 evidence 경로 목록화
- 좁은 파일 범위의 테스트 fixture 수정
- 검색 결과나 로그의 1차 요약

## 검증 원칙

모델 라우팅은 `.codex/`, 서비스 템플릿, `scripts/validate_harness.py`, 테스트가 같은 값을 강제해야 한다. 모델 핀을 바꾸면 이 문서와 `README.md`, `docs/architecture/hq-structure.kr.md`를 함께 갱신하고 `python3 scripts/validate_harness.py --mode all`을 실행한다.
