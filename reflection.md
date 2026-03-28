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

**b. Tradeoffs**

The scheduler only flags conflicts when two tasks share the exact same start time (e.g., both at "07:30"). It does not check whether task durations overlap — for example, a 30-minute task at 07:00 and a 10-minute task at 07:20 would collide in practice but go undetected. This is a reasonable tradeoff for a daily pet care planner because pet care tasks are rarely scheduled down to the minute and owners naturally leave buffer time between activities. Implementing duration-based overlap detection would require storing an end time for every task and running a more complex interval comparison, adding logic complexity that isn't justified for this use case.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
