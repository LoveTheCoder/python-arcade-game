def arrayManipulation(n, queries):
    # Initialize array with zeros
    arr = [0] * (n + 1)
    
    # Process queries using prefix sum technique
    for start, end, value in queries:
        arr[start - 1] += value    # 1-based to 0-based indexing
        if end < len(arr):         # Handle last element case
            arr[end] -= value
    
    # Calculate maximum prefix sum
    max_value = curr_value = 0
    for val in arr:
        curr_value += val
        max_value = max(max_value, curr_value)
    
    return max_value

def main():
    test_cases = [
        (5, [(1, 2, 100), (2, 5, 100), (3, 4, 100)]),
        (10, [(1, 5, 3), (4, 8, 7), (6, 9, 1)]),
        (4, [(2, 3, 603), (1, 1, 286), (4, 4, 882)])
    ]
    
    for n, queries in test_cases:
        result = arrayManipulation(n, queries)
        print(f"Array size: {n}")
        print(f"Operations: {queries}")
        print(f"Maximum value: {result}\n")

if __name__ == "__main__":
    main()