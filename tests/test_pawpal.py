"""
PawPal+ Test Suite
Tests core behaviors of Task, Pet, Owner, and Scheduler.
"""

import pytest
from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# --- Fixtures ---

def make_task(title="Morning walk", time="07:30", frequency="once", pet_name="Biscuit"):
    return Task(title=title, time=time, duration_minutes=20, priority="high",
                frequency=frequency, pet_name=pet_name)

def make_pet_with_owner():
    owner = Owner(name="Rayed")
    dog = Pet(name="Biscuit", species="dog")
    cat = Pet(name="Luna", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner, dog, cat


# --- Task Tests ---

def test_mark_complete_sets_completed_true():
    """Task Completion: mark_complete() should set completed to True."""
    task = make_task()
    task.mark_complete()
    assert task.completed is True


def test_once_task_returns_no_next_occurrence():
    """A one-time task should return None when marked complete (no recurrence)."""
    task = make_task(frequency="once")
    result = task.mark_complete()
    assert result is None


# --- Pet Tests ---

def test_add_task_increases_pet_task_count():
    """Task Addition: adding a task to a Pet should increase its task count."""
    pet = Pet(name="Biscuit", species="dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(make_task())
    assert len(pet.get_tasks()) == 1


# --- Scheduler Tests ---

def test_sort_by_time_returns_chronological_order():
    """Sorting: tasks should be returned sorted by HH:MM time."""
    owner, dog, cat = make_pet_with_owner()
    dog.add_task(make_task(title="Evening walk", time="17:00"))
    dog.add_task(make_task(title="Morning walk", time="07:30"))
    cat.add_task(make_task(title="Feeding",      time="09:00", pet_name="Luna"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times)


def test_daily_task_creates_next_occurrence():
    """Recurrence: marking a daily task complete should produce a task for the next day."""
    task = make_task(frequency="daily")
    original_due = task.due_date
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == original_due + timedelta(days=1)
    assert next_task.completed is False


def test_detect_conflicts_flags_same_time_tasks():
    """Conflict Detection: two tasks at the same time should be flagged."""
    owner, dog, cat = make_pet_with_owner()
    dog.add_task(make_task(title="Morning walk", time="07:30", pet_name="Biscuit"))
    cat.add_task(make_task(title="Feeding",      time="07:30", pet_name="Luna"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    titles = {conflicts[0][0].title, conflicts[0][1].title}
    assert titles == {"Morning walk", "Feeding"}
