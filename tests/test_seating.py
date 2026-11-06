import pytest
from seating import allocate, find_seat


def test_no_adjacent_same_branch():
    students = [
        {"roll_no": str(i), "name": f"S{i}", "branch": b}
        for i, b in enumerate(["CSE", "ECE", "ME"] * 4)
    ]
    rooms = [{"room": "R1", "rows": 3, "cols": 4}]
    grid = allocate(students, rooms)["R1"]
    for row in grid:
        for a, b in zip(row, row[1:]):
            assert a["branch"] != b["branch"]


def test_not_enough_seats():
    students = [{"roll_no": "1", "name": "A", "branch": "CSE"}] * 5
    with pytest.raises(ValueError):
        allocate(students, [{"room": "R1", "rows": 1, "cols": 2}])


def test_find_seat_by_name_and_roll():
    students = [
        {"roll_no": "101", "name": "Aman", "branch": "CSE"},
        {"roll_no": "102", "name": "Divya", "branch": "ECE"},
    ]
    plan = allocate(students, [{"room": "R1", "rows": 1, "cols": 2}])
    assert find_seat(plan, "aman")[0]["room"] == "R1"
    assert find_seat(plan, "102")[0]["student"]["name"] == "Divya"


def test_find_seat_not_found():
    assert find_seat({"R1": [[None]]}, "xyz") == []