def min_trips(weights):
    weights.sort()
    trips = 0
    i, j = 0, len(weights) - 1
    while i <= j:
        # If the lightest and the heaviest can be paired
        if i != j and weights[i] + weights[j] <= 3.00:
            i += 1
        j -= 1
        trips += 1
    return trips

if __name__ == '__main__':
    n = int(input("Enter number of bags: "))
    # Read weights one per line or space separated
    print("Enter the weights:")
    weights = list(map(float, input().split()))
    if len(weights) != n:
        print("Error: Number of weights does not match the given count.")
    else:
        print("Minimum number of trips:", min_trips(weights))