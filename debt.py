class Debt:
    def __init__(self, creditor_name,current_balance, interest_rate, minimum_payment, due_date):
        self.creditor_name = creditor_name
        self.current_balance = current_balance
        self.interest_rate = interest_rate
        self.minimum_payment = minimum_payment
        self.due_date = due_date

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            creditor_name=data["debt_name"],
            current_balance=data["current_balance"],
            interest_rate=data["interest_rate"],
            minimum_payment=data["minimum_payment"],
            due_date=data["due_date"]
        )
    
    #prints a summary of the debt (Name: balance)
    def print_summary(self):
        print(f"{self.creditor_name}: {self.current_balance}")

