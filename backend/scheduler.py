# scheduler.py

from calendar_builder import build_calendar  # import the base calendar builder

def max_slots_per_task(free_slots):
    """
    Heuristic to avoid fatigue:
    ~1 slot per 3 free slots, minimum 1
    """
    return max(1, free_slots // 3)


def generate_schedule(tasks, fixed_commitments, protected_slots):
    """
    Generates a weekly schedule:
    - tasks: list of dicts {task_name, priority, duration_slots}
    - fixed_commitments / protected_slots: lists of dicts with day/start/end/name
    Returns:
    - schedule: 7x24 grid with task names
    - unassigned_tasks: tasks that could not be fully scheduled
    """
    # Build base calendar using imported function
    schedule = build_calendar(fixed_commitments, protected_slots)

    # Sort tasks by priority
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks_sorted = sorted(tasks, key=lambda x: priority_order[x["priority"]])

    unassigned_tasks = []

    for task in tasks_sorted:
        remaining = task["duration_slots"]

        for day in range(7):
            if remaining <= 0:
                break

            # Find free slots in the day
            free_slots = [i for i in range(24) if schedule[day][i] is None]
            free_count = len(free_slots)

            if free_count == 0:
                continue

            # Determine max slots allowed for this task today
            daily_cap = max_slots_per_task(free_count)
            slots_today = min(daily_cap, remaining)

            if slots_today <= 0:
                continue

            # Distribute slots evenly (e.g., 1,4,7 pattern)
            step = max(1, free_count // slots_today)
            chosen_slots = free_slots[::step][:slots_today]

            for slot in chosen_slots:
                schedule[day][slot] = task["task_name"]

            remaining -= slots_today

        if remaining > 0:
            unassigned_tasks.append(task)

    return schedule, unassigned_tasks


def format_schedule(schedule):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    formatted = {}

    for day_idx, day in enumerate(schedule):
        day_name = days[day_idx]
        formatted[day_name] = []

        for hour, slot in enumerate(day):
            if slot is not None:
                formatted[day_name].append({
                    "time": f"{hour}:00 - {hour+1}:00",
                    "activity": slot
                })

    return formatted
