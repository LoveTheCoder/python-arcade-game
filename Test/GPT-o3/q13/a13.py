def find_smallest_largest(arr):
    smallest = min(arr)
    largest = max(arr)
    return smallest, largest

if __name__ == '__main__':
    arr = list(map(int, input("Enter space separated integers: ").split()))
    if arr:
        smallest, largest = find_smallest_largest(arr)
        print("Smallest number:", smallest)
        print("Largest number:", largest)
    else:
        print("The array is empty.")