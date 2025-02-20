def diagonal_difference(matrix):
    n = len(matrix)
    # Validate square matrix
    for row in matrix:
        if len(row) != n:
            raise ValueError("Input must be a square matrix")
    
    primary_sum = 0
    secondary_sum = 0
    
    for i in range(n):
        primary_sum += matrix[i][i]  # Primary diagonal
        secondary_sum += matrix[i][n-1-i]  # Secondary diagonal
    
    return abs(primary_sum - secondary_sum)

def main():
    # Test cases
    test_matrices = [
        [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]],
        
        [[11, 2, 4],
         [4, 5, 6],
         [10, 8, -12]]
    ]
    
    for matrix in test_matrices:
        print(f"Matrix:")
        for row in matrix:
            print(row)
        print(f"Diagonal difference: {diagonal_difference(matrix)}\n")

if __name__ == "__main__":
    main()