import sqlite3
from data_importing.importing import *
from debt import *
from db import *

#tester showing how the functions might be used
if __name__ == "__main__":
    #create connection to db (making a temperary file for testing purposes)
    db:DatabaseManager = DatabaseManager(":memory:")
    importer:ImportService = ImportService(db)
    
    #create table
    db.initialize_schema()
    user_id = db.create_user("test_user", "password123")
    
    #read data from csv and save to table
    importer.import_csv_to_db(user_id,"debt_test_data.csv")
    
    #get data from table
    print("Getting all the debts in the table")
    #from the list of the debts print the summary
    user_debts = db.get_debts_for_user(user_id)
    for debt in user_debts:
        print(debt)