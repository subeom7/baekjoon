# 16236. 아기상어
from collections import deque
import heapq
N = int(input())

matrix = []

for _ in range(N):
    matrix.append(list(map(int, input().split())))

fish_pos = set()
cur_shark_size = 2
ate_fish_count = 0

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

for i in range(N):
    for j in range(N):
        if matrix[i][j] == 9:
            shark_pos = (i, j)
            matrix[i][j] = 0
        
        elif matrix[i][j] in [1, 2, 3, 4, 5, 6]:
            fish_pos.add((i, j)) # i, j, 물고기 크기

def solve():
    global cur_shark_size, ate_fish_count, shark_pos
    res = 0
    while True:
        sec, r, c = bfs()
        if not sec:
            break
        else:
            res += sec
            shark_pos = (r, c)
            ate_fish_count += 1
            if cur_shark_size == ate_fish_count:
                cur_shark_size += 1
                ate_fish_count = 0
    return res

def bfs(): # i, j is the position of target fish
    global shark_pos, fish_pos
    q = deque()
    shark_r, shark_c = shark_pos
    q.append((shark_r, shark_c, 0)) # (shark_r, shark_c, seconds) 
    visited = [[False] * N for _ in range(N)]
    minHeap = []
    visited[shark_r][shark_c] = True

    while q:
        r, c, sec = q.popleft()
        visited[r][c] = True
        
        # heap에 계족 넣지말고 넣기전 확인해서 조기 종료
        if minHeap and minHeap[0][0] < sec:
            break
        if 0 < matrix[r][c] < cur_shark_size:
             heapq.heappush(minHeap, (sec, r, c)) # 가장 빨리 도착한 케이스들 heap push 해서 비교 r -> c 작은 순으로

        for nr, nc in directions:
            if r + nr < 0 or r + nr >= N or c + nc < 0 or c + nc >= N or matrix[r + nr][c +nc] > cur_shark_size or visited[r + nr][c + nc]:
                continue     
            q.append((r + nr, c + nc, sec + 1))
            visited[r + nr][c + nc] = True
        
         # 기존 물고기 먹은걸로 처리
    if minHeap:
        fish_pos.remove((minHeap[0][1], minHeap[0][2]))
        matrix[minHeap[0][1]][minHeap[0][2]] = 0 

    return minHeap[0] if minHeap else (None, None, None)


print(solve())