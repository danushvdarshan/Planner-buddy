
# Prompt-Based Development of the Scheduling Algorithm

This document captures how the Planner Buddy scheduling algorithm
was developed using prompt engineering and iterative human refinement.

It records the evolution from an AI-generated solution to a
final, deterministic algorithm specification used in Planner Buddy v1.

---

## 1. Source Prompt

The scheduling logic was initially generated using the following prompt:

`prompts/scheduling_algorithm_prompt.md`

The prompt defined:
- Weekly time representation (7 days × 24 slots)
- Fixed commitments
- Task priorities and durations
- Deterministic, explainable behavior
- Explicit constraints and exclusions

The prompt did not prescribe implementation details, allowing the AI
to reason about the algorithm structure.

---

## 2. Initial AI-Generated Approach

Based on the prompt, the AI proposed a deterministic, priority-first
scheduling strategy.

The key characteristics of the AI-generated approach were:
- Representation of the week as one-hour slots
- Placement of fixed commitments before tasks
- Strict priority ordering (High → Medium → Low)
- Contiguous allocation of slots equal to task duration
- Sequential scanning of time slots from the beginning of the week
- Explicit handling of unscheduled tasks

This approach satisfied the core constraints of Planner Buddy v1.

---

## 3. Human Refinements and Design Decisions

After reviewing the AI-generated solution, several refinements were
introduced through human judgment and product considerations.

### 3.1 Task Duration as a Mandatory Constraint
Each task must explicitly specify the number of required one-hour slots.
Tasks are never expanded to fill unused time.

This prevents artificial over-allocation and ensures visible free
capacity in the weekly schedule.

### 3.2 Priority Dominance
Task priority strictly governs scheduling order, regardless of task
duration or total available free time.

Longer tasks do not imply higher importance.

### 3.3 Earliest-First and Same-Day Preference
Free slots are scanned from Monday morning to Sunday night.
When possible, contiguous slots within the same day are preferred to
reduce fragmentation.

### 3.4 Transparency for Unscheduled Tasks
Tasks that cannot be scheduled remain unassigned.
Each such task is reported with an explicit reason, ensuring user trust
and system explainability.

---

## 4. Final Scheduling Logic

The finalized scheduling process for Planner Buddy v1 follows these steps:

1. Initialize a 7 × 24 weekly grid.
2. Mark all fixed commitments as occupied.
3. Identify contiguous blocks of free slots.
4. Sort tasks by:
   - Priority (High → Medium → Low)
   - Duration (descending within each priority)
5. For each task:
   - Scan free slots from earliest to latest.
   - Assign the task to the first suitable contiguous block.
   - Mark the assigned slots as occupied.
6. If no suitable block exists:
   - Mark the task as unscheduled and record the reason.
7. Output the final schedule, unscheduled tasks, and remaining free slots.

---

## 5. Final Pseudocode (v1)

initialize weekly_grid[7][24]

mark fixed_commitments as occupied

group tasks by priority: High, Medium, Low

for each priority_group in [High, Medium, Low]:
	sort priority_group by duration descending
	
	for each task in priority_group:
    		block = find_earliest_contiguous_free_block(
                	weekly_grid,
                	task.duration
            		)

    		if block exists:
        		assign task to block
        		mark block as occupied
    		else:
        		record task as unscheduled


---

## 6. Explicit Exclusions (Planner Buddy v1)

The following features are intentionally excluded in v1:
- Deadlines
- Energy levels
- Task dependencies
- Preferred timing or time windows
- Task splitting

These exclusions keep the system deterministic and explainable.

---

## 7. Rationale for Prompt-Based Development

Using prompt-based development allowed:
- Rapid generation of a correct baseline algorithm
- Clear inspection of AI reasoning
- Iterative refinement through human feedback
- Separation between AI exploration and final system specification

The finalized algorithm is documented separately in
`docs/scheduling_algorithm.md` as the authoritative reference.

---

## 8. Future Iterations

Future versions of Planner Buddy may introduce:
- Soft timing preferences
- Urgency and deadlines
- Dependency-aware scheduling
- User-driven re-optimization

These enhancements will build upon the current deterministic core.


