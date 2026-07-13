# 디자인 레퍼런스 선택

## 목적

- 프로젝트 컨셉에 맞는 DESIGN.md 기준을 구현 전에 먼저 고른다.
- 초기 UI 설정과 이후 큰 디자인 변경은 같은 선택 절차를 따른다.
- 외부 DESIGN.md 제공 사이트는 참고 입력이며, 최종 source of truth는 이 레포의 `DESIGN.md`와 관련 design docs다.

## 제공처 확인

- `oh-my-design`: 한국어 친화 카탈로그와 브랜드 철학 레이어를 확인한다.
- `getdesign.md`: Google Stitch 계열 DESIGN.md 분석과 해외 서비스 레퍼런스를 확인한다.
- 두 제공처를 모두 확인하지 못했다면 이유와 대체 근거를 이 문서에 남긴다.

## 후보 추림 기준

- 서비스 컨셉: {{CONCEPT}}
- 타깃 사용자:
{{TARGET_USERS_BULLETS}}
- 문제 정의: {{PROBLEM}}
- 후보는 브랜드 인지도보다 사용자 유형, 신뢰의 종류, 정보 밀도, 전환 행동, 카피 톤이 맞는지를 우선한다.
- 시각, 밀도, voice, component behavior, motion은 필요하면 서로 다른 레퍼런스에서 축별로 조합한다.

## 후보 목록

{{DESIGN_REFERENCE_CANDIDATES_BULLETS}}

## 선택 결과

{{SELECTED_DESIGN_REFERENCE_BULLETS}}

## 적용 축

- layout/density: 선택한 레퍼런스가 첫 화면 구조, 섹션 리듬, 정보 밀도에 어떤 영향을 주는지 기록한다.
- visual language: 색, 표면, 타이포, 이미지 톤 중 무엇을 가져오는지 기록한다.
- voice/microcopy: 버튼, empty/loading/error/success 상태 문구의 말투를 어떤 레퍼런스에서 가져오는지 기록한다.
- component states: hover, focus, disabled, loading, error 상태가 어떤 규칙을 따르는지 기록한다.
- motion: 트랜지션 시간, 이징, 강조 효과의 허용 범위를 기록한다.

## 변경 절차

- `DESIGN.md`를 실질적으로 바꾸기 전에 이 문서에서 새 후보를 다시 추린다.
- `oh-my-design` 후보 1개 이상과 `getdesign.md` 후보 1개 이상을 비교한다.
- 변경이 작은 UI 수정이면 기존 선택 결과를 유지하는지, 특정 축만 바꾸는지 먼저 적는다.
- 선택 결과가 바뀌면 `service.yaml`의 `branding.design_reference_candidates`와 `branding.selected_design_reference`를 갱신한다.
- 그 다음 `DESIGN.md`, `docs/design/art-direction.kr.md`, `docs/design/ui-principles.kr.md`, 필요하면 prompt context를 갱신한다.

## 선택 로그

- {{BOOTSTRAP_TASK_ID}}: 초기 레퍼런스 후보와 선택 결과는 `service.yaml`의 branding 섹션에서 생성됐다.
