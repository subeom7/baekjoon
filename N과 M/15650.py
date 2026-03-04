# 15650. N과 M (2)
N, M = map(int, input().split())

def solve(arr, index):
    if len(arr) == M:
        print(" ".join(map(str, arr)))
        return
    
    for i in range(index + 1, N + 1):
        arr.append(i)
        solve(arr, i)
        arr.pop()
solve([], 0)

