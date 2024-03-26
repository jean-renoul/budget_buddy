from Connection import Connection
from Transactions import Transactions

if __name__ == "__main__":
    connection = Connection("Doe", "John", "John.Doe@gmail.com", "Password10!")
    if connection.login():
        user_balance = connection.get_user_balance()
        if user_balance is not None:
            print("Balance de l'utilisateur:", user_balance)
            name = "Nouvelle transaction"
            date = "2024-03-26"
            category = "Alimentation"
            description = "Achat au supermarché"
            amount = 40.00
            type = "dépense"
            new_transaction = Transactions(connection, name, date, category, description, amount, type)
            if new_transaction.add_transaction():
                print("Nouvelle balance de l'utilisateur après la transaction:", connection.get_user_balance())
            else:
                print("La transaction a échoué.")
        else:
            print("Impossible de récupérer la balance de l'utilisateur.")
    else:
        print("Échec de la connexion.")


