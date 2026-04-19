import sqlite3
from csv_importer import *
from database_functions import *
from debt import *

#tester showing how the functions might be used
if __name__ == "__main__":
    #create connection to db (making a temperary file for testing purposes)
    conn = sqlite3.connect(":memory:")

    #create table
    print("Creating table")
    create_tables(conn)

    #read data
    print("Reading debt from csv")
    debts = read_csv("debt_test_data.csv")
    
    #save debts to db table
    print("Saving Debts")
    save_debt(conn, debts)

    #get data from table
    print("Getting all the debts in the table")
    table_debts = get_all_debts(conn)

    #from the list of the debts print the summary
    for d in table_debts:
        d.print_summary()

    conn.close()