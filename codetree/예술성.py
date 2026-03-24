# 2022 상반기 오전 2번 문제
from collections import deque
N = int(input())

matrix = [list(map(int, input().split())) for _ in range(N)]

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def solve():
    res = 0
    for _ in range(4):
        group_info, group_matrix = get_group_info()
        res += calculate_score(group_info, group_matrix)

        # 십자가 반시계 회전
        rotate_cross_couterclockwise()

        # 좌상단
        rotate_squares_clockwise(0, 0, N // 2)

        # 우상단
        rotate_squares_clockwise(0, N // 2 + 1, N // 2)

        # 좌하단
        rotate_squares_clockwise(N // 2 + 1, 0, N // 2)

        # 우하단
        rotate_squares_clockwise(N // 2 + 1, N // 2 + 1, N // 2)

    return res

# returns [(그룹 a에 속한 칸의 수, 그룹 a를 이루고 있는 숫자 값), (그룹 b에 속한 칸의 수, 그룹 b를 이루고 있는 숫자 값), ...]   
def get_group_info():
    visited = [[-1] * N for _ in range(N)]
    group_num = 0
    group_info = []

    for i in range(N):
        for j in range(N):
            # if not visited
            if visited[i][j] == -1:
                q = deque()
                q.append((i,j))
                cur_num = matrix[i][j]
                visited[i][j] = group_num
                cell_count = 1

                while q:
                    r,c = q.popleft()
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < N and 0 <= nc < N and visited[nr][nc] == -1 and matrix[nr][nc] == cur_num:
                            visited[nr][nc] = group_num
                            cell_count += 1
                            q.append((nr, nc))

                group_info.append((cell_count, cur_num))
                group_num += 1

    return group_info, visited

def calculate_score(group_info, group_matrix):
    total = 0
    num_groups = len(group_info)
    
    adj_count = [[0] * num_groups for _ in range(num_groups)]

    for r in range(N):
        for c in range(N):
            current_group = group_matrix[r][c]
            
            for dr, dc in [(0, 1), (1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    neighbor_group = group_matrix[nr][nc]
                    
                    # 서로 다른 그룹이 맞닿아 있다면 카운트 증가
                    if current_group != neighbor_group:
                        adj_count[current_group][neighbor_group] += 1
                        adj_count[neighbor_group][current_group] += 1

    # 미리 구해둔 맞닿은 side 수 이용
    for i in range(num_groups - 1):
        for j in range(i + 1, num_groups):
            # 맞닿은 변이 존재하는 경우에만 계산
            if adj_count[i][j] > 0:
                score = (group_info[i][0] + group_info[j][0]) * group_info[i][1] * group_info[j][1] * adj_count[i][j]
                total += score
                
    return total


def calculate_num_of_overlaping_sides(i, j, group_matrix):
    count = 0
    for r in range(N):
        for c in range(N):
            if group_matrix[r][c] == i:
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < N and 0 <= nc < N:
                        if group_matrix[nr][nc] == j:
                            count += 1   
    return count

# 십자 모양 반시계 방향 회전
def rotate_cross_couterclockwise():
    global matrix
    cross_col = []
    cross_row = []

    for i in range(N):
        cross_row.append(matrix[i][N // 2])
        cross_col.append(matrix[N // 2][N - 1 - i])

    for i in range(N):
        matrix[i][N // 2] = cross_col[i]
        matrix[N // 2][i] = cross_row[i]

# 나머지 4개의 사각형 시계 방향 회전
def rotate_squares_clockwise(r, c, L):
    #global matrix
    temp_matrix = [[0] * L for _ in range(L)]

    for i in range(L):
        for j in range(L):
            temp_matrix[j][i] = matrix[L + r - i - 1][j + c]

    for i in range(L):
        for j in range(L):
            matrix[i + r][j + c] = temp_matrix[i][j]
print(solve())
