# 브라우저 리뷰 체크리스트

## 리뷰 준비

- 로컬 앱을 실행하고 접근 가능한 URL을 기록한다.
- 가능하면 Codex browser 또는 Computer Use로 직접 화면을 확인한다.
- 리뷰 대상 화면과 핵심 플로우를 먼저 적는다.
- UI 수정 작업이면 `docs/design/ui-edit-brief.kr.md` 또는 현재 task 문서에서 유지 범위, 변경 범위, 금지 범위를 먼저 확인한다.
- UI 수정 작업이면 변경 전 기준 화면을 데스크톱과 모바일에서 먼저 캡처한다.

## 기능 리뷰

- 핵심 플로우를 실제 브라우저에서 처음부터 끝까지 수행한다.
- 버튼, 링크, 폼 제출, 모달, 탭, 내비게이션이 의도대로 동작하는지 본다.
- 브라우저 console 오류와 network 실패가 없는지 확인한다.
- 기능 문제를 발견하면 재현 절차와 함께 기록한다.

## 데스크톱 리뷰

- 첫 화면에서 가장 중요한 CTA가 즉시 보이는가
- 정보 계층이 한 번에 읽히는가
- 카드, 섹션, 표가 과밀하지 않은가
- art direction의 reference와 anti-pattern을 지키는가
- 요청하지 않은 구조 변경이나 스타일 대수술이 추가되지 않았는가

## 모바일 리뷰

- 첫 화면에서 핵심 행동 하나만 선명하게 남는가
- 텍스트가 줄바꿈으로 무너지지 않는가
- 여백이 과도하게 줄지 않는가
- 스크롤 순서가 데스크톱보다 자연스러운가
- 수정 후 오버플로, 터치 타깃 축소, CTA 발견성 저하가 생기지 않았는가

## 수정 전후 비교

- 같은 화면을 수정 전과 수정 후에 같은 viewport 기준으로 다시 캡처한다.
- 요청사항 반영 여부와 사용성 부작용 여부를 따로 적는다.
- 바뀐 요소가 brief에 적힌 범위를 넘지 않았는지 확인한다.
- 작은 문구, 간격, CTA 강조 수정이라면 전체 레이아웃 안정성이 유지되는지 먼저 본다.

## 비주얼 초안 대조

- 구현 전 생성한 비주얼 초안 이미지와 실제 브라우저 화면을 나란히 비교한다.
- 초안의 계층, 색감, 여백, 주요 이미지 사용 의도가 구현에 반영됐는지 확인한다.
- 국문 Pretendard, 영문 Inter 기본 폰트가 적용됐는지 확인하고, 예외가 있으면 art direction의 근거를 대조한다.
- 초안과 다른 부분은 의도된 조정인지 결함인지 구분해서 기록한다.

## fidelity 리뷰

- 구현된 화면이 선택한 layout thesis처럼 읽히는가
- 구현된 화면이 선택한 visual thesis처럼 보이는가
- main visual anchor가 실제로 존재하는가
- utility가 위로 기어 올라와 first view를 평평하게 만들지 않았는가
- spacing, type contrast, surface treatment가 concept 이미지를 배반하지 않는가
- mobile adaptation이 같은 thesis를 유지하는가, 아니면 generic stacked page로 무너졌는가

## 레이아웃 안정성 판정

- `layout-stable`: thesis가 분명하고 이후 수정이 detail polish 수준이다.
- `layout-drifting`: 의도는 보이지만 hierarchy, spacing, surface treatment 중 하나가 약해졌다.
- `layout-failed`: 구조나 first-view intent가 concept에서 크게 이탈했다.
- `layout-stable`이 아니면 구조 조정 또는 concept 재검토를 먼저 하고 detail polish로 넘어가지 않는다.

## evidence 캡처

- 비주얼 초안 이미지 또는 생성 프롬프트 경로
- concept image 경로
- chosen direction 메모
- UI 수정 전 기준 스크린샷
- 데스크톱 첫 화면 스크린샷
- 모바일 첫 화면 스크린샷
- 수정 후 동일 화면 비교 스크린샷
- 비주얼 초안 대비 구현 차이 메모
- 구현 과정에서 무엇이 concept에서 바뀌었고 왜 바뀌었는지 메모
- thesis가 유지됐는지에 대한 판정
- 요청 반영 여부 메모
- 사용성 부작용 여부 메모
- 필요하면 CTA가 보이는 추가 스크린샷
- 핵심 플로우 성공 또는 실패를 보여주는 캡처
- console 또는 network 이상 징후 메모
- hierarchy, spacing, anti-pattern 회피 여부 메모

## 수정 루프

- 브라우저에서 발견한 문제를 build journal과 실행 계획에 기록한다.
- 수정 요청은 가능하면 `docs/design/ui-edit-brief.kr.md`에 구조화해서 남긴다.
- 수정 후 같은 화면을 다시 열어 비교한다.
- 기능 수정 후에는 같은 플로우를 다시 재생해 회귀가 없는지 확인한다.
- 결과가 만족스럽지 않으면 evidence를 갱신하며 다시 반복한다.
