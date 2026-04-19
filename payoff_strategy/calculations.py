class CalculationService:
    def __init__(self, db):
        self.db = db

    def get_totals(self, user_id: int) -> dict:
        raise NotImplementedError

    def compare_strategies_simple(self, user_id: int) -> str:
        raise NotImplementedError
