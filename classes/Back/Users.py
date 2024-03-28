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

    def set_user_balance(self):
        balance = self.db.fetch("SELECT balance FROM users WHERE email = %s", (self.email,))
        self.balance = balance[0][0]

    def set_id(self):
        id = self.db.fetch("SELECT user_id FROM users WHERE email = %s", (self.email,))
        self.id = id[0][0]

    def set_transactions(self):
        transactions = self.db.fetch("SELECT description, amount, date, type FROM transactions WHERE user_id = %s", (self.id,))
        for transaction in transactions:
            transaction = f"{transaction[0]} {transaction[1]} {transaction[2]} {transaction[3]}"
            self.transactions.append(transaction)

    def update(self):
        self.set_id()
        self.set_user_balance()
        self.set_transactions()


