# Learner profile

Read this at the start of every coaching turn. Patch only the section that changed.

## Identity

- Returning Flutter and Dart mobile developer.
- About 1.5 years away from Flutter.
- Goal: recollect and retain, not get apps written for them.
- Materials: supplied by the learner over time. Academind object lecture ingested 2026-09-30.

## Baseline

- No notes, docs, or code pasted yet. (2026-09-25)
- Treat prior production experience as real. Do not invent a syllabus until materials arrive or a retrieval shows a gap.
- 2026-09-30: Academind "Configuring Widgets & Understanding Objects" (7:24). Scaffold background is the example. The idea is that every value is an object, a widget is one kind, and it is configured by another object such as Color. Next lecture transcript is context only: non-widget configuration objects (BoxDecoration, LinearGradient).
- 2026-10-13: Academind lectures from "Onwards to Custom Widgets: Why Do You Need Them?" through "Practice: Reusable Widgets & Constructor Functions". Arc: extract trees into classes that extend StatelessWidget, constructors/`super.key`/`const`, split files, variables/`final`/`const`, then instance fields so StyledText and GradientContainer accept data from outside.
- 2026-10-13: Flutter book library extracted to `Interview Prep/books/flutter resources/` (Flutter Zero MD, F100 HTML→MD, PDF text layers). Teacher system + reviewer live under `flutter resources/teacher/`. CoVet interview on 2026-10-22; prioritize JD gaps (Firebase/Firestore/Cloud Functions conceptual fluency) without inventing production ownership.
- 2026-10-15: CoVet fast-track teacher sprint started. Module 1 = Widget → Element → RenderObject + rebuild/keys. Cleaned library + mock handoff are the source of truth.
- 2026-10-16: Skill folder was missing on disk and restored from the 2026-10-15 session. No teaching-rule change.

## Concept map

### Mastered

- None. Mastered requires two closed-book retrievals, ideally on different days.

### Shaky

- When `build()` runs, and what may run inside it. Recalled `setState` as the UI update. Missed that `setState` marks that `State` dirty after the field changes, and that `build()` only describes widgets. (2026-09-25)
- Widget object vs configuration object. Has `Scaffold`, `backgroundColor`, and `Color`, and that `Scaffold` reads channels from the `Color` object. Placed the ARGB numbers on `backgroundColor`, then on `Color.fromARGB`. Those numbers live on the `Color` object the constructor returns. (2026-09-30)
- Widget / Element / RenderObject. One clean retrieval (2026-10-15 PM): dirty Element → new Widget configs → reuse Element when type+key match → RO update if needed. Not mastered (need second day).
- Keys vs State (2026-10-15): (a) reuse Element/State — clean. (b) hedged "updated state"; correct is dispose old State + create new. Mark shaky until one clean unhedged retrieval.

### Unknown

- Async: `Future` vs `Stream`, and where work belongs off the widget. Retry policy in plain words landed (2026-10-17): signal drop → send again; bad id → error, do not resend; expired login → one silent sign-in, then the same request; dialog and login screen only if that sign-in fails. Not mastered.
- State: UI state vs a repository as the single source of truth.
- Routing: declarative route tree vs imperative `Navigator` pushes.

### In progress (CoVet fast track)

- Layout: constraints down, sizes up, parent sets position (RenderObject-level). Clean retrieval + teach-back (2026-10-15). Row overflow story mostly right; nuance: Row is usually bounded, then passes unbounded max width to non-flex children. Not mastered (need day-2).
- State judgment: BLoC on AINA vs Provider+GetIt on NM Stock. Clean retrieval + teach-back + Test (2026-10-15 late): camera/ID named states vs NM list/detail notifier. One retrieval logged, not mastered.
- Everyday resend (2026-10-16): words fine + signal dropped → press resend. One clean answer. Not the status-code policy. Not mastered.

## Mistake log

- 2026-10-18: Module 5. Did not remember an AINA test. Then said he did not write the FAQ or username tests himself; Cursor drafted them by copying other developers' tests. Honest claim: commits are his, authorship of the design is not. Do not coach him to say he wrote the suite by hand.
- 2026-10-17: Login-expired case. Went straight to a dialog and the login screen. Missed the one silent sign-in attempt first. Dialog + login is only after that attempt fails.
- 2026-10-16: Authenticated REST retry. Said clueless, then said the follow-up lecture was too advanced to follow. Later still did not know what "retry" meant. Gap is the word: send the same request again.
- 2026-10-16: Texting hint missed. Could not say when to press send again versus change the words. Gap is that everyday split, still before status codes.
- 2026-10-15: Keys test. Answered Element reuse/create; skipped State preserve vs dispose/recreate.
- 2026-10-15: W/E/RO retrieval. Named Element dirty from `setState` but skipped Widget (config) and RenderObject (layout/paint) jobs, and Element reuse when type+key match.
- 2026-09-25: `build()` / `setState`. Placed the name assignment in `build()` and treated `setState` as the thing that paints. The assignment belongs in the `setState` callback. `setState` then schedules a rebuild through `Element.markNeedsBuild` (`Element._dirty`). It does not paint. Also missed that `build()` only returns widgets.
- 2026-09-30: Configuring widgets / objects. Answer was "color." That names the object that stores the data. It leaves out the `Scaffold` widget object and the handoff: `Scaffold` reads the `Color` object's stored values when it paints.
- 2026-09-30: Teach-back revision. Asked if `Color.fromARGB` is what stores the four numbers. `Color.fromARGB` is a constructor that builds a `Color`. The numbers are stored on the `Color` object it returns.

## Method that works for me

- 2026-09-25: Reviews need mechanism in numbered steps, one short snippet, and a boundary table when the concept has an inside/outside rule. A one-paragraph correction is too thin. Still one concept, then teach-back, with no sample answer to paste. Short drills, no full solutions.
- 2026-09-30: Numbered steps and a boundary table in a Review do not land on the first read. Explain in connected prose, three layers (what they already have, the missing link, one deeper mechanism), with each important term highlighted inside the sentence. One snippet when the material had code, then one closing sentence that deepens the same idea. A table only for an inside/outside rule. Retrieval, one concept, and teach-back stay.
- 2026-09-30: After a miss, another withheld question made the idea harder. When they ask for the answer, give that one sentence plainly.

## Next assignment

- 2026-10-18: Teach-back the honest AINA test sentence: what he added, and what he will not claim.
