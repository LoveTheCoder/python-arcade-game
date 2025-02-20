from mpmath import mp

def calculate_constants(digits=100):
    # Set precision
    mp.dps = digits

    # Calculate constants
    pi = mp.pi
    e = mp.e
    phi = (1 + mp.sqrt(5)) / 2

    # Format and display results
    print(f"Pi (π) to {digits} digits:")
    print(str(pi) + "\n")
    
    print(f"e to {digits} digits:")
    print(str(e) + "\n")
    
    print(f"Golden Ratio (φ) to {digits} digits:")
    print(str(phi))

if __name__ == "__main__":
    calculate_constants()