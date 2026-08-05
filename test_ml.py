from ml_service import predict_buy_confidence

confidence = predict_buy_confidence(
    return_value=0.002,
    ma5=503.5,
    ma10=502.8
)

print(confidence)