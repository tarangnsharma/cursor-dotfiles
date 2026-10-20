---
name: Guide Viewer UX Overhaul
overview: "Redesign the guide viewer into a hybrid reading experience: calm, highly legible core with selective premium visual accents, while keeping source meaning unchanged and improving representation of Mental Model text."
todos:
  - id: baseline-reset
    content: Redesign base layout and typography to a calmer reading-first baseline.
    status: completed
  - id: mental-model-system
    content: Implement low-noise Mental Model cards with render-time separator and line-chunk normalization.
    status: completed
  - id: representation-layer
    content: Add source-preserving render transforms to reduce visual bold/emphasis overload.
    status: completed
  - id: premium-accents
    content: Apply selective premium visual accents without harming readability.
    status: completed
  - id: navigation-ergonomics
    content: Refine focus mode, TOC docking/collapse behavior, and question-jump affordances.
    status: completed
  - id: qa-a11y-perf
    content: Run readability, accessibility, and performance validation across desktop/mobile states.
    status: completed
isProject: false
---

# Phased UI/UX Upgrade Plan

## Outcomes

- Make the viewer feel calm and premium at the same time (hybrid direction).
- Reduce cognitive load in scanning and long-form reading.
- Improve Mental Model readability without changing conceptual meaning.
- Remove visual harshness from em dashes and heavy inline emphasis through presentation-layer formatting.

## In-Scope Files

- Viewer logic: [c:\Users\trngs\Desktop\tarangnsharma\Interview Prep\Senior Flutter Interview Prep\guide-viewer\src\main.ts](c:/Users/trngs/Desktop/tarangnsharma/Interview%20Prep/Senior%20Flutter%20Interview%20Prep/guide-viewer/src/main.ts)
- Viewer styling: [c:\Users\trngs\Desktop\tarangnsharma\Interview Prep\Senior Flutter Interview Prep\guide-viewer\src\style.css](c:/Users/trngs/Desktop/tarangnsharma/Interview%20Prep/Senior%20Flutter%20Interview%20Prep/guide-viewer/src/style.css)
- Source markdown (read-only for structure awareness; no meaning changes): [c:\Users\trngs\Desktop\tarangnsharma\Interview Prep\Senior Flutter Interview Prep\Flutter-Senior-Interview-Rancho-Guide.md](c:/Users/trngs/Desktop/tarangnsharma/Interview%20Prep/Senior%20Flutter%20Interview%20Prep/Flutter-Senior-Interview-Rancho-Guide.md)

## Phase 1: Visual Baseline Reset (Calm Core)

- Simplify top header and controls into a quieter utility bar (priority controls first, secondary controls tucked into a compact menu).
- Rebalance page proportions: wider breathing margin, narrower reading column, subtler card borders/shadows.
- Normalize typography scale:
  - reduce heading weight spikes,
  - increase paragraph readability via consistent measure/line-height,
  - reduce bold intensity in body rendering.
- Rework TOC text density and spacing for scannability (shorter labels, better active-state contrast).

## Phase 2: Mental Model Readability System

- Keep Mental Model optional but redesign as low-noise “insight cards” with cleaner disclosure UI.
- Add presentation-layer text smoothing for Mental Model blocks only:
  - render-time substitution of em dash (`—`) to gentler separators (e.g., punctuation + spacing) without changing source meaning,
  - sentence-group line chunking to avoid long dense paragraphs and improve scan flow.
- Add alternate “Expanded prose” toggle for users who prefer uninterrupted paragraph mode.

## Phase 3: Content Representation Layer (No Meaning Change)

- Introduce renderer transforms (DOM-level, post-markdown render):
  - soften excessive inline emphasis by reducing visual dominance (font-weight/color),
  - maintain semantic emphasis but prevent bold-heavy wall-of-text.
- Add paragraph rhythm helpers:
  - max sentence group length per visual block,
  - consistent spacing between conceptual units.
- Ensure transforms are scoped and reversible (feature flags/classes), preserving original markdown source.

## Phase 4: Hybrid Premium Accents (Selective)

- Add restrained premium cues inspired by modern showcase sites:
  - subtle gradient progress indicator,
  - cleaner section dividers and chips,
  - refined motion for TOC/focus transitions.
- Avoid heavy hero dominance; prioritize reading over spectacle.

## Phase 5: Interaction and Navigation Ergonomics

- Improve focus mode into true “rehearsal mode”:
  - clear active question framing,
  - unobtrusive next/prev affordances,
  - visible shortcut hints.
- Enhance TOC collapse behavior with better left-edge docking and re-open discoverability.
- Add “jump back to current question” anchor when users scroll deep.

## Phase 6: QA, Accessibility, and Performance

- Validate readability on long sessions (desktop first, then responsive).
- Accessibility pass:
  - heading hierarchy,
  - keyboard reachability,
  - contrast targets,
  - reduced-motion compatibility.
- Performance pass:
  - keep interactions responsive with large markdown,
  - avoid layout jank from runtime transforms.

## Delivery Strategy

- Implement in small vertical slices and evaluate after each phase before moving forward.
- Keep each phase behind clear class/feature boundaries to allow quick rollback of any visual experiment.

```mermaid
flowchart TD
    currentUI[CurrentViewerUI] --> phase1[Phase1CalmBaseline]
    phase1 --> phase2[Phase2MentalModelSystem]
    phase2 --> phase3[Phase3RenderNormalization]
    phase3 --> phase4[Phase4PremiumAccents]
    phase4 --> phase5[Phase5NavigationErgonomics]
    phase5 --> phase6[Phase6QAandA11y]
    phase6 --> targetUI[ReadableHybridPremiumUI]
```
