def simple_array_sum(ar):
    return sum(ar)

# Test cases
def main():
    test_cases = [
        [1, 2, 3],
        [1, 2, 3, 4, 10, 11],
        [0],
        []
    ]
    
    for test in test_cases:
        print(f"Array: {test}")
        print(f"Sum: {simple_array_sum(test)}\n")

if __name__ == "__main__":
    main()