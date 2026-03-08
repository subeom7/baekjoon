# 2023 하반기 오전 1번 문제

# 각 기사는 list(list) 형태로 관리하면 좋을듯, 각 인덱스가 기사 번호 [None, [r, c, h, w, k], ... ], 0번 사용 하지 않고, 죽은기사는 None으로 표현
# 함정과 벽은 고정이니 matrix 그대로 사용

# ========== 함수 ===============
# can_move: 왕의 order를 따랐을때 한명이라도 벽 (range 밖도 포함)에 부딪히는 기사가 있는지 확인. 있다면 empty set. 없다면 움직일 knight_set return. 아마 bfs로 확인?
# solve: 메인 함수, 명령들 iterate하면서 실행 
# def apply_damage 기사별로 연쇄적으로 충돌하여 이동후 각 기사들의 범위안에 몇개의 trap이있는지 카운트 해서 k 감소시킴 (0되면 기사 사라지도록 None처리 및 knigh_damage도 0처리)
# 처음 왕의 명령을 따른 기사는 데미지 x

# move_knights: 실제로 knights들의 위치를 이동시키고 처음 명령을 받은 knight를 제외한 다른 knights들을 리스트 형태로 반환
from collections import deque
L, N, Q = map(int, input().split())

# r,c,h,w,k
knights = [None]
knights_damage = [0] * (N + 1)

# [[knight_num, d], ...]
orders = []
# 상, 우, 하 좌
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

matrix = []
for _ in range(L):
    matrix.append(list(map(int, input().split())))

for i in range(1, N + 1):
    knight = list(map(int, input().split()))
    # r,c 0-indexed로 바꿔줌
    knight[0] -= 1
    knight[1] -= 1
    
    knights.append(knight)

for i in range(Q):
    orders.append(list(map(int, input().split())))

def solve():
    for knight_num, d in orders:
        # 이미 사라진 기사에 대해 명령인지 확인 (이경우 스킵해야함)
        if not knights[knight_num]:
            continue

        knights_to_move = can_move(knight_num, d)
        if knights_to_move:
            move_knights(knights_to_move, d)
            knights_to_move.remove(knight_num) # 명령을 받은 기사는 데미지 안받으니까 뺌
            apply_damage(knights_to_move)
    return sum(knights_damage)

def can_move(start_night, d):
    knights_to_move = set()
    q = deque([start_night])

    while q:
        knight_num = q.popleft()
        knights_to_move.add(knight_num)
        r, c, h, w, _ = knights[knight_num]

        dr,dc = directions[d]

        nr, nc = r + dr, c + dc

        # 벽 부딪히는지 확인
        for i in range(nr, nr + h):
            for j in range(nc, nc + w):
                if not (0 <= i < L and 0 <= j < L) or matrix[i][j] == 2:
                    return set()
        
        for other_idx in range(1, N + 1):
            if other_idx in knights_to_move or not knights[other_idx]:
                continue
            
            tr, tc, th, tw, _ = knights[other_idx]

            # 이중 하나라도 해당되면 안겹침
            # 현재 knight의 최대 높이 인덱스가 other knight의 최소보다 작은지
            # 또는 other knight의 최대 높이 인덱스가 현재 knight의 최소 높이 index보다 낮은지
            # 또는 현재 knight의 최대 넓이 인덱스가 other knight의 최소보다 작은지
            # 또는 other knight의 최대 넓이 인덱스가 현재 knight의 최소넓이 index보다 낮은지
            # not으로 complement하면 겹치는지 확인
            if not (tr + th <= nr or nr + h <= tr or tc + tw <= nc or nc + w <= tc):
                knights_to_move.add(other_idx)
                q.append(other_idx)

    return knights_to_move

def move_knights(knight_set, d):
    dr, dc = directions[d]
    for knight_num in knight_set:
        knights[knight_num][0] += dr
        knights[knight_num][1] += dc
    return

def apply_damage(moved_knights):
    for knight_num in moved_knights:
        r,c,h,w,k = knights[knight_num]
        damage = 0
        for i in range(r, r + h):
            for j in range(c, c + w):
                if matrix[i][j] == 1:
                    damage += 1

        if k - damage <= 0:
            knights[knight_num] = None
            knights_damage[knight_num] = 0
        else:
            k -= damage
            knights_damage[knight_num] += damage
            knights[knight_num] = [r,c,h,w,k]

print(solve())