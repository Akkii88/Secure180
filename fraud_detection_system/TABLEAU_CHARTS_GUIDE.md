# Tableau Dashboard Charts Guide

Based on your website dashboard, here are the **6 charts** you should create in Tableau:

---

## 📊 Chart List (Match Your Website)

| # | Chart Name | Website Section | Tableau Type |
|---|------------|-----------------|---------------|
| 1 | **KPI Cards** | Top row | KPI / Text |
| 2 | **Good vs Bad** | Doughnut | Pie/Donut |
| 3 | **Payment Stream** | Line chart | Line |
| 4 | **Store Fraud** | Horizontal bar | Bar (horizontal) |
| 5 | **Fraud by Hour** | Bottom bar | Bar (vertical) |
| 6 | **Geographic Map** | Globe | Map |

---

## 🔧 Step-by-Step Setup

### Prerequisites
1. Start system: `./start_all.sh`
2. In Tableau: Connect → PostgreSQL → Database: `fraudshield` → Live connection

---

### Chart 1: KPI Cards (4 cards)

Create 4 "Text" objects showing:

| KPI | Field | Calculation |
|-----|-------|-------------|
| Total Transactions | `count(transaction_id)` | COUNT |
| Fraud Detected | `SUM(CASE WHEN prediction=1 THEN 1 ELSE 0 END)` | - |
| Fraud Rate | `SUM(prediction) / COUNT(*) * 100` | - |
| Money Saved | `SUM(CASE WHEN prediction=1 THEN amount ELSE 0 END)` | SUM |

**Tip:** Right-click field → Create Calculated Field

---

### Chart 2: Good vs Bad (Donut)

- **Type:** Pie Chart
- **Fields:**
  - **Color:** `prediction` (0=Legitimate, 1=Fraud)
  - **Size:** COUNT
- **Labels:** Show percentage

**Colors:**
- Legitimate: Blue (#00d4ff)
- Fraud: Red (#ff2d55)

---

### Chart 3: Payment Stream (Line)

- **Type:** Line Chart
- **Fields:**
  - **X-Axis:** `timestamp` (continuous)
  - **Y-Axis:** `amount`
  - **Color:** `prediction` (filter to show fraud in red)
- **Settings:** Show last 60 points

---

### Chart 4: Store Fraud Rates (Horizontal Bar)

- **Type:** Bar Chart (horizontal)
- **Fields:**
  - **Y-Axis:** `merchant_category`
  - **X-Axis:** `SUM(CASE WHEN prediction=1 THEN 1 ELSE 0 END) / COUNT(*) * 100` (Fraud Rate %)
- **Sort:** Descending by fraud rate
- **Colors:** Gradient from blue (low) to red (high)

---

### Chart 5: Fraud by Hour (Vertical Bar)

- **Type:** Bar Chart
- **Fields:**
  - **X-Axis:** Hour (extract from timestamp: `DATEPART('hour', timestamp)`)
  - **Y-Axis:** COUNT of fraud transactions (prediction = 1)
- **Sort:** Natural (0-23)

---

### Chart 6: Geographic Map

- **Type:** Map
- **Fields:**
  - **Geography:** `location` (Tableau will auto-recognize cities)
  - **Size:** COUNT of fraud
- **Map Style:** Dark theme

**Location field examples:**
- "New York/USA" → New York
- "London/UK" → London

---

## 📐 Layout建议

```
┌──────────────────────────────────────────────────┐
│  KPI CARDS (4 across)                            │
├─────────────────┬────────────────────────────────┤
│                 │                                │
│  DONUT          │  LINE CHART (Payment Stream)  │
│  Good vs Bad    │                                │
│                 │                                │
├─────────────────┴────────────────────────────────┤
│                                                  │
│  HORIZONTAL BAR (Store Categories)              │
│                                                  │
├────────────────────────────┬─────────────────────┤
│                            │                     │
│  MAP (Locations)           │  BAR (Hourly)       │
│                            │                     │
└────────────────────────────┴─────────────────────┘
```

---

## 🎨 Color Palette (Match Website)

Use these colors in Tableau:

| Element | Color Code |
|---------|------------|
| Background | #020810 (dark) |
| Accent/Cyan | #00d4ff |
| Success/Green | #00ff9d |
| Danger/Red | #ff2d55 |
| Warning/Yellow | #ffb800 |
| Purple | #a855f7 |
| Border | #0d2444 |

---

## ⏱️ Auto-Refresh Options

| Option | How |
|--------|-----|
| **Manual** | Press Cmd+R (Mac) or F5 (Windows) |
| **Auto** | Use Tableau Bridge (requires Cloud subscription) |
| **Website** | Updates automatically via WebSocket |

---

## 💾 Saving Your Work

1. **Save your workbook:** File → Save (creates .twb file)
2. **Reopen later:** Just open the .twb file, it reconnects automatically
3. **Don't lose work:** Always save before closing Tableau!

---

## 🔄 Quick Refresh

After creating charts:
1. Press **Cmd+R** to refresh all data
2. New transactions appear every 2 seconds in PostgreSQL
3. Refresh again to see updated numbers

---

**Note:** Your website uses data from both SQLite (historical) + PostgreSQL (live). Tableau only shows live session data from PostgreSQL (cleared on each system restart).