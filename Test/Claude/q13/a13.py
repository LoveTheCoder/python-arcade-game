def find_min_max(arr):
    if not arr:
        return None, None
        
    min_num = max_num = arr[0]
    
    for num in arr[1:]:
        if num < min_num:
            min_num = num
        if num > max_num:
            max_num = num
            
    return min_num, max_num

def test_find_min_max():
    test_cases = [
        [1, 2, 3, 4, 5],           # Sorted array
        [5, 4, 3, 2, 1],           # Reverse sorted
        [3, 1, 4, 1, 5, 9, 2, 6],  # Random order
        [1],                        # Single element
        [-1, -5, 0, 2, -9],        # Negative numbers
        [2, 2, 2, 2],              # All same values
    ]
    
    for arr in test_cases:
        min_val, max_val = find_min_max(arr)
        print(f"Array: {arr}")
        print(f"Min: {min_val}, Max: {max_val}\n")

if __name__ == "__main__":
    test_find_min_max()