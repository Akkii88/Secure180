#!/bin/bash
# FraudShield AI - Complete Startup Script
# Starts everything: Backend, Website, PostgreSQL, Tableau Server

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║      🚀 FRAUDSHIELD AI - STARTING ALL SERVICES           ║"
echo "╚═══════════════════════════════════════════════════════════╝"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================
# Step 1: Start PostgreSQL (if not running)
# ============================================
echo -e "${BLUE}1️⃣  Starting PostgreSQL...${NC}"
if ! brew services list | grep -q "postgresql@14.*started"; then
    brew services start postgresql@14 2>/dev/null
fi
echo -e "${GREEN}   ✅ PostgreSQL ready${NC}"

# ============================================
# Step 2: Start the Fraud Detection System
# ============================================
echo -e "${BLUE}2️⃣  Starting FraudShield AI Backend...${NC}"
cd /Users/ankit/Desktop/Secore180/fraud_detection_system

# Start in background
nohup python3 run_system.py > /tmp/fraudshield.log 2>&1 &
FROG_PID=$!

# Wait for server to start
sleep 5
echo -e "${GREEN}   ✅ Backend running (PID: $FROG_PID)${NC}"

# ============================================
# Step 3: Start Tableau Web Data Connector
# ============================================
echo -e "${BLUE}3️⃣  Starting Tableau Live Connector...${NC}"
nohup python3 tableau_server.py > /tmp/tableau_server.log 2>&1 &
TABLEAU_PID=$!
sleep 2
echo -e "${GREEN}   ✅ Tableau Connector running (PID: $TABLEAU_PID)${NC}"

# ============================================
# Summary
# ============================================
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                   📋 ACCESS URLs                       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}🌐 Website Dashboard:${NC}  http://localhost:8000"
echo -e "${GREEN}📖 API Documentation:${NC}  http://localhost:8000/docs"
echo -e "${GREEN}📊 Tableau Connector:${NC}  http://localhost:8765"
echo -e "${GREEN}📈 Live Data API:${NC}       http://localhost:8765/data.json"
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                📊 TABLEAU SETUP                        ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "To connect Tableau Desktop:"
echo "  1. Open Tableau Desktop"
echo "  2. Connect → To a Server → PostgreSQL"
echo "  3. Server: localhost"
echo "  4. Database: fraudshield"
echo "  5. Username: ankit (leave password empty)"
echo "  6. Select 'Live' connection"
echo ""
echo "Or use Web Data Connector:"
echo "  1. Connect → To a Server → Web Data Connector"
echo "  2. URL: http://localhost:8765"
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                 📝 USAGE TIPS                          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "• Press Cmd+R in Tableau to refresh data"
echo "• Transaction updates every 2 seconds"
echo "• Check logs: tail -f /tmp/fraudshield.log"
echo ""
echo "To STOP everything:"
echo "  pkill -f run_system.py"
echo "  pkill -f tableau_server.py"
echo ""

# Save PIDs for reference
echo "$FROG_PID" > /tmp/fraudshield.pid
echo "$TABLEAU_PID" > /tmp/tableau_connector.pid
echo -e "${GREEN}✅ All services started! Open http://localhost:8000${NC}"