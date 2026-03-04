# 14891. 톱니바퀴
# previous_pole == current_pole 회전 안함
from collections import deque

# N극은 0, S극은 1

# 1-indexed이기때문에 0번인덱스는 빈값으로 대체
gears = [[deque()]]
for _ in range(4):
    gears.append(deque(map(int, input())))
K = int(input())

spins = [] #[(gear number, direction)]
for _ in range(K):
    spins.append(tuple(map(int, input().split())))

def solve():
    for gear_num, direction in spins:

        left_pole_match = gears[gear_num][6] == gears[gear_num - 1][2] if gear_num != 1 else True
        right_pole_match = gears[gear_num][2] == gears[gear_num + 1][6] if gear_num != 4 else True
        
        gears[gear_num].rotate(direction)

        left_direction = direction
        right_direction = direction
        # 왼쪽으로 전파
        for i in range(gear_num - 1, 0, -1):
            if not left_pole_match:
                left_direction *= -1
                if i > 1:
                    left_pole_match = gears[i][6] == gears[i - 1][2]
                gears[i].rotate(left_direction)
            else:
                # 회전이 멈출시 전파도 멈춤
                break
        
        # 오른쪽으로 전파
        for i in range(gear_num + 1, 5):
            if not right_pole_match:
                right_direction *= -1
                if i < 4:
                    right_pole_match = gears[i][2] == gears[i + 1][6]
                gears[i].rotate(right_direction)
            else:
                # 회전이 멈출시 전파도 멈춤
                break
    
    # 점수 계산
    res = 0
    for i in range(4):
        res += gears[i + 1][0] * (2 ** i)
    return res

print(solve())