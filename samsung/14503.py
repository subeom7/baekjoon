# 14503. 로봇 청소기
N, M = map(int, input().split())
r, c, d = map(int, input().split())

matrix = []

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

res = 0

for _ in range(N):
    matrix.append(list(map(int, input().split())))

def solve(r, c, d, matrix):
    global res
    if matrix[r][c] == 0:
        matrix[r][c] = 2
        res += 1

    if check_empty_cell(r, c, matrix): # 현재 칸의 주변 4칸 중 청소되지 않은 빈 칸이 있는 경우
        for i in range(1, 5):
            # 90도 회전
            next_direction = d - i if d - i >= 0 else 4 + (d - i)
            nr, nc = directions[next_direction]
            if 0 <= r + nr < N and 0 <= c + nc < M and matrix[r + nr][c + nc] == 0:
                solve(r + nr, c + nc, next_direction, matrix)
                break
            
    else: # 현재 칸의 주변 4칸 중 청소되지 않은 빈 칸이 없는 경우
        backward_direction = (d + 2) % 4
        nr, nc = directions[backward_direction]
        # 뒤로 후진
        if 0 <= r + nr < N and 0 <= c + nc < M and matrix[r + nr][c + nc] != 1:
            solve(r + nr, c + nc, d, matrix)
        else:
            return
            
def check_empty_cell(r, c, matrix):
    global directions
    for nr, nc in directions:       
        if 0 <= r + nr < N and 0 <= c + nc < M and matrix[r + nr][c + nc] == 0:
            return True

    return False

solve(r, c, d, matrix)
print(res)