from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from price_engine import generate_prices
import asyncio

app = FastAPI()

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
    try:
        while True:
            prices = generate_prices()
            await websocket.send_json(prices)
            await asyncio.sleep(1)
    except Exception:
        pass