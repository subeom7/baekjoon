# 20055. 컨베이어 벨트 위의 로봇
from collections import deque
N, K = map(int, input().split())

# (내구도, 로봇 유무)
belt = deque()
A = list(map(int, input().split()))
for i in range(N * 2):
    belt.append([A[i], 0])

def solve():
    res = 0
    while True:
        res += 1
        belt.rotate(1)
        belt[N-1][1] = 0

        move_robots()
        belt[N-1][1] = 0

        if belt[0][0] != 0:
            belt[0][1] = 1
            belt[0][0] -= 1

        if count_zero_durabilities():
            return res  

def count_zero_durabilities():
    count = 0
    for durability, _ in belt:
        if durability == 0:
            count += 1
        
        if count >= K:
            return True
        
    return False

def move_robots():
    for i in range(N - 2, -1 ,-1):
        # 로봇 스스로 한칸 이동
        if belt[i][1] == 1 and belt[i + 1][1] == 0 and belt[i + 1][0] >= 1:
            belt[i][1] = 0
            belt[i + 1][1] = 1
            belt[i + 1][0] -= 1

print(solve())
