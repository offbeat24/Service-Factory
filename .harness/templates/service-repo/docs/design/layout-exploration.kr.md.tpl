# 레이아웃 탐색

## 목적

- serious UI 작업에서 레이아웃 사고를 코드보다 먼저 끝내기 위한 탐색 문서다.
- 이 문서의 목표는 “어느 구조로 갈지”를 정하는 것이지, 바로 예쁜 화면을 확정하는 것이 아니다.

## 사용 방법

- 최소 2개의 구조 방향을 비교한다.
- 방향마다 데스크톱과 모바일의 읽기 순서, 밀도, dominant action 배치를 함께 적는다.
- 각 방향의 장점뿐 아니라 실패 가능성도 적어 첫 시안에서 구조가 흔들리지 않게 한다.

## 공통 입력

- 대상 화면: 첫 화면 또는 핵심 플로우의 첫 장면
- primary action: 화면이 가장 먼저 유도해야 하는 행동 1개
- 필수 제약: 기존 브랜드 제약, 기술 제약, 반응형 제약, 접근성 제약
- 참고 문서: `docs/product/product-spec.kr.md`, `docs/design/art-direction.kr.md`, `docs/design/ui-principles.kr.md`

## 방향 A

- 구조 요약: 하나의 dominant hero가 감정적 몰입을 만들고, utility는 fold 아래로 미룬다.
- 섹션 순서: 가치 제안 -> 핵심 행동 -> proof -> 보조 구조
- 밀도 전략: 첫 화면은 넓고 깊게, 이후 섹션에서만 정보 밀도를 올린다.
- 데스크톱 구성: 넓은 여백과 강한 수직 리듬으로 읽기 속도를 조절한다.
- 모바일 구성: hero와 CTA를 먼저 보여주고, proof와 utility는 순차적으로 쌓는다.
- 왜 작동할 수 있는가: 첫 인상과 행동 유도가 충돌하지 않고 하나의 의도에 집중된다.
- 왜 실패할 수 있는가: proof를 너무 뒤로 미루면 신뢰가 약해질 수 있다.
- 동종 레퍼런스: category 안에서 hierarchy를 잘 다룬 화면을 붙인다.
- 이종 레퍼런스: category 밖에서 몰입형 첫 화면을 잘 만든 화면을 붙인다.

## 방향 B

- 구조 요약: utility를 더 빨리 노출하되, 첫 화면의 dominant action은 여전히 하나로 유지한다.
- 섹션 순서: 가치 제안 -> 즉시 사용 가능한 utility -> proof -> 세부 설명
- 밀도 전략: 첫 화면 안에서 요약 정보와 행동을 함께 보여주되 카드 과밀은 금지한다.
- 데스크톱 구성: 2열 또는 비대칭 분할을 써서 설명과 utility를 분리한다.
- 모바일 구성: utility를 너무 위로 끌어올리지 않고, CTA 다음 순서에 배치한다.
- 왜 작동할 수 있는가: 성급한 사용자에게 더 빠르게 제품 구조를 보여줄 수 있다.
- 왜 실패할 수 있는가: 잘못 구현하면 generic SaaS 요약 카드 영역처럼 보일 수 있다.
- 동종 레퍼런스: category 안에서 utility와 hierarchy 균형이 좋은 화면을 붙인다.
- 이종 레퍼런스: 다른 category에서 정보 요약을 잘 압축한 화면을 붙인다.

## 선택 방향

- 선택한 방향: A 또는 B
- 선택 이유: 사용자 행동, 브랜드 의도, 차별화, 반응형 안정성 기준으로 적는다.
- 버린 방향의 이유: 왜 구조적으로 덜 강했는지 적는다.

## 레이아웃 테제

- 예: “한 화면에 하나의 행동만 남기고, 나머지 utility는 신뢰 형성 뒤에 펼치는 editorial landing 구조.”

## generic 회피 선언

- 피할 구조 1: interchangeable centered gradient hero
- 피할 구조 2: generic 3-column feature card grid
- 피할 구조 3: dashboard card noise above the fold
- 왜 이 화면이 generic하지 않은가: 구성이 category 평균과 어디서 달라지는지 적는다.
