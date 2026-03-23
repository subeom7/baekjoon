# 2023 상반기 오전 1번 문제
from collections import deque
import heapq

N, M, K = map(int, input().split())

matrix = [list(map(int, input().split())) for _ in range(N)]
# 우/하/좌/상
laser_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# 방향 8개
cannon_directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

# 각 포탑이 언제 공격했는지 기록 필요, 포탑 죽을때 마다 del 해주어야함
# (r,c): 공격후 지난 시간
turret_attack_periods = {}

for i in range(N):
    for j in range(M):
        if matrix[i][j] != 0:
            turret_attack_periods[(i,j)] = 1

# 격자 밖으로 나가도 공격범위 가능
# r > N 이면 r % N하고 c > M 이면 c % M하면 될듯 다면 이 위치도 0이면 대상 x
def solve():
    for i in range(K):
        if is_end():
            break
        increase_turret_attack_period()
        attacker_r, attacker_c = find_weakest_turret()
        strongest_turret_r, strongest_turret_c = find_strongest_turret()
        matrix[attacker_r][attacker_c] += (N + M)
        # 레이저 공격 (공격 가능 여부 True, False 반환)
        affected_pos = find_laser_attack_target((attacker_r, attacker_c), (strongest_turret_r, strongest_turret_c))
        # 레이저 공격
        if affected_pos:
            for r, c in affected_pos:
                if (r,c) == (strongest_turret_r, strongest_turret_c):
                    matrix[r][c] -= matrix[attacker_r][attacker_c]
                else:
                    matrix[r][c] -= matrix[attacker_r][attacker_c] // 2
        else:
            # 포탄 공격
            affected_pos = cannon_attack((attacker_r, attacker_c), (strongest_turret_r, strongest_turret_c))

        turret_attack_periods[(attacker_r, attacker_c)] = 1

        # 포탑 정비: 공격할때 공격받지않은 1이상인 포탑 +1
        affected_pos.append((attacker_r, attacker_c))
        increase_turret_attack_power(affected_pos)
    return get_result()

        
def find_weakest_turret():
    minHeap = []
    for i in range(N):
        for j in range(M):
            if matrix[i][j] < 1:
                continue
            heapq.heappush(minHeap, (matrix[i][j], turret_attack_periods[(i,j)], -(i+j), -j, (i,j)))
    return heapq.heappop(minHeap)[4]

def find_strongest_turret():
    minHeap = []
    for i in range(N):
        for j in range(M):
            if matrix[i][j] < 1:
                continue
            heapq.heappush(minHeap, (-matrix[i][j], -turret_attack_periods[(i,j)], (i+j), j, (i,j)))
    return heapq.heappop(minHeap)[4]

def find_laser_attack_target(attacker_pos, strongest_turret_pos):
    global matrix
    ar, ac = attacker_pos
    sr, sc = strongest_turret_pos
    q = deque()
    q.append((ar, ac, []))
    visited = [[False] * M for _ in range(N)]
    visited[ar][ac] = True
    while q:
        r, c, paths = q.popleft()
        if (r,c) == (sr,sc):
            return paths
        
        for dr, dc in laser_directions:
            # 격자 밖으로 나와도 반대편으로 나오도록
            nr, nc = transform_coordinate(r + dr, c + dc)
            if matrix[nr][nc] < 1:
                continue
            if visited[nr][nc]:
                continue
            visited[nr][nc] = True
            q.append((nr, nc, paths + [(nr, nc)]))

    return []

def cannon_attack(attacker_pos, strongest_turret_pos):
    global matrix
    ar, ac = attacker_pos
    sr, sc = strongest_turret_pos
    affected_pos = []

    matrix[sr][sc] -= matrix[ar][ac]
    affected_pos.append((sr, sc))

    for dr, dc in cannon_directions:
        nr, nc = transform_coordinate(sr + dr, sc + dc)

        # 공격자는 스플레쉬 대미지 안받음!!!
        if matrix[nr][nc] < 1 or (nr, nc) == (ar, ac):
            continue

        matrix[nr][nc] -= matrix[ar][ac] // 2
        affected_pos.append((nr, nc))
    return affected_pos
    

# 공격이 끝난후 부서지지 않은 포탑 중 공격과 무관했던 포탑은 공격력이 1씩 증가
def increase_turret_attack_power(affected_pos):
    global matrix
    for i in range(N):
        for j in range(M):
            if matrix[i][j] > 0 and not (i,j) in affected_pos:
                matrix[i][j] += 1

# 공격한지 얼마 지났는지, 턴 지날 때마다 +1
def increase_turret_attack_period():
    global turret_attack_periods
    # 순회하면서 0이하 된 포탑은 del 
    for i in range(N):
        for j in range(M):
            if matrix[i][j] < 1 and turret_attack_periods.get((i,j)):
                del turret_attack_periods[(i,j)]
            elif turret_attack_periods.get((i, j)):
                turret_attack_periods[(i,j)] += 1

def transform_coordinate(r, c):
    if r >= N:
        r = r % N
    elif r < 0:
        r = N + r

    if c >= M:
        c = c % M
    elif c < 0:
        c = M + c
    return r, c

def is_end():
    turrent_count = 0
    for i in range(N):
        for j in range(M):
            if matrix[i][j] > 0:
                turrent_count += 1 
    return turrent_count == 1

def get_result():
    res = 0
    for i in range(N):
        for j in range(M):
           res = max(matrix[i][j], res)
    return res

print(solve())