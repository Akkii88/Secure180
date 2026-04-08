"""
Tableau Cloud/Server Real-time Pusher for FraudShield AI.

This script pushes live transaction data to Tableau Cloud or Tableau Server
for real-time dashboard updates.

Supports:
- Tableau Cloud (https://online.tableau.com)
- Tableau Server (on-premise)
"""

import os
import sys
import json
import time
from datetime import datetime

# Configuration - Update these for your Tableau setup
TABLEAU_SITE = os.environ.get("TABLEAU_SITE", "")  # Site name for Tableau Cloud
TABLEAU_PROJECT = os.environ.get("TABLEAU_PROJECT", "Default")
TABLEAU_Datasource = os.environ.get("TABLEAU_DATASOURCE", "FraudShield_Realtime")

try:
    import tableauserverclient as TSC

    TAB_CLIENT_AVAILABLE = True
except ImportError:
    TAB_CLIENT_AVAILABLE = False
    print("⚠️ tableau-server-client not installed. Run: pip install tableauserverclient")


class TableauPusher:
    """Push real-time data to Tableau Cloud/Server."""

    def __init__(self):
        self.server_url = os.environ.get("TABLEAU_SERVER_URL", "")
        self.token_name = os.environ.get("TABLEAU_TOKEN_NAME", "")
        self.token_value = os.environ.get("TABLEAU_TOKEN_VALUE", "")
        self.site_id = os.environ.get("TABLEAU_SITE_ID", "")
        self.server = None
        self.connected = False

    def connect(self):
        """Connect to Tableau Server/Cloud."""
        if not TAB_CLIENT_AVAILABLE:
            print("❌ Tableau Server Client not available")
            return False

        if not self.server_url:
            print("❌ TABLEAU_SERVER_URL not set")
            return False

        try:
            # Create server instance
            self.server = TSC.Server(self.server_url, use_server_version=True)

            # Authenticate with personal access token
            tableau_auth = TSC.PersonalAccessTokenAuth(
                self.token_name,
                self.token_value,
                self.site_id if self.site_id else None,
            )

            self.server.auth.sign_in(tableau_auth)
            self.connected = True
            print(f"✅ Connected to Tableau: {self.server_url}")
            return True

        except Exception as e:
            print(f"❌ Tableau connection failed: {e}")
            return False

    def disconnect(self):
        """Disconnect from Tableau."""
        if self.server and self.connected:
            self.server.auth.sign_out()
            self.connected = False

    def push_extract(self, data: list):
        """Push data as Tableau Extract (.hyper) - Best for large datasets."""
        if not self.connected:
            print("❌ Not connected to Tableau")
            return False

        try:
            # Create in-memory DataFrame and export as .hyper
            import pandas as pd

            df = pd.DataFrame(data)

            # Save as hyper file (requires Tableau Hyper SDK - simplified here)
            # For production, use: tableauhyperapi

            print(f"📊 Prepared {len(data)} records for Tableau")
            return True

        except Exception as e:
            print(f"❌ Push failed: {e}")
            return False

    def publish_datasource(self, file_path: str, datasource_name: str):
        """Publish a datasource to Tableau."""
        if not self.connected:
            print("❌ Not connected to Tableau")
            return False

        try:
            # Find project
            projects = [
                p for p in TSC.Pager(self.server.projects) if p.name == TABLEAU_PROJECT
            ]

            if not projects:
                print(f"❌ Project '{TABLEAU_PROJECT}' not found")
                return False

            project_id = projects[0].id

            # Publish datasource
            datasource = TSC.DatasourceItem(project_id)
            datasource = self.server.datasources.publish(
                datasource, file_path, TSC.PublishMode.CreateNew
            )

            print(f"✅ Published datasource: {datasource_name}")
            return True

        except Exception as e:
            print(f"❌ Publish failed: {e}")
            return False


# ============================================
# ALTERNATIVE: Tableau Bridge / REST API Push
# ============================================


class TableauRESTPusher:
    """Push data via Tableau REST API - simpler alternative."""

    def __init__(self):
        self.server_url = os.environ.get("TABLEAU_SERVER_URL", "")
        self.username = os.environ.get("TABLEAU_USERNAME", "")
        self.password = os.environ.get("TABLEAU_PASSWORD", "")
        self.site_id = os.environ.get("TABLEAU_SITE_ID", "")

    def push_csv_to_append(self, csv_path: str):
        """
        Append CSV data to existing datasource using REST API.

        Steps:
        1. Export current datasource to CSV
        2. Append new data
        3. Publish updated datasource

        Note: Full implementation requires Tableau Server Admin access.
        """
        print("📤 Use Tableau Bridge or REST API for live streaming:")
        print("   1. Publish your workbook to Tableau Cloud/Server")
        print("   2. Install Tableau Bridge client")
        print("   3. Configure to keep extract refresh running")
        print("   4. Use /stats and /transactions API endpoints for live data")

        return False


# ============================================
# SIMPLEST SOLUTION: REST API Endpoints
# ============================================


def get_rest_api_info():
    """Show how to connect Tableau to live APIs."""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║            REAL-TIME TABLEAU CONNECTION OPTIONS                      ║
╚══════════════════════════════════════════════════════════════════════╝

OPTION 1: Tableau Web Data Connector (Live)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Start your fraud system: python run_system.py
2. Your API runs at: http://localhost:8000
3. Use: http://localhost:8000/stats  (for stats)
4. Use: http://localhost:8000/transactions  (for transaction data)

OPTION 2: Tableau Bridge (Best for Cloud)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Download Tableau Bridge from: https://www.tableau.com/products/bridge
2. Install and sign in with your Tableau Cloud account
3. Publish your workbook to Tableau Cloud
4. Configure Bridge to refresh extracts every 1-5 minutes
5. Your data will auto-refresh!

OPTION 3: Direct REST API
━━━━━━━━━━━━━━━━━━━━━━━━━
Create custom WDC that reads from:
- http://localhost:8000/stats
- http://localhost:8000/transactions

OPTION 4: PostgreSQL + Tableau
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Set up PostgreSQL database
2. Connect Tableau directly to PostgreSQL
3. Use Tableau Bridge to keep connection live
""")

    return {
        "stats_endpoint": "http://localhost:8000/stats",
        "transactions_endpoint": "http://localhost:8000/transactions",
        "websocket_endpoint": "ws://localhost:8000/ws",
    }


# ============================================
# PUSH FUNCTION FOR MAIN API
# ============================================


def push_to_tableau(result: dict):
    """
    Add this to your main_api.py transaction loop.
    Called on every transaction for real-time updates.
    """
    # For now, just log - full implementation requires Tableau credentials
    print(f"📊 Would push to Tableau: {result.get('transaction_id', 'N/A')}")
    return True


if __name__ == "__main__":
    # Show connection info
    get_rest_api_info()

    # Test connection if credentials provided
    if os.environ.get("TABLEAU_SERVER_URL"):
        pusher = TableauPusher()
        pusher.connect()
        pusher.disconnect()
    else:
        print("\n💡 To enable Tableau push, set these environment variables:")
        print("   export TABLEAU_SERVER_URL='https://your-site.tableau.com'")
        print("   export TABLEAU_TOKEN_NAME='your-token-name'")
        print("   export TABLEAU_TOKEN_VALUE='your-token-value'")
        print("   export TABLEAU_SITE_ID='your-site-id'")
