# 14890. 경사로
N, L = map(int, input().split())

matrix = [list(map(int, input().split())) for _ in range(N)]

def solve():
    res = 0
    for i in range(N):
        res += validate(matrix[i])
    
    # transpose해서 col 방향 확인
    rotated = list(zip(*matrix))

    for i in range(N):
        res += validate(rotated[i])

    return res

def validate(lis):
    visited = [0] * len(lis)
    for i in range(len(lis) - 1):
        height_diff = lis[i + 1] - lis[i]
        if height_diff == 1:
            if i - L + 1 >= 0:
                for j in range(i - L + 1, i + 1):
                    if visited[j]:
                        return False
                    visited[j] = True
            else:
                return False
            
        elif height_diff == -1:
            if i + L < N:
                for j in range(i + 1, i + L + 1):
                    if visited[j] or lis[j] != lis[i + 1]:
                        return False
                    visited[j] = True
            else:
                return False

        elif height_diff != 0:
            return False

    return True

print(solve())