class CalculationService:
    def __init__(self, db):
        self.db = db

    def get_totals(self, user_id: int) -> dict:
        debts = self.db.get_debts_for_user(user_id)

        total_debt = sum(d["current_balance"] for d in debts)
        total_min_payment = sum(d["minimum_payment"] for d in debts)

        return {
            "total_debt": total_debt,
            "total_min_payment": total_min_payment,
            "num_debts": len(debts),
        }
        

    def compare_strategies_simple(self, user_id: int) -> str:
        debts = self.db.get_debts_for_user(user_id)

        if not debts:
            return "No debts found."

        snowball = sorted(debts, key=lambda d: d["current_balance"])

        avalanche = sorted(debts, key=lambda d: d["interest_rate"], reverse=True)

        result = "SNOWBALL STRATEGY:\n"
        for i, d in enumerate(snowball, 1):
            result += (
                f"{i}. {d['creditor_name']} - "
                f"${d['current_balance']:.2f} "
                f"({d['interest_rate']}%)\n"
            )

        result += "\nAVALANCHE STRATEGY:\n"
        for i, d in enumerate(avalanche, 1):
            result += (
                f"{i}. {d['creditor_name']} - "
                f"{d['interest_rate']}%\n"
            )

        result += "\n\nSnowball: Pay smallest debts first (quick wins)"
        result += "\nAvalanche: Pay highest interest first (save money)"

        return result

    
