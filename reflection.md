# PawPal+ Project Reflection

## 1. System Design
    Three core actions:
        1. Add a pet
        2. Add/schedule a care task
        3. Generate and view today's schedule

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

    I was able to design the four classes which were task, pet, owner, and scheduler. Task holds all the activity data. Pet stores a pet's identity and its list of tasks. Owner manages multple pets and can flatten all their tasks into one big list. Finally scheduler is basically what acts as the brain. It uses owner to sort, filter and detect conflicts and also handle task completion. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

    After throroughly reviewing the scehduler and getting feedback from my LLM, I added a get_pet(name) helper method to Owner. Without this, scheduler would have to repeat pet-lookup logic in every method that needs to find a specific pet by name. I was told to move this to owner to keep each class focusd on its own responsibilities.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

    The scheduler created consideres three contraints. These constraints are time, priority, and frequency. Time is basically the primary sort key mainly because a pet owner needs to know what to do and especially when. This is more useful than priority alone. For me, priority became secondary as a tiebreaker for cases where two tasks share the same start time. Frequency was also the third constraint mainly because it determines whether the schedule is able to self-maintain itself. 

**b. Tradeoffs**

    There are many tradeoffs I had to go through in this project. One tradeoff would be that the scheduler only flags conflicts when two tasks share the exact same start time. It does not check whether task durations overlap. for example, a 30-minute task at 07:00 and a 10-minute task at 07:20 would collide in practice but go undetected. This is a reasonable tradeoff for a daily pet care planner because pet care tasks are rarely scheduled down to the minute and owners naturally leave buffer time between activities. Implementing duration-based overlap detection would require storing an end time for every task and running a more complex interval comparison, adding logic complexity that isn't justified for this use case. This went past the scope of the project and its use case. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

    I collaborated with Ai throughout all phases of this project. During the design phase, I prompted it to generate me a Mermaid UML with my idea of the initial structure after brainstorming classes and attributes. During the implementation process, I utilized agent mode to scaffold all four of the class sceletons and have it help me flesh out the logic a bit more and make sure I am not missing anything. During the testing phase, I had it suggest to me edge cases that I might have not throught of such as filtering by unknown pet names or marking an aleready complete task. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

    There are manyu ways I judged and verified the AI outputs and ideas. For example, when asked to simplify detect_conflicts(), the AI suggested replacing the nested loop with a one-liner using itertools.combinations. The result was less readable for someone like me who was unfamilar with the itertools module. This is why I kept the explicit nested loop because the pairwise comparison logic is immediately visible.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

    I basically tested 14 different behaviors accross task, pet, owner, and scheduler. These were task completion status, one-time and recurring task recurrence (daily and weekly), sort order correctness, priority tiebreaking in sorting, filtering by pet name and completion status, conflict detection with and without clashes, and edge cases like an empty scheduler or filtering for a pet that doesn't exist. These tests were very helpful because they helped verify that the algorithmic logic actually worked correctly before I connected to streamlit. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

    I am very confident that the core scheduling bnehaviors and mostly everything work correctly. This is because all 14 tests passed. While there definetly could be more tests done to further ensure, these tests tested the core logic and algroithmic structure for the project. My confidence rating is 4 out of 5. But next time, the one gap I would further test is duration based overlap detections. This is where if two tasks overlap in time but don't share an exact start time won't be flagged.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

    I am the most satisfied with how clean the whole app looks on browser and just how cleanly the four classes separated their responsibilities. The scheduler never directly touches a task list. I find this boundary and separation in the logic of the code very satisfying as it made the code way easier to test. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

    If I had another iteration for this project, I would like to add duration aware conflict detection and a due_date filter. This is so that the schedule only shows tasks due today rather than all the tasks ever added.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

    The most important thjing I would takeaway from completing this project is that while Ai is a fast and capable collaborator, it does not know what you are trying to build. The only person that truly knows is you, and your boss/customer. If I had accepted all suggestions without thinking, I would get code that I no longer understand as a developer and would have to play cat and mouse trying to understand it as it prompts more and more into my project. 