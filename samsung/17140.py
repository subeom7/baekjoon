# 17140. 이차원 배열과 연산

# R 연산: 배열 A의 모든 행에 대해서 정렬을 수행한다. 행의 개수 ≥ 열의 개수인 경우에 적용된다.
# C 연산: 배열 A의 모든 열에 대해서 정렬을 수행한다. 행의 개수 < 열의 개수인 경우에 적용된다.

# 0은 무시
# 각 연산이 끝나고 가장 큰 row나 col을 기준으로 0을 채워줘야함
# 행 또는 열의 크기가 100을 넘어가는 경우에는 처음 100개를 제외한 나머지는 버린다.

# r_operation은 쉽고 c_operation은 그냥 matrix transpose한다음 r_operation하고 다시 matrix transpose로 되돌려놓으면 될듯

from collections import Counter
r, c, k = map(int, input().split())

# 1-indexed에서 0-indexed로 변경
r -= 1
c -= 1

matrix = []
for _ in range(3):
    matrix.append(list(map(int, input().split())))

def solve():
    res = 0

    while res <= 100:
        # 매칭 찾음
        if 0 <= r < len(matrix) and 0 <= c < len(matrix[0]) and matrix[r][c] == k:
            return res
        
        # 행의 개수 ≥ 열의 개수인 경우
        if len(matrix) >= len(matrix[0]):
            r_operation()

        # 행의 개수 < 열의 개수인 경우
        else:
            c_operation()
        
        res += 1
    return -1

# 각 숫자의 frequency map 구해서 row 재구성해야함
# 주의: 계산 시 0 제외해야함
def r_operation():
    global matrix
    max_r = 0
    new_matrix = []
    for i in range(len(matrix)):
        filtered_list = [val for val in matrix[i] if val != 0]
        freq_map = Counter(filtered_list)

        # 수의 등장 횟수가 커지는 순으로, 그러한 것이 여러가지면 수가 커지는 순으로 정렬
        sorted_freq_map = sorted(freq_map.items(), key=lambda x: (x[1], x[0]))
        new_row = []

        for key, freq in sorted_freq_map:
            new_row.extend([key, freq])

        # 100개 넘어가면 잘라냄
        new_row = new_row[:100]
        new_matrix.append(new_row)
        max_r = max(max_r, len(new_row))
    
    for row in new_matrix:
        target_zeros = max_r - len(row)
        row.extend([0] * target_zeros)
         
    matrix = new_matrix

def c_operation():
    global matrix

    # A^T
    matrix = list(map(list, zip(*matrix)))
    r_operation()
    # 다시 한번더 A^T 해서 복원
    matrix = list(map(list, zip(*matrix)))

print(solve())