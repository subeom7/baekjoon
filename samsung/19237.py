# 19237. 어른 상어
from collections import defaultdict
# =================================== 변수 설계 ===================================
# N: 격자 N x N
# M: 상어 수
# K: 상어 냄새 지속 턴 수

# 0번은 안씀
# 1번 index: 상어 방향 상(1)일때 우선순위 차례대로 4개
# 2번 index: 상어 방향 하(2)일때 우선순위 차례대로 4개
# 3번 index: 상어 방향 좌(3)일때 우선순위 차례대로 4개
# 4번 index: 상어 방향 우(4)일때 우선순위 차례대로 4개
# dir_priority: {
#   shark_num : [[0,0,0,0], [], [], [], []]
# }

# 쫓겨난 상어는 (-1,-1,-1)로 처리
#   shark_position = {
#   shark_num: [r, c, d]
# }

# matrix: 
# [[[현재 냄새의 주인 번호, 냄새 남은 턴 수, 현재 상어 번호 / 0이면 없는것으로 간주], ...], [], ...]

# =================================== 함수 설계 ===================================
# 모든 상어가 동시에 이동한 후 한 칸에 여러 마리의 상어가 남아 있으면, 가장 작은 번호를 가진 상어를 제외하고 모두 격자 밖으로 쫓겨난다.
# 동시이동 구현하기 위해서는 번호가 낮은 상어가 더 우선 순위가 높으므로 번호가 낮은 순으로 먼저 이동함, 이때 이동할 칸에 자신보다 번호가 높은 상어가있더라도 일단 무시 (곧 움직일것이기 때문)
# 그 이후 상어가 이동하면서 이동할 칸에 자신보다 번호가 낮은 상어가있다면 그 상어는 이미 움직였을것이기 때문에, 지금 현재 움직이려는 상어는 쫓겨난것으로 처리 

# def decrease_smell_count: 상어가 움직이기전에 냄새가 존재하는 모든칸의 냄새 - 1 (칸에 냄새가 0이면 냄새 없는 것으로 간주, 이시점에 냄새 주인 번호도 0) 

# def move_sharks: 숫자가 낮은 상어부터 우선순위 고려해서 냄새가 없거나 (matrix[nr][nc][1] == 0 or matrix[nr][nc][0] == 현재 상어 번호, 이때는 다시 k개로 냄새 초기화)

# N: 격자 크기, M: 상어 수, k: 냄새 지속 턴 수
N, M, k = map(int, input().split())
shark_position = defaultdict(list)

# 0번 안씀
# 상, 하, 좌, 우
directions = [(0,0), (-1, 0), (1, 0), (0, -1), (0, 1)]

# matrix 구성
matrix = []
for i in range(N):
    row_data = list(map(int, input().split()))
    row = []
    for j in range(N):
        if row_data[j] != 0:
            # direction 일단은 0
            row.append([row_data[j], k, row_data[j]])
            shark_position[row_data[j]] = [i, j, 0]
        else:
            row.append([0, 0, 0])

    matrix.append(row)

# direction 받기
direction_inputs = list(map(int, input().split()))
for i in range(1, M + 1):
    r, c, _ = shark_position[i]
    shark_position[i][2] = direction_inputs[i - 1]

# direction 우선순위 받기
dir_priority = defaultdict(list)

for i in range(1, M + 1):
    dir_priority[i].append([0, 0, 0, 0])
    for _ in range(4):
        dir_priority[i].append(list(map(int, input().split())))

def solve():
    res = 0
    while True:    
        if is_end():
            return res
        if res >= 1000:
            return -1
        move_sharks()
        res += 1

# 디버깅용
def print_matrix():
    for i in range(N):
        print(matrix[i])

def move_sharks():
    # 하나의 격자안에는 하나의 상어밖이 존재하지 못한다고 가정 
    # 작은수부터 iterate할거니까, 이미 visited에 해당 (r,c)가 존재하면 현재 상어는 더 수가 큰 상어이기 때문에 그 칸에 들어오려는 순간 쫒겨남
    visited = set()

    # i = shark_num
    for i in range(1, M + 1):
        r, c, d = shark_position[i]

        # 이미 쫓겨난 상어는 스킵
        if r == -1:
            continue
        
        # 현재 상어에 해당하는 우선순위 방향
        move_priority = dir_priority[i][d]

        next_flag = True
        # 먼저 인접한 칸 중 아무 냄새가 없는 칸의 방향으로 잡음
        for dir_index in move_priority:
            dr, dc = directions[dir_index]
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N and matrix[nr][nc][1] == 0:
                if (nr,nc) not in visited:
                    shark_position[i] = [nr, nc, dir_index]
                    visited.add((nr,nc))     
                else:
                    shark_position[i] = [-1, -1, -1]

                # 상어 이동 후 이전 칸 처리
                matrix[r][c][2] = 0
                next_flag = False
                break

        # 아무 냄새가 없는 칸이 없으면 자신의 냄새가 있는 칸의 방향으로 잡음
        if next_flag:
            for dir_index in move_priority:
                dr, dc = directions[dir_index]
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N and matrix[nr][nc][0] == i:
                    if (nr,nc) not in visited:
                        shark_position[i] = [nr, nc, dir_index]     
                        visited.add((nr,nc))      
                    else:
                        shark_position[i] = [-1, -1, -1]

                    # 상어 이동 후 이전 칸 처리
                    matrix[r][c][2] = 0
                    break
    decrease_smell_count()
    update_matrix()


# 1번 상어만 생존하는지 체크
def is_end():
    for i in range(2, M + 1):
        r, _, _ = shark_position[i]
        if r != -1:
            return False
    return True

# update_matrix: 현재 shark_position 기반으로 matrix의 shark 상태 업데이트 필요할듯
def update_matrix():
    for i in range(1, M + 1):
        r, c, _ = shark_position[i]
        if r != -1:
            matrix[r][c] = [i, k, i]

def decrease_smell_count():
    for i in range(N):
        for j in range(N):
            if matrix[i][j][1] != 0:
                matrix[i][j][1] -= 1

            if matrix[i][j][1] == 0:
                matrix[i][j][0] = 0

print(solve())