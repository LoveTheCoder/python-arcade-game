def are_arrays_equal(arr1, arr2):
    return arr1 == arr2

if __name__ == "__main__":
    n1 = int(input().strip())
    arr1 = list(map(int, input().split()))
    n2 = int(input().strip())
    arr2 = list(map(int, input().split()))
    print("Equal" if are_arrays_equal(arr1, arr2) else "Not Equal")