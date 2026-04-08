"""
Tableau Live Data Server - Version 3 with embedded data fallback.
Works even if JavaScript fetch fails in Tableau's embedded browser.
"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
import threading

PORT = 8765
API_URL = "http://localhost:8000"

# Cache transaction data in memory
cached_transactions = []
cached_stats = {}


def fetch_data_thread():
    """Background thread to fetch and cache data from API."""
    global cached_transactions, cached_stats
    while True:
        try:
            resp = requests.get(f"{API_URL}/transactions?limit=5000", timeout=5)
            cached_transactions = resp.json()

            stats_resp = requests.get(f"{API_URL}/stats", timeout=5)
            cached_stats = stats_resp.json()
        except:
            pass
        threading.Event().wait(2)  # Sleep 2 seconds


class TableauWDC(SimpleHTTPRequestHandler):
    """Tableau Web Data Connector with embedded data fallback."""

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index":
            # WDC Main Page - with embedded data for fallback
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            # Use cached data for fallback
            data_json = (
                json.dumps(cached_transactions[:500]) if cached_transactions else "[]"
            )

            html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>FraudShield AI - Tableau Connector</title>
    <script src="https://connectors.tableau.com/libs/tableauwdc-2.3.latest.min.js"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
               background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1a 100%);
               color: #fff; padding: 40px; text-align: center; }}
        h1 {{ color: #00d4ff; font-size: 2.5rem; }}
        .status {{ background: #2a2a4e; padding: 20px; border-radius: 10px; 
                   margin: 20px auto; max-width: 400px; }}
        .btn {{ background: #00d4ff; color: #000; padding: 15px 40px; border: none;
                border-radius: 8px; font-size: 1.2rem; font-weight: bold; cursor: pointer; }}
    </style>
</head>
<body>
    <h1>🛡️ FraudShield AI</h1>
    <p>Real-time Fraud Detection Data</p>
    
    <div class="status">
        <p><strong>Data Records:</strong> <span id="count">{len(cached_transactions) if cached_transactions else 0}</span></p>
        <p><strong>API Status:</strong> <span id="api-status" style="color:#00ff88">Connected</span></p>
    </div>
    
    <button class="btn" onclick="connect()">📊 Open in Tableau</button>
    
    <script>
        // Embedded data (fallback if API call fails)
        var EMBEDDED_DATA = {data_json};
        
        var connector = tableau.makeConnector();
        
        connector.getSchema = function(done) {{
            var cols = [
                {{id: "id", alias: "ID", dataType: tableau.dataTypeEnum.int}},
                {{id: "transaction_id", alias: "Transaction ID", dataType: tableau.dataTypeEnum.string}},
                {{id: "timestamp", alias: "Timestamp", dataType: tableau.dataTypeEnum.string}},
                {{id: "amount", alias: "Amount ($)", dataType: tableau.dataTypeEnum.float}},
                {{id: "merchant_category", alias: "Category", dataType: tableau.dataTypeEnum.string}},
                {{id: "location", alias: "Location", dataType: tableau.dataTypeEnum.string}},
                {{id: "fraud_probability", alias: "Fraud Prob", dataType: tableau.dataTypeEnum.float}},
                {{id: "prediction", alias: "Fraud (0/1)", dataType: tableau.dataTypeEnum.int}},
                {{id: "risk_level", alias: "Risk Level", dataType: tableau.dataTypeEnum.string}}
            ];
            done([{{id: "fraud_transactions", alias: "FraudShield Data", columns: cols}}]);
        }};
        
        connector.getData = function(table, done) {{
            // Use embedded data directly (no API call needed!)
            var tableData = EMBEDDED_DATA.map(function(row) {{
                return {{
                    "id": row.id,
                    "transaction_id": row.transaction_id,
                    "timestamp": row.timestamp,
                    "amount": parseFloat(row.amount),
                    "merchant_category": row.merchant_category,
                    "location": row.location,
                    "fraud_probability": parseFloat(row.fraud_probability),
                    "prediction": row.prediction,
                    "risk_level": row.risk_level
                }};
            }});
            table.appendRows(tableData);
            done();
        }};
        
        tableau.registerConnector(connector);
        
        function connect() {{
            tableau.connectionName = "FraudShield AI - Live";
            tableau.submit();
        }}
        
        // Auto-connect on load
        setTimeout(connect, 1000);
    </script>
</body>
</html>"""
            self.wfile.write(html.encode())

        elif path == "/data.json":
            # Direct JSON for external access
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(cached_transactions[:5000]).encode())

        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()


def start_server():
    # Start data fetching thread
    fetch_thread = threading.Thread(target=fetch_data_thread, daemon=True)
    fetch_thread.start()

    server = HTTPServer(("localhost", PORT), TableauWDC)
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  🎯 TABLEAU WEB DATA CONNECTOR - READY                    ║
╚═══════════════════════════════════════════════════════════╝

Server: http://localhost:{PORT}

📋 IN TABLEAU:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Connect → To a Server → Web Data Connector
2. Enter: http://localhost:{PORT}
3. Click Connect
4. Data will load automatically!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    server.serve_forever()


if __name__ == "__main__":
    start_server()
