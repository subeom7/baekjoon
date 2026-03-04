# 14499. 주사위 굴리기
N, M, x, y, K = map(int, input().split())

matrix = []
for _ in range(N):
    matrix.append(list(map(int, input().split())))

moves = list(map(int, input().split()))

# 1-indexed 이므로 0번 index 무시
dice = [0, 0, 0, 0, 0, 0, 0]
directions = [(0,0), (0, 1), (0, -1), (-1, 0), (1, 0)]

def solve():
    global x, y, matrix
    for direction in moves:
        nr, nc = directions[direction]
        if not (0 <= x + nr < N and 0 <= y + nc < M):
            continue
        x, y = x + nr, y + nc
        roll(direction)
        if matrix[x][y] == 0:
            matrix[x][y] = dice[6]
        else:
            dice[6] = matrix[x][y]
            matrix[x][y] = 0
        
        print(dice[1])

def roll(direction):
    # 위, 북, 동, 서, 남, 아래
    d1, d2, d3, d4, d5, d6 = dice[1], dice[2], dice[3], dice[4], dice[5], dice[6]

    # ========= 동쪽이나 서쪽으로 움직일때 2와5의 위치에는 영향이 없음 ==========

    # 동쪽으로 움직일때
    if direction == 1:
        dice[1], dice[3], dice[4], dice[6] = d4, d1, d6, d3

    # 서쪽으로 움직일때
    elif direction == 2:
        dice[1], dice[3], dice[4], dice[6] = d3, d6, d1, d4
    
    # ========= 북쪽이나 남쪽으로 움직일때 4와3의 위치에는 영향이 없음 ===========

    # 북쪽으로 움직일때
    elif direction == 3:
        dice[1], dice[2], dice[5], dice[6] = d5, d1, d6, d2
    
    # 남쪽으로 움직일때
    elif direction == 4:
        dice[1], dice[2], dice[5], dice[6] = d2, d6, d1, d5

solve()