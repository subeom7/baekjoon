# 15664. N과 M (10)
N, M = map(int, input().split())

num_list = sorted(list(map(int, input().split())))

dup_check = set()

visited = [False] * N
def solve(index, arr):
    if len(arr) == M:
        if str(arr) not in dup_check:
            print(*arr)
            dup_check.add(str(arr))
        return
    
    for i in range(index + 1, N):
        if visited[i]:
            continue
        
        visited[i] = True
        arr.append(num_list[i])
        solve(i, arr)
        visited[i] = False
        arr.pop()

solve(-1, [])