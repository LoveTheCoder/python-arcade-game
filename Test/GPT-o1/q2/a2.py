def sum_of_elements(arr):
    return sum(arr)

if __name__ == "__main__":
    n = int(input().strip())
    arr = [int(input().strip()) for _ in range(n)]
    print(sum_of_elements(arr))