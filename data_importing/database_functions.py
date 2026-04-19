import sqlite3
from debt import *

#creates a table to store the info given a database connection
def create_tables(conn:sqlite3.Connection ):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS debts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            debt_name TEXT NOT NULL,
            account_type TEXT NOT NULL,
            current_balance REAL NOT NULL,
            interest_rate REAL NOT NULL,
            minimum_payment REAL NOT NULL,
            due_date INTEGER NOT NULL
        )
    """)

    conn.commit()

#takes in a database and list of debts and adds them to the database
def save_debt(conn: sqlite3.Connection, debts):
    #open connection
    cursor = conn.cursor()

    for debt in debts:
        cursor.execute("""
            INSERT INTO debts
            (debt_name, account_type, current_balance,
            interest_rate, minimum_payment, due_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            debt["Debt Name"],
            debt["Account Type"],
            debt["Current Balance"],
            debt["Interest Rate (%)"],
            debt["Minimum Payment"],
            debt["Due Date"]
        ))

    conn.commit()

#returns a list of all the debts in the table
def get_all_debts(conn: sqlite3.Connection) -> list[Debt]:
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM debts")
    rows = cursor.fetchall()
    return [Debt.from_dict(row) for row in rows]

#execute any sql command on a connection
def execute(conn:sqlite3.Connection, command:str, params=()):
    cursor = conn.cursor()
    cursor.execute(command,params)
    conn.commit()



