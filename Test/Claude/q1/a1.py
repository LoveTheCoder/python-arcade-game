def min_trips(n, weights):
    # Sort weights in descending order
    weights.sort(reverse=True)
    
    trips = 0
    left = 0
    right = n - 1
    
    while left <= right:
        # If only one bag left or current bag is too heavy to pair
        if left == right or weights[left] + weights[right] > 3.0:
            trips += 1
            left += 1
        else:
            # Can take two bags
            trips += 1
            left += 1
            right -= 1
            
    return trips

# Example usage
def main():
    # Sample inputs
    n = int(input())
    weights = []
    for _ in range(n):
        weights.append(float(input()))
    
    result = min_trips(n, weights)
    print(result)

if __name__ == "__main__":
    main()