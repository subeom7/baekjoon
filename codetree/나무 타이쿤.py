# 2021 상반기 오후 1번 문제

# → ↗ ↑ ↖ ← ↙ ↓ ↘
# 1-indexed, 0번 안씀
directions = [(0,0), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]

n, m = map(int, input().split())

matrix = [list(map(int, input().split())) for _ in range(n)]

moves = []
for _ in range(m):
    d, p = map(int, input().split())
    moves.append((d, p))

# 초기 영양제 위치
supplements = {(n - 1, 0), (n - 2, 0), (n - 1, 1), (n - 2, 1)}

def solve():
    for d, p in moves:
        move_supplements(d, p)
        apply_supplements()
        cut_trees_and_buy_supplements()
    return calculate_height_sum()

def move_supplements(d, p):
    global supplements
    new_supplements = set()
    dr, dc = directions[d]

    for r, c in supplements:
        nr, nc = (r + dr * p) % n, (c + dc * p) % n
        new_supplements.add((nr, nc))

    supplements = new_supplements

def apply_supplements():
    global matrix
    for r, c in supplements:
        matrix[r][c] += 1

    for r, c in supplements:
        for i in range(2, len(directions), 2):
            dr, dc = directions[i]
            nr, nc = r + dr, c + dc

            if 0 <= nr < n and 0 <= nc < n and 1 <= matrix[nr][nc]:
                matrix[r][c] += 1

# 나무 자르고 영양제 재생성 
def cut_trees_and_buy_supplements():
    global supplements
    new_supplements = set()

    for i in range(n):
        for j in range(n):
            if (i, j) in supplements:
                continue
            if matrix[i][j] >= 2:
                matrix[i][j] -= 2
                new_supplements.add((i, j))
    supplements = new_supplements

def calculate_height_sum():
    res = 0
    for i in range(n):
        for j in range(n):
            res += matrix[i][j]
    return res

print(solve())