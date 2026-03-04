# 15657. N과 M (8)
N, M = map(int, input().split())
num_list = list(map(int, input().split()))

num_list.sort()

def solve(arr):
    if len(arr) == M:
        print(*arr)
        return
    
    for i in range(N):
        if arr and arr[-1] > num_list[i]:
            continue
        arr.append(num_list[i])
        solve(arr)
        arr.pop()

solve([])