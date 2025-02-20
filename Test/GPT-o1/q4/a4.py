def count_tallest_candles(candles):
    tallest = max(candles)
    return candles.count(tallest)

if __name__ == "__main__":
    n = int(input().strip())
    candles = list(map(int, input().split()))
    print(count_tallest_candles(candles))