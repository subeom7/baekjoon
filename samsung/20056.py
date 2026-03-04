# 20056. 마법사 상어와 파이어볼
N, M, K = map(int, input().split())

# 파이어볼 관리 리스트
fireballs = []
directions = [(-1, 0), (-1, 1), (0, 1), (1,1), (1,0), (1, -1), (0, -1), (-1,-1)]

for i in range(M):
    fireballs.append(list(map(int, input().split()))) 
    fireballs[i][0] -= 1
    fireballs[i][1] -= 1

def solve():
    global fireballs
    res = 0
    for _ in range(K):
        pos_dict = {}
        move()
        for  r, c, m, s, d in fireballs:
            if not pos_dict.get((r,c)):
                pos_dict[(r,c)] = [m, s, d, True, 1] # m, s, d, direction_match, num_of_combination
            else:
                direction_match = (pos_dict[(r,c)][2] % 2 == d % 2) and pos_dict[(r,c)][3]
                pos_dict[(r,c)][0] += m
                pos_dict[(r,c)][1] += s
                pos_dict[(r,c)][3] = direction_match
                pos_dict[(r,c)][4] += 1
        fireballs = []
        for key, value in pos_dict.items():
            i, j = key
            if value[4] >= 2:
                mass = value[0] // 5
                speed = value[1] // value[4]
                if mass == 0:
                    continue
                dir = 0 if value[3] else 1
                for _ in range(4):
                    fireballs.append([i, j, mass, speed, dir])
                    dir += 2
            else:
                fireballs.append([i, j, value[0], value[1], value[2]])
    
    for balls in fireballs:
        res += balls[2]
    
    return res


def move():
    global fireballs
    for i in range(len(fireballs)):
        r, c, _, s, d = fireballs[i]
        nr, nc = directions[d]

        new_r = (r + nr * s) % N
        new_c = (c + nc * s) % N
        fireballs[i][0] = new_r
        fireballs[i][1] = new_c

print(solve())