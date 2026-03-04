# 14502. 연구소
from collections import deque

N, M = map(int, input().split())
matrix = []
for _ in range(N):
    matrix.append(list(map(int, input().split())))

res = 0
empty_pos = []
virus_pos = []
for i in range(N):
    for j in range(M):
        if matrix[i][j] == 0:
            empty_pos.append((i, j))
        elif matrix[i][j] == 2:
            virus_pos.append((i, j))

def solve(wall_pos, index):
    global res
    if len(wall_pos) == 3:
        res = max(res, calculate_safety_cells(wall_pos))
        return
    
    for i in range(index + 1, len(empty_pos)):
        wall_pos.append(empty_pos[i]) # [(i, j)] 형태임
        solve(wall_pos, i)
        wall_pos.pop()

def calculate_safety_cells(wall_pos):
         
    matrix_copy = [row[:] for row in matrix]
    q = deque([pos for pos in virus_pos])
    safety_count = len(empty_pos) - 3

    directions = [(1,0), (-1, 0), (0, 1), (0, -1)]

    while q:
        r, c = q.popleft()
        for nr, nc in directions:
            if r + nr < 0 or c + nc < 0 or r + nr >= N or c + nc >= M or matrix_copy[r + nr][c + nc] != 0 or (r + nr, c + nc) in wall_pos:
                        continue
            matrix_copy[r + nr][c + nc] = -1
            safety_count -= 1
            q.append((r + nr, c + nc))

    return safety_count

solve([], -1)
print(res)