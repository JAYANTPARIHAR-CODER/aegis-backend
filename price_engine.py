import random

SYMBOLS = ['AAPL', 'MSFT', 'NVDA', 'SPY', 'TSLA']

prices = {
    'AAPL': 189.56,
    'MSFT': 415.82,
    'NVDA': 875.35,
    'SPY': 521.34,
    'TSLA': 218.32,
}

def generate_prices():
    for symbol in SYMBOLS:
        change = random.uniform(-2, 2)
        prices[symbol] = round(prices[symbol] + change, 2)
    return prices.copy()