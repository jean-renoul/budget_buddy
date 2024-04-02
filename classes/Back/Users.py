from classes.Back.Db import Db

class Users:

    def __init__(self, last_name, first_name, email, password, balance=1000.00):
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.password = password
        self.balance = balance
        self.transactions = []
        self.db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "jean-renoul_budget-buddy")
    
    def get_balance(self):
        return self.balance
    
    def set_user_balance(self):
        balance = self.db.fetch("SELECT balance FROM users WHERE email = %s", (self.email,))
        self.balance = balance[0][0]

    def set_id(self):
        id = self.db.fetch("SELECT user_id FROM users WHERE email = %s", (self.email,))
        self.id = id[0][0]

    def set_transactions(self):
        transactions = self.db.fetch("SELECT name, description, amount, date, category, type FROM transactions WHERE user_id = %s", (self.id,))
        self.transactions = transactions

    def sort_transactions_by_amount(self):
        self.transactions = sorted(self.transactions, key=lambda x: x[2])

    def sort_transactions_by_date(self):
        self.transactions = sorted(self.transactions,reverse=True, key=lambda x: x[3])

    def sort_transactions_by_category(self):
        self.transactions = sorted(self.transactions, key=lambda x: x[4])

    def sort_transactions_by_type(self):
        self.transactions = sorted(self.transactions, key=lambda x: x[5])

    def update(self):
        self.set_id()
        self.set_user_balance()
        self.set_transactions()

