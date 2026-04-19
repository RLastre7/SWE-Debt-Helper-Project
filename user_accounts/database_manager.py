from __future__ import annotations

import sqlite3
from pathlib import Path

from .models import User


class DatabaseManager:
    def __init__(self, db_path: str | Path = "debt_helper.db") -> None:
        self.db_path = Path(db_path)
        self._initialize_database()

    def _get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_database(self) -> None:
        with self._get_connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    monthly_budget REAL NOT NULL DEFAULT 0,
                    preferred_strategy TEXT NOT NULL DEFAULT 'snowball'
                )
                """
            )
            connection.commit()

    def create_user(
        self,
        username: str,
        password_hash: str,
        monthly_budget: float = 0.0,
        preferred_strategy: str = "snowball",
    ) -> bool:
        try:
            with self._get_connection() as connection:
                cursor = connection.execute(
                    """
                    INSERT INTO users (username, password_hash, monthly_budget, preferred_strategy)
                    VALUES (?, ?, ?, ?)
                    """,
                    (username, password_hash, monthly_budget, preferred_strategy),
                )
                connection.commit()
                return cursor.rowcount == 1
        except sqlite3.IntegrityError:
            return False

    def get_user_by_username(self, username: str) -> User | None:
        with self._get_connection() as connection:
            row = connection.execute(
                """
                SELECT user_id, username, password_hash, monthly_budget, preferred_strategy
                FROM users
                WHERE username = ?
                """,
                (username,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_user(row)

    def get_user_by_id(self, user_id: int) -> User | None:
        with self._get_connection() as connection:
            row = connection.execute(
                """
                SELECT user_id, username, password_hash, monthly_budget, preferred_strategy
                FROM users
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_user(row)

    def update_user_preferences(
        self,
        user_id: int,
        preferred_strategy: str,
    ) -> bool:
        with self._get_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE users
                SET preferred_strategy = ?
                WHERE user_id = ?
                """,
                (preferred_strategy, user_id),
            )
            connection.commit()
            return cursor.rowcount == 1

    @staticmethod
    def _row_to_user(row: sqlite3.Row) -> User:
        return User(
            userID=row["user_id"],
            username=row["username"],
            password=row["password_hash"],
            monthlyBudget=row["monthly_budget"],
            preferredStrategy=row["preferred_strategy"],
        )
