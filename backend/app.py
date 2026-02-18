
from scheduler import generate_schedule
from calendar_builder import build_events
from flask import Flask, request, jsonify, send_from_directory, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/schedule", methods=["POST"])
def run_schedule():
    data = request.get_json()
    non_negotiables = data.get("non_negotiables", [])

    tasks = data.get("tasks",[])

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
        protected_slots=protected_slots,
        non_negotiables=non_negotiables
    )
    
    events = build_events(schedule)
    
    return jsonify({
        "schedule": events,
        "unassigned_tasks": unassigned
    })

if __name__ == "__main__":
    app.run(debug=True)
