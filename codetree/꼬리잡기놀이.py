# 2022 상반기 오후 1번 문제
from collections import deque
N, M, K = map(int, input().split())

matrix = [list(map(int, input().split())) for _ in range(N)]

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def solve():
    res = 0
    for turn in range(K):
        move_people()
        res += move_ball(turn)
    return res

# 머리사람 따라 한칸 이동
def move_people():
    global matrix
    matrix_copy = [row[:] for row in matrix]
    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 3:
                visited = [[False] * N for _ in range(N)]
                visited[i][j] = True
                nr, nc = find_next_pos(i, j, visited)
                q = deque()
                q.append((i,j, nr, nc))
                while q:
                    r, c, nr, nc = q.popleft()
                    
                    if matrix[r][c] == 3:
                        matrix_copy[r][c] = 4
                        
                    if nr is None or nc is None:
                        break
                        
                    matrix_copy[nr][nc] = matrix[r][c]
                    visited[nr][nc] = True 
                    if matrix[r][c] == 1:
                        break
                        
                    next_r, next_c = find_next_pos(nr, nc, visited)
                    q.append((nr, nc, next_r, next_c))
    matrix = matrix_copy

def find_next_pos(r, c, visited):
    if matrix[r][c] == 1:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N:
                if not visited[nr][nc] and matrix[nr][nc] == 4:
                    return nr, nc
                elif matrix[nr][nc] == 3: 
                    return nr, nc
                
    elif matrix[r][c] == 3:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N and not visited[nr][nc] and matrix[nr][nc] == 2:
                return nr, nc
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N and not visited[nr][nc] and matrix[nr][nc] == 1:
                return nr, nc
    else: 
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N and not visited[nr][nc] and matrix[nr][nc] in [1, 2]:
                return nr, nc
                
    return None, None

def calculate_point(i, j):
    q = deque()
    visited = [[False] * N for _ in range(N)]
    if matrix[i][j] == 1:
        return 1
    if matrix[i][j] == 3:
        q = deque()
        count = 1
        q.append((i, j))
        visited[i][j] = True

        while q:
            r, c = q.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N and not visited[nr][nc] and matrix[nr][nc] in [1, 2]:
                    count += 1
                    visited[nr][nc] = True
                    q.append((nr, nc))
        return count * count


    
    q.append((i,j, 1))
    visited[i][j] = True

    while q:
        r, c, point = q.popleft()
        if matrix[r][c] == 4 or matrix[r][c] == 3:
            continue
        if matrix[r][c] == 1:
            return point * point
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N and not visited[nr][nc] and matrix[nr][nc] in [2, 1]:
                q.append((nr, nc, point + 1))
                visited[nr][nc] = True
    return point * point


# 공을 획득한 팀은 머리사람과 꼬리사람이 바뀜
def swap_head_and_tail(i, j):
    global matrix
    visited = [[False] * N for _ in range(N)]
    q = deque()
    count = 1
    q.append((i, j))
    visited[i][j] = True

    while q:
        r, c = q.popleft()
        if matrix[r][c] == 1:
            matrix[r][c] = 3
        elif matrix[r][c] == 3:
            matrix[r][c] = 1

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N and not visited[nr][nc] and matrix[nr][nc] in [1, 2, 3]:
                count += 1
                visited[nr][nc] = True
                q.append((nr, nc))

def move_ball(cur_turn):
    cur_round = (cur_turn // N) % 4
    point = 0

    if cur_round == 0:
        for j in range(N):
            if 1 <= matrix[cur_turn % N][j] <=3:
                point = calculate_point(cur_turn % N, j)
                swap_head_and_tail(cur_turn % N, j)
                break
    elif cur_round == 1:
        for i in range(N - 1, -1, -1):
            if 1 <= matrix[i][cur_turn % N] <=3:
                point = calculate_point(i, cur_turn % N)
                swap_head_and_tail(i, cur_turn % N)
                break
    
    elif cur_round == 2:
        for j in range(N - 1, -1, -1):
            if 1 <= matrix[N - cur_turn % N - 1][j] <=3:
                point = calculate_point(N - cur_turn % N - 1, j)
                swap_head_and_tail(N - cur_turn % N - 1, j)
                break
    elif cur_round == 3:
        for i in range(N):
            if 1 <= matrix[i][N - cur_turn % N - 1] <=3:
                point = calculate_point(i, N - cur_turn % N - 1)
                swap_head_and_tail(i, N - cur_turn % N - 1)
                break
    return point

def print_matrix():
    for row in matrix:
        print(row)
print(solve())