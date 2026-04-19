import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from db import DatabaseManager
from user_accounts.accounts import AccountsService
from payoff_strategy.calculations import CalculationService
from data_importing.importing import ImportService


class DebtHelperUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Debt Helper")
        self.root.geometry("900x600")

        # Shared DB
        self.db = DatabaseManager("debt_helper.db")
        self.db.initialize_schema()

        # Other modules (might be stubs right now)
        self.accounts = AccountsService(self.db)
        self.calcs = CalculationService(self.db)
        self.importer = ImportService(self.db)

        self.current_user_id = None

        # Screen container
        self.container = ttk.Frame(self.root, padding=10)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for FrameClass in (LoginFrame, DashboardFrame, DebtManagementFrame):
            frame = FrameClass(self.container, self)
            self.frames[FrameClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show("LoginFrame")

    def show(self, name: str):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

    def run(self):
        self.root.mainloop()


class LoginFrame(ttk.Frame):
    def __init__(self, parent, app: DebtHelperUI):
        super().__init__(parent)
        self.app = app

        ttk.Label(self, text="Debt Helper", font=("Arial", 18, "bold")).pack(pady=15)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Username").grid(row=0, column=0, sticky="w", pady=5)
        self.username = tk.StringVar()
        ttk.Entry(form, textvariable=self.username, width=30).grid(row=0, column=1, pady=5)

        ttk.Label(form, text="Password").grid(row=1, column=0, sticky="w", pady=5)
        self.password = tk.StringVar()
        ttk.Entry(form, textvariable=self.password, show="*", width=30).grid(row=1, column=1, pady=5)

        self.status = ttk.Label(self, text="", foreground="red")
        self.status.pack(pady=5)

        btns = ttk.Frame(self)
        btns.pack(pady=15)

        ttk.Button(btns, text="Log In", command=self.login).grid(row=0, column=0, padx=10)
        ttk.Button(btns, text="Create Account", command=self.create_account).grid(row=0, column=1, padx=10)

    def login(self):
        u = self.username.get().strip()
        p = self.password.get().strip()
        if not u or not p:
            self.status.config(text="Enter username and password.")
            return

        try:
            user_id = self.app.accounts.login(u, p)
        except NotImplementedError:
            messagebox.showinfo("Not Ready", "Login module not implemented yet.")
            return

        if user_id is None:
            self.status.config(text="Invalid username or password.")
            return

        self.app.current_user_id = user_id
        self.status.config(text="")
        self.app.show("DashboardFrame")

    def create_account(self):
        u = self.username.get().strip()
        p = self.password.get().strip()
        if not u or not p:
            self.status.config(text="Enter username and password.")
            return

        try:
            ok = self.app.accounts.create_account(u, p)
        except NotImplementedError:
            messagebox.showinfo("Not Ready", "Create account module not implemented yet.")
            return

        if not ok:
            self.status.config(text="Username already exists.")
            return

        messagebox.showinfo("Success", "Account created. You can log in now.")
        self.status.config(text="")


class DashboardFrame(ttk.Frame):
    def __init__(self, parent, app: DebtHelperUI):
        super().__init__(parent)
        self.app = app

        top = ttk.Frame(self)
        top.pack(fill="x", pady=10)

        ttk.Label(top, text="Dashboard", font=("Arial", 16, "bold")).pack(side="left")
        ttk.Button(top, text="Log Out", command=self.logout).pack(side="right")

        self.total_debt_label = ttk.Label(self, text="Total Debt: $0.00", font=("Arial", 12))
        self.total_debt_label.pack(pady=10)

        self.total_min_label = ttk.Label(self, text="Total Min Payments: $0.00 / month", font=("Arial", 12))
        self.total_min_label.pack(pady=10)

        actions = ttk.LabelFrame(self, text="Actions", padding=10)
        actions.pack(fill="x", pady=20)

        ttk.Button(actions, text="View Debts", command=lambda: self.app.show("DebtManagementFrame")).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(actions, text="Import CSV", command=self.import_csv).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(actions, text="Strategy Summary", command=self.strategy_summary).grid(row=0, column=2, padx=10, pady=5)

    def on_show(self):
        if self.app.current_user_id is None:
            self.app.show("LoginFrame")
            return

        # Update totals if calc module exists
        try:
            totals = self.app.calcs.get_totals(self.app.current_user_id)
            self.total_debt_label.config(text=f"Total Debt: ${totals['total_debt']:.2f}")
            self.total_min_label.config(text=f"Total Min Payments: ${totals['total_min_payment']:.2f} / month")
        except NotImplementedError:
            # Keep placeholders if not ready
            self.total_debt_label.config(text="Total Debt: (not calculated yet)")
            self.total_min_label.config(text="Total Min Payments: (not calculated yet)")

    def logout(self):
        self.app.current_user_id = None
        self.app.show("LoginFrame")

    def import_csv(self):
        if self.app.current_user_id is None:
            return

        path = filedialog.askopenfilename(title="Select CSV", filetypes=[("CSV Files", "*.csv")])
        if not path:
            return

        try:
            count = self.app.importer.import_debts_from_csv(self.app.current_user_id, path)
            messagebox.showinfo("Import Complete", f"Imported {count} debts.")
            self.on_show()
        except NotImplementedError:
            messagebox.showinfo("Not Ready", "Import module not implemented yet.")
        except Exception as e:
            messagebox.showerror("Import Error", str(e))

    def strategy_summary(self):
        if self.app.current_user_id is None:
            return

        try:
            summary = self.app.calcs.compare_strategies_simple(self.app.current_user_id)
            messagebox.showinfo("Strategy Summary", summary)
        except NotImplementedError:
            messagebox.showinfo("Not Ready", "Payoff strategy module not implemented yet.")


class DebtManagementFrame(ttk.Frame):
    def __init__(self, parent, app: DebtHelperUI):
        super().__init__(parent)
        self.app = app

        top = ttk.Frame(self)
        top.pack(fill="x", pady=10)

        ttk.Label(top, text="Debt Management", font=("Arial", 16, "bold")).pack(side="left")
        ttk.Button(top, text="Back", command=lambda: self.app.show("DashboardFrame")).pack(side="right")

        self.tree = ttk.Treeview(self, columns=("Creditor", "Balance", "APR", "MinPay", "Due"), show="headings")
        for col, title in [
            ("Creditor", "Creditor"),
            ("Balance", "Balance"),
            ("APR", "APR"),
            ("MinPay", "Min Payment"),
            ("Due", "Due Date"),
        ]:
            self.tree.heading(col, text=title)
            self.tree.column(col, width=150)
        self.tree.pack(fill="both", expand=True, pady=10)

        btns = ttk.Frame(self)
        btns.pack(pady=10)

        ttk.Button(btns, text="Add Dummy Debt (temp)", command=self.add_dummy).grid(row=0, column=0, padx=8)
        ttk.Button(btns, text="Refresh", command=self.refresh).grid(row=0, column=1, padx=8)

        # Placeholder buttons for later
        ttk.Button(btns, text="Edit Selected (later)", state="disabled").grid(row=0, column=2, padx=8)
        ttk.Button(btns, text="Delete Selected (later)", state="disabled").grid(row=0, column=3, padx=8)

    def on_show(self):
        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        if self.app.current_user_id is None:
            return

        debts = self.app.db.get_debts_for_user(self.app.current_user_id)
        for d in debts:
            self.tree.insert(
                "", "end",
                values=(
                    d["creditor_name"],
                    f"${d['current_balance']:.2f}",
                    f"{d['interest_rate']:.2f}",
                    f"${d['minimum_payment']:.2f}",
                    d["due_date"],
                ),
            )

    def add_dummy(self):
        if self.app.current_user_id is None:
            return

        # Safe for you to do: calls shared db layer
        self.app.db.add_debt(
            user_id=self.app.current_user_id,
            creditor_name="Demo Credit Card",
            current_balance=1200.00,
            interest_rate=24.99,
            minimum_payment=35.00,
            due_date="2026-04-30",
        )
        self.refresh()
