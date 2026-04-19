import sqlite3
import pandas as pd
from pathlib import Path


# will read from csv file and return the neccesary data in a list of dicts
# CSV should be in format: Debt Name,Account Type,Current Balance,Interest Rate (%),Minimum Payment,Due Date
# examples:
#     Chase Credit Card,Credit Card,1500.00,19.99,50.00,15
#     Student Loan A,Loan,12000.00,4.5,150.00,1
def read_csv(file: str) -> list[dict]:
    #parent folder
    base_path = Path(__file__).parent

    # build full path safely
    full_path = base_path / file

    # check if exists
    if not full_path.exists():
        print("File not found:", full_path)
        return
    data = pd.read_csv(full_path)
    all_debts = data.to_dict(orient="records")
    return all_debts




