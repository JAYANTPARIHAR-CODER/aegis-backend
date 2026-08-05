from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from price_engine import generate_prices, calculate_features, SYMBOLS
from ml_service import predict_buy_confidence
import asyncio
import traceback

# Create FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"status": "AEGIS backend is running"}


@app.websocket("/ws/price")
async def price_stream(websocket: WebSocket):
    await websocket.accept()
    print("✅ WebSocket Client Connected")

    try:
        while True:
            # Generate latest prices
            prices = generate_prices()

            response = {}

            for symbol in SYMBOLS:
                try:
                    # Calculate ML features
                    features = calculate_features(symbol)

                    if features:
                        return_value, ma5, ma10 = features

                        confidence = predict_buy_confidence(
                            return_value,
                            ma5,
                            ma10
                        )
                    else:
                        confidence = 50.0

                    response[symbol] = {
                        "price": float(prices[symbol]),
                        "buyConfidence": float(confidence)
                    }

                except Exception:
                    print(f"Prediction failed for {symbol}")
                    traceback.print_exc()

                    response[symbol] = {
                        "price": float(prices[symbol]),
                        "buyConfidence": 50.0
                    }

            await websocket.send_json(response)
            print(response)

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("❌ WebSocket Client Disconnected")

    except Exception:
        print("\n========= BACKEND ERROR =========")
        traceback.print_exc()
        print("================================")