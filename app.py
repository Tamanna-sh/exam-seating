import csv
from flask import Flask, render_template
from seating import allocate

app = Flask(__name__)


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate")
def generate():
    students = read_csv("data/students.csv")
    rooms = [
        {"room": r["room"], "rows": int(r["rows"]), "cols": int(r["cols"])}
        for r in read_csv("data/rooms.csv")
    ]
    try:
        plan = allocate(students, rooms)
    except ValueError as e:
        return render_template("result.html", plan={}, error=str(e))
    return render_template("result.html", plan=plan, error=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)