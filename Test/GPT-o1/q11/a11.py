def can_plan_cuts(cuts, min_length):
    # Simple interpretation: if total length >= min_length,
    # at least one plan can make the last cut from a rod >= min_length
    return 1 if sum(cuts) >= min_length else 0

if __name__ == "__main__":
    n = int(input().strip())
    cuts = list(map(int, input().split()))
    min_length = int(input().strip())
    print(can_plan_cuts(cuts, min_length))