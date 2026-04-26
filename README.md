Debt Helper Final Product  
Team 3  

What this is  
Debt Helper is a simple desktop app prototype that helps a user keep track of multiple debts in one place. The goal is to make debt tracking less messy than spreadsheets and give a basic payoff strategy view.

Tech used  
Python  
Tkinter for the desktop UI  
SQLite for local data storage  
Pandas for CSV importing  

How to run  
1. Download or clone the repo  
2. Open Command Prompt or PowerShell in the project folder  
3. Install dependencies (recommended)  
   - python -m pip install -r requirements.txt  
4. Run the app  
   - python main.py  
   - If python does not work, try: py main.py  
5. The app window should open to the login screen  

How to test quickly  
1. Create an account (any username and password)  
2. Log in  
3. Click View Debts and add the dummy debt  
4. Import a CSV file and confirm imported debts appear  
5. Click Strategy Summary to view the payoff strategy output  

CSV import format  
The importer expects this header format:  
Debt Name,Current Balance,Interest Rate (%),Minimum Payment,Due Date  

A sample file is included in the repo:  
sampledebts.csv  

What works right now  
Account creation and login (local)  
Add and view debts (basic list)  
CSV import and saving debts to the database  
Dashboard totals (based on stored debts)  
Strategy summary (basic comparison output)  
Basic UI navigation  

What is still in progress  
Payments are not fully implemented yet  
Reminders are not fully implemented yet  
UI polish and extra input validation is still being improved  

Repo structure  
user_interface  
Tkinter screens and navigation  

user_accounts  
Account creation and login logic  

data_importing  
CSV import logic  

payoff_strategy  
Payoff strategy logic and summaries  

db.py and debt.py  
Database setup and Debt data structure  

Notes  
This is a class project prototype. The focus is on being functional and testable, not on full production security or a fully polished UI.
