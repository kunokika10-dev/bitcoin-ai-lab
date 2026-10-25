"""
Bitcoin AI Lab – 1. verzió
Ingyenes BTC/USDT történelmi adatletöltés és grafikon.
Nincs API-kulcs, nincs fizetős szolgáltatás.
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone

# --- 1. Adatok letöltése a Binance nyilvános API-jából ---
def fetch_btc_klines(symbol="BTCUSDT", interval="1d", limit=1000):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    raw = r.json()

    df = pd.DataFrame(raw, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "trades",
        "taker_buy_base", "taker_buy_quote", "ignore",
    ])
    df["date"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)
    return df[["date", "open", "high", "low", "close", "volume"]]


# --- 2. Grafikon rajzolása ---
def plot_price(df, outfile="btc_chart.png"):
    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["close"], linewidth=1)
    plt.title("BTC/USDT – napi záróárfolyam")
    plt.xlabel("Dátum")
    plt.ylabel("Ár (USDT)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(outfile, dpi=120)
    plt.close()
    print(f"Grafikon elmentve: {outfile}")


# --- 3. Fő program ---
def main():
    print("Bitcoin adatok letöltése...")
    df = fetch_btc_klines()
    print(f"Letöltve {len(df)} nap adata.")
    print(f"Első nap: {df['date'].iloc[0]}")
    print(f"Utolsó nap: {df['date'].iloc[-1]}")
    print(f"Utolsó záróár: {df['close'].iloc[-1]:.2f} USDT")

    df.to_csv("btc_data.csv", index=False)
    print("Adatok elmentve: btc_data.csv")

    plot_price(df)


if __name__ == "__main__":
    main()
