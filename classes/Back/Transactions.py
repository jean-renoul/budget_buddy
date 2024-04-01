
from datetime import datetime
from classes.Back.Db import Db
from classes.Back.BalanceUpdater import BalanceUpdater

class Transactions:
    def __init__(self,user_id, name, description, category, amount, transaction_type, date=None):
        self.db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "jean-renoul_budget-buddy")
        self.balance_updater = BalanceUpdater()
        self.user_id = user_id
        self.name = name
        self.description = description
        self.category = category
        self.amount = amount
        self.transaction_type = transaction_type
        self.date = date

    def add_transaction(self):
        date = date if self.date else datetime.now().date()
        query = "INSERT INTO transactions (user_id, name, description, category, amount, type, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        params = (self.user_id, self.name, self.description, self.category, self.amount, self.transaction_type, date)
        self.db.executeQuery(query, params)
        # Mettre à jour la balance de l'utilisateur
        self.balance_updater.update_balance(self.user_id, self.amount, self.transaction_type)

if __name__ == "__main__":
    transaction_manager = Transactions()
    # Exemple d'utilisation : ajout d'une transaction
    transaction_manager.add_transaction(user_id=4, name="Shopping", description="Tacos", category="Food", amount=20.0, transaction_type="expense")
