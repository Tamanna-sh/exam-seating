import csv
from flask import Flask, render_template, request
from seating import allocate, find_seat

app = Flask(__name__)


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_plan():
    students = read_csv("data/students.csv")
    rooms = [
        {"room": r["room"], "rows": int(r["rows"]), "cols": int(r["cols"])}
        for r in read_csv("data/rooms.csv")
    ]
    return allocate(students, rooms)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/find")
def find():
    query = request.args.get("q", "")
    try:
        plan = build_plan()
    except ValueError as e:
        return render_template("seat.html", matches=[], query=query, error=str(e))
    matches = find_seat(plan, query)
    return render_template("seat.html", matches=matches, query=query, error=None)


@app.route("/generate")
def generate():
    try:
        plan = build_plan()
    except ValueError as e:
        return render_template("result.html", plan={}, error=str(e))
    return render_template("result.html", plan=plan, error=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)