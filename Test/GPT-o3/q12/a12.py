def arrays_equal(arr1, arr2):
    if len(arr1) != len(arr2):
        return False
    for a, b in zip(arr1, arr2):
        if a != b:
            return False
    return True

if __name__ == '__main__':
    print("Enter the elements of the first array (space separated):")
    arr1 = list(map(int, input().split()))
    print("Enter the elements of the second array (space separated):")
    arr2 = list(map(int, input().split()))
    if arrays_equal(arr1, arr2):
        print("Arrays are equal.")
    else:
        print("Arrays are not equal.")