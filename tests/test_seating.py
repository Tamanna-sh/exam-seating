import pytest
from seating import allocate, find_seat
from app import app

ROOM = [{"room": "R1", "rows": "2", "bench_cols": "2"}]


def make_students(n):
    branches = ["CSE", "ECE", "ME"]
    return [
        {"roll_no": str(100 + i), "name": f"S{i}", "branch": branches[i % 3],
         "class": "B.Tech", "year": "3"}
        for i in range(n)
    ]


def test_same_bench_different_branch():
    plan = allocate(make_students(8), ROOM)
    for row in plan["R1"]:
        for bench in row:
            if bench[0] and bench[1]:
                assert bench[0]["branch"] != bench[1]["branch"]


def test_front_back_different_branch():
    grid = allocate(make_students(8), ROOM)["R1"]
    for r in range(1, len(grid)):
        for c in range(len(grid[r])):
            for k in range(2):
                a, b = grid[r][c][k], grid[r - 1][c][k]
                if a and b:
                    assert a["branch"] != b["branch"]


def test_not_enough_seats():
    with pytest.raises(ValueError):
        allocate(make_students(9), ROOM)


def test_find_seat_by_roll_and_name():
    plan = allocate(make_students(8), ROOM)
    assert find_seat(plan, "100")[0]["room"] == "R1"
    assert find_seat(plan, "s1")[0]["student"]["roll_no"] == "101"


def test_find_seat_not_found():
    assert find_seat({"R1": [[[None, None]]]}, "xyz") == []


def test_health_route():
    assert app.test_client().get("/health").data == b"ok"


def test_search_route():
    response = app.test_client().get("/find?q=101")
    assert response.status_code == 200
    assert b"Aman" in response.data
