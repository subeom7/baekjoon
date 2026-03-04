# 15649. N과 M (1)
N, M = map(int, input().split())

visited = [False] * (N + 1)

def solve(list):
    if len(list) == M:
        print(*list)
        return
    
    for i in range(1, N + 1):
        if visited[i]:
            continue
        visited[i] = True
        list.append(i)
        solve(list)
        list.pop()
        visited[i] = False

solve([])
