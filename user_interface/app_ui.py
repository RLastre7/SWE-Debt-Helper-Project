import tkinter as tk
from tkinter import ttk, messagebox

from db import DatabaseManager
from user_accounts.accounts import AccountsService
from payoff_strategy.calculations import CalculationService
from data_importing.importing import ImportService

class DebtHelperUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Debt Helper")
        self.root.geometry("900x600")

        self.db = DatabaseManager("debt_helper.db")
        self.db.initialize_schema()

        # These are other people's modules. Stubs are ok for now.
        self.accounts = AccountsService(self.db)
        self.calcs = CalculationService(self.db)
        self.importer = ImportService(self.db)

        self.current_user_id = None

        self.container = ttk.Frame(self.root, padding=10)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for FrameClass in (LoginFrame, DashboardFrame):
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

        btns = ttk.Frame(self)
        btns.pack(pady=15)

        ttk.Button(btns, text="Log In", command=self.login).grid(row=0, column=0, padx=10)
        ttk.Button(btns, text="Create Account", command=self.create).grid(row=0, column=1, padx=10)

    def login(self):
        try:
            user_id = self.app.accounts.login(self.username.get().strip(), self.password.get().strip())
            if user_id is None:
                messagebox.showerror("Login Failed", "Invalid username or password.")
                return
            self.app.current_user_id = user_id
            self.app.show("DashboardFrame")
        except NotImplementedError:
            messagebox.showinfo("Not Ready", "Login module not implemented yet.")

    def create(self):
        try:
            ok = self.app.accounts.create_account(self.username.get().strip(), self.password.get().strip())
            if ok:
                messagebox.showinfo("Success", "Account created. You can log in now.")
            else:
                messagebox.showerror("Error", "Username already exists.")
        except NotImplementedError:
            messagebox.showinfo("Not Ready", "Create account module not implemented yet.")

class DashboardFrame(ttk.Frame):
    def __init__(self, parent, app: DebtHelperUI):
        super().__init__(parent)
        self.app = app

        ttk.Label(self, text="Dashboard", font=("Arial", 16, "bold")).pack(pady=15)
        self.summary = ttk.Label(self, text="Totals will show here once calculations module is done.")
        self.summary.pack(pady=10)

        ttk.Button(self, text="Log Out", command=self.logout).pack(pady=10)

    def on_show(self):
        # Later you will call self.app.calcs.get_totals(user_id)
        pass

    def logout(self):
        self.app.current_user_id = None
        self.app.show("LoginFrame")
