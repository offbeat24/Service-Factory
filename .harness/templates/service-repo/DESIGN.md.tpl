---
name: {{SERVICE_NAME}}
colors:
  primary: "{{DESIGN_PRIMARY_COLOR}}"
  accent: "{{DESIGN_ACCENT_COLOR}}"
  background: "{{DESIGN_BACKGROUND_COLOR}}"
  surface: "{{DESIGN_SURFACE_COLOR}}"
  text: "{{DESIGN_TEXT_COLOR}}"
typography:
  korean:
    fontFamily: "{{DESIGN_KOREAN_FONT}}"
  english:
    fontFamily: "{{DESIGN_ENGLISH_FONT}}"
rounded:
  sm: 8px
  md: 16px
spacing:
  sm: 8px
  md: 16px
motion:
  style: "{{DESIGN_MOTION_STYLE}}"
  emphasis: "{{DESIGN_MOTION_EMPHASIS}}"
---

# DESIGN.md

## Overview

- This file is the authoritative visual spec for `{{SERVICE_NAME}}`.
- Agents should read this file before generating UI, then use `docs/design/*.kr.md` as the deeper rationale and review layer.
- The product should feel `{{DESIGN_TONE}}` and follow a `{{DESIGN_VISUAL_DIRECTION}}` direction.

## Brand Voice

- Keywords:
{{DESIGN_KEYWORDS_BULLETS}}
- Selected DESIGN.md reference:
{{SELECTED_DESIGN_REFERENCE_BULLETS}}
- Narrative: the interface should make the primary action feel inevitable, calm, and decisive instead of playful or noisy.
- Principles:
  - one dominant action per screen
  - strong hierarchy before utility density
  - specific brand cues instead of generic AI SaaS defaults

## Color Palette

{{DESIGN_PALETTE_BULLETS}}

## Typography

{{DESIGN_TYPOGRAPHY_BULLETS}}

## Layout Principles

{{DESIGN_LAYOUT_PRINCIPLES_BULLETS}}

## Component Styling

{{DESIGN_COMPONENT_RULES_BULLETS}}

## Motion

{{DESIGN_MOTION_BULLETS}}

## Imagery

{{DESIGN_IMAGERY_BULLETS}}

## Do / Don't

### Do

- Make the first screen clearly owned by one primary action.
- Use spacing, typography, and surface rhythm to create hierarchy before adding borders or decoration.
- Preserve the same thesis from desktop to mobile instead of shrinking the desktop layout blindly.

### Don't

{{DESIGN_ANTI_REFERENCES_BULLETS}}

## Agent Guidance

- Read order for UI work: `AGENTS.md` -> `DESIGN.md` -> `service.yaml` -> `docs/prompting/prompt-context.kr.md` -> relevant design docs.
- Treat `DESIGN.md` as the compact design source of truth.
- Use `docs/design/art-direction.kr.md` for references, anti-patterns, and asset strategy.
- Use `docs/design/ui-principles.kr.md` for layout, component, responsive, and implementation rules.
- For `ui-foundation` and `ui-new-screen`, complete `ui-intent-brief`, `layout-exploration`, and `visual-concepts` before code.
