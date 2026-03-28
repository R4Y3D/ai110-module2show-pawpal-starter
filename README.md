# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Smarter Scheduling

PawPal+ uses algorithmic logic to go beyond a simple task list:

- **Sort by time** — tasks are sorted chronologically by HH:MM start time, with priority (high → medium → low) as a tiebreaker when two tasks share the same time slot
- **Filter by pet or status** — view only a specific pet's tasks, or show only pending/completed tasks across all pets
- **Conflict detection** — the scheduler scans all tasks pairwise and warns when two tasks are scheduled at the exact same time
- **Recurring tasks** — marking a daily or weekly task complete automatically creates the next occurrence with an updated due date using Python's `timedelta`

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

The suite contains 14 automated tests covering:

- **Task completion** — `mark_complete()` sets status correctly for one-time, daily, and weekly tasks
- **Recurrence logic** — daily tasks produce a next occurrence due tomorrow; weekly tasks due in 7 days
- **Sorting correctness** — tasks added out of order are returned in chronological HH:MM order, with priority as a tiebreaker
- **Conflict detection** — same-time tasks are flagged; clean schedules return an empty list
- **Filtering** — tasks can be filtered by pet name, completion status, or both; unknown pet names return `[]` gracefully
- **Edge cases** — scheduler with no tasks, filtering for a non-existent pet, marking an already-complete task

**Confidence level: ⭐⭐⭐⭐ (4/5)**
The core scheduling behaviors are fully verified. The one gap is duration-based overlap detection — two tasks that overlap in time but don't share an exact start time won't be flagged. That's a known tradeoff documented in `reflection.md`.

---

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
