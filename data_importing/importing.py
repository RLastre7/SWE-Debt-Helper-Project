class ImportService:
    def __init__(self, db):
        self.db = db

    def import_debts_from_csv(self, user_id: int, csv_path: str) -> int:
        raise NotImplementedError
