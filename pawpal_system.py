"""
PawPal+ Logic Layer
Classes: Task, Pet, Owner, Scheduler
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Task:
    """Represents a single pet care activity."""
    title: str
    time: str                  # "HH:MM" format
    duration_minutes: int
    priority: str              # "low" | "medium" | "high"
    frequency: str             # "once" | "daily" | "weekly"
    pet_name: str
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task complete. Returns a new Task for the next occurrence if recurring."""
        pass


@dataclass
class Pet:
    """Represents a pet with its associated care tasks."""
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        pass

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        pass


class Owner:
    """Represents the pet owner who manages one or more pets."""

    def __init__(self, name: str):
        self.name = name
        self.pets: list = []

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        pass

    def get_all_tasks(self) -> list:
        """Return a flat list of all tasks across all pets."""
        pass


class Scheduler:
    """The brain of PawPal+. Organizes and manages tasks across all pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self) -> list:
        """Return all tasks sorted chronologically by HH:MM time."""
        pass

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> list:
        """Return tasks filtered by completion status and/or pet name."""
        pass

    def detect_conflicts(self) -> list:
        """Return a list of (task_a, task_b) pairs scheduled at the same time."""
        pass

    def mark_task_complete(self, title: str, pet_name: str) -> None:
        """Find the task by title and pet, mark it complete, and handle recurrence."""
        pass
