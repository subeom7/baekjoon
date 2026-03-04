# 15663. N과 M (9)
N, M = map(int, input().split())

num_list = sorted(list(map(int, input().split())))

dup_check = set()

visited = [False] * N
def solve(arr):
    if len(arr) == M:
        if str(arr) not in dup_check:
            print(*arr)
            dup_check.add(str(arr))
        return
    
    for i in range(N):
        if visited[i]:
            continue
        
        visited[i] = True
        arr.append(num_list[i])
        solve(arr)
        visited[i] = False
        arr.pop()

solve([])