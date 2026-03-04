# 15665. N과 M (11)
N, M = map(int, input().split())

num_list = sorted(list(map(int, input().split())))

dup_check = set()

def solve(arr):
    if len(arr) == M:
        if str(arr) not in dup_check:
            print(*arr)
            dup_check.add(str(arr))
        return
    
    for i in range(N):
        arr.append(num_list[i])
        solve(arr)
        arr.pop()

solve([])