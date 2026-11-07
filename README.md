# Exam Seating Generator

A web app that generates exam seating plans from CSV files. Students of the same branch are not seated next to each other.

## Tech stack
Python (Flask), Docker, Jenkins (CI/CD), Git and GitHub, pytest.

## How it works
1. data/students.csv holds roll number, name and branch.
2. data/rooms.csv holds each room with its rows and columns.
3. seating.py mixes the branches and fills the rooms seat by seat.
4. app.py shows the plan in the browser.
5. 5. Bench-based rooms: each bench has two seats, and neighbouring students are from different branches.
6. Students search by name or roll number to get a seat slip with room, block, floor, invigilator, bench and seat.
7. A room map shows the student's bench, and each room has a printable invigilator sheet.

## Run with Docker
    docker build -t exam-seating .
    docker run -p 5000:5000 exam-seating

Then open http://localhost:5000

## Run tests
    python -m pytest

## CI/CD pipeline (Jenkins)
Checkout, Install, Test, Docker Build, Deploy.

## Team
- ysh: seating logic, Flask app and web pages
- Tamanna: tests, Dockerfile, Jenkins pipeline, documentation
