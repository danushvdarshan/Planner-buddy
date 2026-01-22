
## Source
This algorithm was generated using the prompt:
`prompts/scheduling_algorithm_prompt.md`

## AI-Generated Explanation
The scheduling process works in a deterministic, priority-first manner.
First, the entire week is represented as a sequence of one-hour time slots across seven days. Each slot has a status indicating whether it is occupied by a fixed commitment or is free.
All fixed, non-negotiable commitments are placed into the schedule first and marked as unavailable. These slots cannot be modified during scheduling.
Next, user-defined tasks are grouped by priority. Tasks with High priority are processed first, followed by Medium, and then Low priority tasks.
For each task, the algorithm scans the schedule to find a contiguous block of free time slots whose length matches the task’s required duration. The scan is performed in a fixed order (for example, from Monday morning to Sunday night) to ensure determinism.
When a suitable contiguous block is found, the task is assigned to those slots, and the slots are marked as occupied. If no such block exists, the task is left unassigned.
This process continues until all tasks have been considered. The final schedule contains all fixed commitments and the maximum number of tasks placed according to priority and availability.

## AI-Generated Pseudocode
	initialize schedule as 7 × 24 time slots

	mark fixed commitment slots as occupied

	group tasks by priority in the order:
    		High → Medium → Low

	for each priority group:
    		for each task in the group:
        		required_slots = task.duration

        		for each day from Monday to Sunday:
            			for each hour from 0 to 23:
                			if required_slots of consecutive free slots exist starting here:
                    				assign task to those slots
                    				mark those slots as occupied
                   				break out of search loops

        		if task was not assigned:
            			mark task as unassigned

	return final schedule and list of unassigned tasks

## Edge Cases Identified by AI

1) Insufficient free slots
When total available free time is less than the sum of task durations.

2)Fragmented free time
Free slots exist but are not contiguous enough to fit a task’s duration.

3)All slots occupied by fixed commitments
No tasks can be scheduled.

4)Multiple tasks with equal priority
Tasks are scheduled in the order they are provided by the user.

5)Tasks with duration longer than any available block
Such tasks remain unassigned.

## Human Evaluation
The algorithm correctly enforces priority-based scheduling and ensures
deterministic behavior by scanning time slots in a fixed order.

Its simplicity makes it easy to understand and debug, which is suitable
for my initial idea of Planner Buddy which is essentially to make a compact and workable timetable. However, it does not yet account
for user preferences such as preferred time windows or workload balancing.
## Improvements / Refinements
(To be filled in later iterations)

