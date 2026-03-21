# 2023 상반기 오후 1번 문제
import heapq
N, M, K = map(int, input().split())

matrix = [list(map(int, input().split())) for _ in range(N)]

people = []

move_count = 0
# 상하좌우
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

for _ in range(M):
    r,c = map(int, input().split())
    people.append((r - 1, c - 1))

r,c  = map(int, input().split())
exit_pos = (r - 1, c - 1)

def solve():
    for _ in range(K):
        move_people()

        if is_end():
            return
        
        L, r, c = find_square()
        rotate_square_clockwise(L, r, c)


def move_people():
    global people, move_count
    new_list = []
    for r,c in people:
        cur_dis = abs(r - exit_pos[0]) + abs(c - exit_pos[1])
        for dr, dc in directions:
            nr = r + dr
            nc = c + dc
            next_dis = abs(nr - exit_pos[0]) + abs(nc - exit_pos[1])

            # 탈출성공
            if (nr, nc) == exit_pos:
                move_count += 1
                break

            # 탈출구와 가까워지므로 이동
            if 0 <= nr < N and 0 <= nc < N and matrix[nr][nc] <= 0 and next_dis < cur_dis:
                new_list.append((nr, nc))
                move_count += 1
                break

        # 이동 못했음
        else:
            new_list.append((r,c))

    people = new_list

def is_end():
    return len(people) == 0

# 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형 찾기
# 가장 작은 크기를 갖는 정사각형이 2개 이상이면, 좌상단 r 좌표가 작은 것이 우선됨, 그래도 같으면 c 좌표가 작은 것이 우선됨
# L = max(abs(exit_r - person_r), abs(exit_c - person_c))  
def find_square():
    exit_r, exit_c = exit_pos
    minHeap = []
    for person_r, person_c in people:
        cur_L = max(abs(exit_r - person_r), abs(exit_c - person_c)) + 1
 
        # sr <= exit_r < sr + L
        # sr <= exit_r
        # exit_r < sr + L
        # exit_r - L < sr
        # exit_r - L < sr <= exit_r
        # person_r - L < sr <= person_r
        # sc 도 마찬가지 로직
        
        # sr의 가능한 범위
        sr_left = max(exit_r - cur_L + 1, person_r - cur_L + 1, 0)
        # sc의 가능한 범위
        sc_left = max(exit_c - cur_L + 1, person_c - cur_L + 1, 0)

        #sr_right = min(exit_r, person_r, N - 1 - cur_L)
        #sc_right = min(exit_c, person_c, N - 1 - cur_L)
        
        # sr, sc는 좌상단 좌표
        heapq.heappush(minHeap, (cur_L, sr_left, sc_left))

    return heapq.heappop(minHeap)

def find_square_bruteforce():
    exit_r, exit_c = exit_pos
    for L in range(2, N + 1):
        for i in range(N - L + 1):
            for j in range(N - L + 1):
                if not (i <= exit_r < i + L and j <= exit_c < j + L):
                    continue

                for people_r, people_c in people:
                    if i <= people_r < i + L and j <= people_c < j + L:
                        return L, i, j
                    
# 위에서 선택된 정사각형을 시계방향으로 90도 회전, 회전된 벽은 내구도가 1씩 깎임
def rotate_square_clockwise(L, r, c):
    global matrix, exit_pos, people
    new_matrix = [[0] * L for _ in range(L)]
    for i in range(L):
        for j in range(L):
            new_matrix[i][j] = matrix[r + L - j - 1][c + i]
            if 0 < new_matrix[i][j]:
                new_matrix[i][j] -= 1

    for i in range(r, r + L):
        for j in range(c, c + L):
            matrix[i][j] = new_matrix[i - r][j - c]

    # 탈출구 회전
    exit_r, exit_c = exit_pos
    if r <= exit_r < r + L and c <= exit_c < c + L:
        rel_r, rel_c = exit_r - r, exit_c - c
        rot_r, rot_c = rel_c, L - rel_r - 1

        exit_pos = (rot_r + r, rot_c + c)

    # 사람 회전
    for i in range(len(people)):
        people_r, people_c = people[i]
        if r <= people_r < r + L and c <= people_c < c + L:
            rel_r, rel_c = people_r - r, people_c - c
            rot_r, rot_c = rel_c, L - rel_r - 1
            people[i] = (rot_r + r, rot_c + c)


solve()
print(move_count)
print(f"{exit_pos[0] + 1} {exit_pos[1] + 1}")