class Debt:
    def __init__(self, name, account_type, balance, interest, min_payment, due_date):
        self.name = name
        self.account_type = account_type
        self.balance = balance
        self.interest = interest
        self.min_payment = min_payment
        self.due_date = due_date

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["debt_name"],
            account_type=data["account_type"],
            balance=data["current_balance"],
            interest=data["interest_rate"],
            min_payment=data["minimum_payment"],
            due_date=data["due_date"]
        )
    
    #prints a summary of the debt (Name: balance)
    def print_summary(self):
        print(f"{self.name}: {self.balance}")

