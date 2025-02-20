def count_tallest_candles(candles):
    max_height = max(candles)
    return candles.count(max_height)

def main():
    # Test cases
    test_cases = [
        [4, 4, 1, 3],        # Should return 2
        [3, 2, 1, 3],        # Should return 2
        [1, 1, 1, 1],        # Should return 4
        [3],                 # Should return 1
        [1, 2, 3, 4, 4, 4]   # Should return 3
    ]
    
    for candles in test_cases:
        print(f"Candles: {candles}")
        print(f"Number of tallest candles: {count_tallest_candles(candles)}\n")

if __name__ == "__main__":
    main()