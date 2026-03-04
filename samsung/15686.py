# 15686. 치킨배달
N, M = map(int, input().split())
city = []
for _ in range(N):
    city.append(list(map(int, input().split())))
res = float('inf')
chicken_coordinates = []
for i in range(N):
    for j in range(N):
        if city[i][j] == 2:
            chicken_coordinates.append((i, j))

def solve(chicken_pos, index):
    global res
    if len(chicken_pos) == M:
        res = min(res, calculate_min_distance(chicken_pos))
        return

    for i in range(index + 1, len(chicken_coordinates)):
        chicken_pos.append(chicken_coordinates[i])
        solve(chicken_pos, i)
        chicken_pos.pop()

def calculate_min_distance(chicken_pos):
    min_sum = 0
    for i in range(N):
        for j in range(N):
            # 집 찾음, 그 집에서 가장 가까운 치킨집과의 거리 계산
            if city[i][j] == 1:
                cur_min = float('inf')
                for r, c in chicken_pos:
                    dist = abs(r-i) + abs(c - j)
                    cur_min = min(cur_min, dist)
            
                min_sum += cur_min
    return min_sum

solve([], -1)
print(res)