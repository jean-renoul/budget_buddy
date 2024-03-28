
from datetime import datetime
from Db import Db
from BalanceUpdater import BalanceUpdater

class TransactionManager:
    def __init__(self):
        self.db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "jean-renoul_budget-buddy")
        self.balance_updater = BalanceUpdater()

    def add_transaction(self, user_id, name, description, category, amount, transaction_type, date=None):
        date = date if date else datetime.now().date()
        query = "INSERT INTO transactions (user_id, name, description, category, amount, type, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        params = (user_id, name, description, category, amount, transaction_type, date)
        self.db.executeQuery(query, params)
        # Mettre à jour la balance de l'utilisateur
        self.balance_updater.update_balance(user_id, amount, transaction_type)

if __name__ == "__main__":
    transaction_manager = TransactionManager()
    # Exemple d'utilisation : ajout d'une transaction
    transaction_manager.add_transaction(user_id=4, name="Shopping", description="T-Shirt", category="Closes", amount=20.0, transaction_type="income")
