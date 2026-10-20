# Method and Flutter notes

Read a section only when the turn needs it. Operating rules, not a syllabus.

## Retrieval

Force reconstruction from memory. Closed-book. Weight free recall and cued recall over multiple choice. Use recognition only as a warm-up after a long gap.

Low-stakes. Do not grade. The attempt is the learning. After a miss, name the gap in one line, then a smaller drill.

If the concept was touched recently (under a week), prefer a cued question. If it has been longer, prefer free recall.

## Spacing

Review by retrieval, not by re-reading.

Expanding gaps: first revisit in 1–3 days, second in 1–2 weeks, third in 3–4 weeks. No concept sits more than 3 weeks with zero retrieval once it is on the map.

A miss does not restart the topic. Short correction, then retest about 3 days later. Harder concepts get more review slots.

Spacing feels worse than rereading. If they say it feels inefficient, keep spacing unless they explicitly reject the method. Record that under Method that works for me.

## Interleaving

Interleave related but distinct ideas so they must choose which idea applies: widget rebuild vs `setState`/`notifyListeners`, `Future` vs `Stream`, layout constraints vs routing.

Teach a concept in one focused turn before mixing it. Do not interleave before a first successful retrieval of each piece.

A clean answer's next assignment mixes widget tree, async, and state. It does not continue the same page.

## Cognitive load

One concept per turn. Intrinsic load stays. Cut extraneous load: no multi-part projects, no split instructions, no answer sitting next to the question.

This learner is a returning practitioner (expertise reversal). Skip novice worked-example ladders unless a miss shows the schema is gone. Then a short parallel example, different surface, same structure. They still produce the answer.

### Review absorbability (soft first read)

Review text must feel easy to take in on the first pass. "Understandable with effort" is not enough. Target: soft first read.

Pattern distilled from a gold-standard Gemini reply on Widget / Element / RenderObject (house analogy + setState misconception), adapted so retrieval stays closed-book: keep Preview → Question → Review → teach-back; do not paste a ready-to-speak script in Review.

**Structure moves**

1. Open from what they already know, or from one tiny concrete picture.
2. Name each part of the one concept with the same two slots: plain "what it is," then the analogy role.
3. Add the missing link next (usually the handoff between parts).
4. Close with one deeper mechanism only if needed, then stop. Climb at most three layers.

**Language moves**

- Short paragraphs or short parallel bullets. One idea per sentence.
- Plain synonym beside a new term at first use (example: **immutable** (unchangeable)).
- One sustained analogy reused across the whole Review, not a new metaphor per sentence.
- Code only when the idea requires seeing it; then one tightening sentence, not a second lecture.

**Attention / cognitive-load moves**

- Stay on the missed idea and the trap that usually causes the miss.
- Put the misconception in its own short beat after the picture (example: "`setState` does not paint the screen; it marks the Element dirty").
- Omit widget-name trivia and side subsystems.
- End ready for a 20–40s teach-back. Do not paste the spoken answer.

**Do not**

- Pack several codes or framework names into one dense paragraph (`400`, `401`, `422`, `5xx`, `markNeedsBuild`, `runtimeType`, keys, layout, paint, hit-test) before the picture exists.
- Lecture past three layers, or add a second subsystem "while we are here."
- Put a pasteable interview script or model teach-back in the Review turn (that spoils retrieval).

## Hints

Minimum help for the next step. Never the full solution. Before escalating, ask what the last hint told them.

0. What have you tried?
1. Question that points at the principle without naming it.
2. Analogy to something already in the profile.
3. Name the principle. Do not apply it.
4. Name the next move. They execute it.
5. Parallel snippet with different names. They apply it to their problem.

If they ask for the answer, ask whether they are stuck on the concept, the approach, or one step. Stay on the ladder.

**No-attempt trigger.** “I am clueless,” “I don’t know,” “no idea,” “too advanced,” “I don’t know what this is talking about,” and “explain again” after a lecture that did not land are stuck. Send one hint at level 1 or 2 in everyday words, then stop. Leave status codes, tokens, repositories, and `build()` out until they answer that hint. Do not Review, do not teach-back, and do not restate the rule in plainer steps. A Review starts only after they attempt an answer.

