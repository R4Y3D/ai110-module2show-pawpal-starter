"""
PawPal+ Logic Layer
Classes: Task, Pet, Owner, Scheduler
"""

from dataclasses import dataclass, field
from datetime import date, timedelta
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
        self.completed = True
        if self.frequency == "daily":
            return Task(
                title=self.title,
                time=self.time,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                pet_name=self.pet_name,
                due_date=self.due_date + timedelta(days=1),
            )
        if self.frequency == "weekly":
            return Task(
                title=self.title,
                time=self.time,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                pet_name=self.pet_name,
                due_date=self.due_date + timedelta(weeks=1),
            )
        return None


@dataclass
class Pet:
    """Represents a pet with its associated care tasks."""
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        return self.tasks


class Owner:
    """Represents the pet owner who manages one or more pets."""

    def __init__(self, name: str):
        self.name = name
        self.pets: list = []

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Return a pet by name, or None if not found."""
        return next((p for p in self.pets if p.name == name), None)

    def get_all_tasks(self) -> list:
        """Return a flat list of all tasks across all pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The brain of PawPal+. Organizes and manages tasks across all pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self) -> list:
        """Return all tasks sorted by HH:MM time, with priority as a tiebreaker."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            self.owner.get_all_tasks(),
            key=lambda t: (t.time, priority_order.get(t.priority, 3))
        )

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> list:
        """Return tasks filtered by completion status and/or pet name."""
        tasks = self.owner.get_all_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        return tasks

    def detect_conflicts(self) -> list:
        """Return a list of (task_a, task_b) pairs scheduled at the same time."""
        tasks = self.owner.get_all_tasks()
        conflicts = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                if tasks[i].time == tasks[j].time:
                    conflicts.append((tasks[i], tasks[j]))
        return conflicts

    def mark_task_complete(self, title: str, pet_name: str) -> None:
        """Find the task by title and pet, mark it complete, and handle recurrence."""
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            return
        for task in pet.get_tasks():
            if task.title == title and not task.completed:
                next_task = task.mark_complete()
                if next_task:
                    pet.add_task(next_task)
                break
