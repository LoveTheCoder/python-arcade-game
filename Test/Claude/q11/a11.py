def can_cut_last(cuts, min_length):
    def try_cuts(remaining_cuts, current_length):
        if not remaining_cuts:  # All cuts used
            return True
        
        for i in range(len(remaining_cuts)):
            # Try this cut
            cut_length = remaining_cuts[i]
            # If this is the last cut, check if remaining length >= min_length
            if len(remaining_cuts) == 1 and current_length - cut_length < min_length:
                continue
                
            # Create new cuts list without current cut
            new_cuts = remaining_cuts[:i] + remaining_cuts[i+1:]
            
            # If valid cut and recursive solution exists
            if cut_length <= current_length and try_cuts(new_cuts, current_length - cut_length):
                return True
                
        return False

    # Start with sum of all cuts as total length
    total_length = sum(cuts)
    return try_cuts(cuts, total_length)

def main():
    test_cases = [
        ([2, 3, 4], 3),  # True
        ([4, 3, 2], 5),  # False
        ([1, 1, 1], 2),  # False
        ([5, 2, 3], 4),  # True
    ]
    
    for cuts, min_length in test_cases:
        result = can_cut_last(cuts, min_length)
        print(f"Cuts: {cuts}, Min Length: {min_length}")
        print(f"Can perform last cut: {result}\n")

if __name__ == "__main__":
    main()