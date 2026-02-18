console.log("JS LOADED");

document.addEventListener("DOMContentLoaded", () => {

    const generateBtn = document.getElementById("generate");
    const addTaskBtn = document.getElementById("add-task");
    const container = document.getElementById("task-container");
    const calendar = document.getElementById("calendar");
    const nonNegContainer = document.getElementById("non-negotiable-container");
    const addNonNegBtn = document.getElementById("add-non-negotiable");

    const DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];

    // =============================
    // Build empty calendar grid
    // =============================
    function buildCalendarGrid() {
        calendar.innerHTML = "";

        calendar.innerHTML += `<div></div>`;

        DAYS.forEach(day => {
            calendar.innerHTML += `<div class="day-header">${day}</div>`;
        });

        for (let hour = 0; hour < 24; hour++) {

            const label = hour.toString().padStart(2, "0") + ":00";
            calendar.innerHTML += `<div class="hour-label">${label}</div>`;

            DAYS.forEach(day => {
                calendar.innerHTML += `
                    <div class="cell"
                         data-day="${day}"
                         data-hour="${hour}">
                    </div>
                `;
            });
        }
    }

    buildCalendarGrid();

    // =============================
    // Add Flexible Task Row
    // =============================
    addTaskBtn.onclick = () => {

        const row = document.createElement("div");
        row.className = "task-row";

        row.innerHTML = `
            <input type="text" class="task-name" placeholder="Task Name">

            <select class="task-priority">
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
            </select>

            <input type="number" class="task-duration" placeholder="Duration (hours)">
        `;

        container.appendChild(row);
    };

    // =============================
    // Add Non-Negotiable Row
    // =============================
    addNonNegBtn.onclick = () => {

        const row = document.createElement("div");
        row.className = "non-neg-row";

        row.innerHTML = `
            <input type="text" class="nn-name" placeholder="Commitment Name">
            <input type="number" class="nn-start" min="0" max="23" placeholder="Start Hour">
            <input type="number" class="nn-end" min="0" max="23" placeholder="End Hour">

            <select class="nn-repeat">
                <option value="daily">Daily</option>
                <option value="weekday">Weekdays</option>
                <option value="weekend">Weekends</option>
            </select>
        `;

        nonNegContainer.appendChild(row);
    };

    // =============================
    // Render Schedule
    // =============================
    function renderSchedule(events) {

        document.querySelectorAll(".cell").forEach(cell => {
            cell.innerHTML = "";
            cell.style.position = "relative";
        });

        const ROW_HEIGHT = 50;

        events.forEach(event => {

            const startCell = document.querySelector(
                `.cell[data-day="${event.day}"][data-hour="${event.start_hour}"]`
            );

            if (!startCell) return;

            const block = document.createElement("div");
            block.className = "task-block";
            block.textContent = event.activity.task.task_name;

            const duration = event.end_hour - event.start_hour;

            block.style.position = "absolute";
            block.style.top = "2px";
            block.style.left = "2px";
            block.style.right = "2px";
            block.style.height = `${(duration * ROW_HEIGHT) - 4}px`;
            block.style.zIndex = "10";

            const priority = event.activity.task?.priority || "";
            const reason = event.activity.reason || "";
            const taskName = event.activity.task?.task_name || "";

            if (reason === "Fixed commitment") {
                block.classList.add("fixed");
            }
            else if (reason === "Protected slot") {
                block.classList.add("protected");
            }
            else if (priority === "Non-negotiable") {
                block.classList.add("non-negotiable");
            }
            else if (taskName === "Sleep") {
                block.classList.add("sleep");
            }
            else if (priority === "High") {
                block.classList.add("high");
            }
            else if (priority === "Medium") {
                block.classList.add("medium");
            }
            else {
                block.classList.add("low");
            }

            block.title = reason;

            startCell.appendChild(block);
        });
    }

    // =============================
    // Generate Schedule
    // =============================
    generateBtn.onclick = async () => {

        console.log("Generate button clicked");

        const rows = document.querySelectorAll(".task-row");
        let tasks = [];

        rows.forEach(row => {
            const name = row.querySelector(".task-name").value;
            const priority = row.querySelector(".task-priority").value;
            const duration = parseInt(row.querySelector(".task-duration").value);

            if (name && duration) {
                tasks.push({
                    task_name: name,
                    priority: priority,
                    duration_slots: duration
                });
            }
        });

        let non_negotiables = [];

        document.querySelectorAll(".non-neg-row").forEach(row => {

            const name = row.querySelector(".nn-name").value;
            const start = parseInt(row.querySelector(".nn-start").value);
            const end = parseInt(row.querySelector(".nn-end").value);
            const repeat = row.querySelector(".nn-repeat").value;

            if (name && !isNaN(start) && !isNaN(end)) {
                non_negotiables.push({
                    name: name,
                    start: start,
                    end: end,
                    repeat: repeat
                });
            }
        });

        if (tasks.length === 0 && non_negotiables.length === 0) {
            alert("Please enter at least one task or commitment.");
            return;
        }

        const response = await fetch("/schedule", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                tasks: tasks,
                fixed_commitments: [],
                protected_slots: [],
                non_negotiables: non_negotiables
            })
        });

        const data = await response.json();
        renderSchedule(data.schedule);
    };

});
