# 2023 하반기 오후 1번 문제
from collections import deque

# N: 게임판 크기
# M: 게임 턴 수
# P: 산타의 수
# C: 루돌프의 힘
# D: 산타의 힘
N, M, P, C, D = map(int, input().split())

r,c = map(int, input().split())

rudolph_pos = (r - 1, c - 1)

# 1-index, 0사용 x
# -1은 격자 밖으로 밀려난 santa 표기
# r,c, 기절 여부, 현재 점수
santa_pos = [[-1, -1, -1, 0] for _ in range(P + 1)]

for _ in range(P):
    i, r, c = map(int, input().split())
    santa_pos[i] = [r - 1 ,c - 1, 0, 0]

# 대각선 포함
rudolph_directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (1,1), (-1,1), (1, -1), (-1,-1)]
# 상우하좌
santa_directions =[(-1, 0), (0, 1), (1, 0), (0, -1)]

def solve():
    for i in range(M):
        
        if is_end():
            break
        collision, santa_i, dr, dc = move_rudolph()
        # 충돌 발생
        if collision:
            collide(santa_i, dr, dc, C)

        move_santa()
        increase_score()
        disable_stun()

def move_rudolph():
    global rudolph_pos
    min_dist = float('inf')
    santa_r, santa_c = -1, -1
    santa_i = -1
    for i in range(1, P + 1):
        r, c, _, _= santa_pos[i]
        if r == -1:
            continue
        cur_dist = (r - rudolph_pos[0]) ** 2 + (c - rudolph_pos[1]) ** 2
        if cur_dist < min_dist:
            min_dist = cur_dist
            santa_r, santa_c = r, c
            santa_i = i
        elif cur_dist == min_dist:
            if r > santa_r:
                santa_r, santa_c = r, c
                santa_i = i
            elif r == santa_r:
                if c > santa_c:
                    santa_r, santa_c = r, c
                    santa_i = i

    min_rudolph_dist = float('inf')
    rudolph_r, rudolph_c = -1, -1
    rudolph_dr, rudolph_dc = 0, 0
    for dr, dc in rudolph_directions:
        nr, nc = dr + rudolph_pos[0], dc + rudolph_pos[1]
        cur_dist = (santa_r - nr) ** 2 + (santa_c - nc) ** 2
        if min_rudolph_dist > cur_dist:
            min_rudolph_dist = cur_dist
            rudolph_r, rudolph_c = nr, nc
            rudolph_dr, rudolph_dc = dr, dc

    rudolph_pos = (rudolph_r, rudolph_c)
    # 충돌 발생체크 해야함
    return min_rudolph_dist == 0, santa_i, rudolph_dr, rudolph_dc

def move_santa():
    global santa_pos
    for i in range(1, P + 1):
        r, c, stunned, _ = santa_pos[i]
        if stunned or r == -1:
            continue

        min_dist = (r - rudolph_pos[0]) ** 2 + (c - rudolph_pos[1]) ** 2
        min_r, min_c = -1, -1
        santa_dr, santa_dc = 0, 0

        for dr, dc in santa_directions:
            nr, nc = r + dr, c + dc
            next_dist = (nr - rudolph_pos[0]) ** 2 + (nc - rudolph_pos[1]) ** 2
            if 0 <= nr < N and 0 <= nc < N and not check_for_santa(nr, nc):
                if min_dist > next_dist:
                    min_dist = next_dist
                    min_r, min_c = nr, nc
                    santa_dr, santa_dc = dr, dc

        if min_r != -1:
            if (min_r, min_c) == rudolph_pos:
                santa_pos[i][0] = min_r
                santa_pos[i][1] = min_c
                # 충돌 발생!!!!!!!!!!!!!!!!!!!!!!!
                collide(i, -santa_dr, -santa_dc, D)
                pass
            else:
                santa_pos[i][0] = min_r
                santa_pos[i][1] = min_c

def check_for_santa(r, c):
    for i in range(1, P + 1):
        santa_r, santa_c, _, _ = santa_pos[i]
        if (r,c) == (santa_r, santa_c):
            return i
    return 0

def collide(santa_i, dr, dc, strength):
    q = deque()
    santa_pos[santa_i][2] = 2
    santa_pos[santa_i][3] += strength

    r, c = santa_pos[santa_i][0], santa_pos[santa_i][1]
    nr, nc = r + dr * strength, c + dc * strength

    # 충돌후 밀려난 위치가 격자 안일때
    if 0 <= nr < N and 0 <= nc < N:
        santa_index = check_for_santa(nr, nc)
        if santa_index:
            q.append(santa_index)
        santa_pos[santa_i][0] = nr
        santa_pos[santa_i][1] = nc
    # 충돌후 밀려난 위치가 격자 밖일때 탈락 판정
    else:
        santa_pos[santa_i][0] = -1
        santa_pos[santa_i][1] = -1
        santa_pos[santa_i][2] = -1

    while q:
        santa_num = q.popleft()
        r, c = santa_pos[santa_num][0], santa_pos[santa_num][1]
        nr, nc = r + dr, c + dc

        # 충돌후 밀려난 위치가 격자 안일때
        if 0 <= nr < N and 0 <= nc < N:
            santa_index = check_for_santa(nr, nc)
            if santa_index:
                q.append(santa_index)
            santa_pos[santa_num][0] = nr
            santa_pos[santa_num][1] = nc
        # 충돌후 밀려난 위치가 격자 밖일때 탈락 판정
        else:
            santa_pos[santa_num][0] = -1
            santa_pos[santa_num][1] = -1
            santa_pos[santa_num][2] = -1

def disable_stun():
    for i in range(1, P + 1):
        if santa_pos[i][2] > 0:
            santa_pos[i][2] -= 1

def is_end():
    for i in range(1, P + 1):
        if santa_pos[i][0] != -1:
            return False
    return True

def increase_score():
    global santa_pos
    for i in range(1, P + 1):
        if santa_pos[i][0] != -1:
            santa_pos[i][3] += 1
    return True
def print_score():
    for i in range(1, P + 1):
        print(santa_pos[i][3], end=" ")

solve()
print_score()