# 14888. 연산자 끼워넣기

N = int(input())

arr = list(map(int, input().split()))

plus, minus, multiply, divide = map(int, input().split())

max_val = float("-inf")
min_val = float("inf")

def solve(index, cur_value, plus, minus, multiply, divide):
    global max_val, min_val
    
    if index == N:
        max_val = max(max_val, cur_value)
        min_val = min(min_val, cur_value)
        return
    
    op = arr[index]

    if plus:
        solve(index + 1, cur_value + op, plus - 1, minus, multiply, divide) 

    if minus:
        solve(index + 1, cur_value - op, plus, minus - 1, multiply, divide) 

    if multiply:
        solve(index + 1, cur_value * op, plus, minus, multiply - 1, divide) 

    if divide:
        solve(index + 1, int(cur_value / op), plus, minus, multiply, divide - 1) 

solve(1, arr[0], plus, minus, multiply, divide)

print(max_val)
print(min_val)