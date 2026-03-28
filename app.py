import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")
st.caption("A smart pet care scheduler — sort, filter, and detect conflicts across all your pets.")

# --- Application Memory ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")

owner = st.session_state.owner

# ── Sidebar: Owner & Pet Setup ────────────────────────────────────────────────
with st.sidebar:
    st.header("Setup")

    # Owner name
    owner_name_input = st.text_input("Your name", value=owner.name or "Jordan")
    if owner.name != owner_name_input:
        owner.name = owner_name_input

    st.divider()

    # Add a pet
    st.subheader("Add a Pet")
    new_pet_name = st.text_input("Pet name", value="Mochi")
    new_species = st.selectbox("Species", ["dog", "cat", "other"])

    if st.button("Add pet", use_container_width=True):
        if owner.get_pet(new_pet_name):
            st.warning(f"'{new_pet_name}' already exists.")
        else:
            owner.add_pet(Pet(name=new_pet_name, species=new_species))
            st.success(f"Added {new_species} '{new_pet_name}'!")

    if owner.pets:
        st.divider()
        st.subheader("Your Pets")
        for p in owner.pets:
            task_count = len(p.get_tasks())
            st.markdown(f"**{p.name}** ({p.species}) — {task_count} task{'s' if task_count != 1 else ''}")

# ── Main: Schedule a Task ─────────────────────────────────────────────────────
st.subheader("Schedule a Task")

if not owner.pets:
    st.info("Add a pet in the sidebar to get started.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
        task_pet = st.selectbox("Assign to pet", [p.name for p in owner.pets])
    with col2:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
        task_duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        task_priority = st.selectbox("Priority", ["high", "medium", "low"])
        task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task", use_container_width=True):
        pet = owner.get_pet(task_pet)
        pet.add_task(Task(
            title=task_title,
            time=task_time,
            duration_minutes=int(task_duration),
            priority=task_priority,
            frequency=task_frequency,
            pet_name=task_pet,
        ))
        st.success(f"Task '{task_title}' added to {task_pet} at {task_time}.")

st.divider()

# ── Main: Today's Schedule ────────────────────────────────────────────────────
st.subheader("Today's Schedule")

# Filter controls
col_a, col_b = st.columns(2)
with col_a:
    pet_filter = st.selectbox(
        "Filter by pet",
        ["All pets"] + [p.name for p in owner.pets],
    )
with col_b:
    status_filter = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

if st.button("Generate schedule", use_container_width=True):
    scheduler = Scheduler(owner)

    # Apply filters
    completed_filter = None
    if status_filter == "Pending":
        completed_filter = False
    elif status_filter == "Completed":
        completed_filter = True

    pet_name_filter = None if pet_filter == "All pets" else pet_filter

    tasks = scheduler.filter_tasks(completed=completed_filter, pet_name=pet_name_filter)
    # Sort the filtered subset by time + priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks = sorted(tasks, key=lambda t: (t.time, priority_order.get(t.priority, 3)))

    if not tasks:
        st.info("No tasks match the current filters.")
    else:
        # Schedule table
        table_data = [
            {
                "Time": t.time,
                "Task": t.title,
                "Pet": t.pet_name,
                "Priority": t.priority.capitalize(),
                "Duration (min)": t.duration_minutes,
                "Frequency": t.frequency.capitalize(),
                "Status": "Done" if t.completed else "Pending",
            }
            for t in tasks
        ]
        st.table(table_data)

        # Summary metrics
        total = len(tasks)
        done = sum(1 for t in tasks if t.completed)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total tasks", total)
        col2.metric("Completed", done)
        col3.metric("Pending", total - done)

    st.divider()

    # Conflict warnings — always check across ALL tasks, not just the filtered view
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.subheader("Scheduling Conflicts")
        st.caption("The following tasks are scheduled at the same time. Consider rescheduling one.")
        for a, b in conflicts:
            st.warning(
                f"**{a.time}** — **{a.title}** ({a.pet_name}) "
                f"conflicts with **{b.title}** ({b.pet_name}). "
                f"One of these may be missed."
            )
    else:
        st.success("No scheduling conflicts — your day is well planned!")
