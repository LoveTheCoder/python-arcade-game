def array_manipulation(n, operations):
    arr = [0] * (n + 1)
    for start, end, value in operations:
        arr[start - 1] += value
        if end < n:
            arr[end] -= value
    max_val = 0
    running_sum = 0
    for x in arr:
        running_sum += x
        if running_sum > max_val:
            max_val = running_sum
    return max_val

if __name__ == "__main__":
    n, m = map(int, input().split())
    ops = []
    for _ in range(m):
        s, e, v = map(int, input().split())
        ops.append((s, e, v))
    print(array_manipulation(n, ops))