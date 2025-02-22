def matching_strings(strings, queries):
    frequency = {}
    for s in strings:
        frequency[s] = frequency.get(s, 0) + 1
    
    result = []
    for q in queries:
        result.append(frequency.get(q, 0))
    return result

if __name__ == "__main__":
    n = int(input().strip())
    strings = [input().strip() for _ in range(n)]
    q = int(input().strip())
    queries = [input().strip() for _ in range(q)]
    counts = matching_strings(strings, queries)
    for c in counts:
        print(c)