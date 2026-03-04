# 23288. 주사위 굴리기 2
from collections import deque
N, M, K = map(int, input().split())

matrix = []
# 동, 남, 서, 북
# -1 모듈러 반시계 90도, + 1 모듈러 시계 90도
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# 0 사용 x
# 위, 북, 동, 서, 남, 아래
dice = [0, 1, 2, 3, 4, 5, 6]

# 0: 동
# 1: 남
# 2: 서
# 3: 북
# 얘도 모듈러 연산으로 관리
# dice roll 방향 + matrix directions index에 동시에 쓰임
direction_index = 0

for _ in range(N):
    matrix.append(list(map(int, input().split())))

def solve():
    global direction_index
    res = 0
    r, c = 0, 0

    for i in range(K):
        nr, nc = directions[direction_index]
        if not (0 <= r + nr < N and 0 <= c + nc < M):
            direction_index = (direction_index + 2) % 4
            nr, nc = directions[direction_index]
        
        r, c = r + nr, c + nc
        roll(direction_index)
        res += bfs(r, c)
        
        # 주사위 자체를 rotate 할필요가 없었음
        # 시계방향 90도 회전
        if matrix[r][c] < dice[6]:
            #rotate(1)
            direction_index = (direction_index + 1) % 4
        # 반시계방향 90도 회전
        elif matrix[r][c] > dice[6]:
            #rotate(-1)
            direction_index = (direction_index - 1) % 4
    
    return res

def roll(direction):
    global dice
    d1, d2, d3, d4, d5, d6 = dice[1], dice[2], dice[3], dice[4], dice[5], dice[6]

    # 동, 서로 굴릴때는 2, 5 영향 없음
    # 동쪽으로 굴리기
    if direction == 0:
        dice[1], dice[3], dice[4], dice[6] = d4, d1, d6, d3
    # 서쪽으로 굴리기
    elif direction == 2:
        dice[1], dice[3], dice[4], dice[6] = d3, d6, d1, d4

    # 북, 남으로 굴릴때는 3, 4 영향 없음
    # 남쪽으로 굴리기
    elif direction == 1:
        dice[1], dice[2], dice[5], dice[6] = d2, d6, d1, d5
    # 북쪽으로 굴리기
    elif direction == 3:
        dice[1], dice[2], dice[5], dice[6] = d5, d1, d6, d2


# 문제 이해 잘못함, 방향을 90도 돌려야하는데, 주사위도 같이 90도 돌리고있었음 (이 함수 필요없음)
# 1 이면 clockwise 90도, -1이면 counter-clockwise 90도 
@DeprecationWarning
def rotate(direction):
    # rotate는 아래 윗면은 안움직임 (1, 6번 고정)
    d2, d3, d4, d5 = dice[2], dice[3], dice[4], dice[5]

    # 시계방향 90도
    if direction == 1:
        dice[2], dice[3], dice[4], dice[5] = d4, d2, d5, d3

    # 반시계방향 90도
    elif direction == -1:
        dice[2], dice[3], dice[4], dice[5] = d3, d5, d2, d4

def bfs(r, c):
    q = deque()
    matrix_copy = [matrix[i][:] for i in range(N)]
    visited = [[False] * M for _ in range(N)]

    count = 1
    q.append((r, c))
    visited[r][c] = True

    while q:
        i, j = q.popleft()

        for nr, nc in directions:
            if 0 <= i + nr < N and 0 <= j + nc < M and not visited[i + nr][j + nc] and matrix_copy[i + nr][j + nc] == matrix_copy[r][c]:
                count += 1
                visited[i + nr][j + nc] = True
                q.append((i + nr, j + nc))
    
    return count * matrix_copy[r][c]

print(solve())
