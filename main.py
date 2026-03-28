"""
PawPal+ CLI Demo Script
Demonstrates sorting, filtering, recurring tasks, and conflict detection.
"""

from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Rayed")

dog = Pet(name="Biscuit", species="dog")
cat = Pet(name="Luna", species="cat")

owner.add_pet(dog)
owner.add_pet(cat)

# --- Add Tasks intentionally OUT OF ORDER to prove sorting works ---
dog.add_task(Task(title="Evening walk",     time="17:00", duration_minutes=30, priority="high",   frequency="daily",  pet_name="Biscuit"))
dog.add_task(Task(title="Morning walk",     time="07:30", duration_minutes=20, priority="high",   frequency="daily",  pet_name="Biscuit"))
dog.add_task(Task(title="Flea medication",  time="09:00", duration_minutes=5,  priority="medium", frequency="weekly", pet_name="Biscuit"))
cat.add_task(Task(title="Feeding",          time="07:30", duration_minutes=10, priority="high",   frequency="daily",  pet_name="Luna"))
cat.add_task(Task(title="Litter box clean", time="12:00", duration_minutes=10, priority="medium", frequency="daily",  pet_name="Luna"))
cat.add_task(Task(title="Playtime",         time="15:00", duration_minutes=15, priority="low",    frequency="once",   pet_name="Luna"))

scheduler = Scheduler(owner=owner)

# --- 1. SORTING: Today's Schedule sorted by time (priority tiebreaker at 07:30) ---
print("=" * 58)
print(f"  PawPal+ | Today's Schedule for {owner.name}")
print("=" * 58)

for task in scheduler.sort_by_time():
    status = "[x]" if task.completed else "[ ]"
    print(f"{status} {task.time}  {task.title:<22} | {task.pet_name:<8} | {task.priority:<6} | {task.duration_minutes} min")

print()
print("  ^ Tasks added out of order. sort_by_time() uses lambda key=(time, priority).")
print("    Note: 07:30 'Feeding' (high) and 'Morning walk' (high) - same time, same priority.")

# --- 2. FILTERING: by pet name ---
print()
print("-" * 58)
print("  Filter: Biscuit's tasks only")
print("-" * 58)
for task in scheduler.filter_tasks(pet_name="Biscuit"):
    print(f"  {task.time}  {task.title:<22} | {task.frequency}")

# --- 3. FILTERING: pending tasks only ---
print()
print("-" * 58)
print("  Filter: pending (not completed) tasks across all pets")
print("-" * 58)
for task in scheduler.filter_tasks(completed=False):
    print(f"  {task.time}  {task.title:<22} | {task.pet_name}")

# --- 4. CONFLICT DETECTION ---
print()
print("-" * 58)
conflicts = scheduler.detect_conflicts()
if conflicts:
    print("  Conflicts detected:")
    for a, b in conflicts:
        print(f"  {a.time} | '{a.title}' ({a.pet_name}) clashes with '{b.title}' ({b.pet_name})")
else:
    print("  No scheduling conflicts.")

# --- 5. RECURRING TASKS: mark complete, verify next occurrence added ---
print()
print("-" * 58)
print("  Marking 'Morning walk' complete (daily -> recurs tomorrow)")
print("-" * 58)
scheduler.mark_task_complete("Morning walk", "Biscuit")

for task in scheduler.filter_tasks(pet_name="Biscuit"):
    status = "DONE   " if task.completed else "pending"
    print(f"  {status} | {task.title:<22} | due: {task.due_date}")
