def find_min_and_max(arr):
    smallest = min(arr)
    largest = max(arr)
    return smallest, largest

if __name__ == "__main__":
    n = int(input().strip())
    arr = list(map(int, input().split()))
    mn, mx = find_min_and_max(arr)
    print(mn, mx)