import mysql.connector
from Connection import Connection

class Transactions:
    def __init__(self, connection):
        self.connection = connection

    def execute_transaction(self):
        if self.connection.login():
            user_balance = self.connection.get_user_balance()
            if user_balance is not None:
                print("Balance de l'utilisateur:", user_balance)
                name = "Nouvelle transaction"
                date = "2024-03-26"
                category = "Alimentation"
                description = "Achat au supermarché"
                amount = 40.00
                type = "dépense"
                new_transaction = Transactions(self.connection, name, date, category, description, amount, type)
                if new_transaction.add_transaction():
                    print("Nouvelle balance de l'utilisateur après la transaction:", self.connection.get_user_balance())
                else:
                    print("La transaction a échoué.")
            else:
                print("Impossible de récupérer la balance de l'utilisateur.")
        else:
            print("Échec de la connexion.")

    def add_transaction(self, name, date, category, description, amount, type):
        try:
            if self.connection.db.is_connected():
                cursor = self.connection.db.cursor()

                if amount <= 0:
                    print("Le montant de la transaction doit être positif.")
                    return False
                if type not in ['dépense', 'revenu']:
                    print("Le type de transaction doit être 'dépense' ou 'revenu'.")
                    return False

                cursor.execute("INSERT INTO transactions (name, date, category, description, amount, type) VALUES (%s, %s, %s, %s, %s, %s)",
                                (name, date, category, description, amount, type))
                self.connection.db.commit()

                # Mettre à jour la balance de l'utilisateur en fonction du type de transaction
                if type == 'dépense':
                    updated_balance = self.connection.get_user_balance() - amount
                else:
                    updated_balance = self.connection.get_user_balance() + amount
                
                # Mettre à jour la balance de l'utilisateur dans la base de données
                self.connection.update_user_balance(updated_balance)

                print("La transaction a été ajoutée avec succès.")
                print("Nouvelle balance de l'utilisateur:", updated_balance)  # Imprimer la nouvelle balance

                return True

        except mysql.connector.Error as e:
            print("Erreur lors de l'ajout de la transaction :", e)
            return False
        
        finally:
            pass

if __name__ == "__main__":
    connection = Connection("Doe", "John", "John.Doe@gmail.com", "Password10!")

    # Créer une instance de la classe Transactions
    transaction_handler = Transactions(connection)

    # Appeler la méthode execute_transaction() pour exécuter la transaction
    transaction_handler.execute_transaction()
