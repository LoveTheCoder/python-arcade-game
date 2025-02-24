from decimal import Decimal, getcontext

# Increase the precision to safely calculate around 110+ digits
getcontext().prec = 110

def compute_pi():
    # Chudnovsky algorithm
    # Reference: https://en.wikipedia.org/wiki/Chudnovsky_algorithm
    # pi = (426880 * sqrt(10005)) / sum_{k=0..∞} of (factor(k))
    # We'll sum enough terms for ~110 digits
    from math import factorial
    one = Decimal(1)
    sqrtC = Decimal(10005).sqrt()
    pi_sum = Decimal(0)
    k = 0
    while k < 10:  # 10 terms is usually enough for ~100 digits
        numerator = Decimal((factorial(6*k)) * (13591409 + 545140134*k))
        denominator = Decimal(factorial(3*k)) * (factorial(k) ** 3) * (Decimal(-640320) ** (3*k))
        pi_sum += numerator / denominator
        k += 1
    pi = (Decimal(426880) * sqrtC) / pi_sum
    return pi

def compute_e():
    # e = sum_{n=0..∞} of 1/n!
    # We'll sum up to ~30 terms for good measure
    from math import factorial
    e_sum = Decimal(0)
    for i in range(30):
        e_sum += Decimal(1) / Decimal(factorial(i))
    return e_sum

def compute_golden_ratio():
    # phi = (1 + sqrt(5)) / 2
    return (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)

def first_100_digits(num_decimal):
    # Convert to string, remove extra digits after 100 total digits
    # We'll gather up to 101 or 102 total (to be safe),
    # then slice. We keep the decimal point as well.
    s = str(num_decimal)
    # If there's a decimal point, we want up to 100 digits total (including digits before the decimal).
    # We'll slice accordingly.
    count = 0
    output = []
    for char in s:
        if char.isdigit():
            count += 1
        output.append(char)
        if count == 100:
            break
    return "".join(output)

if __name__ == "__main__":
    pi_approx = compute_pi()
    e_approx = compute_e()
    phi_approx = compute_golden_ratio()
    
    print("Pi (first 100 digits):", first_100_digits(pi_approx))
    print("e (first 100 digits):", first_100_digits(e_approx))
    print("Golden Ratio (first 100 digits):", first_100_digits(phi_approx))