from Db import Db

class BalanceUpdater:
    def __init__(self):
        self.db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "jean-renoul_budget-buddy")

    def update_balance(self, user_id, amount, transaction_type):
        current_balance = self.get_user_balance(user_id)
        if transaction_type == 'expense':
            new_balance = current_balance - amount
        else:
            new_balance = current_balance + amount
        query = "UPDATE users SET balance = %s WHERE user_id = %s"
        params = (new_balance, user_id)
        self.db.executeQuery(query, params)

    def get_user_balance(self, user_id):
        query = "SELECT balance FROM users WHERE user_id = %s"
        params = (user_id,)
        result = self.db.fetch(query, params)
        if result:
            return result[0][0]
        else:
            return None
