# 2024 상반기 오후 1번 문제
from collections import deque

def solve():
    R, C, K = map(int, input().split())

    moves = []
    matrix = [[0] * C for _ in range(R + 3)]

    #  북, 동, 남, 서
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    is_exit = [[False] * C for _ in range(R + 3)]
    res = 0

    for _ in range(K):
        c, d = map(int, input().split())
        moves.append((c - 1, d))
    
    # 움직일수 있는지 없는 지 return 반환 
    def move_down(pos):
        r, c = pos
        for dr, dc in directions:
            nr, nc = r + dr + 1, c + dc
            if not (0 <= nr < R + 3 and 0 <= nc < C and matrix[nr][nc] == 0):
                return False
        return True

    def move_left_and_down(pos):
        r, c = pos
        for dr, dc in directions:
            # 왼쪽 움직일수있는지
            nr, nc = r + dr, c + dc - 1
            if not (0 <= nr < R + 3 and 0 <= nc < C and matrix[nr][nc] == 0):
                return False
        # 왼쪽 움직인 상태에서 아래로 내려갈수있는지
        return move_down((r, c - 1))

    def move_right_and_down(pos):
        r, c = pos
        for dr, dc in directions:
            # 오른쪽 움직일수있는지
            nr, nc = r + dr, c + dc + 1
            if not (0 <= nr < R + 3 and 0 <= nc < C and matrix[nr][nc] == 0):
                return False
        # 오른쪽 움직인 상태에서 아래로 내려갈수있는지
        return move_down((r, c + 1))

    def is_out():
        for i in range(3):
            for j in range(C):
                if matrix[i][j] != 0:
                    return True
        return False
 
    def bfs(pos, is_exit, matrix):
        i, j = pos
        q = deque()
        
        max_r = i - 3
        visited = [[False] * C for _ in range(R + 3)]
        visited[i][j] = True
        q.append((i,j))
        while q:
            r, c = q.popleft()
            cur_golem = matrix[r][c]
            max_r = max(max_r, r - 3)

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R + 3 and 0 <= nc < C and not visited[nr][nc]:
                    if is_exit[r][c] and not visited[nr][nc] and matrix[nr][nc] != 0:
                        visited[nr][nc] = True
                        q.append((nr, nc))

                    elif matrix[nr][nc] == cur_golem:
                        visited[nr][nc] = True
                        q.append((nr, nc))

        return max_r + 1


    # 메인로직 시작
    for i in range(1, K + 1):
        c, d = moves[i - 1]
        r = 1
        cur_pos = []
        for dr, dc in directions:
            #  북, 동, 남, 서
            cur_pos.append([r + dr, c + dc])

        # 4번 인덱스에 중앙 좌표 추가
        cur_pos.append([r,c])

        while True:
            if move_down(cur_pos[4]):
                for pos in cur_pos:
                    pos[0] += 1 

            elif move_left_and_down(cur_pos[4]):
                for pos in cur_pos:
                    pos[0] += 1 
                    pos[1] -= 1
                # 출구 위치 업데이트
                d = (d - 1) % 4
            elif move_right_and_down(cur_pos[4]):
                for pos in cur_pos:
                    pos[0] += 1 
                    pos[1] += 1
                # 출구 위치 업데이트
                d = (d + 1) % 4
            else:
                break
        
        # 실제 마지막 위치 matrix에 그리기
        for r, c in cur_pos:
            matrix[r][c] = i
        
        # 보드, is_exit 초기화
        if is_out():
            matrix = [[0] * C for _ in range(R + 3)]
            is_exit = [[False] * C for _ in range(R + 3)]
        else:
            exit_r, exit_c = cur_pos[d]
            is_exit[exit_r][exit_c] = True
            res += bfs(cur_pos[4], is_exit, matrix)

    return res

print(solve())