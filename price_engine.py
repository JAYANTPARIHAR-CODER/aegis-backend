import random
from collections import deque
import numpy as np

SYMBOLS = ['AAPL', 'MSFT', 'NVDA', 'SPY', 'TSLA']

prices = {
    'AAPL': 189.56,
    'MSFT': 415.82,
    'NVDA': 875.35,
    'SPY': 521.34,
    'TSLA': 218.32,
}

# Keep the last 20 prices for each stock
price_history = {
    symbol: deque(maxlen=20)
    for symbol in SYMBOLS
}

# Initialize history with the starting price
for symbol in SYMBOLS:
    for _ in range(20):
        price_history[symbol].append(prices[symbol])


def generate_prices():
    for symbol in SYMBOLS:
        change = random.uniform(-0.5, 0.5)
        prices[symbol] = round(prices[symbol] + change, 2)

        # Save new price
        price_history[symbol].append(prices[symbol])

    return prices.copy()


def calculate_features(symbol):
    history = list(price_history[symbol])

    if len(history) < 10:
        return None

    return_value = (history[-1] - history[-2]) / history[-2]
    ma5 = np.mean(history[-5:])
    ma10 = np.mean(history[-10:])

    return return_value, ma5, ma10