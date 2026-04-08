# FraudShield AI - Complete Project Flow Guide

## 🎯 Project Overview

When you start FraudShield AI, here's what happens:

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRAUDSHIELD AI FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐  │
│   │ Transaction │ ──▶ │ Fraud AI     │ ──▶ │  SQLite DB  │  │
│   │ Simulator   │     │ Detector     │     │  (History) │  │
│   └──────────────┘     └──────────────┘     └──────────────┘  │
│         │                    │                    │              │
│         │                    │                    │              │
│         ▼                    ▼                    ▼              │
│   ┌──────────────────────────────────────────────────────┐     │
│   │              WEBSITE DASHBOARD                      │     │
│   │         http://localhost:8000                      │     │
│   │         (Real-time updates via WebSocket)         │     │
│   └──────────────────────────────────────────────────────┘     │
│                         │                                    │
│                         │                    ┌──────────────┐  │
│                         └───────────────────▶│ PostgreSQL  │  │
│                                            │  (Live)     │  │
│                                            └──────────────┘  │
│                                                 │            │
│                                                 ▼            │
│                                            ┌──────────────┐  │
│                                            │  TABLEAU    │  │
│                                            │  Desktop    │  │
│                                            └──────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 How to Start Everything

### Method 1: Single Command (Recommended!)

```bash
cd /Users/ankit/Desktop/Secore180/fraud_detection_system
./start_all.sh
```

