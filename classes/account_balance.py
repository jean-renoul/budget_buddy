import mysql.connector

from Db import Db

class AccountBalance:
    def __init__(self, name):
        self.name = name
        self.db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "jean-renoul_budget-buddy")

    def get_transactions(self):
        query = "SELECT user_id, amount, type FROM transactions WHERE name = %s ORDER BY transaction_id"
        params = (self.name,)
        transactions = self.db.fetch(query, params)
        return transactions

    def calculate_balance(self):
        transactions = self.get_transactions()
        balance = 1000  # Solde initial
        prev_user_id = None
        for user_id, amount, type in transactions:
            if prev_user_id is None or prev_user_id != user_id:
                # Nouvel ID, imprimer le solde actuel
                if prev_user_id is not None:
                    print(f"Solde actuel pour l'utilisateur avec l'ID {prev_user_id}: {balance}")
                balance = 1000  # Réinitialiser le solde pour le nouvel ID
            if type == "revenu":
                balance += amount
            elif type == "dépense":
                balance -= amount
            prev_user_id = user_id
        # Dernier solde pour le dernier utilisateur
        if prev_user_id is not None:
            print(f"Solde actuel pour l'utilisateur avec l'ID {prev_user_id}: {balance}")

if __name__ == "__main__":
    account_balance = AccountBalance("Renoul Jean")  # Remplacez par le nom de l'utilisateur souhaité
    account_balance.calculate_balance()
