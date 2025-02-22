from decimal import Decimal, getcontext

# Set precision high enough to calculate 100 digits after the decimal point.
getcontext().prec = 110

def compute_pi():
    # Chudnovsky algorithm for pi
    getcontext().prec += 2  # Increase precision during intermediate steps.
    C = 426880 * Decimal(10005).sqrt()
    M = Decimal(1)
    L = Decimal(13591409)
    X = Decimal(1)
    S = L
    k = 1
    while True:
        M = (M * (6*k - 5) * (2*k - 1) * (6*k - 1)) / (k**3 * Decimal(640320)**3)
        L += 545140134
        X *= -262537412640768000
        term = M * L / X
        S += term
        # Stop when the term is extremely small
        if abs(term) < Decimal(1e-105):
            break
        k += 1
    pi = C / S
    getcontext().prec -= 2  # Reset precision
    return +pi  # Unary plus applies the new precision

def compute_e():
    # Compute e using its series expansion: e = sum(1/n!, n=0 to infinity)
    e = Decimal(0)
    fact = Decimal(1)
    # Use more terms to ensure 100 digits precision.
    for i in range(0, 110):
        if i > 0:
            fact *= i
        e += Decimal(1) / fact
    return e

def compute_phi():
    # Golden ratio: phi = (1 + sqrt(5)) / 2
    return (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)

if __name__ == '__main__':
    pi_val = compute_pi()
    e_val = compute_e()
    phi_val = compute_phi()

    # Format the output to display 100 digits after the decimal point.
    print("First 100 digits of pi:")
    print(format(pi_val, ".100f"))

    print("\nFirst 100 digits of e:")
    print(format(e_val, ".100f"))

    print("\nFirst 100 digits of the golden ratio:")
    print(format(phi_val, ".100f"))