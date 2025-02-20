def array_manipulation(n, operations):
    # Create an array of 0's with extra space for difference array technique
    arr = [0] * (n + 2)
    
    for a, b, k in operations:
        arr[a] += k
        arr[b + 1] -= k
    
    max_val = 0
    current = 0
    for i in range(1, n + 1):
        current += arr[i]
        if current > max_val:
            max_val = current
    return max_val

if __name__ == '__main__':
    n = int(input("Enter the size of the array: "))
    m = int(input("Enter the number of operations: "))
    operations = []
    print("Enter each operation as 'a b k' on a new line:")
    for _ in range(m):
        a, b, k = map(int, input().split())
        operations.append((a, b, k))
    
    result = array_manipulation(n, operations)
    print("Maximum value in the array:", result)