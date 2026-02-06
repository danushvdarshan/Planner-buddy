from flask import Flask, request, jsonify
from scheduler import generate_schedule

app = Flask(__name__)

@app.route("/")
def index():
    return "Planner Buddy Backend Running"

@app.route("/schedule", methods=["POST"])
def run_schedule():
    data = request.get_json()

    tasks = data["tasks"]

    fixed_commitments = []
    for fc in data.get("fixed_commitments", []):
        for slot in range(fc["start"], fc["end"]):
            fixed_commitments.append(
                (fc["day"], slot, fc["name"])
            )

    protected_slots = []
    for ps in data.get("protected_slots", []):
        for slot in range(ps["start"], ps["end"]):
            protected_slots.append(
                (ps["day"], slot, ps["name"])
            )

    schedule, unassigned = generate_schedule(
        tasks=tasks,
        fixed_commitments=fixed_commitments,
        protected_slots=protected_slots
    )

    return jsonify({
        "schedule": schedule,
        "unassigned_tasks": unassigned
    })

if __name__ == "__main__":
    app.run(debug=True)
