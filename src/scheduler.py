from typing import List, Dict, Tuple

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
HOURS_PER_DAY = 24


class Task:
    def __init__(self, name: str, priority: str, duration: int):
        self.name = name
        self.priority = priority
        self.duration = duration


def initialize_week() -> Dict[str, List[str]]:
    """
    Creates an empty weekly schedule.
    Each day has 24 slots initialized as 'FREE'.
    """
    return {day: ["FREE"] * HOURS_PER_DAY for day in DAYS}


def add_fixed_commitments(
    schedule: Dict[str, List[str]],
    commitments: List[Tuple[str, int, int, str]],
):
    """
    commitments: (day, start_hour, duration, label)
    """
    for day, start, duration, label in commitments:
        for hour in range(start, start + duration):
            schedule[day][hour] = label


def schedule_tasks(
    schedule: Dict[str, List[str]],
    tasks: List[Task],
) -> List[Task]:
    """
    Assigns tasks into free slots based on priority.
    Returns list of unassigned tasks.
    """
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    tasks = sorted(tasks, key=lambda t: priority_order[t.priority])

    unassigned = []

    for task in tasks:
        placed = False

        for day in DAYS:
            slots = schedule[day]
            for hour in range(HOURS_PER_DAY - task.duration + 1):
                if all(slots[h] == "FREE" for h in range(hour, hour + task.duration)):
                    for h in range(hour, hour + task.duration):
                        slots[h] = task.name
                    placed = True
                    break
            if placed:
                break

        if not placed:
            unassigned.append(task)

    return unassigned

