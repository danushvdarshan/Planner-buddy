# scheduler.py

def max_slots_per_task(free_slots):
    return max(1, free_slots // 3)

def generate_schedule(tasks, fixed_commitments, protected_slots, non_negotiables):

    schedule = [[None for _ in range(24)] for _ in range(7)]

    # Apply fixed commitments
    for day, slot, name in fixed_commitments:
        schedule[day][slot] = {
            "task": {"task_name": name, "priority": "Fixed"},
            "reason": "Fixed commitment"
        }

    # Apply protected slots
    for day, slot, name in protected_slots:
        schedule[day][slot] = {
            "task": {"task_name": name, "priority": "Protected"},
            "reason": "Protected slot"
        }

        # Apply non-negotiables
    for item in non_negotiables:

        repeat = item.get("repeat", "daily")
        name = item["name"]
        start = item["start"]
        end = item["end"]

        # Determine days
        if repeat == "daily":
            days = range(7)
        elif repeat == "weekday":
            days = range(0, 5)
        elif repeat == "weekend":
            days = [5, 6]
        elif repeat == "custom":
            days = item.get("days", [])
        else:
            days = []

        for day in days:

            # Handle overnight case
            if start < end:
                for slot in range(start, end):
                    schedule[day][slot] = {
                        "task": {"task_name": name, "priority": "Non-negotiable"},
                        "reason": "Recurring commitment"
                    }
            else:
                # Before midnight
                for slot in range(start, 24):
                    schedule[day][slot] = {
                        "task": {"task_name": name, "priority": "Non-negotiable"},
                        "reason": "Recurring commitment"
                    }

                # After midnight (next day)
                next_day = (day + 1) % 7
                for slot in range(0, end):
                    schedule[next_day][slot] = {
                        "task": {"task_name": name, "priority": "Non-negotiable"},
                        "reason": "Recurring commitment"
                    }


    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks_sorted = sorted(
        tasks,
        key=lambda x: priority_order.get(x["priority"], 3)
    )

    remaining = {id(task): task["duration_slots"] for task in tasks_sorted}
    unassigned_tasks = []

    DAILY_LIMIT = 8
    daily_hours_used = [0] * 7

    # ---------- PHASE 1: Respect Daily Limit ----------
    while any(remaining[id(task)] > 0 for task in tasks_sorted):

        progress_made = False

        for day in range(7):

            if daily_hours_used[day] >= DAILY_LIMIT:
                continue

            for task in tasks_sorted:

                task_id = id(task)

                if remaining[task_id] <= 0:
                    continue

                hour = 0

                while hour < 24:

                    if schedule[day][hour] is not None:
                        hour += 1
                        continue

                    block_size = min(
                        3,
                        remaining[task_id],
                        DAILY_LIMIT - daily_hours_used[day]
                    )

                    if block_size <= 0:
                        break

                    if (
                        hour + block_size <= 24 and
                        all(schedule[day][hour + i] is None for i in range(block_size))
                    ):
                        for i in range(block_size):
                            schedule[day][hour + i] = {
                                "task": task,
                                "reason": f"Distributed block ({block_size} hrs)"
                            }

                        remaining[task_id] -= block_size
                        daily_hours_used[day] += block_size
                        progress_made = True
                        break
                    else:
                        hour += 1

        if not progress_made:
            break

        # If all days reached limit → break to Phase 2
        if all(d >= DAILY_LIMIT for d in daily_hours_used):
            break


    # ---------- PHASE 2: Overflow (No Daily Cap) ----------
    while any(remaining[id(task)] > 0 for task in tasks_sorted):

        progress_made = False

        for day in range(7):

            for task in tasks_sorted:

                task_id = id(task)

                if remaining[task_id] <= 0:
                    continue

                hour = 0

                while hour < 24:

                    if schedule[day][hour] is not None:
                        hour += 1
                        continue

                    block_size = min(3, remaining[task_id])

                    if (
                        hour + block_size <= 24 and
                        all(schedule[day][hour + i] is None for i in range(block_size))
                    ):
                        for i in range(block_size):
                            schedule[day][hour + i] = {
                                "task": task,
                                "reason": f"Overflow block ({block_size} hrs)"
                            }

                        remaining[task_id] -= block_size
                        progress_made = True
                        break
                    else:
                        hour += 1

        if not progress_made:
            break


    # Collect unassigned tasks
    for task in tasks_sorted:
        if remaining[id(task)] > 0:
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
