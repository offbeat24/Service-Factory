# UI 수정 프롬프트 템플릿

## 목적

- 이 템플릿은 UI 수정 요청을 넓은 재해석이 아니라 좁은 변경으로 유도하기 위한 작업용 프롬프트 틀이다.
- 프롬프트만으로 통제하지 않고, `docs/design/design-reference-selection.kr.md`, `docs/design/ui-edit-brief.kr.md`, `docs/design/browser-review.kr.md`, `docs/prompting/prompt-context.kr.md`와 함께 사용한다.
- 새 화면, 랜딩, 첫 대시보드, 구조 재설계 작업에는 이 템플릿 대신 `docs/prompting/ui-foundation-prompt-template.kr.md`를 사용한다.

## 사용 방법

- 한 번에 한 화면 또는 한 플로우만 대상으로 쓴다.
- 프롬프트를 보내기 전에 brief와 기준 스크린샷을 먼저 준비한다.
- "개선"보다 "유지 범위와 변경 범위를 좁게 지키기"를 우선한다.
- 디자인 방향을 실질적으로 바꾸는 수정이면 먼저 `oh-my-design`와 `getdesign.md` 후보를 다시 비교하고 선택 근거를 갱신한다.
- 응답 결과는 바로 완료 처리하지 말고 브라우저 비교 evidence로 다시 판단한다.

## 프롬프트 템플릿

```text
다음 문서를 먼저 읽고 그 기준 안에서만 수정한다.
- docs/prompting/prompt-context.kr.md
- docs/design/art-direction.kr.md
- docs/design/design-reference-selection.kr.md
- docs/design/ui-principles.kr.md
- docs/design/browser-review.kr.md
- docs/design/ui-edit-brief.kr.md

이번 수정의 목표:
- [한 문장으로 현재 수정 목표]

이번 수정에서 유지할 것:
- [유지할 레이아웃, 카피, 컴포넌트, 브랜드 요소]

이번 수정에서 바꿀 것:
- [간격, 타이포, CTA 강조도, 특정 섹션 등]

이번 수정에서 금지할 것:
- [전면 재구성, 새 섹션 추가, 정보 구조 변경 등]

이번 수정에서 유지해야 할 layout thesis 또는 visual thesis:
- [현재 화면이 이미 가진 구조적 강점]

작업 단위 제한:
- 한 화면, 한 의도, 한 검증 루프로만 진행한다.
- 요청 범위를 벗어나는 재해석은 하지 않는다.

검증 요구:
- 변경 전후 같은 화면을 비교할 수 있게 만든다.
- 요청 반영 여부와 사용성 부작용 여부를 따로 점검한다.
- 모바일 오버플로, 가독성 저하, CTA 발견성 저하가 생기면 실패로 본다.

응답 형식:
1. 변경 범위
2. 예상 영향
3. 검증 포인트
```
