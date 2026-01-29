# Scheduling Algorithm (v1)

## 1. Scope & Philosophy

This document defines the **v1 scheduling logic** for the planner.

Design goals:

* Be **predictable** and **transparent** to users
* Respect **fixed user commitments** (duration is mandatory)
* Allow **unused free time** without force-filling
* Keep the model simple, extensible, and UI-driven

Future features (intentionally excluded from v1):

* Auto task stretching or shrinking
* Deadlines, dependencies, or soft constraints
* AI-driven reprioritization

---

## 2. Core Assumptions (Frozen for v1)

### 2.1 Time Slots

* A **slot** is a fixed unit of time
* Slot duration is **user-defined** via UI
* Allowed values (v1):

  * `30 minutes`
  * `1 hour`

All scheduling is done in **number of slots**, not clock time.

---

### 2.2 Task Requirements

Every task **must** define:

| Field          | Type        | Required | Notes                     |
| -------------- | ----------- | -------- | ------------------------- |
| task_name      | string      | ✅        | Display name              |
| priority       | categorical | ✅        | e.g., High / Medium / Low |
| duration_slots | integer     | ✅        | Fixed, non-negotiable     |

Optional fields are deliberately excluded in v1.

---

### 2.3 Priority Model

* Priority is **categorical** at the user level
* Backend will map categories → numeric weights later
* Priority influences **ordering**, not duration

Example (internal mapping – not exposed):

* High → 3
* Medium → 2
* Low → 1

---

### 2.4 Free Slots

* If available slots > required slots:

  * Remaining slots are left **unassigned**
  * Displayed as **Free / Available**

No auto-filling, no stretching.

---

## 3. Inputs

### 3.1 Weekly Slot Capacity

Available and unavailable time slots are inferred from the interactive weekly grid in the UI, where users mark fixed commitments.

TOTAL_SLOTS and FREE_SLOTS are derived from this grid automatically; the user does not need to provide them manually.

### 3.1.1 Protected Slots (System-Level Constraints)

Some time slots are non-negotiable and must never be scheduled for tasks. 
These include:
- Sleep
- Meals
- Commute / travel
- Fixed commitments (classes, meetings)

All protected slots are **provided by the UI** in the weekly time grid. 
The scheduler treats them as unavailable when assigning tasks.

---

### 3.2 Task List

```
TASKS = [
  {
    task_name: string,
    priority: categorical,
    duration_slots: integer
  },
  ...
]
```

---

## 4. Scheduling Strategy (v1)

### High-level idea

1. Sort tasks by priority
2. Assign slots greedily
3. Stop when slots are exhausted
4. Leave unused slots empty

---

## 5. Pseudocode

initialize schedule as 7 × 24 time slots

# 1. Mark protected slots as unavailable
mark slots for sleep, meals, commute, and fixed commitments as occupied

group tasks by priority in the order: High → Medium → Low

for each priority group:
    for each task in the group:
        required_slots = task.duration_slots

        for each day from Monday to Sunday:
            for each hour from 0 to 23:
                if required_slots of consecutive free slots exist starting here:
                    assign task to those slots
                    mark those slots as occupied
                    break out of search loops

        if task was not assigned:
            mark task as unassigned

return final schedule and list of unassigned tasks

---

## 6. Behavior Guarantees

* Tasks are **never split**
* Tasks are **never auto-resized**
* Priority outranks duration
* Empty time is a **feature**, not a bug

---

## 7. Example

### Input

```
TOTAL_SLOTS = 50

TASKS = [
  { name: "Project Report", priority: High, duration_slots: 20 },
  { name: "DSA Practice", priority: Medium, duration_slots: 10 },
  { name: "Blog Writing", priority: Low, duration_slots: 5 }
]
```

### Output

```
Scheduled Tasks:
- Project Report (20)
- DSA Practice (10)
- Blog Writing (5)

Free Slots:
- 15
```

---

## 8. What v1 Does NOT Solve

* Importance vs urgency conflicts
* Deadlines or time windows
* Task dependencies
* Context switching costs

These will be introduced in future versions.

---

## 9. Next Planned Extensions

* Deadline-aware scheduling
* Dependency graphs
* Soft constraints
* AI-driven suggestions
* Adaptive priority learning

---

**This document intentionally favors clarity over cleverness.**

