# 아트 디렉션

## 디자인 목표

- 톤: {{DESIGN_TONE}}
- 비주얼 방향: {{DESIGN_VISUAL_DIRECTION}}
- 키워드:
{{DESIGN_KEYWORDS_BULLETS}}

## 참고 레퍼런스

{{DESIGN_REFERENCES_BULLETS}}

## DESIGN.md 레퍼런스 후보

{{DESIGN_REFERENCE_CANDIDATES_BULLETS}}

## 선택한 DESIGN.md 레퍼런스

{{SELECTED_DESIGN_REFERENCE_BULLETS}}

## 피해야 할 패턴

{{DESIGN_ANTI_REFERENCES_BULLETS}}

## 컬러 토큰

{{DESIGN_PALETTE_BULLETS}}

## 타이포그래피 방향

{{DESIGN_TYPOGRAPHY_BULLETS}}

## 타이포그래피 정책

- 기본 구현 폰트는 국문 Pretendard, 영문 Inter로 고정한다.
- 브랜드나 콘텐츠 테마상 다른 글꼴이 더 적합한 경우에만 예외를 허용한다.
- 예외를 적용하면 이 문서에 이유, 적용 범위, 대체 폰트를 함께 기록한다.

## 레이아웃 캐릭터

- 첫 화면의 dominant action이 구조를 이끌고, 보조 utility는 그 뒤를 따른다.
- 설명보다 먼저 감정적 톤과 행동 우선순위가 읽혀야 한다.
- 브랜드가 차분하더라도 평평한 box grid로 화면을 끝내지 않는다.

## 표면 전략

- 큰 덩어리의 surface가 장면을 만들고, 작은 카드 반복은 보조 역할에 그친다.
- 섹션 경계는 배경, 여백, 타이포 대비로 먼저 만들고 테두리 남발은 줄인다.

## 비주얼 초안 생성 절차

- 웹 디자인 구현 전에 Codex가 이미지 기반 비주얼 초안을 먼저 만든다.
- 초안은 첫 화면, 핵심 상태, 모바일 대응 중 작업 범위에 필요한 장면을 포함한다.
- 생성 프롬프트와 산출 이미지 경로를 `artifacts/evidence/<task-id>/`에 기록한다.
- 구현 중 필요한 경우 생성 이미지를 배경, 일러스트, 텍스처 같은 실제 자산으로 활용한다.

## 이미지와 일러스트 방향

{{DESIGN_IMAGERY_BULLETS}}

## 이미지 처리 전략

- 이미지가 있다면 분위기와 시선 유도를 담당하게 하고, 정보 전달은 텍스트와 레이아웃이 맡는다.
- 이미지가 없어도 구조 자체가 충분히 설득력 있어야 한다.

## 섹션 리듬

- 첫 화면은 한 번에 하나의 핵심 메시지만 강하게 읽히게 한다.
- 아래 섹션으로 갈수록 정보 밀도를 올리되, 리듬이 갑자기 잘게 쪼개지지 않게 한다.

## 대비 전략

- 강조는 CTA, 헤드라인, 핵심 proof에만 집중한다.
- 모든 요소를 동시에 세게 만들지 않고, 약한 대비와 강한 대비를 의도적으로 섞는다.

## 반복할 시그니처 모티프

- 브랜드에 맞는 surface 처리, 간격 리듬, headline 압축감 같은 요소를 2~3개만 반복한다.
- 시그니처 모티프는 장식보다 계층과 기억성에 기여해야 한다.

## 기본값으로 굳어지면 안 되는 패턴

- generic gradient hero
- 의미 없는 3열 feature card grid
- 첫 화면 상단의 noisy dashboard tiles
- typography 의도 없이 기본 font stack으로 후퇴한 화면
