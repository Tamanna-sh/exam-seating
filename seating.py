from itertools import zip_longest
from collections import defaultdict


def interleave_by_branch(students):
    groups = defaultdict(list)
    for s in students:
        groups[s["branch"]].append(s)
    ordered = sorted(groups.values(), key=len, reverse=True)
    result = []
    for batch in zip_longest(*ordered):
        result.extend(s for s in batch if s)
    return result


def allocate(students, rooms):
    queue = interleave_by_branch(students)
    plan, i = {}, 0
    for room in rooms:
        grid = [[None] * room["cols"] for _ in range(room["rows"])]
        for r in range(room["rows"]):
            for c in range(room["cols"]):
                if i < len(queue):
                    grid[r][c] = queue[i]
                    i += 1
        plan[room["room"]] = grid
    if i < len(queue):
        raise ValueError(f"{len(queue) - i} students have no seat, add rooms")
    return plan