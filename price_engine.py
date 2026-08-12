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

# Keep the last 30 prices for each stock (need more history for RSI/EMA)
price_history = {
    symbol: deque(maxlen=30)
    for symbol in SYMBOLS
}

for symbol in SYMBOLS:
    for _ in range(30):
        price_history[symbol].append(prices[symbol])


def generate_prices():
    for symbol in SYMBOLS:
        change = random.uniform(-0.5, 0.5)
        prices[symbol] = round(prices[symbol] + change, 2)
        price_history[symbol].append(prices[symbol])
    return prices.copy()


def calculate_features(symbol):
    history = np.array(list(price_history[symbol]))

    if len(history) < 27:
        return None

    # Return
    return_value = (history[-1] - history[-2]) / history[-2]

    # Moving averages
    ma5 = np.mean(history[-5:])
    ma10 = np.mean(history[-10:])

    # EMA (simple approximation using pandas-free method)
    def ema(values, span):
        alpha = 2 / (span + 1)
        e = values[0]
        for v in values[1:]:
            e = alpha * v + (1 - alpha) * e
        return e

    ema12 = ema(history[-26:], 12)
    ema26 = ema(history[-26:], 26)
    macd = ema12 - ema26

    # RSI (14-period)
    deltas = np.diff(history[-15:])
    gains = deltas[deltas > 0].sum() / 14 if len(deltas[deltas > 0]) > 0 else 0
    losses = -deltas[deltas < 0].sum() / 14 if len(deltas[deltas < 0]) > 0 else 0
    rs = gains / losses if losses != 0 else 0
    rsi = 100 - (100 / (1 + rs)) if losses != 0 else 100

    # Volatility & momentum
    volatility = np.std(history[-10:])
    momentum = history[-1] - history[-10]

    return return_value, ma5, ma10, macd, rsi, volatility, momentum