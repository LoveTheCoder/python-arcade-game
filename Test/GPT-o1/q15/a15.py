def left_rotate(arr, d):
    d = d % len(arr)
    return arr[d:] + arr[:d]

if __name__ == "__main__":
    n, d = map(int, input().split())
    arr = list(map(int, input().split()))
    rotated_arr = left_rotate(arr, d)
    print(*rotated_arr)