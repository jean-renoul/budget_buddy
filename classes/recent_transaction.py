import mysql.connector
from Db import Db



class RecentTransaction:
    def __init__(self, user_id):
        self.user_id = user_id
        self.db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "jean-renoul_budget-buddy")

    def get_recent_transactions(self):
        query = "SELECT category, amount, type, date FROM transactions WHERE user_id = %s ORDER BY date DESC"
        params = (self.user_id,)
        transactions = self.db.fetch(query, params)
        return transactions

    def print_recent_transactions(self):
        transactions = self.get_recent_transactions()
        if transactions:
            print(f"Recent transactions for User ID {self.user_id}:")
            for transaction in transactions:
                print(f" {transaction[0]} {transaction[1]} {transaction[2]} {transaction[3]}")
        else:
            print(f"No recent transactions found for User ID {self.user_id}.")

if __name__ == "__main__":
    recent_transaction = RecentTransaction(6)  # Remplacez par l'ID utilisateur souhaité
    recent_transaction.print_recent_transactions()
