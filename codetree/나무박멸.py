# 2022 상반기 오후 2번 문제
from collections import defaultdict
import heapq

n, m, K, C = map(int, input().split())

matrix = [list(map(int, input().split())) for _ in range(n)]

# 상하좌우
directions = [(-1,0), (1, 0), (0, -1), (0, 1)]

# 대각선 방향
diagonal_directions = [(1,1), (-1, 1), (1, -1), (-1, -1)]

# 재초제는 dict로 관리
# (r, c): period
weedkiller = defaultdict(int)

res = 0

def solve():
    for i in range(m):
        grow_trees()
        propagate_trees()
        decrease_weedkiller_period()
        apply_weedkiller()

def grow_trees():
    global matrix
    for i in range(n):
        for j in range(n):
            if matrix[i][j] > 0:
                for dr, dc in directions:
                    nr, nc = i + dr, j + dc
                    if 0 <= nr < n and 0 <= nc < n and matrix[nr][nc] > 0:
                        matrix[i][j] += 1


def propagate_trees():
    global matrix

    cells_to_update = []
    for i in range(n):
        for j in range(n):
            if matrix[i][j] > 0:
                propagate_cells = []
                for dr, dc in directions:
                    nr, nc = i + dr, j + dc
                    if 0 <= nr < n and 0 <= nc < n and matrix[nr][nc] == 0 and not weedkiller.get((nr, nc)):
                        propagate_cells.append((nr, nc))

                for dr, dc in propagate_cells:
                    # (r, c, num_to_add)
                    cells_to_update.append((dr, dc, matrix[i][j] // len(propagate_cells)))

    for r, c, num_to_add in cells_to_update:
        matrix[r][c] += num_to_add


def apply_weedkiller():
    global matrix, weedkiller, res
    _, r, c = find_most_affected_cell()
    res += matrix[r][c]
    matrix[r][c] = 0
    weedkiller[(r,c)] = C

    for dr, dc in diagonal_directions:
        for k in range(1, K + 1):
            nr, nc = r + dr * k, c + dc * k
            if 0 <= nr < n and 0 <= nc < n:
                if matrix[nr][nc] < 1:
                    if matrix[nr][nc] == 0:
                        weedkiller[(nr, nc)] = C
                    break
                else:
                    res += matrix[nr][nc]
                    matrix[nr][nc] = 0
                    weedkiller[(nr, nc)] = C

def find_most_affected_cell():
    # (num, r, c)
    # num은 큰 순서대로 이니까 - 붙여야함
    minHeap = []
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == -1:
                continue

            if matrix[i][j] == 0:
                heapq.heappush(minHeap, (0, i, j))
                continue
            cur_num = matrix[i][j]
            for dr, dc in diagonal_directions:
                for k in range(1, K + 1):
                    nr, nc = i + dr * k, j + dc * k
                    if 0 <= nr < n and 0 <= nc < n:
                        if matrix[nr][nc] < 1:
                            break
                        else:
                            cur_num += matrix[nr][nc]
            heapq.heappush(minHeap, (-cur_num, i, j))
    return heapq.heappop(minHeap) 

def decrease_weedkiller_period():
    global weedkiller

    for key, val in weedkiller.items():
        if val > 0:
            weedkiller[key] -= 1

solve()
print(res)
