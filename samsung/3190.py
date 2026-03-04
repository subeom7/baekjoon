# 3190. 뱀
from collections import deque
N = int(input())
K = int(input())
apple_pos = deque()
for _ in range(K):
    r, c = map(int, input().split())
    apple_pos.append((r - 1, c - 1))

L = int(input())

direction_change = deque()
for _ in range(L):
    x, c = input().split()
    direction_change.append((int(x), c))

def solve():
    cur_time = 0
    snake_q = deque()
    snake_q.append((0, 0))
    direction_index = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while True:
        direction = None
        if direction_change and direction_change[0][0] == cur_time:
            direction = direction_change[0][1]
            direction_change.popleft()
        
        if direction == "D":
            direction_index = (direction_index + 1) % 4
        elif direction == "L":
            direction_index = (direction_index - 1) % 4
        
        nr, nc = directions[direction_index]

        r, c = nr + snake_q[0][0], nc + snake_q[0][1]

        cur_time += 1

        if r < 0 or r >= N or c < 0 or c >= N or (r, c) in snake_q:
            return cur_time

        snake_q.appendleft((r, c))
        if (r,c) not in apple_pos:
            snake_q.pop()
        else:
            apple_pos.remove((r,c))

print(solve())