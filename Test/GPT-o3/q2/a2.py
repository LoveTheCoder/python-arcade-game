def sum_elements(arr):
    return sum(arr)

if __name__ == '__main__':
    # Input: space-separated integers on one line.
    arr = list(map(int, input("Enter space separated integers: ").split()))
    result = sum_elements(arr)
    print("Sum of elements:", result)