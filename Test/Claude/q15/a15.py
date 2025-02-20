def rotateLeft(arr, d):
    if not arr:
        return arr
        
    # Normalize d if it's larger than array length
    d = d % len(arr)
    
    # Use array slicing for rotation
    return arr[d:] + arr[:d]

def test_rotation():
    test_cases = [
        ([1, 2, 3, 4, 5], 2),     # Basic rotation
        ([1, 2, 3, 4, 5], 5),     # Full rotation
        ([1, 2, 3, 4, 5], 7),     # More than array length
        ([], 4),                   # Empty array
        ([1], 3),                  # Single element
    ]
    
    for arr, d in test_cases:
        result = rotateLeft(arr, d)
        print(f"Original array: {arr}")
        print(f"Rotated {d} positions: {result}\n")

if __name__ == "__main__":
    test_rotation()