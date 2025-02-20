def are_arrays_equal(arr1, arr2, ordered=True):
    """
    Compare two arrays for equality.
    ordered=True: arrays must have same elements in same order
    ordered=False: arrays must have same elements regardless of order
    """
    if len(arr1) != len(arr2):
        return False
        
    if ordered:
        return arr1 == arr2
    else:
        # Convert to dictionaries to count occurrences
        return Counter(arr1) == Counter(arr2)

from collections import Counter

def main():
    # Test cases
    test_cases = [
        ([1, 2, 3], [1, 2, 3]),           # True for both
        ([1, 2, 3], [3, 2, 1]),           # True for unordered, False for ordered
        ([1, 2, 2], [1, 2, 3]),           # False for both
        ([], []),                          # True for both
        ([1, 1, 1], [1, 1, 1]),           # True for both
    ]
    
    for arr1, arr2 in test_cases:
        print(f"\nArrays: {arr1} and {arr2}")
        print(f"Ordered comparison: {are_arrays_equal(arr1, arr2, True)}")
        print(f"Unordered comparison: {are_arrays_equal(arr1, arr2, False)}")

if __name__ == "__main__":
    main()