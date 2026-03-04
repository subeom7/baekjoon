# 15654. N과 M (5)
N, M = map(int, input().split())

num_list = list(map(int, input().split()))

num_list.sort()
def solve(arr):
    if len(arr) == M:
        print(" ".join(map(str, arr)))
        return

    for num in num_list:
        if num in arr:
            continue
        arr.append(num)
        solve(arr)
        arr.pop()

solve([])