# 21611. 마법사 상어와 블리자드
N, M = map(int, input().split())

matrix = []
blizzards = []
for _ in range(N):
    matrix.append(list(map(int, input().split())))

for _ in range(M):
    blizzards.append(tuple(map(int, input().split()))) # [(d1, s1), (d2, s2), ...] 형태

# 상 하 좌 우
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# 좌 하 우 상
snail_directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

shark_r, shark_c = N // 2, N // 2

# 상어 위치는 -1로 표시
matrix[shark_r][shark_c] = -1
res = 0

def solve():
    for i in range(len(blizzards)):
        d, s = blizzards[i]
        apply_blizzard(d,s)
        flattened_matrix = shift_matrix()
        flat_list_to_reconstruct = explode_marbles(flattened_matrix)

        # 마지막이면 reconstruct 필요없으므로 조기 종료
        if i != len(blizzards) - 1:
            group_and_reconstruct_marbles(flat_list_to_reconstruct)
    return res

# 1단계: 블리자드 공격 시행
def apply_blizzard(d, s):
    global matrix

    # d는 1-indexed이기때문에 방향 구할때 -1 해줘야함
    nr, nc = directions[d - 1]

    # 블리자드 떨궈서 구멍내기
    for i in range(s, 0, -1):
        matrix[shark_r + nr * i][shark_c + nc * i] = 0

# 2단계: 블라자드 공격으로 뚫린 위치를 매꾸기 위해 구슬 shift
def shift_matrix():
    flattened_matrix = []
    dir_index = 0
    moves_per_turn = 1
    r, c = shark_r, shark_c

    # 1차원 matrix 만들기
    while r != 0 or c != 0:
        nr, nc = snail_directions[dir_index % 4]
        for _ in range(moves_per_turn):
            r += nr
            c += nc

            if matrix[r][c] != 0:
                flattened_matrix.append(matrix[r][c])

            if r == 0 and c == 0:
                break
        
        dir_index += 1
        if dir_index % 2 == 0 and dir_index !=0:
            moves_per_turn += 1

    return flattened_matrix

# 3단계: 4개 이상 반복되는 구슬이 있을 시 폭발, 폭발 가능한 구슬 없을때 까지 반복
# return 1번 구슬 개수 * 1, 2번 구슬 개수 * 2, 3번 구슬 개수 * 3
def explode_marbles(flat_list):
    global res
    marbles = [x for x in flat_list if x != 0]
    exploded_counts = {1: 0, 2: 0, 3: 0} 
    
    while True:
        explode_flag = False
        next_marbles = []
        n = len(marbles)
        l = 0

        while l < n:
            r = l
            while r < n and marbles[r] == marbles[l]:
                r += 1
            
            count = r - l
            
            if count >= 4:
                explode_flag = True
                exploded_counts[marbles[l]] += count
            else:
                next_marbles.extend(marbles[l:r])
            
            l = r
        marbles = next_marbles
        
        if not explode_flag:
            break
            
    # 점수 계산 (1번*1 + 2번*2 + 3번*3)
    res += exploded_counts[1] * 1 + exploded_counts[2] * 2 + exploded_counts[3] * 3
    
    return marbles

# 4단계: 구슬들을 그룹화하고 그룹화된 기준으로 matrix를 재건
def group_and_reconstruct_marbles(flat_list):
    global matrix
    matrix = [[0] * N for _ in range(N)]
    l, r = 0, 0
    new_list = []
    n = len(flat_list)

    # grouping 및 새 1차원 리스트 생성
    while l < n:
        while r < n and flat_list[l] == flat_list[r]:
            r += 1

        new_list.append(r - l)
        new_list.append(flat_list[l])
        l = r

    dir_index = 0
    moves_per_turn = 1
    r, c = shark_r, shark_c
    index = 0

    # 1차원 리스트 다시 2차원으로 재건
    while (r != 0 or c != 0) and index < len(new_list):
        nr, nc = snail_directions[dir_index % 4]
        for _ in range(moves_per_turn):
            r += nr
            c += nc
            
            matrix[r][c] = new_list[index] if index < len(new_list) else 0
            index += 1

            if r == 0 and c == 0:
                break

        dir_index += 1
        if dir_index % 2 == 0 and dir_index !=0:
            moves_per_turn += 1

print(solve())