This starts:
- ✅ PostgreSQL database
- ✅ Fraud detection backend (http://localhost:8000)
- ✅ Tableau Web Data Connector (http://localhost:8765)

---

### Method 2: Manual Start

```bash
# Terminal 1: Start PostgreSQL
brew services start postgresql@14

# Terminal 2: Start FraudShield
cd fraud_detection_system
python3 run_system.py

# Terminal 3: Start Tableau Connector (optional - for Web Data Connector)
python3 tableau_server.py
```

---

## 📊 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| **Website Dashboard** | http://localhost:8000 | Cyberpunk dashboard with charts |
| **API Docs** | http://localhost:8000/docs | API documentation |
| **Tableau WDC** | http://localhost:8765 | Web Data Connector |
| **Live Data JSON** | http://localhost:8765/data.json | Direct JSON for developers |
| **PostgreSQL** | localhost:5432/fraudshield | Direct database connection |

---

## 🔄 How Data Flows

### 1. Transaction Generation (Every 2 seconds)
```
Transaction Simulator → Fraud Detector (PyCaret AutoML)
```

### 2. Data Storage
- **SQLite** (fraud_detection.db) - All historical data
- **PostgreSQL** (fraudshield) - Live streaming data for Tableau

### 3. Website Dashboard
- Updates via **WebSocket** - Real-time, no refresh needed!
- URL: http://localhost:8000

### 4. Tableau Dashboard
- Connects to **PostgreSQL** directly (Live connection)
- Shows: Bar charts, scatter plots, KPIs
- Refresh manually with **Cmd+R** (or use Tableau Bridge for auto)

---

## ⏸️ How to Resume Your Work

### If you close everything and come back:

#### Step 1: Start the System (1 command!)
```bash
cd /Users/ankit/Desktop/Secore180/fraud_detection_system
./start_all.sh
```

This will:
- Start PostgreSQL (if not running)
- Start the FraudShield AI backend
- Start the Tableau Web Data Connector

#### Step 2: Open the Website Dashboard
```bash
open http://localhost:8000
```
- You'll see all historical data + live updates
- No manual refresh needed - updates happen automatically via WebSocket

#### Step 3: Open Tableau Desktop
1. Open **Tableau Desktop**
2. Go to **Connect** → **To a Server** → **PostgreSQL**
3. Fill in the connection details:
   - **Server:** `localhost`
   - **Port:** `5432`
   - **Database:** `fraudshield`
   - **Username:** `ankit`
   - **Password:** (leave empty)
4. Select **Live** connection (NOT Extract)
5. Click **Sign In**

#### Step 4: Refresh Your Tableau View
- Press **Cmd+R** (Mac) or **F5** (Windows) to refresh
- Your charts will show the latest data from PostgreSQL

---

### 🔍 Quick Check: Is Everything Running?

Run these commands to verify:

```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# Check if FraudShield is running
ps aux | grep run_system

# Check database has data
psql -d fraudshield -c "SELECT COUNT(*) FROM transactions;"

# Check logs
tail -f /tmp/fraudshield.log
```

---

### 📊 What You'll See After Resume

| Component | What You See |
|-----------|-------------|
| **Website** | All historical transactions + live updates every 2 seconds |
| **Tableau** | Transaction data from PostgreSQL (950+ records) |
| **Charts** | Bar chart showing risk levels (HIGH/MEDIUM/LOW) |

---

### 📊 Your Tableau Progress is Saved Separately!

**Important:** Your charts and work in Tableau are saved in a **workbook file (.twb)**, not in the database connection. This means:

| Action | Result |
|--------|--------|
| Close Tableau | Your charts are saved in the `.twb` file |
| Reopen the `.twb` file | Charts reappear automatically |
| Reconnect to PostgreSQL | Data updates, charts stay the same |
| Delete the `.twb` file | You lose your chart work |

### How Tableau Saves Your Work:

1. **Your chart work is in a `.twb` file:**
   - This contains all your charts, colors, layouts
   - Saved separately from the data connection

2. **Data comes from PostgreSQL:**
   - The connection just brings in data
   - Charts are stored in the workbook file

3. **Two ways to work:**

   **Option A: Reopen your saved workbook (RECOMMENDED)**
   ```
   1. Open your saved .twb file
   2. Tableau auto-reconnects to PostgreSQL
   3. Press Cmd+R to refresh
   4. Your charts are all there!
   ```

   **Option B: Start fresh with new connection**
   ```
   1. Connect → PostgreSQL → fraudshield
   2. Build charts again
   3. Don't forget to Save! (Cmd+S)
   ```

### Quick Resume Checklist:

```bash
# 1. Start the system
cd /Users/ankit/Desktop/Secore180/fraud_detection_system
./start_all.sh

# 2. Open your saved Tableau workbook
open "FraudShield Dashboard.twb"  # or whatever you named it

# 3. Refresh data
# In Tableau: Press Cmd+R (Mac) or F5 (Windows)
```

---

### 💾 Important Reminders:

| Remember | Why |
|----------|-----|
| **Save your .twb file** | Otherwise you lose your chart work |
| **Use Live connection** | Data updates when you refresh |
| **Press Cmd+R** | Manual refresh in Tableau Desktop |
| **Don't delete .twb** | Chart progress is gone forever! |

---

### 🔧 Troubleshooting After Resume

**Problem: Tableau shows "Unable to connect"**

```bash
# 1. Check if PostgreSQL is running
brew services list | grep postgresql

# 2. If not running, start it
brew services start postgresql@14

# 3. Check if database exists
psql -l | grep fraudshield

# 4. If database doesn't exist, recreate it
# Run: python3 -c "from database.postgres_handler import PostgresHandler; p = PostgresHandler(); p.create_table()"
```

**Problem: Website shows old data or errors**

```bash
# Check the logs
tail -f /tmp/fraudshield.log

# Restart the system
pkill -f run_system.py
cd /Users/ankit/Desktop/Secore180/fraud_detection_system
./start_all.sh
```

---

## 🛑 How to Stop Everything

```bash
# Stop FraudShield
pkill -f run_system.py

# Stop Tableau Connector
pkill -f tableau_server.py

# Stop PostgreSQL (optional)
brew services stop postgresql@14
```

---

## 📈 Current Data Status

Check anytime:
```bash
# Check SQLite (all data)
sqlite3 fraud_detection_system/database/fraud_detection.db "SELECT COUNT(*) FROM transactions;"

# Check PostgreSQL (live data)
psql -d fraudshield -c "SELECT COUNT(*) FROM transactions;"
```

---

## 🎨 Building Charts in Tableau

### Recommended Charts:

1. **Horizontal Bar** - Risk levels (HIGH/MEDIUM/LOW)
2. **Scatter Plot** - Fraud probability vs Amount
3. **Line Chart** - Transactions over time
4. **Pie Chart** - Merchant categories
5. **KPI Cards** - Total transactions, Fraud count

### Remember:
- Use **Live** connection (not Extract) for real-time data
- Press **Cmd+R** to refresh (or use Tableau Bridge for auto)

---

## ✅ What's Working Now

- [x] Website Dashboard (http://localhost:8000)
- [x] Real-time transaction flow (every 2 seconds)
- [x] PostgreSQL database (fraudshield)
- [x] Tableau Desktop connection (Live)
- [x] Bar chart visualization

---

## 🔜 Next Steps You Can Add:

- [ ] Tableau Bridge for auto-refresh
- [ ] More chart types
- [ ] Publish to Tableau Cloud
- [ ] Mobile alerts for fraud detection

---

**Last Updated:** April 9, 2026
**Version:** 1.0