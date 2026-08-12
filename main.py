from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from price_engine import generate_prices, calculate_features, SYMBOLS
from ml_service import predict_buy_confidence
import asyncio
import traceback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

portfolio_locked = False

@app.get("/")
def read_root():
    return {"status": "AEGIS backend is running"}

@app.post("/api/liquidate")
def liquidate():
    global portfolio_locked
    portfolio_locked = True
    return {"status": "liquidated", "message": "All positions closed, trading locked"}

@app.post("/api/reset")
def reset():
    global portfolio_locked
    portfolio_locked = False
    return {"status": "reset", "message": "Portfolio reset, trading enabled"}

@app.websocket("/ws/price")
async def price_stream(websocket: WebSocket):
    await websocket.accept()
    print("✅ WebSocket Client Connected")

    try:
        while True:
            if portfolio_locked:
                try:
                    await websocket.send_json({"locked": True})
                except Exception:
                    break
                await asyncio.sleep(1)
                continue

            prices = generate_prices()
            response = {"locked": False}

            for symbol in SYMBOLS:
                try:
                    features = calculate_features(symbol)
                    if features:
                        return_value, ma5, ma10, macd, rsi, volatility, momentum = features
                        confidence = predict_buy_confidence(return_value, ma5, ma10, macd, rsi, volatility, momentum)
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

            try:
                await websocket.send_json(response)
            except Exception:
                break
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("❌ WebSocket Client Disconnected")
    except Exception:
        print("\n========= BACKEND ERROR =========")
        traceback.print_exc()
        print("================================")
    finally:
        print("🔌 WebSocket connection closed, loop exited cleanly")