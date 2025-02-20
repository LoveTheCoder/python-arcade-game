def birthday_cake_candles(candles):
    tallest = max(candles)
    return candles.count(tallest)

if __name__ == '__main__':
    candles = list(map(int, input("Enter the candle heights (space separated): ").split()))
    result = birthday_cake_candles(candles)
    print("Number of tallest candles:", result)