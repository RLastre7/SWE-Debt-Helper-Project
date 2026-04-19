from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class User:
    """User entity. One user can own many debt records through userID."""

    userID: int | None
    username: str
    password: str
    monthlyBudget: float = 0.0
    preferredStrategy: str = "snowball"
