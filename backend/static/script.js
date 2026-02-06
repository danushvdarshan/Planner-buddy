console.log("JS LOADED");

document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("generate");
    const output = document.getElementById("output");

    btn.onclick = async () => {
        console.log("Button clicked");

        const response = await fetch("/schedule", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                tasks: [
                    {
                        task_name: "GATE Preparation",
                        priority: "High",
                        duration_slots: 30
                    }
                ],
                fixed_commitments: [],
                protected_slots: []
            })
        });

        const data = await response.json();

        output.innerHTML = ""; // clear old output

        const schedule = data.schedule;

        if (schedule.length === 0) {
            output.textContent = "No schedule generated.";
            return;
        }

        schedule.forEach(event => {
            const line = document.createElement("div");

            const taskName = event.activity.task.task_name;
            const start = event.start_hour.toString().padStart(2, "0");
            const end = event.end_hour.toString().padStart(2, "0");

            line.textContent =
                `${event.day} | ${start}:00 - ${end}:00 → ${taskName}`;

            output.appendChild(line);
        });
    };
});

