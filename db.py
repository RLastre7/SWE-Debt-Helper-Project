import sqlite3
from typing import Any, Dict, List, Optional
from debt import *

class DatabaseManager:
    def __init__(self, db_path: str = "debt_helper.db"):
        self.conn = sqlite3.connect(db_path)
        self.db_path = db_path
        self.conn.row_factory = sqlite3.Row

    def initialize_schema(self) -> None:
        conn = self.conn
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            monthly_budget REAL DEFAULT 0,
            preferred_strategy TEXT DEFAULT 'snowball'
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS debt (
            debt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            creditor_name TEXT NOT NULL,
            current_balance REAL NOT NULL,
            interest_rate REAL NOT NULL,
            minimum_payment REAL NOT NULL,
            due_date TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES user(user_id)
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS payment (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            debt_id INTEGER NOT NULL,
            amount_paid REAL NOT NULL,
            payment_date TEXT NOT NULL,
            remaining_balance REAL NOT NULL,
            FOREIGN KEY(debt_id) REFERENCES debt(debt_id)
        )
        """)

        conn.commit()

    def create_user(self, username: str, password_hash: str) -> bool:
        try:
            conn = self.conn
            conn.execute(
                "INSERT INTO user (username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        conn = self.conn
        row = conn.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        return dict(row) if row else None

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        conn = self.conn
        row = conn.execute("SELECT * FROM user WHERE user_id = ?", (user_id,)).fetchone()
        return dict(row) if row else None

    def update_user_preferences(self, user_id: int, preferred_strategy: str) -> bool:
        conn = self.conn
        cur = conn.execute(
            "UPDATE user SET preferred_strategy = ? WHERE user_id = ?",
            (preferred_strategy, user_id),
        )
        conn.commit()
        return cur.rowcount == 1
    
    def add_debt(self, user_id: int,debt: Debt) -> int:
            conn = self.conn
            cur = conn.execute("""
                INSERT INTO debt (user_id, creditor_name, current_balance, interest_rate, minimum_payment, due_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, debt.creditor_name, debt.current_balance, debt.interest_rate, debt.minimum_payment, debt.due_date))
            conn.commit()
            return int(cur.lastrowid)
    

    def get_debts_for_user(self, user_id: int) -> List[Dict[str, Any]]:
        conn = self.conn
        rows = conn.execute("SELECT * FROM debt WHERE user_id = ? ORDER BY debt_id", (user_id,)).fetchall()
        return [dict(r) for r in rows]
