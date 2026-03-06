# 19236. 청소년 상어

# [[(물고기 번호, 물고기 방향)], [...], [...], [...]]
matrix = []
# index가 물고기 번호, 각 칸은 (r, c, d), 0번은 사용하지 않음 
fish_arr = [None] * 17

# 0번 사용안함
# 1 ~ 8번
# ↑, ↖, ←, ↙, ↓, ↘, →, ↗
directions = [None, (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]

for i in range(4):
    row_list = []
    row = (list(map(int, input().split())))
    for j in range(0, 8, 2):
        row_list.append((row[j], row[j + 1]))
        fish_arr[row[j]] = (i, j // 2, row[j + 1])
    
    matrix.append(row_list)

# 죽은 물고기는 -1번으로 표기, 상어는 0번 표기
# 첫번째 칸 상어가 잡아먹고 direction 승계
first_fish_num, first_direction = matrix[0][0]
matrix[0][0] = (0, first_direction)
fish_arr[first_fish_num] = (-1, -1, -1)

res = 0
# 백트랙킹, 각 단계별로 move_fish한 matrix map이 있고 그 맵안에서 최대 상어가 3번 움직일수있음
# matrix, fish_arr, score, shark_r, shark_c는 각 상어 이동 마다 다시 복원할수 있어야함
def solve(matrix, fish_arr, score, shark_r, shark_c):
    global res
    res = max(res, score)
    move_fish(matrix, fish_arr)
    
    _, shark_dir_index = matrix[shark_r][shark_c]
    
    # 상어는 최대 3칸만 이동 가능
    for i in range(1, 4):
        dr, dc = directions[shark_dir_index]
        nr, nc = shark_r + dr * i, shark_c + dc * i

        # copy 안해주면 상어가 한번 움직이고 백트랙킹으로 돌아오면 손상된 맵에서 시작하므로 copy해줌 (deep copy는 느리니까 사용 x)
        if 0 <= nr < 4 and 0 <= nc < 4 and matrix[nr][nc][0] != -1:
            target_fish_num, target_fish_dir = matrix[nr][nc]
            matrix_copy = [row[:] for row in matrix]
            fish_arr_copy = fish_arr[:]

            # 상어 기존 인덱스 빈칸 처리
            matrix_copy[shark_r][shark_c] = (-1, -1)
            # 상어가 이동한 인덱스 0처리 및 기존 물고기 방향 승계
            matrix_copy[nr][nc] = (0, target_fish_dir)

            # fish_arr에서 기존 물고기 사망 처리
            fish_arr_copy[target_fish_num] = (-1, -1, -1)
            solve(matrix_copy, fish_arr_copy, score + target_fish_num, nr, nc)


def move_fish(matrix, fish_arr):
    # 1번 부터 16번 물고기 순회
    for i in range(1, 17):
        r, c, d = fish_arr[i]
        # 죽은 물고기는 스킵
        if r == -1:
            continue
        # 1번 부터 9번 까지 반시계 방향 순회
        for j in range(0, 8):
            # 0 방지를 위해 안에서 -1 밖에서 + 1 해서 45도 반시계 회전
            direction_index = (d + j - 1) % 8 + 1
            dr, dc = directions[direction_index]
            nr, nc = r + dr, c + dc

            if 0 <= nr < 4 and 0 <= nc < 4 and matrix[nr][nc][0] != 0:
                target_fish_num, target_fish_direction = matrix[nr][nc]
                # 만약 물고기가 있는 칸이었다면
                if target_fish_num != -1:
                    
                    # 변경할 대상 칸의 물고기의 기존 direciton 유지하고 r,c 만 업데이트
                    _, _, fish_dir = fish_arr[target_fish_num]
                    fish_arr[target_fish_num] = (r,c,fish_dir)
                
                # r,c 업데이트 하고 다음 칸 swap (-1,-1,-1)이어도 기존 칸이 빈칸이 되니 swap이 맞음
                fish_arr[i] = (nr, nc, direction_index)
                matrix[r][c] = (target_fish_num, target_fish_direction)
                matrix[nr][nc] = (i, direction_index)
                # 이동할 칸 찾았으면 중지
                break

# 첫번째 물고기 잡아먹은것도 점수에 포함
solve(matrix, fish_arr, first_fish_num, 0, 0)
print(res)
