def can_plan_cuts(cuts, minLength):
    total = sum(cuts)
    # The whole rod must be long enough to even start.
    if total < minLength:
        return False
    # We must perform at least one cut.
    # When a cut is made at some index i (1 <= i < len(cuts)+1),
    # it splits the rod into two contiguous parts:
    # left = cuts[0:i] and right = cuts[i:].
    # In planning the order, we can always defer cutting the part
    # (either left or right) that is at least minLength so that it is processed last.
    # So we need at least one valid cut position where one of the parts has sum >= minLength.
    prefix = 0
    n = len(cuts)
    for i in range(1, n + 1):
        prefix += cuts[i - 1]
        suffix = total - prefix
        if prefix >= minLength or suffix >= minLength:
            return True
    return False

if __name__ == '__main__':
    # Input the rod segments (in order)
    cuts = list(map(float, input("Enter the rod segments (space separated): ").split()))
    minLength = float(input("Enter the machine's minimum length requirement: "))
    if can_plan_cuts(cuts, minLength):
        print("It is possible to plan the cuts.")
    else:
        print("It is not possible to plan the cuts.")