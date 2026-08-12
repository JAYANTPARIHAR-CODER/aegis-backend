import joblib
import pandas as pd

model = joblib.load("buy_sell_model.pkl")

FEATURE_NAMES = ["return", "ma5", "ma10", "macd", "rsi", "volatility", "momentum"]


def predict_buy_confidence(return_value, ma5, ma10, macd, rsi, volatility, momentum):
    features = pd.DataFrame(
        [[return_value, ma5, ma10, macd, rsi, volatility, momentum]],
        columns=FEATURE_NAMES
    )

    probability = model.predict_proba(features)[0][1]
    return round(probability * 100, 2)  