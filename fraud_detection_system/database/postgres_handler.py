"""
PostgreSQL Database Handler for FraudShield AI - Real-time streaming to Tableau.
"""

import os
import json
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

# PostgreSQL connection - using local socket (no password needed for local mac user)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost/fraudshield")

engine = create_engine(DATABASE_URL, poolclass=NullPool)


def init_postgres_db():
    """Initialize PostgreSQL database with tables."""
    with engine.connect() as conn:
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                transaction_id VARCHAR(50) UNIQUE,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                amount DECIMAL(12,2),
                merchant_category VARCHAR(100),
                location VARCHAR(100),
                fraud_probability DECIMAL(5,4),
                prediction INTEGER,
                risk_level VARCHAR(20)
            )
        """)
        )

        conn.execute(
            text("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON transactions(timestamp DESC)
        """)
        )

        conn.execute(
            text("""
            CREATE INDEX IF NOT EXISTS idx_risk_level ON transactions(risk_level)
        """)
        )

        conn.commit()
    print("✅ PostgreSQL database initialized!")


def insert_transaction_postgres(result: dict):
    """Insert transaction to PostgreSQL for real-time Tableau streaming."""
    try:
        with engine.connect() as conn:
            conn.execute(
                text("""
                INSERT INTO transactions 
                (transaction_id, timestamp, amount, merchant_category, location, 
                 fraud_probability, prediction, risk_level)
                VALUES (:tid, :ts, :amt, :cat, :loc, :prob, :pred, :risk)
                ON CONFLICT (transaction_id) DO NOTHING
            """),
                {
                    "tid": result.get("transaction_id", ""),
                    "ts": result.get("timestamp", datetime.now().isoformat()),
                    "amt": result.get("amount", 0),
                    "cat": result.get("merchant_category", "Unknown"),
                    "loc": result.get("location", "Unknown"),
                    "prob": result.get("fraud_probability", 0),
                    "pred": result.get("prediction", 0),
                    "risk": result.get("risk_level", "LOW"),
                },
            )
            conn.commit()
    except Exception as e:
        print(f"PostgreSQL insert error: {e}")


def get_recent_transactions_postgres(limit: int = 100):
    """Get recent transactions from PostgreSQL."""
    with engine.connect() as conn:
        result = conn.execute(
            text("""
            SELECT id, transaction_id, timestamp, amount, merchant_category,
                   location, fraud_probability, prediction, risk_level
            FROM transactions
            ORDER BY timestamp DESC
            LIMIT :limit
        """),
            {"limit": limit},
        )

        return [dict(row._mapping) for row in result]


def get_fraud_stats_postgres():
    """Get fraud statistics from PostgreSQL."""
    with engine.connect() as conn:
        result = conn.execute(
            text("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END) as fraud_count,
                SUM(CASE WHEN risk_level = 'HIGH' THEN 1 ELSE 0 END) as high_risk,
                SUM(CASE WHEN risk_level = 'MEDIUM' THEN 1 ELSE 0 END) as medium_risk,
                SUM(CASE WHEN risk_level = 'LOW' THEN 1 ELSE 0 END) as low_risk,
                AVG(fraud_probability) as avg_fraud_prob
            FROM transactions
        """)
        )
        row = result.fetchone()
        return (
            {
                "total_transactions": row[0] or 0,
                "fraud_detected": row[1] or 0,
                "high_risk": row[2] or 0,
                "medium_risk": row[3] or 0,
                "low_risk": row[4] or 0,
                "avg_fraud_probability": float(row[5] or 0),
            }
            if row
            else {}
        )


def clear_transactions():
    """Clear all transactions from PostgreSQL - call at startup for fresh start."""
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM transactions"))
        conn.commit()
    print("🗑️  Cleared all transactions from PostgreSQL (fresh start!)")
