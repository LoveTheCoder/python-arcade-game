from collections import Counter

def matchingStrings(stringList, queries):
    # Create frequency map
    freq = Counter(stringList)
    
    # Return array of counts for each query
    return [freq[q] for q in queries]

def main():
    test_cases = [
        (
            ["ab", "ab", "abc"],           # stringList
            ["ab", "abc", "bc"]            # queries
        ),
        (
            ["aba", "baba", "aba", "xzxb"],
            ["aba", "xzxb", "ab"]
        ),
        (
            [],                            # Empty string list
            ["abc"]
        ),
        (
            ["def", "de", "fgh"],
            []                             # Empty queries
        )
    ]
    
    for stringList, queries in test_cases:
        result = matchingStrings(stringList, queries)
        print(f"String List: {stringList}")
        print(f"Queries: {queries}")
        print(f"Results: {result}\n")

if __name__ == "__main__":
    main()