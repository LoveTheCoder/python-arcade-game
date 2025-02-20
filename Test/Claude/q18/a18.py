import numpy as np
from numpy import roots
import cmath

def get_polynomial():
    degree = int(input("Enter the degree of polynomial: "))
    coefficients = []
    for i in range(degree + 1):
        coef = float(input(f"Enter coefficient for x^{degree-i}: "))
        coefficients.append(coef)
    return coefficients

def solve_polynomial(coefficients):
    # Use numpy's roots function which handles all degrees
    roots_result = roots(coefficients)
    return roots_result

def format_solution(solutions):
    print("\nSolutions:")
    for i, sol in enumerate(solutions, 1):
        if abs(sol.imag) < 1e-10:  # Real solution
            print(f"x{i} = {sol.real:.4f}")
        else:  # Complex solution
            print(f"x{i} = {sol.real:.4f} + {sol.imag:.4f}i")

def main():
    print("Polynomial Solver")
    print("Enter coefficients from highest to lowest degree")
    try:
        coefficients = get_polynomial()
        solutions = solve_polynomial(coefficients)
        format_solution(solutions)
    except ValueError:
        print("Invalid input. Please enter numeric values.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()