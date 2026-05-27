import yfinance as yf
import pandas as pd

# =========================
# USER INPUTS
# =========================

stocks = [
    "RELIANCE.NS",
    "BEL.NS",
    "HAL.NS",
    "TCS.NS",
    "ONGC.NS",
    "SBIN.NS",
    "ADANIPOWER.NS"
]

LOOKBACK_WINDOW = 10
MINIMUM_HIGHER_CLOSES = 6

# =========================
# SCANNER
# =========================

print("\nStarting Momentum Persistence Scanner...\n")

qualified_stocks = []

for stock in stocks:

    try:
        df = yf.download(
            stock,
            period="30d",
            interval="1d",
            auto_adjust=True,
            progress=False
        )

        # Higher close logic
        df['higher_close'] = (
            df['Close'] > df['Close'].shift(1)
        ).astype(int)

        # Rolling count
        df['count'] = (
            df['higher_close']
            .rolling(LOOKBACK_WINDOW)
            .sum()
        )

        latest_count = df['count'].iloc[-1]

        if latest_count >= MINIMUM_HIGHER_CLOSES:
            qualified_stocks.append(stock)

            print(
                f"{stock} → "
                f"{int(latest_count)} higher closes "
                f"in last {LOOKBACK_WINDOW} days"
            )

    except Exception as e:
        print(f"Error scanning {stock}: {e}")

# =========================
# FINAL OUTPUT
# =========================

print("\n======================")
print("QUALIFIED STOCKS")
print("======================\n")

for s in qualified_stocks:
    print(s)

print("\nScanner completed.\n")
