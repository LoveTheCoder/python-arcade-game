def count_query_occurrences(input_strings, queries):
    freq = {}
    for s in input_strings:
        freq[s] = freq.get(s, 0) + 1
    return [freq.get(q, 0) for q in queries]

if __name__ == '__main__':
    n = int(input("Enter the number of input strings: "))
    input_strings = [input() for _ in range(n)]
    
    q = int(input("Enter the number of queries: "))
    queries = [input() for _ in range(q)]
    
    results = count_query_occurrences(input_strings, queries)
    print("Query results:")
    for count in results:
        print(count)