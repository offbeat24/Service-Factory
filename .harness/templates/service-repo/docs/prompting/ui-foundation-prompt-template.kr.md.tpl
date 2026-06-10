# UI 파운데이션 프롬프트 템플릿

## 목적

- 이 템플릿은 첫 랜딩, 첫 대시보드, 핵심 신규 화면처럼 구조와 비주얼 언어를 먼저 결정해야 하는 UI 작업에 쓴다.
- 코드 구현보다 앞서 intent brief, layout exploration, visual concepts, concept-image plan을 고정하게 만드는 것이 목적이다.

## 사용 방법

- `ui-foundation` 또는 `ui-new-screen` task에서 사용한다.
- 구현 전에 최소 2개의 구조 방향과 2개의 비주얼 컨셉을 비교한 뒤 하나를 선택한다.
- 같은 category reference와 cross-category reference를 모두 포함한다.
- concept image 경로와 anti-reference를 함께 적지 않으면 완료로 보지 않는다.

## 프롬프트 템플릿

```text
다음 문서를 먼저 읽고 그 기준 안에서만 작업한다.
- docs/prompting/prompt-context.kr.md
- docs/design/art-direction.kr.md
- docs/design/ui-intent-brief.kr.md
- docs/design/layout-exploration.kr.md
- docs/design/visual-concepts.kr.md
- docs/design/ui-principles.kr.md
- docs/design/browser-review.kr.md

이번 작업의 분류:
- [ui-foundation 또는 ui-new-screen]

대상 화면:
- [화면 또는 플로우 첫 장면]

primary user action:
- [이 화면이 가장 먼저 유도해야 할 행동 1개]

구조 방향 비교:
- 방향 A: [구조 요약]
- 방향 B: [구조 요약]

비주얼 컨셉 비교:
- 컨셉 A: [비주얼 요약]
- 컨셉 B: [비주얼 요약]

선택한 layout thesis:
- [한 문장]

선택한 visual thesis:
- [한 문장]

왜 이 화면이 generic하지 않은가:
- [category 평균과 구조적으로 다른 점]

반드시 피할 패턴:
- [anti-pattern 1]
- [anti-pattern 2]
- [anti-pattern 3]

reference 요구:
- same-category reference 1개 이상
- cross-category reference 1개 이상
- anti-reference 1개 이상
- concept image 또는 board 2개 이상
- 선택안 mobile adaptation image 1개

구현 요구:
- concept image의 계층, 간격, 표면 처리, CTA 강조를 최대한 보존한다.
- 코드는 chosen thesis를 실행하는 수단으로만 사용한다.

검증 요구:
- desktop/mobile first-view screenshot
- concept 대비 구현 차이 메모
- thesis 유지 여부 판정
- layout-stable / layout-drifting / layout-failed 분류

응답 형식:
1. 선택한 방향과 근거
2. 구현에 남겨야 할 핵심 시각 규칙
3. 위험 요소
4. 브라우저 검증 포인트
```
