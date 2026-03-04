# 13458. 시험 감독
import sys

num_room = int(sys.stdin.readline())
room = list(map(int, sys.stdin.readline().split()))
main_advisor_limit, sub_advisor_limit = tuple(map(int, sys.stdin.readline().split()))
res = num_room

for i in room:
    base = i - main_advisor_limit
    if base > 0:
        q, r = divmod(base, sub_advisor_limit)
        res += q + (1 if r != 0 else 0)

print(res)