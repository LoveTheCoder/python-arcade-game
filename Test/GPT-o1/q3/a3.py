def diagonal_difference(matrix):
    n = len(matrix)
    primary = sum(matrix[i][i] for i in range(n))
    secondary = sum(matrix[i][n - 1 - i] for i in range(n))
    return abs(primary - secondary)

if __name__ == "__main__":
    n = int(input().strip())
    matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)
    print(diagonal_difference(matrix))