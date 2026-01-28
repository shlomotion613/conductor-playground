# Pacing Calendar: One-Page Spec

## The Problem in Two Sentences

1. **Create quickly**: I want to import my school calendar, teaching schedule, and curriculum instead of typing everything into a spreadsheet.
2. **Edit quickly**: When a snow day hits, a lesson runs long, or I skip ahead, I want to shift all affected lessons with one click instead of manually moving every cell.

---

## User

**Amalia**: High school biology teacher. Teaches 4 different curricula for 4 different grades. No clerk. Two young kids. Uses Google Docs and Excel but not a power user.

---

## The Thin Vertical Slice

**One user**: Amalia (or any teacher managing multiple curricula)
**One dataset**: School calendar + teaching schedule + lesson sequences for each curriculum
**One workflow**: Import → Adjust → Export
**One output**: Spreadsheet (CSV/Excel) she can print or import elsewhere

---

## Three-Phase Workflow

### Phase 1: Import
- Upload school district calendar PDF → extract holidays and non-school days
- Set teaching schedule per curriculum (e.g., "Grade 9 Bio meets Mon/Wed")
- Import curriculum/lesson list from document OR enter manually

### Phase 2: Adjust
- View calendar with lessons mapped to teaching days
- When disruption happens: click a date → shift lessons forward (snow day, lesson ran long, etc.)
- Skip a lesson → remove it and cascade
- Reorder lessons via drag-and-drop
- **Adjust one curriculum at a time** (switch between 4 curricula in one app)

### Phase 3: Export
- Export to spreadsheet (CSV/Excel) for printing or further editing
- Export to calendar app (.ics for Google Calendar, Apple Calendar, Outlook)

---

## What We Are Building

**Import:**
- District calendar PDF import: drag-and-drop to extract holidays and non-school days
- Teaching schedule per curriculum: which days of the week each class meets
- Curriculum import from document (PDF/Word/spreadsheet) with manual fallback
- Support for 4 curricula in one app instance (switchable)

**Adjust:**
- Calendar view that auto-maps lessons to teaching days
- Shift lessons forward from any date (snow day, lesson ran over, etc.)
- Skip/remove a lesson and cascade remaining lessons
- Change lesson duration (1 day → 2 days) and cascade
- Drag-and-drop reordering of lessons
- Undo/redo for adjustments

**Export:**
- Export to CSV/Excel spreadsheet
- Export to calendar app (.ics file for Google Calendar, Apple Calendar, Outlook)

---

## What We Are NOT Building

- No user accounts or login
- No cloud sync or persistence beyond local storage
- No LMS integration (Google Classroom, Canvas)
- No resource attachments or links per lesson
- No mobile app
- No collaboration or sharing
- No "where did I actually end up" tracking
- No notifications or reminders
- No agentic anything
- No partial day types (half-days, delayed openings) in V1

---

## Data

**Input:**
- District calendar PDF (holidays, breaks, non-school days)
- Teaching schedule per curriculum (days of week)
- Curriculum document (PDF/Word/spreadsheet) OR manual lesson entry
- Lesson list per curriculum (title, optional aim, duration)

**Storage:** Browser localStorage (no backend)
- 4 curricula with their schedules and lessons
- School calendar (shared across curricula)
- Export/import as JSON for backup

**Output:** CSV/Excel spreadsheet, .ics calendar file

---

## Week-by-Week Plan

**Week 1: Spec + Skeleton**
- Finalize this spec
- Repo + deploy target (Vercel)
- Hello World React app live
- Research PDF parsing libraries (pdf.js, pdf-lib)
- Research document parsing for curriculum import
- Decide: localStorage schema for multiple curricula

**Week 2: Import Phase**
- Build drag-and-drop PDF upload for school calendar
- Parse PDF to extract holidays and date ranges
- Build teaching schedule UI (select days per curriculum)
- Build curriculum import (parse document OR manual entry)
- Support switching between 4 curricula
- Manual QA: Test with 3-4 different district calendar PDFs

**Week 3: Adjust Phase**
- Build calendar grid view (lessons mapped to dates)
- "Shift from here" functionality (forward cascade)
- Skip/remove lesson with cascade
- Lesson duration changes with cascade
- Undo/redo for all adjustments

**Week 4: Polish Adjust + Reorder**
- Drag-and-drop reordering for lessons
- Handle edge case: lessons exceed term end date (warning)
- Validation: term dates, lesson titles, reasonable limits
- Linter/formatter; small commits

**Week 5: Export + Backup**
- CSV/Excel export
- .ics calendar export (Google Calendar, Apple Calendar, Outlook)
- JSON export/import for backup
- localStorage persistence (survives refresh)
- Error handling: empty states, edge cases
- Basic CI (lint + tests)

**Week 6: Tests + Demo**
- Unit tests: cascade math, date mapping
- Integration test: full flow
- User test with 1-2 teachers
- Demo: import → adjust → export in < 2 minutes

---

## Success Criteria

1. **Import < 5 minutes**: Upload district PDF, set teaching days, import or enter curriculum
2. **Adjust < 5 seconds**: Click one date → shift lessons → done
3. **She actually uses it**: Replaces the Google Doc she abandons every term
4. **Exportable output**: Spreadsheet she can print, or .ics she can import to her calendar app

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Scope creep into "platform" | Non-goals list is law. |
| District calendar PDFs vary wildly | Start with text-based PDFs. Show preview before applying. Manual entry fallback. Target 80% success. |
| Curriculum documents vary wildly | Same approach: preview, edit, manual fallback. |
| localStorage is fragile | JSON export/import for backup. Prominent "Download backup" button. |
| 4 curricula is complex | Start with 1, add multi-curriculum support in Week 2. |
| Lessons exceed term end | Show warning with count of overflow lessons. |

---

## What "Done" Looks Like

Amalia opens the app. She drags in her district calendar PDF and confirms the extracted holidays. She creates 4 curricula: Grade 9 Bio (Mon/Wed), Grade 10 Bio (Tue/Thu), AP Bio (Mon/Wed/Fri), and Honors Bio (Tue/Fri). For each, she imports her curriculum document or types in her lessons.

Three weeks into the term, a snow day cancels school. She opens the app, switches to Grade 9 Bio, clicks October 9, clicks "Shift from here." Every lesson from October 9 forward moves by one day. A toast says "32 lessons shifted."

Later, her Grade 10 class runs behind. She clicks October 15, shifts those lessons too.

At month end, she exports each curriculum to a spreadsheet for her binder, and to .ics so it shows up in her Google Calendar.

Total time for a disruption: 30 seconds per curriculum.

---

## Demo Script (< 2 minutes)

1. Open app (0:00)
2. Drag district calendar PDF → show extracted holidays → confirm (0:15)
3. Show 4 curricula already set up with lessons (0:20)
4. Switch to Grade 9 Bio (0:25)
5. Click October 9 → "Shift from here" → lessons cascade (0:35)
6. Switch to Grade 10 Bio → click October 15 → shift (0:45)
7. Change a lesson duration to 2 days → show cascade (0:55)
8. Drag a lesson to reorder → calendar updates (1:05)
9. Click Export → download spreadsheet (1:15)
10. Click Export → download .ics → show in Google Calendar (1:25)
11. Done (1:30)
