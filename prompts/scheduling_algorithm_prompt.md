# Scheduling Algorithm Prompt

## Context
Planner Buddy is a weekly planning system that divides time into
7 days with 24 one-hour slots per day.

Some slots are pre-filled with fixed, non-negotiable commitments.
The remaining slots are considered free.

Users also provide a list of tasks to complete in the week.

Each task has:
- name
- priority (High, Medium, Low)
- duration (in hours)

## Objective
Create a deterministic scheduling algorithm that assigns tasks
to available time slots.

The primary goal is to schedule higher-priority tasks before
lower-priority ones.

## Rules and Constraints
1. Fixed commitments cannot be moved or overwritten.
2. Tasks require contiguous time slots equal to their duration.
3. No overlapping tasks are allowed.
4. High-priority tasks must be scheduled before Medium and Low.
5. If no suitable slots exist, the task should remain unassigned.
6. The algorithm must be explainable step-by-step.
7. No randomness or machine learning is allowed.

## Expected Output
1. Clear explanation of the algorithm.
2. Pseudocode describing the scheduling process.
3. Edge cases the algorithm must handle.

The solution should be simple, readable, and maintainable.

