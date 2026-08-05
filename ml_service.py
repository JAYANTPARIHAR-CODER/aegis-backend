import joblib
import pandas as pd

# Load the trained model once when the server starts
model = joblib.load("buy_sell_model.pkl")


def predict_buy_confidence(return_value, ma5, ma10):
    features = pd.DataFrame(
        [[return_value, ma5, ma10]],
        columns=["return", "ma5", "ma10"]
    )

    probability = model.predict_proba(features)[0][1]

    return round(probability * 100, 2)