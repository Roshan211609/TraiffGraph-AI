import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "tariffgraph.db"

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS scenarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT, origin TEXT, market TEXT,
            current_tariff REAL, new_tariff REAL,
            exposure_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

def save_scenario(product, origin, market, current_tariff, new_tariff, score):
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "INSERT INTO scenarios(product,origin,market,current_tariff,new_tariff,exposure_score) VALUES(?,?,?,?,?,?)",
            (product, origin, market, current_tariff, new_tariff, score)
        )

def get_recent_scenarios(limit=10):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.execute("""
            SELECT product, origin, market, current_tariff, new_tariff,
                   exposure_score, created_at
            FROM scenarios ORDER BY id DESC LIMIT ?
        """, (limit,))
        rows = cur.fetchall()
    return [
        {
            "Product": r[0], "Origin": r[1], "Market": r[2],
            "Current tariff": f"{r[3]:g}%",
            "Scenario tariff": f"{r[4]:g}%",
            "Exposure": f"{r[5]:.0f}/100",
            "Saved": r[6],
        } for r in rows
    ]
