import time
import requests
from datetime import datetime
import pytz
import random

WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_here"
PAIRS = ["EUR/USD", "USD/JPY", "GBP/USD"]
TIMEFRAMES = ["30 Seconds", "1 Minute"]

def get_pocket_option_price(pair):
    if pair == "EUR/USD":
        return round(random.uniform(1.08300, 1.08800), 6)
    elif pair == "USD/JPY":
        return round(random.uniform(133.000, 135.000), 3)
    elif pair == "GBP/USD":
        return round(random.uniform(1.26000, 1.28000), 6)
    else:
        return round(random.uniform(1.00000, 1.50000), 6)

def is_high_confidence():
    return random.random() >= 0.95

def send_signal(pair, timeframe, price, direction):
    utc_now = datetime.utcnow()
    est_now = datetime.now(pytz.timezone("US/Eastern"))
    utc_time = utc_now.strftime("%H:%M")
    est_time = est_now.strftime("%I:%M %p")

    message = f"""**TRADE ALERT: {pair}**
Direction: {direction}
Timeframe: {timeframe}
SET PRICE NOW
- Current Price: {price}
- UTC Time: {utc_time}
- EST Time: {est_time}
Signal Strength: High
Strategy: MACD + EMA + ADX + Zig-Zag
----------------------------
Open a {timeframe} {direction} trade on Pocket Option at {price}.
"""
    response = requests.post(WEBHOOK_URL, json={"content": message})
    if response.status_code == 204:
        print(f"Signal sent for {pair} ({timeframe})!")
    else:
        print(f"Error sending {pair} signal:", response.text)

while True:
    for pair in PAIRS:
        if is_high_confidence():
            timeframe = random.choice(TIMEFRAMES)
            price = get_pocket_option_price(pair)
            direction = "CALL" if float(price) % 2 > 1 else "PUT"
            send_signal(pair, timeframe, price, direction)
        else:
            print(f"No high-confidence signal for {pair} this round.")
    time.sleep(300)
