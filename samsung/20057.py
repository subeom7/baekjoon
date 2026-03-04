# 20057. 마법사 상어와 토네이도
import math
N = int(input())
matrix = []
for _ in range(N):
    matrix.append(list(map(int, input().split())))

# r, c, ratio
# 마지막은 alpha 칸임
sand_ratio = [
    [-1,  1, 0.01], [1,  1, 0.01],
    [-1,  0, 0.07], [1,  0, 0.07],
    [-2,  0, 0.02], [2,  0, 0.02],
    [-1, -1, 0.10], [1, -1, 0.10],
    [0, -2, 0.05],
    [0, -1, 0.00]   # alpha
]
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def solve():
    res = 0
    dir_index = 0
    r, c = N // 2, N // 2
    moves_per_turn = 1

    while r >= 0 and c >= 0:
        nr, nc = directions[dir_index % 4]
        if dir_index % 2 == 0 and dir_index != 0:
            moves_per_turn += 1

        for _ in range(moves_per_turn):
            r = r + nr
            c = c + nc
            if r >= N or r < 0 or c >= N or c < 0:
                continue
            res += create_tornado(r, c)
        
        dir_index += 1
        rotate_90_to_counterclockwise()
    
    return res
    
def create_tornado(r, c):
    res = 0
    alpha = 0
    for ratio in sand_ratio:
        nr, nc, value = ratio
        value_to_add = math.floor(matrix[r][c] * value) if value != 0 else matrix[r][c] - alpha
        if 0 <= r + nr < N and 0 <= c + nc < N: 
            matrix[r + nr][c + nc] += value_to_add
        else:
            res += value_to_add
        alpha += value_to_add
    return res

def rotate_90_to_counterclockwise():
    global sand_ratio
    for i in range(len(sand_ratio)):
        r,c, _ = sand_ratio[i]
        sand_ratio[i][0] = -c
        sand_ratio[i][1] = r

print(solve())