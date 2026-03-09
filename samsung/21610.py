# 21610. 마법사 상어와 비바라기
N, M = map(int, input().split())

matrix = []
for _ in range(N):
    matrix.append(list(map(int, input().split())))

# (direction, 거리)
moves = []
for _ in range(M):
    moves.append(tuple(map(int, input().split())))

clouds = [[N - 1, 0], [N - 1, 1], [N - 2, 0], [N - 2, 1]]
previous_clouds = set()

# 0번 안씀
# ←, ↖, ↑, ↗, →, ↘, ↓, ↙ 
direcitons = [(0,0), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]

def solve():
    for direction, distance in moves:
        dr, dc = direcitons[direction]
        move(dr, dc, distance)
        get_cells_with_sufficient_water()
    return get_score()

def move(dr, dc, distance):
    global clouds
    for i in range(len(clouds)):
        clouds[i][0] = (clouds[i][0] + dr * distance) % N
        clouds[i][1] = (clouds[i][1] + dc * distance) % N

        r, c = clouds[i][0], clouds[i][1]
        matrix[r][c] += 1
        previous_clouds.add((r,c))
    
    for r, c in clouds:
        for i in range(2, len(direcitons), 2):
            dr, dc = direcitons[i]
            nr, nc = r + dr, c + dc

            if 0 <= nr < N and 0 <= nc < N and matrix[nr][nc] >= 1:
                matrix[r][c] += 1

def get_cells_with_sufficient_water():
    global clouds, previous_clouds
    new_clouds = []
    for i in range(N):
        for j in range(N):
            if (i, j) not in previous_clouds and matrix[i][j] >= 2:
                matrix[i][j] -= 2
                new_clouds.append([i, j])      
    
    clouds = new_clouds
    previous_clouds = set()

def get_score():
    res = 0 
    for i in range(N):
        for j in range(N):
            res += matrix[i][j]
    return res 

print(solve())