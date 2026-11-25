"""
Ambil data EOD semua saham di tickers.txt dari Yahoo Finance -> data/eod.json
Dijalankan otomatis oleh GitHub Actions setiap hari bursa (lihat .github/workflows/daily.yml).
Bisa juga dijalankan manual:  pip install yfinance pandas && python fetch_data.py
"""
import json, os, time, datetime as dt
import pandas as pd
import yfinance as yf

PERIOD = "1y"          # riwayat yang ditarik
KEEP_DAYS = 160        # hari bursa yang disimpan ke JSON (cukup untuk MA100, VMA50, dll)
BATCH = 80

tickers = [l.strip().upper() for l in open("tickers.txt") if l.strip()]
frames = {}
for b in range(0, len(tickers), BATCH):
    batch = [t + ".JK" for t in tickers[b:b + BATCH]]
    for attempt in range(3):
        try:
            data = yf.download(batch, period=PERIOD, interval="1d", group_by="ticker",
                               auto_adjust=False, threads=True, progress=False)
            break
        except Exception as e:
            print("retry", e); time.sleep(10)
    else:
        continue
    for t in batch:
        try:
            df = data[t] if len(batch) > 1 else data
            df = df[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])
            if len(df) >= 30:
                frames[t[:-3]] = df
        except Exception:
            pass
    print(f"{min(b + BATCH, len(tickers))}/{len(tickers)}  ok={len(frames)}")
    time.sleep(2)

# Kalender bersama = gabungan semua tanggal, ambil KEEP_DAYS terakhir
dates = sorted(set().union(*[set(f.index) for f in frames.values()]))[-KEEP_DAYS:]
out = {"generated": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
       "source": "Yahoo Finance (yfinance)",
       "dates": [d.strftime("%Y-%m-%d") for d in dates],
       "t": {}}
for code, df in frames.items():
    df = df.reindex(dates)
    rows = []
    for o, h, l, c, v in df.itertuples(index=False):
        if pd.isna(c) or pd.isna(v) or v <= 0:
            rows.append(None)          # tidak ada transaksi / data bolong
        else:
            rows.append([round(o), round(h), round(l), round(c), int(v)])
    if sum(r is not None for r in rows) >= 30:
        out["t"][code] = rows

os.makedirs("data", exist_ok=True)
with open("data/eod.json", "w") as f:
    json.dump(out, f, separators=(",", ":"))
print(f"Selesai: {len(out['t'])} saham, {len(dates)} hari, terakhir {out['dates'][-1]}")
