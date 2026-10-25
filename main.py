"""
Bitcoin AI Lab – 1. verzió (Coinbase adatokkal)
Ingyenes BTC/USD történelmi adatletöltés és grafikon.
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone

# --- 1. Adatok letöltése a Coinbase nyilvános API-jából ---
def fetch_btc_klines(limit=300):
    # Coinbase API: napi (86400 másodperc) gyertyák
    url = "https://api.exchange.coinbase.com/products/BTC-USD/candles"
    params = {"granularity": 86400} # 1 nap
    headers = {"User-Agent": "Mozilla/5.0"}
    
    r = requests.get(url, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    raw = r.json()
    
    # A Coinbase formátuma: [time, low, high, open, close, volume]
    df = pd.DataFrame(raw, columns=["time", "low", "high", "open", "close", "volume"])
    
    # Dátum formázása és időrendbe rakása (a Coinbase fordítva adja vissza)
    df["date"] = pd.to_datetime(df["time"], unit="s", utc=True)
    df = df.sort_values("date").reset_index(drop=True)
    
    # Adattípusok javítása
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)
        
    return df[["date", "open", "high", "low", "close", "volume"]]


# --- 2. Grafikon rajzolása ---
def plot_price(df, outfile="btc_chart.png"):
    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["close"], linewidth=1, color="orange")
    plt.title("BTC/USD – napi záróárfolyam (Coinbase)")
    plt.xlabel("Dátum")
    plt.ylabel("Ár (USD)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(outfile, dpi=120)
    plt.close()
    print(f"Grafikon elmentve: {outfile}")


# --- 3. Fő program ---
def main():
    print("Bitcoin adatok letöltése a Coinbase-ről...")
    df = fetch_btc_klines()
    print(f"Letöltve {len(df)} nap adata.")
    print(f"Első nap: {df['date'].iloc[0]}")
    print(f"Utolsó nap: {df['date'].iloc[-1]}")
    print(f"Utolsó záróár: {df['close'].iloc[-1]:.2f} USD")

    df.to_csv("btc_data.csv", index=False)
    print("Adatok elmentve: btc_data.csv")

    plot_price(df)


if __name__ == "__main__":
    main()
