"""
PawPal+ Test Suite
Tests core behaviors of Task, Pet, Owner, and Scheduler.
"""

import pytest
from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# --- Helpers ---

def make_task(title="Morning walk", time="07:30", frequency="once",
              pet_name="Biscuit", priority="high", duration=20):
    return Task(title=title, time=time, duration_minutes=duration,
                priority=priority, frequency=frequency, pet_name=pet_name)

def make_pet_with_owner():
    owner = Owner(name="Rayed")
    dog = Pet(name="Biscuit", species="dog")
    cat = Pet(name="Luna", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner, dog, cat


# ── Task Tests ────────────────────────────────────────────────────────────────

def test_mark_complete_sets_completed_true():
    """Task Completion: mark_complete() should set completed to True."""
    task = make_task()
    task.mark_complete()
    assert task.completed is True


def test_once_task_returns_no_next_occurrence():
    """One-time tasks return None on completion — no recurrence created."""
    task = make_task(frequency="once")
    result = task.mark_complete()
    assert result is None


def test_weekly_task_creates_occurrence_seven_days_later():
    """Weekly recurrence: next task should be due exactly 7 days after the original."""
    task = make_task(frequency="weekly")
    original_due = task.due_date
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == original_due + timedelta(weeks=1)
    assert next_task.completed is False


# ── Pet Tests ─────────────────────────────────────────────────────────────────

def test_add_task_increases_pet_task_count():
    """Task Addition: adding a task to a Pet should increase its task count."""
    pet = Pet(name="Biscuit", species="dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(make_task())
    assert len(pet.get_tasks()) == 1


# ── Scheduler: Sorting ────────────────────────────────────────────────────────

def test_sort_by_time_returns_chronological_order():
    """Sorting: tasks added out of order should come back sorted by HH:MM."""
    owner, dog, cat = make_pet_with_owner()
    dog.add_task(make_task(title="Evening walk", time="17:00"))
    dog.add_task(make_task(title="Morning walk", time="07:30"))
    cat.add_task(make_task(title="Feeding",      time="09:00", pet_name="Luna"))

    times = [t.time for t in Scheduler(owner).sort_by_time()]
    assert times == sorted(times)


def test_sort_by_time_priority_tiebreaker():
    """When two tasks share a time, high priority should come before medium."""
    owner, dog, cat = make_pet_with_owner()
    dog.add_task(make_task(title="Low task",  time="08:00", priority="medium"))
    cat.add_task(make_task(title="High task", time="08:00", priority="high", pet_name="Luna"))

    sorted_tasks = Scheduler(owner).sort_by_time()
    assert sorted_tasks[0].priority == "high"
    assert sorted_tasks[1].priority == "medium"


def test_sort_with_no_tasks_returns_empty_list():
    """Edge case: a Scheduler with no tasks should return an empty list, not crash."""
    owner = Owner(name="Rayed")
    owner.add_pet(Pet(name="Biscuit", species="dog"))
    result = Scheduler(owner).sort_by_time()
    assert result == []


# ── Scheduler: Recurrence ─────────────────────────────────────────────────────

def test_daily_task_creates_next_occurrence():
    """Recurrence: marking a daily task complete should produce a task for the next day."""
    task = make_task(frequency="daily")
    original_due = task.due_date
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == original_due + timedelta(days=1)
    assert next_task.completed is False


def test_mark_task_complete_appends_recurring_task_to_pet():
    """Scheduler.mark_task_complete() should add the next occurrence to the pet."""
    owner, dog, _ = make_pet_with_owner()
    dog.add_task(make_task(frequency="daily"))
    assert len(dog.get_tasks()) == 1

    Scheduler(owner).mark_task_complete("Morning walk", "Biscuit")
    assert len(dog.get_tasks()) == 2
    assert dog.get_tasks()[1].completed is False


# ── Scheduler: Filtering ──────────────────────────────────────────────────────

def test_filter_by_pet_name_returns_only_that_pets_tasks():
    """filter_tasks(pet_name=...) should return tasks for that pet only."""
    owner, dog, cat = make_pet_with_owner()
    dog.add_task(make_task(title="Walk",    pet_name="Biscuit"))
    cat.add_task(make_task(title="Feeding", pet_name="Luna"))

    result = Scheduler(owner).filter_tasks(pet_name="Biscuit")
    assert all(t.pet_name == "Biscuit" for t in result)
    assert len(result) == 1


def test_filter_by_unknown_pet_returns_empty_list():
    """Edge case: filtering by a pet name that doesn't exist should return []."""
    owner, dog, _ = make_pet_with_owner()
    dog.add_task(make_task())
    result = Scheduler(owner).filter_tasks(pet_name="Ghost")
    assert result == []


def test_filter_completed_false_excludes_done_tasks():
    """filter_tasks(completed=False) should hide completed tasks."""
    owner, dog, _ = make_pet_with_owner()
    dog.add_task(make_task(title="Walk"))
    dog.add_task(make_task(title="Meds", frequency="once"))

    Scheduler(owner).mark_task_complete("Meds", "Biscuit")
    pending = Scheduler(owner).filter_tasks(completed=False)
    assert all(not t.completed for t in pending)


# ── Scheduler: Conflict Detection ─────────────────────────────────────────────

def test_detect_conflicts_flags_same_time_tasks():
    """Conflict Detection: two tasks at the same time should be flagged."""
    owner, dog, cat = make_pet_with_owner()
    dog.add_task(make_task(title="Morning walk", time="07:30", pet_name="Biscuit"))
    cat.add_task(make_task(title="Feeding",      time="07:30", pet_name="Luna"))

    conflicts = Scheduler(owner).detect_conflicts()
    assert len(conflicts) == 1
    titles = {conflicts[0][0].title, conflicts[0][1].title}
    assert titles == {"Morning walk", "Feeding"}


def test_detect_conflicts_returns_empty_when_no_clashes():
    """Edge case: no conflicts should return an empty list."""
    owner, dog, cat = make_pet_with_owner()
    dog.add_task(make_task(title="Walk",    time="07:30"))
    cat.add_task(make_task(title="Feeding", time="08:00", pet_name="Luna"))

    conflicts = Scheduler(owner).detect_conflicts()
    assert conflicts == []
