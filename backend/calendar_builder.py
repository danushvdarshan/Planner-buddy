# calendar_builder.py

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def build_events(schedule):
    events = []

    for day_idx, day_slots in enumerate(schedule):
        current_activity = None
        start_hour = None

        for hour in range(24):
            slot = day_slots[hour]

            if slot != current_activity:
                if current_activity is not None:
                    events.append({
                        "day": DAYS[day_idx],
                        "start_hour": start_hour,
                        "end_hour": hour,
                        "activity": current_activity
                    })

                if slot is not None:
                    current_activity = slot
                    start_hour = hour
                else:
                    current_activity = None
                    start_hour = None

        if current_activity is not None:
            events.append({
                "day": DAYS[day_idx],
                "start_hour": start_hour,
                "end_hour": 24,
                "activity": current_activity
            })

    return events

