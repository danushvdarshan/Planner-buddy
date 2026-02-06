# scheduler.py

def max_slots_per_task(free_slots):
    return max(1, free_slots // 3)


def generate_schedule(tasks, fixed_commitments, protected_slots):
    # Initialize empty schedule
    schedule = [[None for _ in range(24)] for _ in range(7)]

    # Apply fixed commitments (tuple-based)
    for day, slot, name in fixed_commitments:
        schedule[day][slot] = {
            "task": name,
            "reason": "Fixed commitment"
        }


    # Apply protected slots (tuple-based)
    for day, slot, name in protected_slots:
        schedule[day][slot] = {
            "task": name,
            "reason": "Protected slot"
        }


    # Sort tasks by priority
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks_sorted = sorted(tasks, key=lambda x: priority_order[x["priority"]])

    unassigned_tasks = []

    for task in tasks_sorted:
        remaining = task["duration_slots"]

        for day in range(7):
            if remaining <= 0:
                break

            free_slots = [i for i in range(24) if schedule[day][i] is None]
            free_count = len(free_slots)

            if free_count == 0:
                continue

            daily_cap = max_slots_per_task(free_count)
            slots_today = min(daily_cap, remaining)

            step = max(1, free_count // slots_today)
            chosen = free_slots[::step][:slots_today]

            for slot in chosen:
                schedule[day][slot] = {
                    "task": task,
                    "reason": f"Priority={task['priority']}, daily_cap={daily_cap}, free_slots={free_count}"
                }


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
                    "activity": slot["task"],
                    "reason": slot["reason"]
                })

    return formatted
