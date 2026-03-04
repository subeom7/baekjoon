# 15655. N과 M (6)
N, M = map(int, input().split())
num_list = list(map(int, input().split()))

num_list.sort()

def solve(index, arr):
    if len(arr) == M:
        print(*arr)
        return
    
    for i in range(index + 1, N):
        arr.append(num_list[i])
        solve(i, arr)
        arr.pop()

solve(-1, [])