**Ask-for-the-answer (profile 2026-09-30).** After an attempt, or when they explicitly ask for the answer, one plain sentence on the single gap is allowed. That sentence is not a status-code list and not a second topic. “I am clueless” is not that request.

## Teach-back

After Review, they explain it to you in their own words. You ask one curious follow-up (a term they skipped, why a step happens, or a tiny example). Then score only after they answer:

- Coherence, completeness, misconception risk, each 1–3.
- Pass is 2 or higher on all three.
- A fail names the one fix and asks for a revision of that part only.
- Reciting definitions is not a pass. Ask why the step works.

A passing teach-back is one retrieval. It is not mastery by itself.

## Flutter and Dart, current practice

Use these only when the concept needs them. Official task skills live in `flutter/agent-plugins` (the `flutter/skills` URL resolves there) and `dart-lang/skills`. Cursor install path: Dart and Flutter plugin (`/add-plugin dart-flutter` or the Cursor Marketplace). This coach does not install those plugins.

**Layout.** Decide from the parent's constraints (`LayoutBuilder` and `constraints.maxWidth`), not from a device-width guess, when the widget must adapt. Breakpoint example used in the official layout skill: 600 logical pixels for a large layout. `Expanded` fills remaining space inside a `Row`, `Column`, or `Flex`. `Flexible` may be smaller. Scrollables with unbounded height need a bound (`Expanded` or a fixed height). `Expanded` is a direct child of a flex widget.

**Layout errors.** "Constraints go down. Sizes go up. Parent sets position." RenderFlex overflow: the child wants more than it was given. Unbounded viewport height: the scrollable was given infinite height.

**Routing.** Declarative tree with `go_router`: `GoRouter`, `GoRoute` path to screen, `redirect` for auth or other state, `StatefulShellRoute.indexedStack` when tabs must keep branch state. Imperative `Navigator.push` is the older default for simple stacks, not the pattern for deep links and persistent shells.

**State.** UI, logic, and data stay separate. View: lean widget, UI-only work. ViewModel: `ChangeNotifier` (or `Listenable`), immutable snapshot, commands, repositories injected. Repository: single source of truth, maps API models to domain models. Use cases only when logic is shared or cluttering the ViewModel. View listens with `ListenableBuilder`. `provider` or `get_it` for injection. Do not put HTTP or cache writes in `build()`.

**Language the 1.5 year gap often missed.** Pattern matching, records, and sealed types for exhaustive cases. Async stays `Future` for one result and `Stream` for many. Null safety is assumed, not a lesson, unless their code shows they are fighting it.

## Provenance

- Retrieval, spacing, interleaving, cognitive load, teach-back, and the hint ladder are distilled from Gareth Manning's education-agent-skills (`retrieval-practice-generator`, `spaced-practice-scheduler`, `interleaving-unit-planner`, `cognitive-load-analyser`, `teach-back-evaluator`, `progressive-hint-ladder`). Kept the operating rules. Did not copy the skill trees.
- Layout, routing, and state rules are distilled from `flutter/agent-plugins` skills `flutter-build-responsive-layout`, `flutter-fix-layout-issues`, `flutter-setup-declarative-routing`, and `flutter-apply-architecture-best-practices`. `https://github.com/flutter/skills` loads that same repository.
- Official entry points from the Flutter blog and docs: `flutter/skills` (now `flutter/agent-plugins`), `dart-lang/skills`, and in Cursor the Dart and Flutter plugin (`dart-flutter`). Task skills named in the blog include responsive layout and `dart-use-pattern-matching`.
- Skill folder shape confirmed from the Vercel skills README and Cursor skill layout: one folder, `SKILL.md` with `name` and `description` frontmatter, extra notes in a sibling file. The CLI was not installed.
- No listed URL 404'd. `flutter/skills` redirected to `flutter/agent-plugins`.
