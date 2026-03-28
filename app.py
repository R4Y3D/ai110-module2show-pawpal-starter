import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("PawPal+")

# --- Application Memory ---
# Initialize Owner once in session_state so it persists across re-runs.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")

owner = st.session_state.owner

# --- Owner Setup ---
st.subheader("Owner")
owner_name_input = st.text_input("Your name", value=owner.name or "Jordan")
if owner.name != owner_name_input:
    owner.name = owner_name_input

# --- Add a Pet ---
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    new_pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    new_species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    existing = owner.get_pet(new_pet_name)
    if existing:
        st.warning(f"A pet named '{new_pet_name}' already exists.")
    else:
        owner.add_pet(Pet(name=new_pet_name, species=new_species))
        st.success(f"Added {new_species} '{new_pet_name}'!")

# Show registered pets
if owner.pets:
    st.caption("Registered pets: " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a Task ---
st.subheader("Schedule a Task")

if not owner.pets:
    st.info("Add a pet first before scheduling tasks.")
else:
    pet_options = [p.name for p in owner.pets]
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
        task_pet = st.selectbox("Assign to pet", pet_options)
    with col2:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
        task_duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        pet = owner.get_pet(task_pet)
        new_task = Task(
            title=task_title,
            time=task_time,
            duration_minutes=int(task_duration),
            priority=task_priority,
            frequency=task_frequency,
            pet_name=task_pet,
        )
        pet.add_task(new_task)
        st.success(f"Task '{task_title}' added to {task_pet}!")

st.divider()

# --- Generate Schedule ---
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    if not sorted_tasks:
        st.info("No tasks yet. Add some tasks above.")
    else:
        # Display sorted schedule as a table
        table_data = [
            {
                "Time": t.time,
                "Task": t.title,
                "Pet": t.pet_name,
                "Priority": t.priority,
                "Duration (min)": t.duration_minutes,
                "Frequency": t.frequency,
                "Done": "Yes" if t.completed else "No",
            }
            for t in sorted_tasks
        ]
        st.table(table_data)

        # Show conflict warnings
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for a, b in conflicts:
                st.warning(
                    f"Conflict at {a.time}: '{a.title}' ({a.pet_name}) "
                    f"clashes with '{b.title}' ({b.pet_name})"
                )
        else:
            st.success("No scheduling conflicts.")
