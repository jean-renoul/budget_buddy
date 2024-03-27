from Db import Db

class Transactions:
    def __init__(self, name, date, category, description, amount, type):
        self.name = name
        self.date = date
        self.category = category
        self.description = description
        self.amount = amount
        self.type = type
        self.db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "jean-renoul_budget-buddy")

    def get_transactions(self):
        query = "SELECT * FROM transactions WHERE name = %s"
        return self.db.fetch(query, (self.name,))