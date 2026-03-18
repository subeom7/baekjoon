# 2021 상반기 오전 1번 문제

# find_spot, calculate_score
# 순회하면서, 각 칸의 (좋아하는 인접하는 좋아하는 친구 수, 빈칸 수) 구함, for direction in directions
# 순서는 heap으로 유지

import heapq

N = int(input())

friends = [list(map(int, input().split())) for _ in range(N * N)]

friend_dict = {}

for friend in friends:
    friend_dict[friend[0]] = set(friend[1:])

matrix = [[0] * N for _ in range(N)]

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def solve():
    global matrix
    for friend in friends: 
        r,c = find_spot(friend)  
        matrix[r][c] = friend[0]
    
    return calculate_score()


def find_spot(friend):
    # (좋아하는 친구 수, 인접한 칸 중 비어있는칸, r, c)
    # # heapq.heappush(maxHeap, (-num_friends, -num_empty, r, c)) 
    heap = []
    
    for i in range(N):
        for j in range(N):
            num_friends = 0
            num_empty = 0
            if matrix[i][j] == 0:
                for dr, dc in directions:
                    nr, nc = i + dr, j + dc
                    if 0 <= nr < N and 0 <= nc < N:
                        if matrix[nr][nc] in friend:
                            num_friends += 1
                        elif matrix[nr][nc] == 0:
                            num_empty += 1
                heapq.heappush(heap, (-num_friends, -num_empty, i, j))
    res = heapq.heappop(heap)
    return res[2], res[3] 

def calculate_score():
    res = 0
    score = {
        0: 0,
        1: 1, 
        2: 10,
        3: 100,
        4: 1000
    }

    for i in range(N):
        for j in range(N):
            num_friends = 0
            for dr, dc in directions:
                nr, nc = i + dr, j + dc
                if 0 <= nr < N and 0 <= nc < N and matrix[nr][nc] in friend_dict[matrix[i][j]]:
                    num_friends += 1
            res += score[num_friends]

    return res

print(solve())