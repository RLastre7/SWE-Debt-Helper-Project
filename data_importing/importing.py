import pandas as pd
from pathlib import Path
from debt import Debt
from db import DatabaseManager

class ImportService:
    def __init__(self, db: DatabaseManager):
        self.db = db

    # will read from csv file and return the neccesary data in a list of dicts
    # CSV should be in format: Debt Name,Current Balance,Interest Rate (%),Minimum Payment,Due Date
    # examples:
    #     Chase Credit Card,1500.00,19.99,50.00,15
    #     Student Loan A,12000.00,4.5,150.00,1
    @staticmethod
    def import_debts_from_csv(csv_path: str): 

        path = Path(csv_path)
        if not path.is_absolute():
            path = Path(__file__).parent / path   

        # check if exists
        if not path.exists():
            raise FileNotFoundError(path)
        data = pd.read_csv(path)
        debts = [
            Debt(
                row["Debt Name"],
                row["Current Balance"],
                row["Interest Rate (%)"],
                row["Minimum Payment"],
                row["Due Date"]
            )
            for _, row in data.iterrows()
        ]

        return debts

    #imports from csv and saves to db in one function
    def import_csv_to_db(self,user_id:int ,csv_path: str):
        debts = self.import_debts_from_csv(csv_path)
        for debt in debts:
            self.db.add_debt(user_id,debt)

