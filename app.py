import csv
import json
from collections import Counter
from flask import Flask, render_template, request, abort
from seating import allocate, find_seat

app = Flask(__name__)


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_config():
    with open("config.json", encoding="utf-8-sig") as f:
        return json.load(f)


def build_plan():
    return allocate(read_csv("data/students.csv"), read_csv("data/rooms.csv"))


def room_info(room_name):
    for r in read_csv("data/rooms.csv"):
        if r["room"] == room_name:
            return r
    return {}


@app.route("/")
def index():
    return render_template("index.html", config=load_config())


@app.route("/health")
def health():
    return "ok"


@app.route("/find")
def find():
    query = request.args.get("q", "")
    config = load_config()
    try:
        plan = build_plan()
    except ValueError as e:
        return render_template("slip.html", matches=[], query=query, error=str(e), config=config)
    matches = find_seat(plan, query)
    for m in matches:
        info = room_info(m["room"])
        m["block"] = info.get("block", "")
        m["floor"] = info.get("floor", "")
        m["invigilator"] = info.get("invigilator", "")
    return render_template("slip.html", matches=matches, query=query, error=None, config=config)


@app.route("/map/<room>/<int:bench_no>")
def room_map(room, bench_no):
    plan = build_plan()
    if room not in plan:
        abort(404)
    return render_template(
        "map.html", room=room, grid=plan[room], info=room_info(room),
        highlight=bench_no, config=load_config(),
    )


@app.route("/generate")
def generate():
    config = load_config()
    try:
        plan = build_plan()
    except ValueError as e:
        return render_template("result.html", plan={}, rooms={}, error=str(e), config=config)
    rooms = {r["room"]: r for r in read_csv("data/rooms.csv")}
    return render_template("result.html", plan=plan, rooms=rooms, error=None, config=config)


@app.route("/sheet/<room>")
def sheet(room):
    plan = build_plan()
    if room not in plan:
        abort(404)
    cols = len(plan[room][0])
    entries = []
    for r, row in enumerate(plan[room]):
        for c, bench in enumerate(row):
            for k, s in enumerate(bench):
                if s:
                    entries.append({
                        "bench_no": r * cols + c + 1,
                        "side": "Left" if k == 0 else "Right",
                        "student": s,
                    })
    return render_template(
        "invigilator.html", room=room, entries=entries,
        info=room_info(room), config=load_config(),
    )


@app.route("/stats")
def stats():
    students = read_csv("data/students.csv")
    rooms = read_csv("data/rooms.csv")
    benches = sum(int(r["rows"]) * int(r["bench_cols"]) for r in rooms)
    seats = benches * 2
    return render_template(
        "stats.html", total=len(students), rooms=len(rooms), benches=benches,
        seats=seats, free=seats - len(students),
        by_branch=dict(Counter(s["branch"] for s in students)),
        config=load_config(),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)