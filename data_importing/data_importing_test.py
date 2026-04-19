import sqlite3
from data_importing.csv_importer import *
from debt import *
from db import *

#tester showing how the functions might be used
if __name__ == "__main__":
    #create connection to db (making a temperary file for testing purposes)
    db:DatabaseManager = DatabaseManager(":memory:")
    #create table
    db.initialize_schema()
    userId = db.create_user("test_user", "password123")

    #read data
    debts = read_csv("debt_test_data.csv")
    
    #save debts to db table
    for d in debts:
        db.add_debt(userId,d.account_type, d.balance, d.interest, d.min_payment, d.due_date)
    
    #get data from table
    print("Getting all the debts in the table")
    # table_debts = get_all_debts(conn)

    #from the list of the debts print the summary
    user_debts = db.get_debts_by_user(userId)
    for debt in user_debts:
        print(debt.summary())