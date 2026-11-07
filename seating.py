from collections import defaultdict

SEATS_PER_BENCH = 2


def allocate(students, rooms):
    pools = defaultdict(list)
    for s in students:
        pools[s["branch"]].append(s)

    total_seats = sum(
        int(r["rows"]) * int(r["bench_cols"]) * SEATS_PER_BENCH for r in rooms
    )
    if len(students) > total_seats:
        raise ValueError(
            f"{len(students) - total_seats} students have no seat, add rooms"
        )

    plan = {}
    for room in rooms:
        rows, cols = int(room["rows"]), int(room["bench_cols"])
        grid = [[[None] * SEATS_PER_BENCH for _ in range(cols)] for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                for k in range(SEATS_PER_BENCH):
                    banned = set()
                    if k > 0 and grid[r][c][k - 1]:
                        banned.add(grid[r][c][k - 1]["branch"])
                    if k == 0 and c > 0 and grid[r][c - 1][SEATS_PER_BENCH - 1]:
                        banned.add(grid[r][c - 1][SEATS_PER_BENCH - 1]["branch"])
                    if r > 0 and grid[r - 1][c][k]:
                        banned.add(grid[r - 1][c][k]["branch"])

                    options = sorted(
                        (b for b in pools if pools[b]),
                        key=lambda b: len(pools[b]),
                        reverse=True,
                    )
                    if not options:
                        continue
                    choice = next((b for b in options if b not in banned), options[0])
                    grid[r][c][k] = pools[choice].pop(0)
        plan[room["room"]] = grid
    return plan


def find_seat(plan, query):
    q = query.strip().lower()
    matches = []
    if not q:
        return matches
    for room, grid in plan.items():
        cols = len(grid[0]) if grid else 0
        for r, row in enumerate(grid):
            for c, bench in enumerate(row):
                for k, s in enumerate(bench):
                    if s and (s["name"].lower() == q or s["roll_no"].lower() == q):
                        matches.append({
                            "room": room,
                            "row": r + 1,
                            "bench_col": c + 1,
                            "bench_no": r * cols + c + 1,
                            "side": "Left" if k == 0 else "Right",
                            "student": s,
                        })
    return matches