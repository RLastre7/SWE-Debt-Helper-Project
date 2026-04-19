from __future__ import annotations

import hashlib
import hmac
from typing import Any


class AccountsService:
    """
    Service layer for registration and login.

    Expected database interface:
    - get_user_by_username(username) -> dict | tuple | object | None
    - create_user(username, password_hash) -> bool | Any
    """

    def __init__(self, db) -> None:
        self.db = db

    def create_account(self, username: str, password: str) -> bool:
        normalized_username = self._normalize_username(username)
        self._validate_password(password)

        existing_user = self.db.get_user_by_username(normalized_username)
        if existing_user is not None:
            return False

        password_hash = self._hash_password(password)
        result = self.db.create_user(normalized_username, password_hash)
        return bool(result) if result is not None else True

    def login(self, username: str, password: str):
        normalized_username = self._normalize_username(username)
        user = self.db.get_user_by_username(normalized_username)

        if user is None:
            return None

        stored_hash = self._get_stored_password(user)
        computed_hash = self._hash_password(password)

        if hmac.compare_digest(stored_hash, computed_hash):
            return user
        return None

    def update_preferences(
        self,
        user_id: int,
        preferred_strategy: str,
    ) -> bool:
        if preferred_strategy not in {"snowball", "avalanche"}:
            raise ValueError("Preferred strategy must be 'snowball' or 'avalanche'.")

        return self.db.update_user_preferences(
            user_id=user_id,
            preferred_strategy=preferred_strategy,
        )

    @staticmethod
    def _normalize_username(username: str) -> str:
        normalized = username.strip()
        if not normalized:
            raise ValueError("Username cannot be empty.")
        return normalized

    @staticmethod
    def _validate_password(password: str) -> None:
        if not password:
            raise ValueError("Password cannot be empty.")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def _get_stored_password(user: Any) -> str:
        if isinstance(user, dict):
            return user.get("password_hash") or user["password"]

        if hasattr(user, "password_hash"):
            return user.password_hash

        if hasattr(user, "password"):
            return user.password

        if isinstance(user, (tuple, list)):
            return user[2]

        raise TypeError(f"Unsupported user record type: {type(user)!r}")
