# 14889. 스타트와 링크
N = int(input())
matrix = []
for i in range(N):
    arr = list(map(int, input().split()))
    matrix.append(arr)

res = float("inf")

def solve(team1, index):
    global res
    if len(team1) == N / 2:
        team1_sum = 0

        team2 = [i for i in range(N) if i not in team1]
        team2_sum = 0
        for i in range(N // 2):
            for j in range(i + 1, N // 2):
                a, b = team1[i], team1[j]
                team1_sum += matrix[a][b] + matrix[b][a]

                c,d = team2[i], team2[j]
                team2_sum += matrix[c][d] + matrix[d][c]
                
        res = min(res, abs(team1_sum - team2_sum))
        return
    
    if index == N:
        return

    team1.append(index)
    solve(team1, index + 1)
    team1.pop()

    solve(team1, index + 1)

solve([], 0)

print(res)
    
