# 15652. N과 M (4)
N, M = map(int, input().split())

def solve(arr):
    if len(arr) == M:
        print(" ".join(map(str, arr)))
        return
    
    for i in range(1, N + 1):
        if arr and arr[-1] > i:
            continue
        arr.append(i)
        solve(arr)
        arr.pop()
solve([])

