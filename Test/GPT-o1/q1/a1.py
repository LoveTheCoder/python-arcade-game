def solve_janitor_min_trips(bag_weights):
    bag_weights.sort()
    left, right = 0, len(bag_weights) - 1
    trips = 0
    while left <= right:
        if left != right and bag_weights[left] + bag_weights[right] <= 3.00:
            left += 1
        right -= 1
        trips += 1
    return trips

if __name__ == "__main__":
    # Example usage:
    # Input: number of bags and their weights
    # Output: minimum number of trips
    n = int(input().strip())
    weights = [float(input().strip()) for _ in range(n)]
    print(solve_janitor_min_trips(weights))