# UI 원칙

## 레이아웃 원칙

{{DESIGN_LAYOUT_PRINCIPLES_BULLETS}}

## 첫 화면 구성 규칙

- 첫 화면은 한 개의 primary action이 소유한다.
- headline, supporting proof, CTA의 순서를 흐리지 않는다.
- utility를 너무 빨리 끌어올려 첫 인상을 평평하게 만들지 않는다.

## 밀도 상승 규칙

- 첫 화면 직후에만 밀도를 한 단계 올린다.
- 카드나 표는 필요할 때만 쓰고, 정보량이 늘어날수록 구획 리듬도 함께 강화한다.
- density는 시각적 긴장을 올리기 위한 수단이지, 안전한 채우기 수단이 아니다.

## 데스크톱에서 모바일로의 번역 규칙

- 모바일에서는 같은 thesis를 더 긴 세로 흐름으로 번역한다.
- 데스크톱의 병렬 구성을 단순 shrink하지 말고, 우선순위를 다시 세운다.
- mobile first-view에서도 primary action이 즉시 보여야 한다.

## 섹션 시퀀싱 규칙

- 섹션은 가치 제안 -> 핵심 행동 -> 신뢰 -> 세부 utility 순서로 읽히게 구성한다.
- 예외가 필요하면 왜 그 순서를 어기는지 brief나 exploration 문서에 적는다.

## 리듬과 여백 규칙

- 큰 여백은 hierarchy payoff가 있을 때만 허용한다.
- 섹션 간 간격은 headline 크기와 proof 밀도에 맞춰 차등을 둔다.
- 여백만 늘리고 구조는 평범한 상태를 개선으로 보지 않는다.

## 컴포넌트 규칙

{{DESIGN_COMPONENT_RULES_BULLETS}}

## 컴포넌트 반복 제한

- 같은 형태의 카드, badge, panel을 무의미하게 반복하지 않는다.
- component repetition이 정보 구조를 대체하기 시작하면 레이아웃을 다시 점검한다.

## 모션 원칙

{{DESIGN_MOTION_BULLETS}}

## 반응형 규칙

- 모바일에서는 정보량보다 흐름 우선으로 배치한다.
- 데스크톱에서는 밀도를 올리기보다 여백과 계층을 확장한다.
- 첫 화면에는 가장 중요한 행동 하나만 우선 노출한다.

## 디자인 구현 절차

- 웹 UI 작업은 먼저 Codex가 비주얼 초안 이미지를 만들고 그 결과를 기준으로 구현한다.
- 구현 결과가 초안과 달라져야 할 때는 사용자 가치, 접근성, 반응형 제약 중 무엇 때문인지 기록한다.
- 필요한 경우 생성 이미지를 실제 UI 자산으로 쓰되, 텍스트 가독성과 성능을 브라우저에서 확인한다.
- 폰트는 국문 Pretendard, 영문 Inter를 기본값으로 두고, 테마 예외가 있으면 `docs/design/art-direction.kr.md`의 타이포그래피 정책에 근거를 남긴다.

## 수정 작업 규율

- 부분 수정 요청에서는 레이아웃 전면 재구성, 불필요한 비주얼 리브랜딩, 대규모 컴포넌트 교체를 기본값으로 금지한다.
- 수정 범위는 `docs/design/ui-edit-brief.kr.md` 또는 현재 task 문서에 명시된 화면, 섹션, 요소 단위로 고정한다.
- 한 번의 수정에서는 한 화면, 한 의도, 한 검증 루프를 우선한다.
- 변경 전 반드시 무엇을 유지할지, 무엇을 바꿀지, 무엇을 건드리지 말아야 할지 먼저 적는다.
- 사용성 후퇴를 허용하지 않는다. 클릭 경로 증가, 정보 계층 약화, 가독성 저하, 모바일 오버플로, CTA 발견성 저하가 생기면 수정안을 다시 좁힌다.
- "더 좋아 보이게" 같은 추상 목표보다 요청 반영 여부와 부작용 여부를 분리해 판단한다.

## 디테일 폴리시 전환 기준

- chosen layout thesis와 visual thesis가 데스크톱/모바일 첫 화면에서 모두 읽히면 구조 변경을 멈춘다.
- 이후 반복은 spacing, typography, emphasis, motion, responsive tuning 중심으로 제한한다.
- browser review가 `layout-stable`이 아닌데도 detail polish로 넘어가면 안 된다.

## 디자인 evidence 체크

- 비주얼 초안 이미지 또는 생성 프롬프트 경로
- 선택한 layout thesis와 visual thesis
- UI 수정 전 기준 스크린샷
- 모바일 첫 화면 스크린샷
- 데스크톱 첫 화면 스크린샷
- 초안 대비 구현 차이 메모
- why this is not generic 메모
- 요청 반영 여부 메모
- 사용성 부작용 여부 메모
- CTA 계층과 여백 일관성 메모
- 국문 Pretendard, 영문 Inter 적용 또는 타이포그래피 예외 근거
- 명확한 금지 패턴 회피 여부 확인
- 실제 브라우저 점검 루프는 `docs/design/browser-review.kr.md`를 따르며 기능 검토도 함께 수행한다.
