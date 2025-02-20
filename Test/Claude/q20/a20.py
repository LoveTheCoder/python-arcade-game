from mpmath import mp

def demonstrate_pi_infinite():
    print("Demonstrating why pi has no last decimal:")
    print("Showing last decimal of pi at different precisions...\n")
    
    for precision in [10, 100, 1000, 10000]:
        # Set precision
        mp.dps = precision
        
        # Get pi to current precision
        pi_str = str(mp.pi)
        
        print(f"Precision: {precision} digits")
        print(f"Last decimal: {pi_str[-1]}")
        print(f"Last 5 decimals: {pi_str[-5:]}\n")

if __name__ == "__main__":
    demonstrate_pi_infinite()