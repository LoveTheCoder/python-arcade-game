import numpy as np

def solve_polynomial(coeffs):
    # Calculate all solutions (roots) of the polynomial equation
    # Coefficients should be provided from the highest degree term to the constant.
    return np.roots(coeffs)

if __name__ == '__main__':
    # Ask for the degree of the polynomial (e.g., for ax^2 + bx + c, degree = 2)
    degree = int(input("Enter the degree of the polynomial: "))
    
    print(f"Enter {degree + 1} coefficients (highest degree to constant) separated by spaces:")
    coeffs = list(map(float, input().split()))
    
    if len(coeffs) != degree + 1:
        print(f"Error: Expected {degree + 1} coefficients.")
    else:
        roots = solve_polynomial(coeffs)
        print("The solutions (roots) of the polynomial are:")
        for root in roots:
            print(root)