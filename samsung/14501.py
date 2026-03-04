# 14501. 퇴사
import sys
input = sys.stdin.readline

N = int(input())
schedule = [tuple(map(int, input().split())) for _ in range(N)]

# dp[i] = i일(0-index에서 i번째 날 시작)부터 N일까지 얻을 수 있는 최대 이익
# 편하게 dp[N] = 0을 두기 위해 길이 N+1
dp = [0] * (N + 1)

for i in range(N - 1, -1, -1):
    t, p = schedule[i]
    # 1) i일 상담을 한다면 i+t로 점프 (가능할 때만)
    take = p + dp[i + t] if i + t <= N else 0
    # 2) i일 상담을 안 하면 다음 날로
    skip = dp[i + 1]
    dp[i] = max(take, skip)

print(dp[0])