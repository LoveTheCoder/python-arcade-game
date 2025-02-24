import numpy as np

def solve_polynomial(coefficients):
    """Return all solutions (roots) of the polynomial with given coefficients."""
    return np.roots(coefficients)

if __name__ == "__main__":
    # degree = number of polynomials => if degree = 2, it means a quadratic, needing 3 coefficients
    degree = int(input().strip())
    
    # Collect the coefficients (degree + 1 of them)
    coefficients = []
    for _ in range(degree + 1):
        coefficients.append(float(input().strip()))
    
    # Solve
    solutions = solve_polynomial(coefficients)
    
    # Print solutions
    for sol in solutions:
        print(sol)