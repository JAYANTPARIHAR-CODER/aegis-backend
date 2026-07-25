import random
import time

def generate_price(current_price: float) -> float:
    change = random.uniform(-2, 2)
    new_price = current_price + change
    return round(new_price, 2)

if __name__ == "__main__":
    price = 500.0
    while True:
        price = generate_price(price)
        print(f"Price: {price}")
        time.sleep(1)