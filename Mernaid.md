'''mermaid
classDiagram
    class Owner {
        +String name
        +List~Pet~ pets
        +add_pet(pet: Pet)
        +get_pet(name: String) Pet
        +get_all_tasks() List~Task~
    }

    class Pet {
        +String name
        +String species
        +List~Task~ tasks
        +add_task(task: Task)
        +get_tasks() List~Task~
    }

    class Task {
        +String title
        +String time
        +int duration_minutes
        +String priority
        +String frequency
        +bool completed
        +String pet_name
        +Date due_date
        +mark_complete() Task
    }

    class Scheduler {
        +Owner owner
        +sort_by_time() List~Task~
        +filter_tasks(completed, pet_name) List~Task~
        +detect_conflicts() List
        +mark_task_complete(title, pet_name)
    }

    Owner "1" --> "many" Pet : has
    Pet "1" --> "many" Task : has
    Scheduler "1" --> "1" Owner : manages
    Task --> Task : mark_complete() creates next occurrence
'''
