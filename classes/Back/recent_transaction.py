from Db import Db

class RecentTransaction:
    def __init__(self, db):
        self.db = db

    def get_recent_transactions(self, user_id):
        query = "SELECT category, amount, type, date FROM transactions WHERE user_id = %s ORDER BY date DESC"
        params = (user_id,)
        transactions = self.db.fetch(query, params)
        return transactions

    def print_recent_transactions(self, user_id):
        transactions = self.get_recent_transactions(user_id)
        if transactions:
            print(f"Recent transactions for User ID {user_id}:")
            for transaction in transactions:
                print(f" {transaction[0]} {transaction[1]} {transaction[2]} {transaction[3]}")
        else:
            print(f"No recent transactions found for User ID {user_id}.")

if __name__ == "__main__":
    db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "jean-renoul_budget-buddy")
    recent_transaction = RecentTransaction(db)
    user_id = 4  
    recent_transaction.print_recent_transactions(user_id)
