# 15651. N과 M (3)
N, M = map(int, input().split())

def solve(arr, index):
    if len(arr) == M:
        print(" ".join(map(str, arr)))
        return
    
    for i in range(1, N + 1):
        arr.append(i)
        solve(arr, i)
        arr.pop()
solve([], 0)

