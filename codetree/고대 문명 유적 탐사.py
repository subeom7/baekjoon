# 2024 상반기 오전 1번 문제
from collections import deque
import heapq

K, M = map(int, input().split())

matrix = [list(map(int, input().split())) for _ in range(5)]

relic_nums = list(map(int, input().split()))

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

relic_index = 0

def print_matrix():
    for row in matrix:
        print(row)

def solve():
    for _ in range(K):
        res = 0
        if not rotate_matrix():
            return
        
        point = 1
        while point:
            point = get_relic()
            res += point
            refill_matrix()
        print(res, end=" ")

# 실제 matrix 각 9개 좌표를 돌면서 90, 180, 270도 회전 해보고 유물 1차 획득 가치가 가장높은 matrix를 저장해놓고 마지막에 실제 matrix로 바꿔치기함
def rotate_matrix():
    global matrix
    minHeap = []
    for i in range(1, 4):
        for j in range(1, 4):
            new_matrix = [row[:] for row in matrix]
            for rotate_degree in range(3):
                new_matrix = rotate_90(new_matrix, i, j)
                relic_count = check_relic(new_matrix)
                if relic_count:
                    heapq.heappush(minHeap, (-relic_count, rotate_degree, j, i, new_matrix))
    if not minHeap:
        return False
    matrix = heapq.heappop(minHeap)[4]
    return True
     
def rotate_90(new_matrix, i ,j):
    matrix_copy = [row[:] for row in new_matrix]
    for r in range(-1, 2):
        for c in range(-1, 2):
            new_r = c
            new_c = -r
            matrix_copy[i + new_r][j + new_c] = new_matrix[i + r][j + c]
    return matrix_copy


# 유물 1차 획득 가치 최대화 확인용
def check_relic(new_matrix):
    visited = [[False] * 5 for _ in range(5)]
    res = 0

    for i in range(5):
        for j in range(5):
            if not visited[i][j]:
                count = 0
                q = deque()
                q.append((i, j))
                visited[i][j] = True
                cur_num = new_matrix[i][j]

                while q:
                    count += 1
                    r, c = q.popleft()
                    for dr, dc in directions:
                        nr, nc = r + dr, dc + c
                        if 0 <= nr < 5 and 0 <= nc < 5 and not visited[nr][nc] and new_matrix[nr][nc] == cur_num:
                            visited[nr][nc] = True
                            q.append((nr, nc))

                res += count if count >= 3 else 0
    return res
                    
    

# 실제 유물 연쇄 획득
def get_relic():
    global matrix
    res = 0
    visited = [[False] * 5 for _ in range(5)]
    for i in range(5):
        for j in range(5):
            
            if not visited[i][j]:
                q = deque()
                q.append((i, j))
                visited[i][j] = True
                cur_num = matrix[i][j]
                components = []
                components.append((i,j))
                while q:
                    r, c = q.popleft()
                    for dr, dc in directions:
                        nr, nc = r + dr, dc + c
                        if 0 <= nr < 5 and 0 <= nc < 5 and not visited[nr][nc] and matrix[nr][nc] == cur_num and matrix[nr][nc] != -1:
                            visited[nr][nc] = True      
                            q.append((nr, nc))
                            components.append((nr, nc))
                if len(components) >= 3:
                    res += len(components)
                    for r, c in components:
                        matrix[r][c] = -1
    return res


def refill_matrix():
    global relic_index, matrix
    minHeap = []
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == -1:
                heapq.heappush(minHeap, (j, -i, i, j))

    while minHeap:
        _, _, r, c = heapq.heappop(minHeap)
        matrix[r][c] = relic_nums[relic_index]
        relic_index += 1

solve()