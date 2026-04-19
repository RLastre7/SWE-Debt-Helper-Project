class AccountsService:
    def __init__(self, db):
        self.db = db

    def create_account(self, username: str, password: str) -> bool:
        raise NotImplementedError

    def login(self, username: str, password: str):
        raise NotImplementedError
