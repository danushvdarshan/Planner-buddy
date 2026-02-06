def build_events(schedule):
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    events = []

    for day_idx, day_slots in enumerate(schedule):
        current_cell = None
        start_hour = None

        for hour in range(24):
            cell = day_slots[hour]

            if cell != current_cell:
                if current_cell is not None:
                    events.append({
                        "day": DAYS[day_idx],
                        "start_hour": start_hour,
                        "end_hour": hour,
                        "activity": current_cell
                    })

                if cell is not None:
                    current_cell = cell
                    start_hour = hour
                else:
                    current_cell = None
                    start_hour = None

        # end of day
        if current_cell is not None:
            events.append({
                "day": DAYS[day_idx],
                "start_hour": start_hour,
                "end_hour": 24,
                "activity": current_cell
            })

    return events
