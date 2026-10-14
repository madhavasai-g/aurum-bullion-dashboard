#!/usr/bin/env python3
"""Fetch gold spot and USD/INR references; save a timestamped public JSON snapshot."""
import json, os, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
LATEST = DATA / "latest.json"
HISTORY = DATA / "history.json"
OUNCE_GRAMS = 31.1034768

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "AurumBullionDashboard/1.0 (personal project)"})
    with urllib.request.urlopen(req, timeout=20) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}: {url}")
        return json.loads(response.read().decode("utf-8"))

def main():
    gold = fetch("https://api.gold-api.com/price/XAU")
    fx = fetch("https://open.er-api.com/v6/latest/USD")
    price = float(gold["price"])
    rate = float(fx["rates"]["INR"])
    if price <= 0 or rate <= 0:
        raise ValueError("API returned non-positive price/rate")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    record = {
        "snapshot_at": now,
        "usd_per_ounce": round(price, 4),
        "usd_inr": round(rate, 6),
        "inr_per_gram": round(price * rate / OUNCE_GRAMS, 2),
        "gold_updated_at": gold.get("updatedAt") or gold.get("updated_at") or gold.get("timestamp"),
        "fx_updated_at": fx.get("time_last_update_utc") or fx.get("time_last_update_unix"),
        "sources": {"gold": "https://gold-api.com/", "fx": "https://www.exchangerate-api.com/docs/free"},
        "note": "Indicative spot-equivalent only; not a retail bullion quote. FX update cadence may differ from gold quote."
    }
    DATA.mkdir(parents=True, exist_ok=True)
    old = {}
    if LATEST.exists():
        try: old = json.loads(LATEST.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError): pass
    history = old.get("history", []) if isinstance(old.get("history", []), list) else []
    history.append({"timestamp": record["snapshot_at"], "usd_per_ounce": record["usd_per_ounce"], "usd_inr": record["usd_inr"], "inr_per_gram": record["inr_per_gram"]})
    # Keep a rolling year of scheduled snapshots (up to ~17,520 at 30-minute cadence).
    history = history[-17520:]
    record["history"] = history
    LATEST.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    HISTORY.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
    print(f"Saved ${price:.2f}/oz; USD/INR {rate:.4f}; spot-equivalent ₹{record['inr_per_gram']:.2f}/g")

if __name__ == "__main__":
    try: main()
    except Exception as exc:
        print(f"Price refresh failed: {exc}", file=sys.stderr)
        sys.exit(1)
