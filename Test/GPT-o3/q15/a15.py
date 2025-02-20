def left_rotate(arr, d):
    n = len(arr)
    d = d % n  # Allow d > n
    return arr[d:] + arr[:d]

if __name__ == '__main__':
    arr = list(map(int, input("Enter space separated integers: ").split()))
    d = int(input("Enter the number of left rotations: "))
    rotated = left_rotate(arr, d)
    print("Rotated array:", rotated)