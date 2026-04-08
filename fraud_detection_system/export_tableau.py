"""
Real-time Data Exporter for Tableau Live Connection.
Exports transaction data to CSV that Tableau can refresh automatically.
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
import threading

# Configuration
API_URL = "http://localhost:8000"
OUTPUT_FILE = "data/tableau_live_data.csv"
REFRESH_INTERVAL = 5  # seconds


def fetch_and_export():
    """Fetch data from API and export to CSV."""
    try:
        # Fetch transactions
        resp = requests.get(f"{API_URL}/transactions?limit=1000", timeout=5)
        transactions = resp.json()

        # Fetch stats
        stats_resp = requests.get(f"{API_URL}/stats", timeout=5)
        stats = stats_resp.json()

        # Write CSV
        with open(OUTPUT_FILE, "w") as f:
            # Header
            f.write(
                "id,transaction_id,timestamp,amount,merchant_category,location,fraud_probability,prediction,risk_level,total_transactions,fraud_detected,high_risk,medium_risk,low_risk\n"
            )

            # Add stats as columns
            total = stats.get("total_transactions", 0)
            fraud = stats.get("fraud_detected", 0)
            high = stats.get("high_risk", 0)
            med = stats.get("medium_risk", 0)
            low = stats.get("low_risk", 0)

            for t in transactions:
                f.write(
                    f"{t.get('id', '')},{t.get('transaction_id', '')},{t.get('timestamp', '')},{t.get('amount', 0)},{t.get('merchant_category', '')},{t.get('location', '')},{t.get('fraud_probability', 0)},{t.get('prediction', '')},{t.get('risk_level', '')},{total},{fraud},{high},{med},{low}\n"
                )

        print(f"✅ Exported {len(transactions)} transactions to {OUTPUT_FILE}")
        return True

    except Exception as e:
        print(f"❌ Export failed: {e}")
        return False


def continuous_export():
    """Continuously export data."""
    print(f"📤 Starting continuous export to {OUTPUT_FILE}")
    print("🔄 Data will refresh every 5 seconds")
    print("\n📋 Instructions for Tableau:")
    print("1. Open Tableau Desktop")
    print("2. Connect → To a File → Microsoft Excel")
    print(f"3. Select: {os.path.abspath(OUTPUT_FILE)}")
    print("4. Go to Worksheet")
    print("5. Right-click the data source → Refresh")
    print("\n💡 For auto-refresh: Use Tableau Bridge or publish to Tableau Cloud")

    while True:
        fetch_and_export()
        time.sleep(REFRESH_INTERVAL)


if __name__ == "__main__":
    # Initial export
    fetch_and_export()

    # Continuous export in background
    continuous_export()
