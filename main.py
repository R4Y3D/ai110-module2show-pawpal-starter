"""
PawPal+ CLI Demo Script
Verify backend logic before connecting to the Streamlit UI.
"""

from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Rayed")

dog = Pet(name="Biscuit", species="dog")
cat = Pet(name="Luna", species="cat")

owner.add_pet(dog)
owner.add_pet(cat)

# --- Add Tasks (intentionally out of order to test sorting) ---
dog.add_task(Task(title="Evening walk",      time="17:00", duration_minutes=30, priority="high",   frequency="daily",  pet_name="Biscuit"))
dog.add_task(Task(title="Morning walk",      time="07:30", duration_minutes=20, priority="high",   frequency="daily",  pet_name="Biscuit"))
dog.add_task(Task(title="Flea medication",   time="09:00", duration_minutes=5,  priority="medium", frequency="weekly", pet_name="Biscuit"))
cat.add_task(Task(title="Feeding",           time="07:30", duration_minutes=10, priority="high",   frequency="daily",  pet_name="Luna"))
cat.add_task(Task(title="Litter box clean",  time="12:00", duration_minutes=10, priority="medium", frequency="daily",  pet_name="Luna"))

scheduler = Scheduler(owner=owner)

# --- Today's Schedule (sorted by time) ---
print("=" * 50)
print(f"  PawPal+ | Today's Schedule for {owner.name}")
print("=" * 50)

for task in scheduler.sort_by_time():
    status = "[x]" if task.completed else "[ ]"
    print(f"{status} {task.time}  {task.title:<22} | {task.pet_name:<8} | {task.priority} priority | {task.duration_minutes} min | {task.frequency}")

# --- Conflict Detection ---
print()
conflicts = scheduler.detect_conflicts()
if conflicts:
    print("WARNING: Conflicts detected:")
    for a, b in conflicts:
        print(f"   {a.time} | '{a.title}' ({a.pet_name}) clashes with '{b.title}' ({b.pet_name})")
else:
    print("No scheduling conflicts.")

# --- Mark a daily task complete and show recurrence ---
print()
print("--- Marking 'Morning walk' complete ---")
scheduler.mark_task_complete("Morning walk", "Biscuit")

biscuit_tasks = scheduler.filter_tasks(pet_name="Biscuit")
print(f"Biscuit now has {len(biscuit_tasks)} tasks (recurring task added for next day):")
for task in biscuit_tasks:
    status = "DONE" if task.completed else "pending"
    print(f"  {task.title:<22} | due: {task.due_date} | {status}")
